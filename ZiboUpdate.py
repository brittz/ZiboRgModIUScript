import shutil
import os
import zipfile
import subprocess
import sys

LogFile = "ZiboUpdateLog.txt"

# path where your actual Zibo is installed
dir_path = os.path.dirname(os.path.realpath(__file__))

ZiboPathRoot = 'C:/Program Files (x86)/Steam/steamapps/common/X-Plane 11/Aircraft/Laminar Research'
ZiboPathRootCustom = 'D:/SteamLibrary/steamapps/common/X-Plane 11/Aircraft/Laminar Research'

# bellow could be:
# (1) a file name if this script is in the same path of Zip Files or
# (2) a full path to the zip files (not tested yet)
ZiboZIP = "328/B737-800X_3_28.zip"
AudioBirdFmod = "AXP IMMERSION PACK 737-800X ZIBO V 1807 REV1 STEREO.zip"
RGModZIP = "328/B737-800_RG_mod FULL- 3.28.zip"
TexturePackRGMod = "328/TEXTURE PACK_B737-800_RG_mod FULL- 1.0.0f.zip"

#######################################################################################
if os.path.isfile(LogFile):
    # remove old log file
    os.remove(LogFile)
file = open(LogFile, "w")

def log(text):
    # create a log file
    print(text)
    file.write(text+'\r\n')

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
            log(os.path.join(root, file))
            log(os.path.join(dest_path, file)+'\r\n\r\n')
            
def installZIBO():
    log('Checking for existing Zibo folders...')
    if os.path.exists(ZiboPathRoot+'/B737-800X'):
        os.rename(ZiboPathRoot+'/B737-800X', ZiboPathRoot+'/B737-800X_old')
        log('B737-800X to B737-800X_old renamed')
    extracZIBO()
    copyCameraFiles(ZiboPathRoot+'/B737-800X_old', ZiboPathRoot+'/B737-800X')
    copyLiveries(ZiboPathRoot+'/B737-800X_old/liveries', ZiboPathRoot+'/B737-800X/liveries')
    installFMod(ZiboPathRoot+'/B737-800X/fmod')

def installZiboWithRGMod():
    print('installZiboWithRGMod')

def installZIBOAndRGMod():
    log("Starting install...")
    installZIBO()
    log('Checking for existing Zibo RG mod folders...')
    if os.path.exists(ZiboPathRoot+'/B737-800XRG_mod'):
        os.rename(ZiboPathRoot+'/B737-800XRG_mod', ZiboPathRoot+'/B737-800XRG_mod_old')
        log('B737-800XRG_mod to B737-800XRG_mod_old renamed')
    copydir(ZiboPathRoot+'/B737-800X/',ZiboPathRoot+'/B737-800XRG_mod/')
    installRGMod()
    
def installRGMod():
    log('installRGMod')
    # installing rg mod
    log('Extracting rg mod zip')
    zip_ref = zipfile.ZipFile(RGModZIP, 'r')
    zip_ref.extractall('RGMOD_TEMP')
    zip_ref.close()

    deleteRequiredFiles4RGMod()

    log('copying folder [RGMOD_TEMP/objects] to  ['+ZiboPathRoot+'/B737-800XRG_mod/objects]')
    copydir('RGMOD_TEMP/objects', ZiboPathRoot+'/B737-800XRG_mod/objects')

    log('copying [RGMOD_TEMP/cockpit_3d] to ['+ZiboPathRoot+'/B737-800XRG_mod/cockpit_3d]')
    copydir('RGMOD_TEMP/cockpit_3d', ZiboPathRoot+'/B737-800XRG_mod/cockpit_3d')

    log('copying [RGMOD_TEMP/b738.acf] to ['+ZiboPathRoot+'/B737-800XRG_mod]')
    shutil.copy2('RGMOD_TEMP/b738.acf', ZiboPathRoot+'/B737-800XRG_mod/b738.acf')

    log('copying [RGMOD_TEMP/b738_cockpit.obj] to ['+ZiboPathRoot+'/B737-800XRG_mod]')
    shutil.copy2('RGMOD_TEMP/b738_cockpit.obj', ZiboPathRoot+'/B737-800XRG_mod')

    installRGModTexture4k()
    
    shutil.rmtree('RGMOD_TEMP')

def extracZIBO():
    log('extracting new zibo to ['+ZiboZIP+']')
    zip_ref = zipfile.ZipFile(ZiboZIP, 'r')
    zip_ref.extractall(ZiboPathRoot)
    zip_ref.close()

