# import sys
import os
import platform

from puzzle9.utils.readchar_remapped import readchar
from puzzle9.utils.readpuzz import read_strings_from_file

def move(state, direction, count):
    """Calculates the new state after a move."""
    empty_idx = state.find("0")  # Find the index of the empty space
    row, col = divmod(empty_idx, 3)
    
    # Mapping Vim keys to (row_change, col_change)
    moves = {
        'h': (0, 1), # Left
        'l': (0, -1),  # Right
        'k': (1, 0), # Up
        'j': (-1, 0)   # Down
    }
    
    dr, dc = moves[direction]
    new_row, new_col = row + dr, col + dc

    # Boundary check for 3x3 grid
    if 0 <= new_row < 3 and 0 <= new_col < 3:
        target_idx = new_row * 3 + new_col
        chars = list(state)
        # Swap the empty space with the target tile
        chars[empty_idx], chars[target_idx] = chars[target_idx], chars[empty_idx]
        return "".join(chars), count + 1
    
    return state, count # Return original if move is out of bounds

def draw_board(state, count):
    """Renders the colored 3x3 grid to the terminal."""
    reset = "\033[0m"
    tile_color = "\033[37;44m"      # White text on Blue background
    empty_color = "\033[37;40m"     # White text on Black background
    
    # \033[H moves cursor to top-left; \033[J clears from cursor down
    # This prevents the screen from 'flickering' or scrolling
    print("\033[H\033[J", end="") 
    print("--- 9-SQUARES ---")
    print("Keys: [h,j,k,l] to move, [u, r] to undo, redo | [q] to quit")
    print("[o] to open the list of predefined puzzles\n")

    for row in range(3):
        # Each 'tile' is 3 terminal rows high for a square look
        for subrow in range(3):
            for col in range(3):
                idx = 3 * row + col
                char = state[idx]
                
                # Pick color: Black for the hole, Blue for tiles
                color = empty_color if char == "0" else tile_color
                
                # Only show the number in the middle subrow and if it's not zero
                label = char if subrow == 1 and char != "0" else " "
                
                # Draw the tile segment
                print(f"{color}   {label}   {reset}", end="  ")
            print() # End of terminal line (subrow)
        print() # Vertical gap between tiles
    print("Moves: ", count)

def getPuzzle():
    '''Shows a list of predefined puzzles (read from puzzle.txt) and returns the selected one.'''    
    file_path = "puzzle9/puzzle.txt"  # Replace with your file path

    try:
        results = read_strings_from_file(file_path)
        if results:
            highlight_index = 0
            #loop until user selects a valid puzzle
            while True:
                # clear the screen before showing the puzzles
                print("\033[H\033[J", end="")
                print("Selected puzzle [k,j, Enter, Escape]:")
                # highlight the line  with blue background
                for i, item in enumerate(results):
                    if i == highlight_index:
                        print(f"\033[44m{item}\033[0m")
                    else:
                        print(item)
                # capture user input for navigation
                ch = readchar().lower()
                if ch == 'k':  # Move up
                    highlight_index = (highlight_index - 1) % len(results)
                elif ch == 'j':  # Move down
                    highlight_index = (highlight_index + 1) % len(results)
                elif ch in ('\n', '\r'):  # Enter key to select
                    return results[highlight_index]   
                elif ch == 'e':  # Escape key to cancel
                    return None     
        else:
            print("No matching strings found.")
    except FileNotFoundError as fnf:
        print(fnf)

def main():

    if platform.system() == "Windows":
        os.system("cls")
        
    # Initial state (The goal state)
    state = "851374260"  # '0' represents the empty space
    
    # A win condition 
    goal = "123456780"

    count = 0
    history = []  # Stack for Undo
    redo_stack = []  # Stack for Redo

    try:
        # Hide the cursor for a cleaner game look
        print("\033[?25l", end="")
        
        while True:
            draw_board(state, count)
            
            if state == goal:
                print("\033[32mSOLVED! You win!\033[0m")
            
            # Capture single keypress
            ch = readchar().lower()
            # --- OPEN PREDEFINED PUZZLES ---
            if ch == 'o':
                new_state = getPuzzle()
                if new_state == None:
                    continue
                state = new_state
                count = 0
                history.clear()
                redo_stack.clear()
                # break
                continue

            # --- QUIT ---
            if ch == 'q':
                break

            # --- UNDO ---
            if ch == 'u':
                if history:
                    # Save current to Redo before going back
                    redo_stack.append(state)
                    state = history.pop()
                    count -= 1
                continue

            # --- REDO ---
            if ch == 'r':
                if redo_stack:
                    # Save current to History before going forward
                    history.append(state)
                    state = redo_stack.pop()
                    count += 1
                continue

            # --- NORMAL MOVE ---
            if ch in ('h', 'j', 'k', 'l'):
                new_state, new_count = move(state, ch, count)
                if new_count != count:
                    # Save to history
                    history.append(state)
                    # Redo stack is cleared because we made a new move
                    redo_stack.clear()
                    state, count = new_state, new_count

    except KeyboardInterrupt:
        pass
    finally:
        # Re-show the cursor before exiting
        print("\033[?25h")
        print("\nThanks for playing!")

if __name__ == "__main__":
    main()
