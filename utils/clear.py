import os
import platform

def clear():
    command = "cls" if platform.system() == "Windows" else "clear"
    os.system(command)

if __name__ == "__main__":
    # This runs ONLY when you execute: python clear.py
    clear()
