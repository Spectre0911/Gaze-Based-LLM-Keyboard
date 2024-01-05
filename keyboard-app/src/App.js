import React, { useState } from "react";
import "./App.css";
import Switch from "./Switch";

function getOppositeColor(currentColor) {
  return currentColor === "light-blue-button"
    ? "dark-blue-button"
    : "light-blue-button";
}

function App() {
  // State to track the button class
  const states = [
    ["I", "T", "A", "N", "%", "E", "DEL", "+", "."],
    ["D", "O", "S", "L", "%", "R", "DEL", "+", "."],
    ["D", "O", "S", "L", "%", "R", "DEL", "+", "."],
  ];

  const [buttonClass, setButtonClass] = useState("light-blue-button");
  const [stateNumber, setStateNumber] = useState(0);
  const [buttonLabels, setButtonLabels] = useState(states[0]);

  const handleClick = (label) => () => {
    alert(`Button clicked: ${label}`);
  };

  // Function to toggle the button class
  const onSwitch = () => {
    setStateNumber((prevStateNumber) => (prevStateNumber === 0 ? 1 : 0));

    setButtonClass((prevClass) =>
      prevClass === "light-blue-button"
        ? "dark-blue-button"
        : "light-blue-button"
    );
    setButtonLabels((prevLabels) => states[stateNumber]);
  };

  const buttons = buttonLabels.map((label) => {
    let className;
    switch (label) {
      case "DEL":
        className = "flex-center-button red-button";
        break;
      case ".":
        className = "flex-center-button red-button";
        break;
      case "%":
        className = "flex-center-button wildcard-button";
        break;
      case "<":
      case ">":
        className = "flex-center-button purple-button";
        break;
      case "+":
        return (
          <Switch
            key="Switch"
            buttonClass={getOppositeColor(buttonClass)}
            buttonLabels={states[stateNumber]}
            onSwitchClick={onSwitch}
          />
        );
      default:
        className = `flex-center-button ${buttonClass}`; // Use state for class
        break;
    }

    return (
      <button className={className} key={label} onClick={handleClick(label)}>
        {label}
      </button>
    );
  });

  return (
    <div>
      <div className="grid-container">{buttons}</div>
      <button
        className="flex-center-button space-button"
        onClick={handleClick("Space")}
      >
        Space
      </button>
    </div>
  );
}

export default App;
