# divaAutoBackup

**NECESSARY DEPENDENCY PLEASE INSTALL!!!**

7-Zip needs to be installed for this to work!
Directly download it from here if you don't have it:
https://www.7-zip.org/a/7z2201-x64.exe

**What is this?**

divaAutoBackup or DivaAB or DAB (hahah) or whatever you want to call it is a alternative launcher
(EXE file) for the PC game 'Hatsune Miku: Project DIVA MegaMix+'.

The game natively supports Steam cloud save, but, if you add lots mods to the game, for example, 
a bunch of song packs and module packs, the cloud save function will stop working, and the modloader
will create it's own offline save file, on a separate folder inside %AppData%\Roaming.

I format my PC a lot, and 3 or 4 times now I completely lost my progress in the game because it was
using this offline save due to mods, and I forgot to back it up, so I made this.

The .exe file was made using the ps2exe powershell module.

**How does it work?**

The script uses steam to launch the game through it's AppID, once the game is launched, the program
will check if it is still running every second. If it is, it does nothing, if you close the game
and it detects that it's closed, it creates a backup of your save inside your Documents folder in a
folder called "DivaBackups". If you have some sort of cloud backup going on like GoogleDrive or
OneDrive, it's gonna pick it up and cloud save it for you, problem solved (i hope).

**How do I use it?**

Download the latest .exe file from releases, place it wherever you want and run it.