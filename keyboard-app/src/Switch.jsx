import React from "react";

const Switch = ({ buttonClass, buttonLabels, onSwitchClick, currentWord }) => {
  return (
    <div
      className="flex-center-button switch-button"
      onClick={onSwitchClick}
      style={{
        display: "grid",
        gridTemplateRows: "1fr 1fr 1fr",
        gridTemplateColumns: "1fr 1fr 1fr",
        height: "20vh", // Total height to match button height
        width: "30vw", // Total width to match button width
        gap: "2.5vh 7.5vw", // Adjusted gaps
      }}
    >
      <button className={`flex-center-button ${buttonClass}-small`}>
        {buttonLabels[0]}
      </button>
      <button className={`flex-center-button ${buttonClass}-small`}>
        {buttonLabels[1]}
      </button>
      <button className={`flex-center-button ${buttonClass}-small`}>
        {buttonLabels[2]}
      </button>
      {/* Display currentWord */}
      <button
        style={{
          gridColumn: "1 / -1",
          textAlign: "center",
          color: "black", // Example color
          backgroundColor: "white", // Example background
          fontSize: "4rem", // Example font size
          border: "none",
          height: "5vh",
        }}
      >
        {currentWord}
      </button>
      <button className={`flex-center-button ${buttonClass}-small`}>
        {buttonLabels[3]}
      </button>
      <div /> {/* Empty div for spacing, no need for flex: 1 */}
      <button className={`flex-center-button ${buttonClass}-small`}>
        {buttonLabels[5]}
      </button>
    </div>
  );
};

export default Switch;
