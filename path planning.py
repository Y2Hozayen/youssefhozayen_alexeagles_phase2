import heapq
import random as rand
import tkinter as tk


class Robot:
    def __init__(self):
        self.path = []

    def set_path(self, path):
        self.path = path


cell_size = 60

# GUI class for displaying the grid
class GridGUI:
    def __init__(self, root, grid, robot):
        self.root = root
        self.canvas = tk.Canvas(root, width=size * cell_size, height=size * cell_size)
        self.canvas.pack()
        self.grid = grid
        self.robot = robot
        self.draw_grid()

    def draw_grid(canvas, grid, cell_size, path):
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Determine the color for each cell
                if (col, row) == (0, 0):
                    color = 'blue'  # Start point
                elif (col, row) == (size - 1, size - 1):
                    color = 'green'  # Goal point
                elif (col, row) in path:
                    color = 'yellow'  # Path of the robot
                elif grid[row][col] == 1:
                    color = 'white'  # Free cell
                else:
                    color = 'black'  # Obstacle

                # Draw the rectangle representing the cell
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")


# Creating a map
size = 8
grid = [[1 for _ in range(size)] for _ in range(size)]

# Adding random obstacles
for i in range(rand.randint(10, 20)):
    x, y = rand.randint(0, size - 1), rand.randint(0, size - 1)
    if (x, y) != (0, 0) and (x, y) != (size - 1, size - 1):
        grid[x][y] = 0

# A* algorithm
def a_star(grid, start, goal):
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Priority queue to store (cost, current position)
    open_set = []
    heapq.heappush(open_set, (0, start))

    parent = {}
    g_score = {start: 0}
    f_score = {start: manhattan(start, goal)}

    while open_set:
        # Get the current node with the lowest f_score
        _, current = heapq.heappop(open_set)

        # if goal reached, reconstruct the path backwards
        if current == goal:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1]

        for direction in movements:
            # Create the neighbor tuple instead of a list
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            # Ensure the neighbor is within grid bounds
            if 0 <= neighbor[0] < size and 0 <= neighbor[1] < size:
                # Skip if the neighbor is an obstacle
                if grid[neighbor[0]][neighbor[1]] == 0:
                    continue

                # Calculate the cumulative g_score
                cumulative_g_score = g_score[current] + 1

                # If the neighbor has not been visited or we found a shorter path to it
                if neighbor not in g_score or cumulative_g_score < g_score[neighbor]:
                    parent[neighbor] = current
                    g_score[neighbor] = cumulative_g_score
                    f_score[neighbor] = cumulative_g_score + manhattan(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # If there is no path
    return None

def valid_path(start, goal):
    while True:
        path = a_star(grid, start, goal)

        if path is not None:
            return grid, path

# Main function to initialize tkinter and draw the grid
def main():
    cell_size = 25  # Size of each cell in pixels

    # Initialize the tkinter window
    root = tk.Tk()
    root.title("Grid Drawing")

    # Set up the canvas size based on the grid and cell size
    canvas_width = size * cell_size
    canvas_height = size * cell_size
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Create a robot object
    robot = Robot()

    # Perform A* search to find a path from start (0, 0) to goal (size-1, size-1)
    start = (0, 0)
    goal = (size - 1, size - 1)
    grid, path = valid_path(start, goal)

    # Set the path for the robot
    robot.set_path(path)

    # Draw the grid on the canvas including the robot and path
    GridGUI.draw_grid(canvas, grid, cell_size, robot.path)

    # print the robots path
    print(f"robot path -->{robot.path[1:-1]}")

    # Start the tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
