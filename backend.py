from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import networkx as nx

app = Flask(__name__)
CORS(app)

size = 8

class MazeBlocks:
    passage = 0
    wall = 1
    path1 = 2
    robot = 3
    treasure = 4
    

# Function to generate a maze
def generate_maze(size, num_obstacles):
    maze_map = [[MazeBlocks.passage] * size for _ in range(size)]
    
    # Place obstacles
    obstacles_placed = 0
    while obstacles_placed < num_obstacles:
        r = random.randint(0, size - 1)
        c = random.randint(0, size - 1)
        if (r, c) not in [(0, 0), (size-1, size-1)] and maze_map[r][c] == MazeBlocks.passage:
            maze_map[r][c] = MazeBlocks.wall
            obstacles_placed += 1

    maze_map[0][0] = MazeBlocks.robot  # Starting point
    maze_map[size-1][size-1] = MazeBlocks.treasure  # Ending point
    return maze_map

# Convert maze to a graph for pathfinding
def maze_to_graph(maze):
    G = nx.Graph()
    size = len(maze)

    for r in range(size):
        for c in range(size):
            if maze[r][c] == MazeBlocks.passage or maze[r][c] == MazeBlocks.robot or maze[r][c] == MazeBlocks.treasure:
                G.add_node((r, c))
                if r + 1 < size and maze[r + 1][c] in [MazeBlocks.passage, MazeBlocks.robot, MazeBlocks.treasure]:
                    G.add_edge((r, c), (r + 1, c))
                if c + 1 < size and maze[r][c + 1] in [MazeBlocks.passage, MazeBlocks.robot, MazeBlocks.treasure]:
                    G.add_edge((r, c), (r, c + 1))

    return G

# A* Pathfinding Algorithm
def astar(graph, start, goal):
    try:
        path = nx.astar_path(graph, start, goal, heuristic=lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]))
        return path
    except nx.NetworkXNoPath:
        return None

@app.route('/generate_maze', methods=['POST'])
def generate_maze_route():
    data = request.get_json()
    difficulty = data['difficulty']

    # Set obstacle count based on difficulty
    if difficulty == 'easy':
        num_obstacles = random.randint(5, 10)
    elif difficulty == 'medium':
        num_obstacles = random.randint(10, 15)
    elif difficulty == 'hard':
        num_obstacles = random.randint(15, 20)
    
    # Generate the maze
    maze = generate_maze(size, num_obstacles)
    
    # Return the maze as a JSON matrix
    return jsonify({"maze": maze})

@app.route('/solve_maze', methods=['POST'])
def solve_maze_route():
    data = request.get_json()
    maze = data['maze']
    
    # Convert the maze to a graph
    graph = maze_to_graph(maze)
    
    # Define start and goal points
    start = (0, 0)
    goal = (len(maze) - 1, len(maze) - 1)
    
    # Find the path using A* algorithm
    path = astar(graph, start, goal)

    if path is None:
        return jsonify({"message": "No path found!"})

    # Mark the path on the maze
    for r, c in path:
        if maze[r][c] not in [MazeBlocks.robot, MazeBlocks.treasure]:
            maze[r][c] = MazeBlocks.path1

    # Return the solved maze with the path
    return jsonify({"maze": maze, "path": path})

if __name__ == '__main__':
    app.run(port=5001, debug=True)

