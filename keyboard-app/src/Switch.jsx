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
    display: "grid",
    gridTemplateRows: "1fr 1fr 1fr",
    gridTemplateColumns: "1fr 1fr 1fr",
    height: "25.5vh",
    width: "31.5vw",
    gap: "2.5vh 7.5vw",
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
    <div
      ref={frontButtonRef}
      className={
        selected
          ? "flex-center-button switch-button selected"
          : "flex-center-button switch-button"
      }
      onClick={onSwitch}
      style={switchStyle}
    >
      <button className={buttonClassName}>{buttonLabels[0]}</button>
      <button className={buttonClassName}>{buttonLabels[1]}</button>
      <button className={buttonClassName}>{buttonLabels[2]}</button>
      {/* Display currentWord */}
      <button style={currentWordStyle}>{currentWord}</button>
      <button className={buttonClassName}>{buttonLabels[3]}</button>
      <div /> {/* Empty div for spacing, no need for flex: 1 */}
      <button className={buttonClassName}>{buttonLabels[5]}</button>
    </div>
  );
};

export default Switch;
