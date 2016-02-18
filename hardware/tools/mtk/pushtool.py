#!/usr/bin/env python

import sys
from os import popen, remove
from os.path import dirname, basename
from glob import glob

appname = ""
for i in range(len(sys.argv)):
	if sys.argv[i] == '-app':
		appname = sys.argv[i + 1]

if appname == "":
	sys.exit(-1)

drivepath = popen('grep 3021-0367 /proc/mounts|cut -f2 -d" "').read().rstrip()
if drivepath == "":
    print("\nERROR(%s): Can't find mount point for Xadow GSM+BLE drive" % drivepath)
    print("Is the module in MASS STORAGE MODE? Try to RESET ;-)\n")
    sys.exit(-1)

autostart = "%s/autostart.txt" % drivepath

'''
import gtk
dialog = gtk.FileChooserDialog("Please, select the 'autostart.txt' file in the RePhone disk",
															 None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL,
															 gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
dialog.set_default_response(gtk.RESPONSE_OK)
dialog.set_current_name = 'autostart.txt'

filter = gtk.FileFilter()
filter.set_name("autostart.txt")
filter.add_pattern("*.txt")
dialog.add_filter(filter)

response = dialog.run()
if response == gtk.RESPONSE_CANCEL:
    dialog.destroy()
    sys.exit(0)
autostart = dialog.get_filename()
dialog.destroy()
'''
drivepath = dirname(appname)
#print('cp %s %s/MRE/%s' % (appname, dirname(autostart), basename(appname)))
for f in glob('%s/MRE/*.cpp.vxp' % dirname(autostart)): remove(f)
p = popen('cp %s %s/MRE/%s' % (appname, dirname(autostart), basename(appname)))
a = open(autostart, 'wb')
a.write('[autostart]\r\nApp=C:\\MRE\\%s\r\n' % basename(appname))
a.close()
p = popen('sync; sync; umount %s' % dirname(autostart))
print('\nSUCCESS: Now RESET your Xadow GSM+BLE now to execute your program!\n')
