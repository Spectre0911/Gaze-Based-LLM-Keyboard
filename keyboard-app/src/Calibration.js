import React, { useState, useEffect } from "react";
import Dot from "./Dot";
import App from "./App";

const Calibration = ({ prediction, testMode }) => {
  const totalDots = 12;

  const [dotsClicked, setDotsClicked] = useState(0);
  const order = [0, 1, 2, 5, 8, 11, 10, 9, 6, 3, 4, 7];
  const [currentDotIndex, setCurrentDotIndex] = useState(0);
  const [currentDot, setCurrentDot] = useState(0);

  const handleMaxClicks = () => {
    setDotsClicked(dotsClicked + 1);
  };

  useEffect(() => {
    setCurrentDot(order[currentDotIndex]);
  }, [currentDotIndex]);

  if (dotsClicked === totalDots || testMode) {
    return <App pred={prediction} />;
  }

  return (
    <div className="dot-grid-container">
      {[...Array(totalDots)].map((_, i) => (
        <Dot
          key={i}
          onMaxClicksReached={handleMaxClicks}
          index={i}
          currentDot={currentDot}
          setCurrentDotIndex={setCurrentDotIndex}
        />
      ))}
    </div>
  );
};

export default Calibration;
