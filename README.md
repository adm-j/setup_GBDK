# GBDK Project setup script

This is just a simple python script I threw together to setup a basic GBDK project. It's a bit
overkill but I don't want to come back to this in 6 months and have to remember what I did lol.
This was written for LINUX. This will NOT work on windows, though I expect if you want
to use Windows you should be able to use WSL. No 3rd party libraries, just run it.

It creates a main.c, build.sh, .gitignore and readme files.
build.sh is a simple bash script which will compile your main.c file using GDBK.

To use this, all you need to do is place this script in your taget directory for the
project and run it. Make sure you install GBDK first - see https://gbdk-2020.github.io/gbdk-2020/
The script will ask you a few questions then set things accordingly.

It's a bit bare bones right now, that may change as I learn more.

### **TODO**
I have now added a python script which should allow for compiling a whole project, but when I
have time to get my head around it I really want to have a makefile instead!
