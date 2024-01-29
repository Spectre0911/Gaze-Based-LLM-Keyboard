import React, { useState, useEffect } from "react";
import Dot from "./Dot";
import App from "./App";
const Calibration = ({ prediction }) => {
  const [dotsClicked, setDotsClicked] = useState(0);
  const totalDots = 12;

  const handleMaxClicks = () => {
    setDotsClicked(dotsClicked + 1);
  };

  if (dotsClicked !== totalDots) {
    return <App pred={prediction} />;
  }

  return (
    <div className="dot-grid-container">
      {[...Array(totalDots)].map((_, i) => (
        <Dot key={i} onMaxClicksReached={handleMaxClicks} />
      ))}
    </div>
  );
};

export default Calibration;
