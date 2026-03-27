import sys
import termios
import tty

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

print("Press h, j, k, l or q for quit")

while True:
    ch = getch()
    if ch in ("h", "j", "k", "l", "q"):
        print(f"You pressed: {ch}")
        if ch == "q":
            break
