This script will help you create custom music discs for ItemsAdder packs without worrying about the hastle of doing it manually


**Features**

- generates items.yml, categories.yml, en.yml, and sounds.json.
- Sets display name as the first line of lore
- creates placeholders for .ogg and .png files.
- Multiple discs can be added per pack.

**Usage**

1. Run the script

		python discscript.py

2. Enter your namespace (e.g, iamusic)

3. For each disc:
	- Enter internal name (used for commands and file names)
	- Enter display name (this is what appears ingame)

4. Type done when finished adding discs.

5. Replace placeholders with actual .ogg and .png files.


**File structure**


	contents/                            #root contents folder
	└── <namespace>/                     #namespace that gets made
	    ├── resourcepack/                
	    │   └── <namespace>/
	    │       ├── sounds.json          #links audio to discs
	    │       ├── sounds/
	    │       │   └── music_disc/
	    │       │       └── <disc>.ogg   #audio file to be played
	    │       └── textures/
	    │           └── item/
	    │               └── <disc>.png   #icon for the disc
	    └── configs/
	        ├── items.yml                #config for the disc items
	        ├── categories.yml           #config for disc category
	        └── dictionaries/             
	            └── en.yml               #edit some things in here

**Notes**

i have not tested this on windows/mac etc, only on linux, but i dont see why it wouldnt work
