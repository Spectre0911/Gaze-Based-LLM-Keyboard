import React, { useState, useEffect } from "react";

// WHY DOES JSX NOT SUPPORT ENUMS!!
const Mode = {
  JOYSTICK: 0,
  RELATIVE8: 1,
  RELATIVE4: 2,
};

// The multiplier for the cursor movement
const multiplier = 20;

function Cursor({
  cursorPosition,
  setCursorPosition,
  screenSize,
  setScreenSize,
  pred,
}) {
  const [cursorAngle, setCursorAngle] = useState(0);
  const [mode, setMode] = useState(Mode.RELATIVE4);

  useEffect(() => {
    // Reset cursor position on resize to center of screen
    const updateCursorOnResize = (newWidth, newHeight) => {
      setCursorPosition({
        x: newWidth / 2,
        y: newHeight / 2,
      });
    };

    const handleResize = () => {
      const newWidth = window.innerWidth;
      const newHeight = window.innerHeight;

      setScreenSize({
        width: newWidth,
        height: newHeight,
      });

      updateCursorOnResize(newWidth, newHeight);
    };
    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    const [newDirection, angle] = determineMovementType();

    let newX = Math.min(
      Math.max(multiplier * newDirection.x + cursorPosition.x, 0),
      screenSize.width - 40
    );
    let newY = Math.min(
      Math.max(multiplier * newDirection.y + cursorPosition.y, 0),
      screenSize.height - 40
    );

    const updatedPos = { x: newX, y: newY };
    setCursorPosition(updatedPos);
    setCursorAngle(angle);
  }, [pred]);

  /**
   * For the current mode, determines the movement type to be used
   *
   * @returns (Func) - The movement type function to be used
   */
  function determineMovementType() {
    var angles = [0, 45, 90, 135, 180];
    let thresh = 22.5;
    switch (mode) {
      case Mode.JOYSTICK:
        return determineRegion(
          screenSize.width,
          screenSize.height,
          pred.x,
          pred.y
        );
      case Mode.RELATIVE8:
        return moveRelative(pred, angles, thresh);
      case Mode.RELATIVE4:
        angles = [0, 90, 180];
        return moveRelative(pred, angles, thresh * 2);
      default:
        throw new Error("Invalid mode");
    }
  }

  /**
   * Calculates the angle between two points
   *
   * @param {float} x1
   * @param {float} y1
   * @param {float} x2
   * @param {float} y2
   * @returns
   */
  function calculateAngle(x1, y1, x2, y2) {
    // Calculate the difference in coordinates
    var deltaX = x2 - x1;
    var deltaY = y2 - y1;
    // Calculate the angle in radians
    var angleRadians = Math.atan2(deltaY, deltaX);
    // Convert radians to degrees
    var angleDegrees = angleRadians * (180 / Math.PI);
    // Return the angle
    return angleDegrees;
  }

  /**
   * Rounds the angle to the nearest cardinal direction which are defined in angles
   *
   * @param {Float} theta
   * @param {Float} angles
   * @param {Float} thresh
   * @returns
   */
  function generaliseAngle(theta, angles, thresh) {
    let wasNegative = theta < 0;
    let tempTheta = theta < 0 ? -theta : theta;

    for (let angle of angles) {
      if (tempTheta <= angle + thresh && tempTheta >= angle - thresh) {
        if (wasNegative && angle !== 0 && angle !== 180) {
          return -angle;
        }
        return angle;
      }
    }

    throw new Error("Unexpected case: No angle match found.");
  }

  /**
   * Returns the normalised direction the cursor should move in.
   *
   * @param {Float} generalAngle
   * @returns {}
   */
  function calculateDirection(generalAngle) {
    // Convert angle to radians for trigonometric functions
    let radians = (generalAngle * Math.PI) / 180;

    // Calculate direction vector components
    let x = Math.round(Math.cos(radians));
    let y = Math.round(Math.sin(radians));

    return [{ x: x, y: y }, generalAngle];
  }

  /**
   * Rather than a centralised joystick approach, this moves the cursor in the direction the user is looking a, relative to the cursor itself.
   *
   * @param {Float} pred
   * @returns
   */
  function moveRelative(pred, angles, thresh) {
    let x = pred.x;
    let y = pred.y;
    let angle = calculateAngle(cursorPosition.x, cursorPosition.y, x, y);
    let generalAngle = generaliseAngle(angle, angles, thresh);
    let unitDirection = calculateDirection(generalAngle);
    return unitDirection;
  }

  /**
   * Calculates how the cursor moves in relation to where the user in looking at on the screen.
   * Also reorients the cursor so it points in the direction the user is looking at.
   *
   * @param {Float} width
   * @param {Float} height
   * @param {Float} x
   * @param {Float} y
   * @returns {Array} [The direction for the cursor to travel in, the angle of the cursor]
   */
  function determineRegion(width, height, x, y) {
    let xDirection = 0;
    let yDirection = 0;

    // Determine x direction
    if (x < width / 3) {
      xDirection = -1;
    } else if (x >= (2 * width) / 3) {
      xDirection = 1;
    }

    // Determine y direction
    if (y < height / 3) {
      yDirection = -1;
    } else if (y >= (2 * height) / 3) {
      yDirection = 1;
    }

    // Calculate the angle based on x and y direction
    let angle = 0;
    if (xDirection === 0 && yDirection === 0) {
      angle = 0; // Center
    } else {
      angle = Math.atan2(yDirection, xDirection) * (180 / Math.PI);
      if (angle < 0) {
        angle += 360;
      }
    }

    return [{ x: xDirection, y: yDirection }, angle];
  }

  return (
    <div
      className="cursor"
      key="cursor"
      style={{
        top: cursorPosition.y,
        left: cursorPosition.x,
        transform: `rotate(${cursorAngle}deg)`,
      }}
    />
  );
}

export default Cursor;
