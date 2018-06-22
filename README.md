# ZiboInstallUpdateScript

Auto update your Zibo

1. You need the Python installed;
2. This script needs to be in the same path of ZIP files with the ZIBO and RG MOD;
3. You need the software 7-Zib installed in you machine. The FMOD audio zip is compressed in some type not supported by the python zip library (check if your 7-Zip installation path is as line 92);
4. You must set the zip files name that you have downloaded:

	ZiboPathRoot = "D:/SteamLibrary/steamapps/common/X-Plane 11/Aircraft/Laminar Research"
	
	ZiboZIP = "B737-800X_3_27l.zip"
	
	AudioBirdFmod = "AXP IMMERSION PACK 737-800X ZIBO V 1806 REV4.zip"
	
	RGModZIP = "B737-800_RG_mod FULL- 3.27l.zip"
	
	TexturePackRGMod = "TEXTURE PACK_B737-800_RG_mod FULL- 1.0.0f.zip"

 What do this script do?

1. Install Zibo and RG Mod in diferents folders, so you can have bouth versions in you X-Plane 11;
2. Rename with suffix "_old" the folders (with you have) of Zibo and Zibo with RG mod. The names must be [B737-800X] and [B737-800XRG_mod];
3. Install new Zibo version;
4. Copy liveries from old Zibo to the new one;
5. Copy X-Camera file from old to the new one, if you have it;
6. Install FMOD by AudioBirdXP;
7. Install RG mod with texture pack and remove files required from [zibo/object] folder.

If you only have to install Zibo, without RG mod, simple edit the script and remove lines bellow line 96 (KEEP THE LINES 165 and 168).

Future improvements:
- Option in execution time for install only Zibo.
- Option for select between Zibo 2k or 4k texture.
- Option for select 2k texture install for RG mod.

If you have any ideas or questions let me know.
