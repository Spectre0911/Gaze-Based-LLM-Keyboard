import React, { useState, useRef, useEffect } from "react";

const Dot = ({
  onMaxClicksReached,
  index,
  currentDot,
  setCurrentDotIndex,
  setCurrentCenter,
  totalDots,
}) => {
  const [clicks, setClicks] = useState(0);
  const [greenValue, setGreenValue] = useState(0);
  const [redValue, setRedValue] = useState(255);
  const [secondsPassed, setSecondsPassed] = useState(3);
  const [center, setCenter] = useState({ x: 0, y: 0 });

  const dotRef = useRef(null);

  const updateCenter = async () => {
    const dot = dotRef.current;
    if (dot) {
      const { left, top, width, height } = dot.getBoundingClientRect();
      const centerX = left + window.scrollX + width / 2;
      const centerY = top + window.scrollY + height / 2;
      const newCenter = { x: centerX, y: centerY };
      setCenter(newCenter);
      if (index === currentDot) {
        setCurrentCenter(newCenter);
      }
    }
  };

  useEffect(() => {
    updateCenter();
    // Set up event listener for window resize
    const handleResize = () => {
      updateCenter();
    };
    window.addEventListener("resize", handleResize);

    // Clean up event listener
    return () => window.removeEventListener("resize", handleResize);
  }, []); // Empty dependency array means this effect runs once on mount and cleanup on unmount

  useEffect(() => {
    // This effect updates the center when the currentDot changes, which could affect the dot's position
    updateCenter();
  }, [currentDot]);

  const handleClick = async () => {
    const newClicks = clicks + 1;
    setClicks(newClicks);

    // Update the green value, ensuring it doesn't exceed 255
    const newGreenValue = Math.min(greenValue + 100, 255);
    const newRedValue = Math.max(redValue - 50, 0);

    setRedValue(newRedValue);
    setGreenValue(newGreenValue);

    setCurrentDotIndex((prev) => (prev < totalDots - 1 ? prev + 1 : 0));

    if (newClicks === 3) {
      onMaxClicksReached();
    }
  };

  // Function to simulate a click in the center of the component
  const simulateCenterClick = () => {
    const dot = dotRef.current;
    if (!dot) return; // Guard clause if the ref is not attached

    // Create and dispatch the click event
    const clickEvent = new MouseEvent("click", {
      view: window,
      bubbles: true,
      cancelable: true,
      clientX: center.x,
      clientY: center.y,
    });
    dot.dispatchEvent(clickEvent);
    setSecondsPassed(3);
  };

  useEffect(() => {
    // Check if the current dot is the targeted dot
    if (index === currentDot) {
      // Set a timer to delay the execution

      if (secondsPassed <= 0) {
        simulateCenterClick();
      } else {
        const timer = setTimeout(() => {
          setSecondsPassed((prev) => prev - 1);
        }, 400);

        // Return a cleanup function to clear the timeout if the component unmounts
        // or if the dependencies of useEffect change before the timer is completed.
        return () => clearTimeout(timer);
      }
    }
  }, [currentDot, secondsPassed]);

  // Style that includes dynamic background color
  const dotStyle = {
    backgroundColor: `rgb(${redValue}, ${greenValue}, 0)`,
    display: index === currentDot ? "block" : "none ",
  };

  return (
    <div className="grid-items">
      <button
        className="dot"
        style={dotStyle}
        onClick={handleClick}
        ref={dotRef}
        key={index}
      >
        {secondsPassed}
      </button>
    </div>
  );
};

export default Dot;
