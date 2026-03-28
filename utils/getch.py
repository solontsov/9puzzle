
import sys

# Detect OS and import the correct "getch"
if sys.platform == "win32":
    import msvcrt
    def getch():
        # .decode() converts the byte string to a regular string
        return msvcrt.getch().decode("utf-8", errors="ignore")
else:
    import termios
    import tty
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

if __name__ == "__main__":
    print("Press h, j, k, l or q to quit")
    while True:
        ch = getch()
        if ch in ("h", "j", "k", "l", "q"):
            print(f"\rYou pressed: {ch}") # Use \r to handle raw mode line endings
            if ch == "q":
                break
