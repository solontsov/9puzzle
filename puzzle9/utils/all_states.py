# class to hold all possible states and the minimum number of moves to get there
class AllStates:
    def __init__(self):
        self.states = {}
        next_states = {'123456780'}
        self.process_next_states(next_states, 1)

    def process_next_states(self, next_states, moves):
        new_next_states = set()
        for state in next_states:
            # check possible moves from this state (up, down, left, right)
            zero_index = state.index('0')
            # Example move logic (replace with actual move generation)
            for move in [-3, 3, -1, 1]:
                # Check that the move stays inside the 0..8 board range
                in_bounds = 0 <= zero_index + move < 9

                # Check that we are NOT moving left from column 0
                left_ok = not (zero_index % 3 == 0 and move == -1)

                # Check that we are NOT moving right from column 2
                right_ok = not (zero_index % 3 == 2 and move == 1)

                if in_bounds and left_ok and right_ok:
                    
                    new_state = list(state)
                    new_state[zero_index], new_state[zero_index + move] = new_state[zero_index + move], new_state[zero_index]
                    new_state = ''.join(new_state)
                    if self.add_state(new_state, moves):
                        new_next_states.add(new_state)
        
        if new_next_states and moves < 50:  # Limit the depth to debug
            self.process_next_states(new_next_states, moves + 1)

    def add_state(self, state: str, moves: int) -> bool:
        # Only add the state if it's not already present or if we found a shorter path to it
        # returns True if the state was added or updated, False otherwise
        if state not in self.states or moves < self.states[state]:
            self.states[state] = moves
            return True
        return False

    def get_moves(self, state: str) -> int:
        return self.states.get(state, None)
    
if __name__ == "__main__":
    all_states = AllStates()
    print(all_states.states)
    max_moves = max(all_states.states.values())
    print(f"Max moves to reach any state: {max_moves}")