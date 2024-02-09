import React, { useState, useEffect } from "react";

const mode = 1;

function Cursor({
  cursorPosition,
  setCursorPosition,
  screenSize,
  setScreenSize,
  pred,
}) {
  const [cursorAngle, setCursorAngle] = useState(0);

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
    const multiplier = 10;
    const [newDirection, angle] =
      mode === 0
        ? determineRegion(screenSize.width, screenSize.height, pred.x, pred.y)
        : moveRelative(pred);

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
  function generaliseAngle(theta) {
    let wasNegative = theta < 0;
    let tempTheta = theta < 0 ? -theta : theta;

    let angles = [0, 45, 90, 135, 180];
    for (let angle of angles) {
      if (tempTheta <= angle + 22.5 && tempTheta >= angle - 22.5) {
        if (wasNegative && angle !== 0 && angle !== 180) {
          return -angle;
        }
        return angle;
      }
    }

    throw new Error("Unexpected case: No angle match found.");
  }

  function calculateDirection(generalAngle) {
    // Convert angle to radians for trigonometric functions
    let radians = (generalAngle * Math.PI) / 180;

    // Calculate direction vector components
    let x = Math.round(Math.cos(radians));
    let y = Math.round(Math.sin(radians));

    // Normalize vectors for the specific angles used in this scenario
    // This ensures that the function returns the exact unit vectors expected for these angles
    return [{ x: x, y: y }, generalAngle];
  }

  function moveRelative(pred) {
    let x = pred.x;
    let y = pred.y;
    let angle = calculateAngle(cursorPosition.x, cursorPosition.y, x, y);
    let generalAngle = generaliseAngle(angle);
    console.log("General Angle: ", generalAngle);
    let unitDirection = calculateDirection(generalAngle);
    console.log(unitDirection[0]);
    return calculateDirection(generalAngle);
  }

  /**
   * Calculates how the cursor moves in relation to where the user in looking at on the screen.
   * Also reoreints the cursor so it points in the direction the user is looking at.
   *
   * @param {The width of the screen} width
   * @param {The height of the screen}} height
   * @param {The prediction X-Coordinate} x
   * @param {The prediction Y-Coordinate} y
   * @returns [The direction for the cursor to travel in, the angle of the cursor]
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
      style={{
        top: cursorPosition.y,
        left: cursorPosition.x,
        transform: `rotate(${cursorAngle}deg)`,
      }}
    />
  );
}

export default Cursor;
