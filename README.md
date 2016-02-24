# Arduino IDE for RePhone on GNU/Linux

This is a minimal port of the Arduino IDE for RePhone only for GNU/Linux users.
It has been tested on F23 (Fedora 23) and Ubuntu 12.04.

Please, send bug reports and good/bad experiences to robarago@gmail.com.

# Upload tool

Thanks to *Stefan Mandl*, we have a new awesome upload tools which requires no manual reset. The tool works by uploading the code using the modem device (__ttyACM1__ in my case). You can increase the verbosity of the output of the tool with the Arduino preference switch. This is the kind of output you will get with increased verbosity:
<code>
$ ArduinoGNULinux4RePhone/hardware/tools/mtk/uploader.py -v -v -v -v -clear -port ttyACM1 -app /tmp/build3227371159114637524.tmp/battery_test.cpp.vxp
Opening communication...
Stopping all processes...
Changing operation mode to obtain access to filesystem...
Folder operation back to root folder...
Clearing old sketches from MRE folder...
Deleting file 'C:\MRE\battery_test.cpp.vxp'...
Sending new sketch: 'battery_test.cpp.vxp'...
Filename path: C:\MRE\battery_test.cpp.vxp
Bytes to send: 70366
[ C:\MRE ]
  Size Filename                                                        
====== ===============
     0 .                                                              
     0 ..                                                            
 31812 lua.vxp                                                  
 70366 battery_test.cpp.vxp                        
Sending new 'autoload.txt'...
Filename path: C:\autostart.txt
Bytes to send: 46
[ C: ]
  Size Filename                                                        
====== ===============
    46 autostart.txt                                      
    31 init.lua                                                
    53 result.txt                                            
 10294 music.mp3                                              
     0 MRE                                                          
Change operation mode to compatible...
Rebooting...
<code>

#References

[RePhone main Page](http://www.seeed.cc/rephone)

[Wiki for Arduino_IDE_for_RePhone](http://www.seeedstudio.com/wiki/Arduino_IDE_for_RePhone_Kit)

[Kickstarter page for RePhone](https://www.kickstarter.com/projects/seeed/rephone-kit-worlds-first-open-source-and-modular-p)

[Original uploader by Stefan Mandl](https://github.com/mandl/LinkIt_Assist_2502)

