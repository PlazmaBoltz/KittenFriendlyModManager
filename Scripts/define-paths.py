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




cwd = os.getcwd()
parent = os.path.abspath(os.path.join(cwd, os.pardir))

# Window

import tkinter as tk

root = tk.Tk()
root.title("Kitten Friendly Mod Manager")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.iconbitmap((parent+"\\KittenFriendlyModManager\\Assets\\ksa_ico.ico"))
root.configure(bg='gray19') 

Sidebar = tk.Frame(root, bg='gray10', width=200, height=10000)
Sidebar.place(x=root.winfo_width()-(root.winfo_width()//20),y=0)

Close_button = tk.Button(root, text="Close", width=17, height=8, command=root.destroy, bg='gray48')
Close_button.pack()
Close_button.place(x=root.winfo_width()-(root.winfo_width()//25.3),y=root.winfo_height()-(root.winfo_height()//7.2))
Credits_button = tk.Button(root, text="Credits", width=17, height=8, command=root.destroy, bg='gray48')
Credits_button.pack()
Credits_button.place(x=root.winfo_width()-(root.winfo_width()//25.3),y=root.winfo_height()-(root.winfo_height()//4))

root.mainloop()