def copyCameraFiles(sourcePath, destPath):
    # copy x-camera file for new Zibo folder
    log('copyCameraFiles')
    log('sourcePath: '+sourcePath)
    log('destPath: '+destPath)
    XCameraFile = sourcePath+'/X-Camera_b738.csv'
    cameraFile = sourcePath+'/b738_prefs.txt'
    log('XCameraFile: '+XCameraFile)
    log('cameraFile: '+cameraFile)

    if (os.path.isfile(cameraFile)):
        shutil.copy2(cameraFile, destPath)
        log("Copying camera file from ["+cameraFile+"] to ["+destPath+"]")
    else:
        log("Camera file not found")

    if os.path.isfile(XCameraFile):
        shutil.copy2(XCameraFile, destPath)
        log("Copying X-Camera file from ["+XCameraFile+"] to ["+destPath+"]")
    else:
        log("X-Camera file not found")

def copyLiveries(source, dest):
    # copy liveries
    if os.path.exists(ZiboPathRoot+'/B737-800X/liveries'):
        shutil.rmtree(ZiboPathRoot+'/B737-800X/liveries')

    shutil.copytree(source, dest)
    log("Copying liveries from [B737-800X_old/liveries] to [B737-800X]")

def installFMod(destPath):
    # fmod installation
    log('extracting fmod')
    # zip_ref = zipfile.ZipFile(AudioBirdFmod, 'r')
    # zip_ref.extractall(ZiboPathRoot+'/B737-800X')
    # zip_ref.extractall('AudioBirdFmod')
    # zip_ref.close()

    # The way that fmod zip was compressed is unsupported by python zip libray, so i have to use 7zip program
    subprocess.call(r'"C:\Program Files\7-Zip\7z.exe" x ' + dir_path+'\\"'+AudioBirdFmod + '" -o' + dir_path +'/AudioBirdFmod')

    log('copying fmod to Zibo')
    copydir('AudioBirdFmod/fmod', destPath)
    shutil.rmtree('AudioBirdFmod')

def deleteRequiredFiles4RGMod():
    # Deleting required files for RG Mod
    log('removing required files for RG Mod')
    Files2DeletePath = ZiboPathRoot+'/B737-800XRG_mod/objects'

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

def installRGModTexture4k():
    # installing rg mod texture
    log('Extracting rg mod texture zip')
    zip_ref = zipfile.ZipFile(TexturePackRGMod, 'r')
    zip_ref.extractall('TEXTURERGMOD_TEMP')
    zip_ref.close()

    log('copying folder [TEXTURERGMOD_TEMP/objects] to  ['+ZiboPathRoot+'/B737-800XRG_mod/objects]')
    copydir('TEXTURERGMOD_TEMP/objects', ZiboPathRoot+'/B737-800XRG_mod/objects')
    shutil.rmtree('TEXTURERGMOD_TEMP')
 
#######################################################################################
print('*********************************************************************************************')
print('Welcome!!!')
print('Script made by Brittz')
print('*********************************************************************************************')

log('dir_path : '+dir_path)
log('ZiboPathRoot : '+ZiboPathRoot)
log('ZiboZIP: '+ZiboZIP)
log('AudioBirdFmod: '+AudioBirdFmod)
log('RGModZIP: '+RGModZIP)
log('TexturePackRGMod: '+TexturePackRGMod+'\r\n')

print('>>>>>>>>>>> Before you start, please check the installation paths above. <<<<<<<<<<<<\r\n')

if (os.path.exists(ZiboPathRoot)):
    # ZiboPathRoot = ZiboPathRootCustom
    ZiboPathRootCustom = input('Say the path you want to install the aircraft mod\r\n')

if (os.path.exists(ZiboPathRootCustom)):
    ZiboPathRoot = ZiboPathRootCustom
else:
    input('Invalid Path! Press any key to close the program...')
    sys.exit

# print(mymenu())
# print(ZiboZIP)
# print("1. Instalar Zibo 2k")
# print("2. Instalar Zibo 4k")
# print("3. Instalar Zibo + RG mod 2k")
# print("4. Instalar Zibo + RG mod 4k\r\n")

# option = input("Select a number for install\r\n")

print(installZIBOAndRGMod())
log("Process complete...")
input("Press Enter To Exit...")

file.close()
