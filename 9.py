#!/usr/bin/env python3

# 9 sqares
from utils.clear import clear

clear()

reset = "\033[0m"
tilecolor = f"\033[{38};{44}m"
state="12345678 "
offset = "   "
print()
for row in range(0, 3):
    for subrow in range(0, 3):  
        print(offset, end="  ")
        for column in range(0, 3):
            index = 3*row+column
            label = " "
            code= tilecolor
            current = state[index]
            if current== " ":
                code = ""
            if subrow == 1:
                label = current
            print(f"{code}   {label}   {reset}", end="  ")
        print()
    print()
