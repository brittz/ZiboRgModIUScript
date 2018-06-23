import shutil
import os
import zipfile
import subprocess

LogFile = "ZiboUpdateLog.txt"

# path where your actual Zibo is installed
dir_path = os.path.dirname(os.path.realpath(__file__))
ZiboPathRoot = "D:/SteamLibrary/steamapps/common/X-Plane 11/Aircraft/Laminar Research"
ZiboZIP = "B737-800X_3_27l.zip"
AudioBirdFmod = "AXP IMMERSION PACK 737-800X ZIBO V 1806 REV4.zip"
RGModZIP = "B737-800_RG_mod FULL- 3.27l.zip"
TexturePackRGMod = "TEXTURE PACK_B737-800_RG_mod FULL- 1.0.0f.zip"

#######################################################################################

if os.path.isfile(LogFile):
    # remove old log file
    os.remove(LogFile)
file = open(LogFile, "w")

def log(text):
    # create a log file
    file.write(text)

def copydir(source, dest):
    """Copy a directory structure overwriting existing files"""
    for root, dirs, files in os.walk(source):
        if not os.path.isdir(root):
            os.makedirs(root)

        for file in files:
            rel_path = root.replace(source, '').lstrip(os.sep)
            dest_path = os.path.join(dest, rel_path)

            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)

            shutil.copyfile(os.path.join(root, file), os.path.join(dest_path, file))
            log('Replacing...')
            log(os.path.join(root, file)+'\r\n')
            log(os.path.join(dest_path, file)+'\r\n\r\n')

#######################################################################################

log('dir_path : '+dir_path+'\r\n')
log('ZiboPathRoot : '+ZiboPathRoot+'\r\n')
log('ZiboZIP: '+ZiboZIP+'\r\n')
log('AudioBirdFmod: '+AudioBirdFmod+'\r\n')
log('RGModZIP: '+RGModZIP+'\r\n')
log('TexturePackRGMod: '+TexturePackRGMod+'\r\n\r\n')

# renaming old folders
log('Checking for existing Zibo folders...\r\n')

if os.path.exists(ZiboPathRoot+'/B737-800X'):
    os.rename(ZiboPathRoot+'/B737-800X', ZiboPathRoot+'/B737-800X_old')
    log('B737-800X to B737-800X_old renamed\r\n')

if os.path.exists(ZiboPathRoot+'/B737-800XRG_mod'):
    os.rename(ZiboPathRoot+'/B737-800XRG_mod', ZiboPathRoot+'/B737-800XRG_mod_old')
    log('B737-800XRG_mod to B737-800XRG_mod_old renamed\r\n')

# waiting zip files extration
log('extracting new zibo to ['+ZiboZIP+']')
zip_ref = zipfile.ZipFile(ZiboZIP, 'r')
zip_ref.extractall(ZiboPathRoot)
zip_ref.close()
########
########

# copy x-camera file for new Zibo folder
XCameraFile = ZiboPathRoot+'/B737-800X_old/X-Camera_b738.csv'

if os.path.isfile(XCameraFile):
    shutil.copy2(XCameraFile, ZiboPathRoot+'/B737-800X')
    log("Copying X-Camera file from ["+XCameraFile+"] to ["+ZiboPathRoot+"/B737-800X]\r\n")
else :
    log("X-Camera file not found\r\n")

# copy liveries
if os.path.exists(ZiboPathRoot+'/B737-800X/liveries'):
    shutil.rmtree(ZiboPathRoot+'/B737-800X/liveries')

shutil.copytree(ZiboPathRoot+'/B737-800X_old/liveries', ZiboPathRoot+'/B737-800X/liveries')
log("Copying liveries from [B737-800X_old/liveries] to [B737-800X]\r\n")

# fmod installation
log('extracting fmod\r\n')
# zip_ref = zipfile.ZipFile(AudioBirdFmod, 'r')
# zip_ref.extractall(ZiboPathRoot+'/B737-800X')
# zip_ref.extractall('AudioBirdFmod')
# zip_ref.close()

# The way that fmod zip was compressed is unsupported by python zip libray, so i have to use 7zip program
subprocess.call(r'"C:\Program Files\7-Zip\7z.exe" x ' + dir_path+'\\"'+AudioBirdFmod + '" -o' + dir_path +'/AudioBirdFmod')

log('copying fmod to Zibo')
copydir('AudioBirdFmod/fmod', ZiboPathRoot+'/B737-800X/fmod')

############################################################################################
######## RG MOD ########

# copy ZIBO folder to become RG Mod Aircraft
copydir(ZiboPathRoot+'/B737-800X/',ZiboPathRoot+'/B737-800XRG_mod/')

# Deleting required files for RG Mod
log('removing required files for RG Mod\r\n')
Files2DeletePath = ZiboPathRoot+'/B737-800XRG_mod/objects'

