#!/usr/bin/env python
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301 USA.

import serial
import time
import sys
import re
import argparse
import traceback
import os

class MTKModem(object):

	VERBOSE = 0
	WRITE_SIZE = 400

	def __init__(self, port):
		self.open(port)

	def open(self, port):
		self.ser = serial.Serial(port, 115200, timeout=5)
		self.ser.flushInput()
		self.ser.flushOutput()

	def SendCommand(self, command, getline=True, ignoreError=False):
		if self.VERBOSE > 4:
			print 'send: %s' % (command)
		self.ser.write(command + '\r')
		data = ''
		if getline:
			data=self.ReadLine(ignoreError)
		return data 

	def SendCommandResult(self,command):
		out = []	
		if self.VERBOSE > 4:
			print 'send: %s' % (command)
		self.ser.write(command + '\r')
		while 1:
			data = self.ser.readline().rstrip("\n\r")
			if data == 'OK':
				return out
				break
			if data == 'ERROR':
				raise Exception('Comm Error')
			if data !='':
				out.append(data)	

	def ReadLine(self,ignoreError):
		while 1:
			data = self.ser.readline().rstrip("\n\r")
			if data == 'OK':
				break
			if data == 'ERROR':
				if ignoreError:
					break
				raise Exception('Comm Error')
				
			if data !='' and self.VERBOSE > 4:
				print data

	def clearSketches(self, path):
		fileList = self.SendCommandResult('AT+EFSL="'+path.encode("utf-16-be").encode("hex") +'"')
		for item in fileList:
			diritem  = item.split(",")
			quoted = re.compile('"[^"]*"')
			for value in quoted.findall(item):
				value = value.replace('"', "")
				filename = value.decode("hex")
				if filename.endswith(".cpp.vxp".encode("utf-16-be")):
					self.DeleteFile("C:\\MRE\\" + filename.decode("utf-16-be"))

	def ListFiles(self, path):
		fileList = self.SendCommandResult('AT+EFSL="'+path.encode("utf-16-be").encode("hex") +'"')
		if self.VERBOSE > 0:
			print "[ %s ]" % path
			print "%6.6s %-64.64s" % ("Size", "Filename")
			print "====== ==============="
		for item in fileList:
			diritem  = item.split(",")
			# get file size
			filesize = diritem[1]
			# attribute of file
			#attrib = diritem[2]
			quoted = re.compile('"[^"]*"')
			for value in quoted.findall(item):
				# find filename
				value = value.replace('"', "")
				if self.VERBOSE > 0:
					print ("%6.6s %-64.64s" % (str(filesize), value.decode("hex")))

	def DeleteFile(self, pathFilename):
		# Folder operation Back to root folder
		if self.VERBOSE > 0:
			print "Deleting file '%s'..." % pathFilename
		self.SendCommand('AT+EFSF=3')
		# send command ignore error if file does not exits
		self.SendCommand('AT+EFSD="'+pathFilename.encode("utf-16-be").encode("hex") +'"', True, True)

	def sendAutostart(self, filename):
		a = open('/tmp/autostart.txt', 'wb')
		a.write('[autostart]\r\nApp=C:\\MRE\\%s\r\n' % os.path.basename(filename))
		a.close()
		self.sendFile('C:\\', '/tmp/autostart.txt')

	def sendFile(self, destpath, filename):
		if not os.path.isfile(filename):
			raise Exception('Can not open file: %s') % (filename)
        
		# open file		
		f = file(filename, 'rb')
 		st = os.stat(filename)
		
		size = st.st_size
		if size == 0:
			raise Exception('File is empty')
		
		path = destpath + os.path.basename(filename)
		filenamePath = path.encode("utf-16-be")

		if self.VERBOSE > 0:
			print "Filename path: %s" % filenamePath
			print "Bytes to send: %d" % size

		# open file for write
		self.SendCommand('AT+EFSW=0,"'+ filenamePath.encode("hex") +'"')
		
		# send data to open file
		for i in range(st.st_size / self.WRITE_SIZE):
			var = f.read(self.WRITE_SIZE)
			data = var.encode("hex")
			if size == 400:
				# last paket send eof
 				self.SendCommand('AT+EFSW=2,1,400,"' +data + '"')
			else:
				# send paket
				self.SendCommand('AT+EFSW=2,0,400,"' +data + '"')
			size = size - 400
	
		if size > 0:
			# send last data to open file
			var = f.read(size)
			data = var.encode("hex")
			# send lastpaket
			self.SendCommand('AT+EFSW=2,1,'+str(size) +',"' +data + '"')
	
		# close file
		self.SendCommand('AT+EFSW=1,"' +filenamePath.encode("hex") +'"') 

	def flushCom(self):
		self.ser.flushInput()
		self.ser.flushOutput()

def main():
	parser = argparse.ArgumentParser(description = 'Push Application Utility', prog = 'uploader')
	parser.add_argument('-port', '-p', help = 'Serial port device', default = 'ttyACM1')
	parser.add_argument('-app', help='File for uploading')
	parser.add_argument('-clear', help='Clear old sketches in MRE folder', action='store_true')
	parser.add_argument('-verbose', '-v', help = 'Verbose output', action='count')

	args = parser.parse_args()
	if os.path.isfile(args.app) == False:
		print 'Can not open file "' + args.app + '" for upload. Aborted'
		return
	h = MTKModem('/dev/%s' % args.port)
	time.sleep(0.5)
	h.VERBOSE = args.verbose

	if h.VERBOSE > 3:
		print "Opening communication..."
	h.SendCommand('AT')

	# exit all running process
	if h.VERBOSE > 3:
		print "Stopping all processes..."
	h.SendCommand('AT+[666]EXIT_ALL', False)
	h.flushCom()
	time.sleep(1)

	if h.VERBOSE > 3:
		print "Changing operation mode to obtain access to filesystem..."
	h.SendCommand('AT+ESUO=3')
		
	if h.VERBOSE > 3:
		print "Folder operation back to root folder..."
	h.SendCommand('AT+EFSF=3')
	
	if h.VERBOSE > 3:
		print "Clearing old sketches from MRE folder..."
	if args.clear:
		h.clearSketches('C:\MRE')

	if h.VERBOSE > 3:
		print "Sending new sketch: '%s'..." % os.path.basename(args.app)
	h.sendFile('C:\\MRE\\', args.app)
	h.ListFiles('C:\MRE')

	if h.VERBOSE > 3:
		print "Sending new 'autoload.txt'..."
	h.sendAutostart(args.app)
	h.ListFiles('C:')
		
	if h.VERBOSE > 3:
		print "Change operation mode to compatible..."
	h.SendCommand('AT+ESUO=4')

	if h.VERBOSE > 3:
		print "Rebooting..."
	h.SendCommand('AT+[666]REBOOT', False) 

if __name__ == '__main__':
	try:
		main()
	except Exception, err:
		sys.stderr.write('ERROR: %s\n' % str(err))
		traceback.print_exc()
