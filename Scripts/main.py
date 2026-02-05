import subprocess
import sys
import requests
import json
def run_script_subprocess(script):
    try:
        result = subprocess.run(
            [sys.executable, script],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
        print("Script ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Script failed with exit code {e.returncode}:")
        print("Error output:", e.stderr)
    except FileNotFoundError:
        print("Error: target_script not found.")

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
        run_script_subprocess('Scripts/define-paths.py')
        MainMenu()
    elif textInput == "3":
        print("Ending Process")
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
    elif textInput == "2":
        print("\n")
    elif textInput == "3":
        print("\n")
    elif textInput == "4":
        MainMenu()
    else:
        print("Not a valid input. Please enter something else. \n")
        ModInstallMenu()
def RecieveMods():
    print("tba")


MainMenu()