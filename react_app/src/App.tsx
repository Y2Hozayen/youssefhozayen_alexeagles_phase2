import React, { useState } from "react";
import MatrixGrid from "./components/MatrixGrid";
import Button from "./components/button";
import DifficultySetting from "./components/difficulty";

// Define the initial matrix
const initialMatrix: number[][] = [
  [3, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 4],
];

const App: React.FC = () => {
  const [matrix, setMatrix] = useState<number[][]>(initialMatrix);
  const [difficulty, setDifficulty] = useState("easy"); // Add a state for difficulty

  // Function to reset the maze to its initial state
  const resetMaze = () => {
    setMatrix(initialMatrix);
  };

  // Fetch API function to get a new maze from the backend and update the state
  const fetchMatrix = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5001/generate_maze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ difficulty }), // Send difficulty as part of the request
      });

      if (!response.ok) {
        throw new Error("Failed to fetch the matrix");
      }

      const data = await response.json();
      if (data.maze && Array.isArray(data.maze)) {
        setMatrix(data.maze);
      } else {
        console.error("Invalid matrix data");
      }
    } catch (error) {
      console.error("Error fetching the matrix:", error);
    }
  };

  // Function to send the current maze to the backend for solving
  const solveMaze = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5001/solve_maze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ maze: matrix }), // Send the current maze
      });

      if (!response.ok) {
        throw new Error("Failed to solve the maze");
      }

      const data = await response.json();
      if (data.maze && Array.isArray(data.maze)) {
        setMatrix(data.maze); // Update the matrix with the solved maze
      } else {
        console.error("Invalid solved maze data");
        window.alert("The maze is unsolvable. Please try again.");
      }
    } catch (error) {
      console.error("Error solving the maze:", error);
    }
  };

  return (
    <>
      <h1>Maze Game</h1>
      <MatrixGrid matrix={matrix} />
      <ul>
        <li>
          <div style={{ marginBottom: "20px" }}>
            <DifficultySetting
              value={difficulty} // Pass the current difficulty value
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                setDifficulty(e.target.value)
              } // Handle change event
            />
          </div>
        </li>
        <li>
          <div style={{ marginBottom: "20px" }}>
            <Button color="primary" onClick={fetchMatrix}>
              Fetch New Maze
            </Button>
          </div>
        </li>
        <li>
          <div style={{ marginBottom: "20px" }}>
            <Button color="primary" onClick={resetMaze}>
              Reset Maze
            </Button>
          </div>
        </li>
        <li>
          <div style={{ marginBottom: "20px" }}>
            <Button color="primary" onClick={solveMaze}>
              Solve Maze
            </Button>
          </div>
        </li>
      </ul>
    </>
  );
};

export default App;
