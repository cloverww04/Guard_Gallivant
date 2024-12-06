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
    """Converts file into a 2d array"""
    return[list(line) for line in content.splitlines()]

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

def move(grid, start_pos, direction):
    """Moves the guard in the given direction, rotating upon hitting a '#'."""
    row, col = start_pos

    while True:
        # Check if the guard still exists
        if not find_guard(grid, direction):
            break

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
        if not (0 <= next_row < len(grid) and 0 <= next_col < len(grid[0])):
            break 

        if grid[next_row][next_col] == '#':
            direction = rotate_right(direction)
            return move(grid, (row, col), direction)

        # Move the guard
        grid[row][col] = 'x' 
        grid[next_row][next_col] = direction
        row, col = next_row, next_col

    grid[row][col] = 'x'

    total_x = sum(row.count('x') for row in grid)
    return grid, total_x

def print_map(grid):
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

        start_pos, direction = find_guard(grid)
        if start_pos:
            print(f"Found guard '{direction}' at position: {start_pos}")
            grid, total_x = move(grid, start_pos, direction)
            print("Map after the guard moves:")
            print_map(grid)
            print(f"Total number of 'x': {total_x}")
        else:
            print("Guard symbol not found in the map.")

