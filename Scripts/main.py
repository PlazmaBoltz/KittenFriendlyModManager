import subprocess
import sys
import requests
import json
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

def get_paths():
    with open('Paths/ManifestDirectory', "w") as file:
        file.write(getManifest())
    with open('Paths/KSADirectory', "w") as file:
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
    potDir1 = ("C:\\Program Files (x86)\\Kitten Space Agency")
    potDir2 = ("C:\\Program Files\\Kitten Space Agency")
    potDir3 = ("C:\\Kitten Space Agency")
    potDir4 = ("E:\\Kitten Space Agency") # only for plazma to have an easier time with testing
    if os.path.isfile(potDir1+"\\KSA.dll"):
        print("Found KSA Directory")
        return potDir1
    elif os.path.isfile(potDir2+"\\KSA.dll"):
        print("Found KSA Directory")
        return potDir2
    elif os.path.isfile(potDir3+"\\KSA.dll"):
        print("Found KSA Directory")
        return potDir3
    elif os.path.isfile(potDir4+"\\KSA.dll"):
        print("Found KSA Directory")
        return potDir4
    else:
        print("Could not find KSA Directory. Please input your directory. (example:  C:\\Program Files\\Kitten Space Agency)")
        return getInputForFile()
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
        if open("Paths/KSADirectory").read() and open("Paths/ManifestDirectory").read():
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
        print("\n")
    elif textInput == "4":
        MainMenu()
    else:
        print("Not a valid input. Please enter something else. \n")
        ModInstallMenu()
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
        print("Homepage: "+ recievedJSON["Homepage"]+"\n")
        ModInstallMenu()
    else:
        print("Error with URL: "+str(recieved.status_code))
        getModData(input("Mod Name: "))
def installMod(url, mods):
    recievedJSON = requests.get(repository_url+mods[url]).json()
    print("Downloading "+recievedJSON["title"]+" to "+str(open("Paths/KSADirectory").read())+"\Content")
    f = open(("temp/"+url+".zip"),'wb')
    with urllib.request.urlopen(recievedJSON["Download_Link"]) as response:
        total_size = int(response.getheader("Content-Length").strip())
        bytes_downloaded = 0
        chunk_size = 65536  # 64 KB

        with open(("temp/"+url+".zip"), "wb") as f:
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
    shutil.unpack_archive(("temp/"+url+".zip"), (str(open("Paths/KSADirectory").read())+"\Content"))
    os.remove("temp/"+url+".zip")
    print("Finished Installing")
    print("Enabling Mod")
    file = open("Paths/ManifestDirectory").read()
    if str('[[mods]]\nid = "'+url+'"\nenabled = true\n') in open(file).read():
        print("Mod already enabled")
    else:
        print("Mod not enabled; Enabling.")
        with open(file,'a') as f:
           f.write(str('\n[[mods]]\nid = "'+url+'"\nenabled = true\n'))
    print("Done!\n")
    MainMenu()
MainMenu()