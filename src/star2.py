import os

def read_file(filepath):
    """Reads the input file and returns its content."""
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found.")
        return None

def create_grid(content):
    """Converts file into a 2D array."""
    return [list(line) for line in content.splitlines()]

def rotate_right(direction):
    """Rotates the direction 90 degrees to the right."""
    directions = ['^', '>', 'v', '<']
    idx = directions.index(direction)
    return directions[(idx + 1) % len(directions)]

def find_guard(grid, symbols="^>v<"):
    """Finds the position and direction of the guard symbol."""
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell in symbols:
                return (row_idx, col_idx), cell
    return None, None

def simulate_with_obstruction(grid, obstruction_pos):
    """Simulates the guard's movement with a test obstruction."""
    # Create a copy of the grid to avoid modifying the original
    test_grid = [row[:] for row in grid]
    
    # Place the obstruction dynamically
    row, col = obstruction_pos
    test_grid[row][col] = 'O'
    
    # Find the guard's starting position and direction
    start_pos, direction = find_guard(test_grid)
    if not start_pos:
        return False  # No guard found, invalid grid
    
    # Keep track of visited states (position and direction)
    visited_states = set()
    
    # Simulate guard movement
    row, col = start_pos
    while True:
        # Record the current state
        state = (row, col, direction)
        if state in visited_states:
            return True  # Loop detected
        visited_states.add(state)
        
        # Determine the next position
        next_row, next_col = row, col
        if direction == '^':
            next_row -= 1
        elif direction == '>':
            next_col += 1
        elif direction == 'v':
            next_row += 1
        elif direction == '<':
            next_col -= 1
        
        # Check for bounds
        if not (0 <= next_row < len(test_grid) and 0 <= next_col < len(test_grid[0])):
            break  # Guard moves out of bounds
        
        # Handle the next cell
        next_cell = test_grid[next_row][next_col]
        if next_cell == '#':  # Wall, rotate and stay in place
            direction = rotate_right(direction)
        elif next_cell == 'O':  # Obstruction, treat like a wall
            direction = rotate_right(direction)
        elif next_cell in '^>v<':  # Guard moving into itself
            break
        else:  # Move to the next cell
            test_grid[row][col] = 'x'  # Mark the current position as visited
            test_grid[next_row][next_col] = direction
            row, col = next_row, next_col

    return False  # No loop detected

def find_valid_obstruction_positions(grid):
    """Finds all valid positions for placing an obstruction."""
    valid_positions = []
    guard_pos, _ = find_guard(grid)
    if not guard_pos:
        print("No guard found. Exiting.")
        return valid_positions

    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == '.' and (row_idx, col_idx) != guard_pos:
                # Test this position as an obstruction
                if simulate_with_obstruction(grid, (row_idx, col_idx)):
                    valid_positions.append((row_idx, col_idx))
    return valid_positions

def print_map(grid):
    """Prints the map in a readable format."""
    for row in grid:
        print(''.join(row))

# Main Program
if __name__ == "__main__":
    input_file = "data1.txt"
    print(f"Looking for file: {input_file}")
    content = read_file(input_file)

    if content:
        grid = create_grid(content)
        print("Original Map:")
        print_map(grid)

        # Find valid obstruction positions
        valid_positions = find_valid_obstruction_positions(grid)
        print("Valid obstruction positions:")
        for pos in valid_positions:
            print(pos)
        print(f"Total number of valid positions: {len(valid_positions)}")
    else:
        print("Failed to load the map.")
