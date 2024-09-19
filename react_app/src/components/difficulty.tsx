import React from "react";

// Define the props interface for the DifficultySetting component
interface DifficultySettingProps {
  value: string; // The current value (difficulty)
  onChange: (event: React.ChangeEvent<HTMLSelectElement>) => void; // The onChange event handler
}

// Functional component accepting props
const DifficultySetting: React.FC<DifficultySettingProps> = ({
  value,
  onChange,
}) => {
  return (
    <select value={value} onChange={onChange}>
      <option value="easy">Easy</option>
      <option value="medium">Medium</option>
      <option value="hard">Hard</option>
    </select>
  );
};

export default DifficultySetting;