os.remove(Files2DeletePath+'/738_cockpit_main_2k.obj')
os.remove(Files2DeletePath+'/738cockpit_yoke_2k_NML.png')
os.remove(Files2DeletePath+'/738cockpit_yoke_2k_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_yoke_2k.png')
os.remove(Files2DeletePath+'/738cockpit_yoke.png')
os.remove(Files2DeletePath+'/738cockpit_switches_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_switches_2k_NML.png')
os.remove(Files2DeletePath+'/738cockpit_switches_2k_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_switches_2k.png')
os.remove(Files2DeletePath+'/738cockpit_switches.png')
os.remove(Files2DeletePath+'/738cockpit_shell_2k_NML.png')
os.remove(Files2DeletePath+'/738cockpit_shell_2k.png')
os.remove(Files2DeletePath+'/738cockpit_shell.png')
os.remove(Files2DeletePath+'/738cockpit_seats_2k_NML.png')
os.remove(Files2DeletePath+'/738cockpit_seats_2k.png')
os.remove(Files2DeletePath+'/738cockpit_seats.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_NML.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_efis_NML.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_efis_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_efis_2k_NML.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_efis_2k_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_efis_2k.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_efis.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_2k_NML.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_2k_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_2k.png')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare.png')
os.remove(Files2DeletePath+'/738cockpit_overhead2_2k_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_overhead2_2k.png')
os.remove(Files2DeletePath+'/738cockpit_overhead2.png')
os.remove(Files2DeletePath+'/738cockpit_overhead_2k_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_overhead_2k.png')
os.remove(Files2DeletePath+'/738cockpit_overhead.png')
os.remove(Files2DeletePath+'/738cockpit_main_panel_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_main_panel_2k_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_main_panel_2k.png')
os.remove(Files2DeletePath+'/738cockpit_main_panel.png')
os.remove(Files2DeletePath+'/738cockpit_lower_NML.png')
os.remove(Files2DeletePath+'/738cockpit_lower_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_lower_2k_NML.png')
os.remove(Files2DeletePath+'/738cockpit_lower_2k_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_lower_2k.png')
os.remove(Files2DeletePath+'/738cockpit_lower.png')
os.remove(Files2DeletePath+'/738cockpit_glass_2_NML.png')
os.remove(Files2DeletePath+'/738cockpit_glass_2.png')
os.remove(Files2DeletePath+'/738cockpit_displays_tint_LIT.png')
os.remove(Files2DeletePath+'/738cockpit_displays_tint.png')
os.remove(Files2DeletePath+'/738_cockpit_yokes_2k.obj')
os.remove(Files2DeletePath+'/738_cockpit_switch_2k.obj')
os.remove(Files2DeletePath+'/738_cockpit_seats_2k.obj')
os.remove(Files2DeletePath+'/738_cockpit_roof_2k.obj')
os.remove(Files2DeletePath+'/738_cockpit_pdstl_mic_2k.obj')
os.remove(Files2DeletePath+'/738_cockpit_pdstl_mic.obj')
os.remove(Files2DeletePath+'/738_cockpit_pdstl_efis_2k.obj')
os.remove(Files2DeletePath+'/738_cockpit_pdstl_efis.obj')
os.remove(Files2DeletePath+'/738_cockpit_pdstl_2k.obj')
os.remove(Files2DeletePath+'/738_cockpit_ovhd2_2k.obj')
os.remove(Files2DeletePath+'/738_cockpit_ovhd1_2k.obj')
os.remove(Files2DeletePath+'/738_cockpit_main_2k.obj')
os.remove(Files2DeletePath+'/738_cockpit_floor_2k.obj')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_LIT.dds')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_efis_LIT.dds')
os.remove(Files2DeletePath+'/738cockpit_pedestal_glare_efis.dds')
os.remove(Files2DeletePath+'/738cockpit_overhead.dds')
os.remove(Files2DeletePath+'/738cockpit_main_panel_LIT.dds')
os.remove(Files2DeletePath+'/738cockpit_main_panel.dds')

# installing rg mod
log('Extracting rg mod zip\r\n')
zip_ref = zipfile.ZipFile(RGModZIP, 'r')
zip_ref.extractall('RGMOD_TEMP')
zip_ref.close()

log('copying folder [RGMOD_TEMP/objects] to  ['+ZiboPathRoot+'/B737-800XRG_mod/objects]\r\n')
copydir('RGMOD_TEMP/objects', ZiboPathRoot+'/B737-800XRG_mod/objects')
log('copying [RGMOD_TEMP/cockpit_3d] to ['+ZiboPathRoot+'/B737-800XRG_mod/cockpit_3d]\r\n')
copydir('RGMOD_TEMP/cockpit_3d', ZiboPathRoot+'/B737-800XRG_mod/cockpit_3d')
log('copying [RGMOD_TEMP/b738.acf] to ['+ZiboPathRoot+'/B737-800XRG_mod]\r\n')
copydir('RGMOD_TEMP/b738.acf', ZiboPathRoot+'/B737-800XRG_mod')
log('copying [RGMOD_TEMP/b738_cockpit.obj] to ['+ZiboPathRoot+'/B737-800XRG_mod]\r\n')
copydir('RGMOD_TEMP/b738_cockpit.obj', ZiboPathRoot+'/B737-800XRG_mod')

# installing rg mod texture
log('Extracting rg mod texture zip\r\n')
zip_ref = zipfile.ZipFile(TexturePackRGMod, 'r')
zip_ref.extractall('TEXTURERGMOD_TEMP')
zip_ref.close()

log('copying folder [TEXTURERGMOD_TEMP/objects] to  ['+ZiboPathRoot+'/B737-800XRG_mod/objects]\r\n')
copydir('TEXTURERGMOD_TEMP/objects', ZiboPathRoot+'/B737-800XRG_mod/objects')

# in this line will be a question asking for 2k-cockpit texture installation
# and other custom installs

shutil.rmtree('AudioBirdFmod')
shutil.rmtree('RGMOD_TEMP')
shutil.rmtree('TEXTURERGMOD_TEMP')
file.close()
