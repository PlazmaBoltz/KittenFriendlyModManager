import requests
import os
import urllib.request
import shutil

mods = dict()

# Repo Stuff
git = 'https://raw.githubusercontent.com/'
owner = 'PlazmaBoltz'
repo = 'KSA-Mods-Library'
repository_url = f"{git}/{owner}/{repo}/refs/heads/main/"
current_version = requests.get(repository_url+"current_version.json").json()["current_version"]
#print(current_version)
script_dir = os.path.dirname(os.path.abspath(__file__))

def get_paths():
    with open(os.path.join(script_dir, 'Paths/ManifestDirectory'), "w") as file:
        file.write(getManifest())
    with open(os.path.join(script_dir, 'Paths/KSADirectory'), "w") as file:
        file.write(getDirectory())
def getManifest():
    potDir = ("C:\\users\\"+os.getenv('username')+"\\OneDrive\\Documents\\My Games\\Kitten Space Agency")
    if os.path.isdir(potDir):
        Directory = potDir + "\\manifest.toml"
        print("Found Manifest Directory")
        return Directory
    else:
        #should never be true
        print("Your KSA is potentially corrupted. There should be a file in Documents/My Games/Kitten Space Agency called manifest.toml")
def getInputForFile():
    file = input("Input path for above folder: ")
    if not os.path.isdir(file):
        print("Not a valid folder. Please try again.")
        return getInputForFile()
    else:
        print("Path ''"+file+"'' found.")
        if os.path.isfile(file+"\\KSA.dll"):
            return file
        else:
            print("Not a KSA Folder")
            getInputForFile()
def getDirectory():
    potDir = "C:\\users\\"+os.getenv('username')+"\\OneDrive\\Documents\\My Games\\Kitten Space Agency\\mods"
    if os.path.isdir(potDir):
        Directory = potDir
        print("Found Mods Directory")
        return Directory
    else:
        #should never be true
        print("Your KSA is potentially corrupted. There should be a folder in Documents/My Games/Kitten Space Agency called mods")
def MainMenu():
    print("-- Kitten Friendly Mod Manager --")
    print("1. Install Mods")
    print("2. Check KSA Directories")
    print("3. Quit\n")
    textInput = input("Option to select: ")
    if textInput == "1":
        print("\n")
        ModInstallMenu()
    elif textInput == "2":
        get_paths()
        MainMenu()
    elif textInput == "3":
        print("Ending Process")
    elif textInput == "4":
        debug()
    else:
        print("Not a valid input. Please enter something else. \n")
        MainMenu()
def ModInstallMenu():
    print("-- Install Mods --")
    print("1. Install Mods")
    print("2. View Mods")
    print("3. List installed mods")
    print("4. Back\n")
    textInput = input("Option to select: ")
    if textInput == "1":
        print("\n")
        if open(os.path.join(script_dir, 'Paths/KSADirectory')).read() and open(os.path.join(script_dir, 'Paths/ManifestDirectory')).read():
            mods = getMods()
            for i in mods:
                print(i)
            print("Enter mod name to install.")
            textInput = input("Enter mod name (case sensative): ")
            if textInput in mods:
                if requests.get(repository_url+mods[textInput]).json() != current_version:
                    textInput2 = input("This mod supports an outdated version of KSA, would you still like to install? (y/n): ")
                    if textInput2.lower() == "y":
                        installMod(textInput, mods)
                    else:
                        ModInstallMenu()
            else:
                print("Invalid Mod")
                ModInstallMenu()
        else:
            get_paths()
            print("Fixed KSA paths not existing")
            ModInstallMenu()
        
    elif textInput == "2":
        print("\n")
        mods = getMods()
        for i in mods:
            print(i)
        print("Type a mod name (case sensative) to view it or press enter to go back.")
        textInput = input()
        if textInput in mods:
            getModData(textInput, mods)
        else:
            ModInstallMenu()
    elif textInput == "3":
        print("tba")
        MainMenu()
    elif textInput == "4":
        MainMenu()
    else:
        print("Not a valid input. Please enter something else. \n")
        ModInstallMenu()
def viewInstalledMods():
    folder = open(os.path.join(script_dir, 'Paths/KSADirectory'), "w")
    installedMods = []
    for mod in getMods():
        if os.path.join(folder, mod):
            print(mod)
            installedMods.append(mod)
    print(installedMods)
    readInstalledMods(installedMods)
def readInstalledMods(installedMods):
    print(installedMods)
    inp = str(input("Enter mod to view or press enter to go back: "))
    if inp in installedMods:
        print("\nOptions:")
        print("1. Uninstall")
        print("2. Update")
        print("3. Back")
        inp = str(input("Option: "))
        if inp == "1":
            print("tba")
        if inp == "2":
            print("tba")
        else:
            MainMenu()
    else:
        if inp == "\n":
            MainMenu()
        else:
            print("Invalid Mod Name!")
            readInstalledMods(installedMods)
