import React, { useRef, useEffect } from "react";
import "./App.css";

const prechosen = new Set(["R", "E", "L", "A", "T", "I", "O", "N", "S"]);

function TriggerButton({
  className,
  onClick,
  frontLabel,
  sendCoords,
  selected,
  currentWord,
  trialWord,
  verticalAlign = "center",
  horizontalAlign = "center",
}) {
  const frontButtonRef = useRef(null);

  className = selected ? `${className} selected` : className;

  let fa = <i className="fa-solid fa-arrow-right"></i>;
  let ba = <i className="fa-solid fa-arrow-left"></i>;

  function colourWord(mode) {
    let lengthDifference;
    currentWord = currentWord.toUpperCase();
    trialWord = trialWord.toUpperCase();

    if (trialWord.length > currentWord.length) {
      lengthDifference = trialWord.length - currentWord.length;
      currentWord += " ".repeat(lengthDifference);
    }

    let zippedLetters = currentWord.split("").map((letter, index) => {
      return [letter, trialWord[index]];
    });

    let colouredWord = zippedLetters.map((pair, _) => {
      if (pair[0] === pair[1] || (pair[0] === "%" && !prechosen.has(pair[1]))) {
        return <span style={{ color: "white" }}>{pair[mode]}</span>;
      } else {
        return <span style={{ color: "#ff9496" }}>{pair[mode]}</span>;
      }
    });

    return colouredWord;
  }

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

  if (frontLabel === "%") {
    return (
      <button
        ref={frontButtonRef}
        onClick={onClick}
        key={frontLabel}
        className={className}
        style={{ justifyContent: horizontalAlign, alignItems: verticalAlign }}
      >
        <div className="wildcard-grid">
          <div style={{ fontSize: "3rem", color: "white" }}>
            {trialWord ? colourWord(0) : currentWord}
          </div>
          <div></div>
          <div>%</div>
          <div></div>
          <div style={{ fontSize: "3rem", color: "white" }}>
            {trialWord ? colourWord(1) : ""}
          </div>
        </div>
      </button>
    );
  }

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
