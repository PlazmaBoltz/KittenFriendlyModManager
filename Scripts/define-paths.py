# Scripts
import os

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
    
with open('Paths/ManifestDirectory', "w") as file:
    file.write(getManifest())
with open('Paths/KSADirectory', "w") as file:
    file.write(getDirectory())