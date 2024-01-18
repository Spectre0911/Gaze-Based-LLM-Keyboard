import React, { useRef, useEffect } from "react";
import "./App.css";

function TriggerButton({ className, onClick, label, sendCoords }) {
  const buttonRef = useRef(null);

  useEffect(() => {
    const handleResize = () => {
      if (buttonRef.current) {
        console.log("Buttons redrawn");
        const rect = buttonRef.current.getBoundingClientRect();
        const coords = {
          topLeft: { x: rect.left, y: rect.top },
          topRight: { x: rect.right, y: rect.top },
          bottomLeft: { x: rect.left, y: rect.bottom },
          bottomRight: { x: rect.right, y: rect.bottom },
        };
        console.log(coords);
        sendCoords(label, coords);
      }
    };

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <button ref={buttonRef} onClick={onClick} key={label} className={className}>
      {label}
    </button>
  );
}

export default TriggerButton;
