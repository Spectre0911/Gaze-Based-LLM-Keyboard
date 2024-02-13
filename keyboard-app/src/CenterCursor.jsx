import React, { Component, useEffect, useRef, useState } from "react";
import Calibration from "./Calibration";
import "./CenterCursor.css";

const testMode = true;

const CenterCursor = ({ prediction }) => {
  const [cursorCentered, setCursorCentered] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const dotRef = useRef(null);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  // Function to simulate a click in the center of the component
  const simulateCenterClick = () => {
    const dot = dotRef.current;
    console.log("Ref not attatched");
    if (!dot) return; // Guard clause if the ref is not attached
    console.log("Ref attatched");
    const { left, top, width, height } = dot.getBoundingClientRect();
    const centerX = left + width / 2;
    const centerY = top + height / 2;

    // For demonstration: Logs the center point
    console.log(`Center X: ${centerX}, Center Y: ${centerY}`);

    // Create and dispatch the click event
    const clickEvent = new MouseEvent("click", {
      view: window,
      bubbles: true,
      cancelable: true,
      clientX: centerX,
      clientY: centerY,
    });
    dot.dispatchEvent(clickEvent);
    setCursorCentered(true);
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.code === "Space" && isHovered) {
        console.log("Space pressed");
        simulateCenterClick();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [isHovered]);

  return cursorCentered | testMode ? (
    <Calibration prediction={prediction} testMode={testMode} />
  ) : (
    <div className="center-div">
      <h1 className="tutorial-font">
        {isHovered
          ? "Look at the center of the box and press spacebar"
          : "Center cursor in below box"}
      </h1>
      <button
        ref={dotRef}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={simulateCenterClick}
        className={"center-cursor-button"}
      ></button>
    </div>
  );
};

export default CenterCursor;
