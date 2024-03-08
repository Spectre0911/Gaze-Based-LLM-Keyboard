import React, { useEffect, useRef, useState } from "react";
import Calibration from "./Calibration";
import "./CenterCursor.css";

const keyboardTestMode = false;

const CenterCursor = ({ prediction, setCalibrationComplete, order }) => {
  const [cursorCentered, setCursorCentered] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const dotRef = useRef(null);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  useEffect(() => {
    if (!cursorCentered) {
      const handleKeyDown = (event) => {
        if (event.code === "Space" && isHovered) {
          setCursorCentered(true);
        }
      };

      window.addEventListener("keydown", handleKeyDown);

      return () => {
        window.removeEventListener("keydown", handleKeyDown);
      };
    }
  }, [isHovered]);

  return cursorCentered | keyboardTestMode ? (
    <Calibration
      prediction={prediction}
      keyboardTestMode={keyboardTestMode}
      setCalibrationComplete={setCalibrationComplete}
    />
  ) : (
    <div>
      <div className="center-div">
        <h1 className="tutorial-font">
          {isHovered
            ? "Look at the center of the box"
            : "Center cursor in below box"}
        </h1>
        <button
          ref={dotRef}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          className={"center-cursor-button"}
        ></button>
        <h1 className="tutorial-font">
          {isHovered ? "Press SPACE" : order.join("")}
        </h1>
      </div>
    </div>
  );
};

export default CenterCursor;
