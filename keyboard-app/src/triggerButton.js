import React, { useRef, useEffect } from "react";
import "./App.css";
import ReactCardFlip from "react-card-flip";

function TriggerButton({
  className,
  onClick,
  frontLabel,
  backLabel,
  sendCoords,
  flipCard,
  flipped,
  selected,
}) {
  const frontButtonRef = useRef(null);
  const backButtonRef = useRef(null);
  var className = selected ? `${className} selected` : className;

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
        console.log(coords);
        if (flipped) {
          sendCoords(backLabel, coords);
        } else {
          console.log("in here");
          console.log(frontLabel);
          sendCoords(frontLabel, coords);
        }
      }
    };

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, [flipped]);

  if (flipCard) {
    return (
      <ReactCardFlip isFlipped={flipped} flipDirection="vertical">
        <button
          ref={frontButtonRef}
          onClick={onClick}
          key={frontLabel}
          className={className}
        >
          {frontLabel}
        </button>
        <button
          ref={backButtonRef}
          onClick={onClick}
          key={backLabel}
          className={className}
        >
          {backLabel}
        </button>
      </ReactCardFlip>
    );
  } else {
    return (
      <button
        ref={frontButtonRef}
        onClick={onClick}
        key={frontLabel}
        className={className}
      >
        {frontLabel}
      </button>
    );
  }
}

export default TriggerButton;
