import React from "react";
import "./MatrixGrid.css";

// Define the props type interface
interface MatrixGridProps {
  matrix: number[][]; // 2D array of numbers
}

const MatrixGrid: React.FC<MatrixGridProps> = ({ matrix = [] }) => {
  return (
    <div className="grid-container">
      {matrix.map((row, rowIndex) => (
        <div className="grid-row" key={rowIndex}>
          {row.map((cell, colIndex) => (
            <div
              key={`${rowIndex}-${colIndex}`}
              className={`grid-cell color-${cell}`}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default MatrixGrid;
