# DivaAutoBackup

Diva Auto Backup, DivaAB or DAB (hahah :|) is a cross-platform alternative executable for the game **Hatsune Miku: Project DIVA MegaMix+**.

It's purpose is to replace your original shortcut used to launch game to keep your save file backed up. Here's how it works:

* When launched for the first time will show a setup window asking the user where their Steam instalation is and where they would like to keep their backups.
  - *(on linux the steam path text box will be grayed out because the program calls the "steam" executable from PATH directly)*
* After the user presses **Save**, the settings will be saved to the config file *config.yml* and the program will proceed with it's normal execution.
* It will then use steam to launch the game using it's app_id, wait for the game process to start, and will then check if the game is still running every 1.5 seconds.
* If it detects the game has been closed, a pop-up window will appear asking the user if they would like to backup their save file, if aggreed, the program will compress their save data into a timestamped .zip file and move it to the previously setup backup location. If declined, the program will simply close.

# Ok, cool, where do I download it?

1. Go to the releases tab and download the latest .zip file according to your operating system;
2. Extract the zip file anywhere you want and create a shortcut to the executable somewhere;
   - *Adding it as a Steam game is recommended*
3. Launch your new shortcut or the executable directly as if you were launching Project Diva;
4. Enjoy :3

# Windows Defender says it's a virus
Windows defender is stupid. Use linux.

# I'd like to manually build it myself.
Why? Ok...

1. Install Python;
2. Install the dependencies at *requirements.txt*;
3. Open a terminal on the project directory;
4. Run the command *python build.py* and wait for it to build;
5. Your final build will be located at the *dist* folder;
6. Enjoy? I guess.

# What's that masterpiece blessing my eyes?
That beautiful piece of artwork was the prototype banner before I sunk about 3 minutes of my life making the final one.