def debug():
    #tba
    print("\n\nDebug Console")
    urlPath = input("URL: ")
    recieved = requests.get(repository_url+urlPath)
    print(repository_url+urlPath)
    if recieved.status_code == 200:
        recievedJSON = recieved.json()
        print(recievedJSON)
        print("\n\n")
        print("Title: "+ recievedJSON["title"])
        print("Short Description: "+ recievedJSON["Description_Short"])
        print("Long Description: "+ recievedJSON["Description_Long"])
        if recievedJSON["author"]:
            print("Author: "+recievedJSON["author"])
        print("Version: "+ recievedJSON["Version"])
        print("Supported Version: "+ recievedJSON["Supported_Version"])
        if recievedJSON["Supported_Version"] != current_version:
            print("WARNING: This mod does not support the current version of the game!")
        for i in recievedJSON["Dependencies"]:
            if i["type"] == 1:
                print(i["mod"]+" is a required mod.")
                if i["mod"] == "StarmapAPI":
                    print("Requires Starmap version "+ i["Version"])
            elif i["type"] == 0:
                print(i["mod"]+" is a recommended mod.")
            elif i["type"] == 2:
                print(i["mod"]+" is an unsupported mod.")
        print("Download Link: "+ recievedJSON["Download_Link"])
        print("Homepage: "+ recievedJSON["Homepage"])
    else:
        print("Error with URL: "+str(recieved.status_code))
def getMods():
    index = requests.get(repository_url+"mods.json").json()
    mods = dict()
    for i in index:
        mods[i] = index[i]
    #print(mods)
    return mods
def getModData(url,mods):
    recieved = requests.get(repository_url+mods[url])
    if recieved.status_code == 200:
        recievedJSON = recieved.json()
        print("\n\n")
        print("Title: "+ recievedJSON["title"])
        print("Short Description: "+ recievedJSON["Description_Short"])
        print("Long Description: "+ recievedJSON["Description_Long"])
        if recievedJSON["author"]:
            print("Author: "+recievedJSON["author"])
        print("Version: "+ recievedJSON["Version"])
        print("Supported Version: "+ recievedJSON["Supported_Version"])
        if recievedJSON["Supported_Version"] != current_version:
            print("WARNING: This mod does not support the current version of the game!")
        for i in recievedJSON["Dependencies"]:
            if i["type"] == 1:
                print(i["mod"]+" is a required mod.")
                #if i["mod"] == "StarmapAPI":
                    #print("Requires Starmap version "+ i["Version"])
            elif i["type"] == 0:
                print(i["mod"]+" is a recommended mod.")
            elif i["type"] == 2:
                print(i["mod"]+" is an unsupported mod.")
        print("Download Link: "+ recievedJSON["Download_Link"])
        print("Homepage: "+ recievedJSON["Homepage"]+"\n")
        ModInstallMenu()
    else:
        print("Error with URL: "+str(recieved.status_code))
        getModData(input("Mod Name: "))
def installMod(url, mods):
    recievedJSON = requests.get(repository_url+mods[url]).json()
    print("Downloading "+recievedJSON["title"]+" to "+str(open(os.path.join(script_dir, 'Paths/KSADirectory')).read()))
    f = open((os.path.join(script_dir, ("temp\\"+url+".zip"))),'wb')
    with urllib.request.urlopen(recievedJSON["Download_Link"]) as response:
        total_size = int(response.getheader("Content-Length").strip())
        bytes_downloaded = 0
        chunk_size = 65536  # 64 KB

        with open((os.path.join(script_dir, (("temp\\"+url+".zip")))), "wb") as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break

                f.write(chunk)
                bytes_downloaded += len(chunk)

                percent = (bytes_downloaded / total_size) * 100
                print(f"Downloading: "+str(percent)+"% - ("+str(bytes_downloaded)+"B/"+str(total_size)+"B)")
    f.close()
    print("Finished Downloading")
    print("Extracting Files")
    shutil.unpack_archive((os.path.join(script_dir, ("temp\\"+url+".zip"))), (str(open(os.path.join(script_dir, 'Paths/KSADirectory')).read())))
    os.remove(os.path.join(script_dir, ("temp\\"+url+".zip")))
    print("Finished Installing")
    print("Enabling Mod")
    file = open(os.path.join(script_dir, 'Paths/ManifestDirectory')).read()
    if str('[[mods]]\nid = "'+url+'"\nenabled = true\n') in open(file).read():
        print("Mod already enabled")
    else:
        print("Mod not enabled; Enabling.")
        with open(file,'a') as f:
           f.write(str('\n[[mods]]\nid = "'+url+'"\nenabled = true\n'))
    print("Done!\n")
    MainMenu()
MainMenu()