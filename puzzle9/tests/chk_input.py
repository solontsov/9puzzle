from logging import raiseExceptions
from select import select
import sys

from readchar import readchar



if __name__ == "__main__":
    ch = readchar()
    code = ord(ch)

    print("You pressed:", ch)
    print("Code:", code)