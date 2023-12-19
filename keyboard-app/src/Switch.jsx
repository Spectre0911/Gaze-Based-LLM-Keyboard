import React from "react";

const Switch = ({ onSwitchClick }) => {
  return (
    <button className="switch-button">
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <div className="dark-blue-button-small">D</div>
          <div className="dark-blue-button-small">O</div>
          <div className="dark-blue-button-small">S</div>
        </div>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <div className="dark-blue-button-small">L</div>
          <div className="dark-blue-button-small">R</div>
        </div>
      </div>
    </button>
  );
};

export default Switch;
