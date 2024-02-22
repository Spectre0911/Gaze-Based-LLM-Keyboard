import React, { useRef, useEffect } from "react";
import "./App.css";

function TriggerButton({
  className,
  onClick,
  frontLabel,
  sendCoords,
  selected,
  verticalAlign = "center",
  horizontalAlign = "center",
}) {
  const frontButtonRef = useRef(null);

  var className = selected ? `${className} selected` : className;

  let fa = <i className="fa-solid fa-arrow-right"></i>;
  let ba = <i className="fa-solid fa-arrow-left"></i>;

  useEffect(() => {
    // Could probably calculate this a bit more intelligently in app.js
    const handleResize = () => {
      if (frontButtonRef.current) {
        const rect = frontButtonRef.current.getBoundingClientRect();
        let topLeft = { x: rect.left, y: rect.top };
        let topRight = { x: rect.right, y: rect.top };
        let bottomLeft = { x: rect.left, y: rect.bottom };
        let bottomRight = { x: rect.right, y: rect.bottom };
        const coords = {
          topLeft: topLeft,
          topRight: topRight,
          bottomLeft: bottomLeft,
          bottomRight: bottomRight,
        };

        sendCoords(frontLabel, coords);
      }
    };

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, [frontLabel]);

  useEffect(() => {
    console.log("SPACE");
  }, [selected]);

  return (
    <button
      ref={frontButtonRef}
      onClick={onClick}
      key={frontLabel}
      className={className}
      style={{ justifyContent: horizontalAlign, alignItems: verticalAlign }}
    >
      {frontLabel === "->" ? fa : frontLabel == "<-" ? ba : frontLabel}
    </button>
  );
}

export default TriggerButton;
