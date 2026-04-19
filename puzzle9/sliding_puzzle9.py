class SlidingPuzzle9:
    def __init__(self, all_states):
        self.all_states = all_states
        self.goal = "123456780"
        self.load_random_hard_state()

    def load_random_hard_state(self):
        hard_states = [s for s, m in self.all_states.states.items() if m > 10]
        self.reset_session(random.choice(hard_states))

    def reset_session(self, state):
        self.state = state
        self.count = 0
        self.history = []
        self.redo_stack = []
        self.optimal_at_start = self.all_states.get_moves(state)

    def try_move(self, direction):
        moves = {'h': (0, 1), 'l': (0, -1), 'k': (1, 0), 'j': (-1, 0)} # TODO: check this mapping
        dr, dc = moves[direction]
        
        idx = self.state.find("0")
        r, c = divmod(idx, 3)
        nr, nc = r + dr, c + dc

        if 0 <= nr < 3 and 0 <= nc < 3:
            self.history.append(self.state)
            self.redo_stack.clear()
            
            chars = list(self.state)
            target_idx = nr * 3 + nc
            chars[idx], chars[target_idx] = chars[target_idx], chars[idx]
            
            self.state = "".join(chars)
            self.count += 1
            return True
        return False

    def undo(self):
        if self.history:
            self.redo_stack.append(self.state)
            self.state = self.history.pop()
            self.count -= 1

    def redo(self):
        if self.redo_stack:
            self.history.append(self.state)
            self.state = self.redo_stack.pop()
            self.count += 1

    def get_move_color(self):
        """Returns green if on optimal path, red otherwise."""
        min_remaining = self.all_states.get_moves(self.state)
        if min_remaining is not None and (self.count + min_remaining == self.optimal_at_start):
            return "\033[32m" # Green
        return "\033[31m"     # Red

def draw_board(game):
    # TODO: move this to main.py
    # (Same terminal clearing logic)
    # ...
    # Use the helper to determine move count color
    color = game.get_move_color()
    print(f"{color}Moves: {game.count}\033[0m (Optimal: {game.optimal_at_start})")

''' Note: The above code is a refactored version of the original, 
with the main game logic encapsulated in a SlidingPuzzle9 class.
TODO: refactor main.py
def main():
    all_states = AllStates()
    game = SlidingPuzzle(all_states)
    
    # Hide cursor
    print("\033[?25l", end="")

    while True:
        draw_board(game)
        
        if game.state == game.goal:
            # Handle win logic...
            pass

        ch = readchar().lower()
        
        if ch == 'q': break
        elif ch == 'o':
            new_s = getPuzzle()
            if new_s: game.reset_session(new_s)
        elif ch == 'u': game.undo()
        elif ch == 'r': game.redo()
        elif ch in 'hjkl':
            game.try_move(ch)
            '''