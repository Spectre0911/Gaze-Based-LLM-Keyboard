import React from "react";
import "./App.css";
import Switch from "./Switch";

function App() {
  const handleClick = (label) => () => {
    alert(`Button clicked: ${label}`);
  };

  const buttons = ["I", "T", "A", "N", "%", "E", "DEL", "S", "."].map(
    (label) => {
      let className;
      switch (label) {
        case "DEL":
          className = "red-button";
          break;
        case ".":
          className = "red-button";
          break;
        case "%":
          className = "wildcard-button";
          break;
        case "S":
          return Switch({ onSwitchClick: handleClick("Switch") });
        default:
          className = "light-blue-button"; // Default class
          break;
      }

      return (
        <button className={className} key={label} onClick={handleClick(label)}>
          {label}
        </button>
      );
    }
  );

  return (
    <div>
      <div className="grid-container">{buttons}</div>
      <button className="space-button" onClick={handleClick("Space")}>
        Space
      </button>
    </div>
  );
}

export default App;
