import sys
import time
import os

# --- Platform-specific setup ---
if sys.platform == 'win32':
    import msvcrt
    def get_raw_byte():
        return msvcrt.getch().decode('ascii', errors='ignore')
    
    def get_extra_bytes():
        extra = ""
        while msvcrt.kbhit():
            extra += msvcrt.getch().decode('ascii', errors='ignore')
        return extra
else:
    import tty
    import termios
    import select
    import fcntl

    def get_raw_byte():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def get_extra_bytes():
        extra = ""
        fd = sys.stdin.fileno()
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)
        try:
            while True:
                chunk = sys.stdin.read(1)
                if not chunk: break
                extra += chunk
        except:
            pass
        finally:
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
        return extra

# --- Unified Logic ---
def readchar():
    ch = get_raw_byte()

    # Windows Arrow Keys often start with \x00 or \xe0
    # Unix Arrow Keys start with \x1b (ESC)
    if ch in ('\x1b', '\x00', '\xe0'):
        # Wait 50ms for the rest of the sequence to arrive
        time.sleep(0.05) 
        sequence = get_extra_bytes()
        
        if not sequence:
            # On Windows, if we caught \xe0 or \x00 with no sequence, 
            # it might be a weird function key; on Unix \x1b is ESC.
            return 'e' if ch == '\x1b' else f"raw:{repr(ch)}"

        # Mapping sequences to hjkl
        # Windows uses different codes than Linux
        win_map = {'H': 'k', 'P': 'j', 'M': 'l', 'K': 'h'} # Codes after \xe0
        nix_map = {'[A': 'k', '[B': 'j', '[C': 'l', '[D': 'h'} # Codes after \x1b
        
        if ch == '\x1b': return nix_map.get(sequence, f"esc+{sequence}")
        return win_map.get(sequence, f"winseq:{sequence}")

    if ch in ('\r', '\n'):
        return '\n'

    return ch

if __name__ == "__main__":
    print(f"Running on: {sys.platform}")
    print("Arrows -> hjkl | ESC -> 'e' | 'q' -> Quit")
    
    while True:
        try:
            res = readchar()
            print(f"Key: {repr(res)}")
            if res == 'q':
                break
        except KeyboardInterrupt:
            break