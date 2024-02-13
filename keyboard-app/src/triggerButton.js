import React, { useRef, useEffect } from "react";
import "./App.css";
import ReactCardFlip from "react-card-flip";
import LoadingIcons from "react-loading-icons";

function TriggerButton({
  className,
  onClick,
  frontLabel,
  backLabel,
  sendCoords,
  flipCard,
  selected,
  flipped,
  buffering = false,
  fl2 = "NA",
}) {
  const frontButtonRef = useRef(null);
  const backButtonRef = useRef(null);

  var className = selected ? `${className} selected` : className;

  let fa = <i className="fa-solid fa-arrow-right"></i>;
  let ba = <i className="fa-solid fa-arrow-left"></i>;

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
        if (flipped && flipCard) {
          sendCoords(backLabel, coords);
        } else {
          sendCoords(frontLabel, coords);
        }
      }
    };

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, [flipped, frontLabel]);

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
  } else if (buffering) {
    return (
      <div className={className}>
        <LoadingIcons.ThreeDots stroke="white" strokeOpacity={0.1} />
      </div>
    );
  } else {
    return (
      <button
        ref={frontButtonRef}
        onClick={onClick}
        key={frontLabel}
        className={className}
      >
        {frontLabel === "->" ? fa : frontLabel == "<-" ? ba : frontLabel}
      </button>
    );
  }
}

export default TriggerButton;
