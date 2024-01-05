import React from "react";

const Switch = ({ buttonClass, buttonLabels, onSwitchClick }) => {
  return (
    <div
      className="flex-center-button switch-button"
      onClick={onSwitchClick}
      style={{
        display: "grid",
        gridTemplateRows: "1fr 1fr", // Two rows
        gridTemplateColumns: "1fr 1fr 1fr", // Three columns
        height: "100%",
        gap: "10vh 7.5vw", // Adjust the gap as needed
      }}
    >
      <div className={`flex-center-button ${buttonClass}-small`}>
        {buttonLabels[0]}
      </div>
      <div className={`flex-center-button ${buttonClass}-small`}>
        {" "}
        {buttonLabels[1]}
      </div>
      <div className={`flex-center-button ${buttonClass}-small`}>
        {" "}
        {buttonLabels[2]}
      </div>
      <div className={`flex-center-button ${buttonClass}-small`}>
        {" "}
        {buttonLabels[3]}
      </div>
      <div /> {/* Empty div for spacing, no need for flex: 1 */}
      <div className={`flex-center-button ${buttonClass}-small`}>
        {" "}
        {buttonLabels[5]}
      </div>
    </div>
  );
};

export default Switch;
