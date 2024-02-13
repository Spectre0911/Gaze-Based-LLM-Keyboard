import React, { useRef, useEffect } from "react";

const Switch = ({
  buttonClass,
  buttonLabels,
  currentWord,
  onSwitch,
  sendCoords,
  selected,
}) => {
  const frontButtonRef = useRef(null);

  useEffect(() => {
    // Could probably calculate this a bit more intelligently in app.js
    const handleResize = () => {
      if (frontButtonRef.current) {
        const rect = frontButtonRef.current.getBoundingClientRect();
        const coords = {
          topLeft: { x: rect.left, y: rect.top },
          topRight: { x: rect.right, y: rect.top },
          bottomLeft: { x: rect.left, y: rect.bottom },
          bottomRight: { x: rect.right, y: rect.bottom },
        };
        sendCoords("+", coords);
      }
    };

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  });

  const switchStyle = {
    backgroundColor:
      buttonClass === "light-blue-button" ? "#9496ff" : "#3d8ea6",
  };

  const currentWordStyle = {
    gridColumn: "1 / -1",
    textAlign: "center",
    color: selected ? "#96ff94" : "white",

    backgroundColor:
      buttonClass === "light-blue-button" ? "#9496ff" : "#3d8ea6",

    fontSize: "4rem", // Example font size
    border: "none",
    height: "5vh",
  };

  const buttonClassName = `flex-center-button ${buttonClass}-small ${
    selected ? "selected" : ""
  }`;

  return (
    <button
      ref={frontButtonRef}
      className={
        selected
          ? "switch flex-center-button switch-button selected"
          : "switch flex-center-button switch-button"
      }
      onClick={onSwitch}
      style={switchStyle}
    >
      <div className={buttonClassName}>{buttonLabels[0]}</div>
      <div className={buttonClassName}>{buttonLabels[1]}</div>
      <div className={buttonClassName}>{buttonLabels[2]}</div>
      <div style={currentWordStyle}>{currentWord}</div>
      <div className={buttonClassName}>{buttonLabels[3]}</div>
      <div />
      <div className={buttonClassName}>{buttonLabels[5]}</div>
    </button>
  );
};

export default Switch;
