# Arduino IDE for RePhone on GNU/Linux

This is a minimal port of the Arduino IDE for RePhone only for GNU/Linux users.
It has been tested on F23 (Fedora 23) and Ubuntu 12.04.

The upload tool `hardware/tools/mtk/pushtool.py` is a simple helper to copy the VXP to the MSD (massive storate module) of the RePhone when plugged in this mode. This tool also changes the `autorun.txt` file so than upon reboot, the sketch should be executed automatically.

Please, send bug reports and good/bad experiences to robarago@gmail.com.

#References

[RePhone main Page](http://www.seeed.cc/rephone)

[Wiki for Arduino_IDE_for_RePhone](http://www.seeedstudio.com/wiki/Arduino_IDE_for_RePhone_Kit)

[Kickstarter page for RePhone](https://www.kickstarter.com/projects/seeed/rephone-kit-worlds-first-open-source-and-modular-p)

