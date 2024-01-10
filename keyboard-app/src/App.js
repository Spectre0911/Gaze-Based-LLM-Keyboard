import React, { useState } from "react";
import "./App.css";
import Switch from "./Switch";

function getOppositeColor(currentColor) {
  return currentColor === "light-blue-button"
    ? "dark-blue-button"
    : "light-blue-button";
}

function App() {
  // State to track the button class

  const lightBlueStates = [
    ["I", "T", "A", "N", "~", "E", "DEL", "+", "."],
    ["I", "T", "A", "N", "~", "E", "DEL", "+", "->"],
    ["I", "T", "A", "N", "~", "E", "<-", "+", "->"],
  ];

  const darkBlueStates = [
    ["D", "O", "S", "L", "~", "R", "DEL", "+", "."],
    ["D", "O", "S", "L", "~", "R", "DEL", "+", "->"],
    ["D", "O", "S", "L", "~", "R", "<-", "+", "->"],
  ];

  const allStates = [lightBlueStates, darkBlueStates];
  const [switchFace, setSwitchFace] = useState(0);
  const [currentState, setCurrentState] = useState(0);
  const [buttonClass, setButtonClass] = useState("light-blue-button");
  const [rightArrowCount, setRightArrowCount] = useState(0);
  const [currentWord, setCurrentWord] = useState("");
  const [currentSentence, setCurrentSentence] = useState("");
  const [allWords, setAllWords] = useState([]);

  var buttonLabels = allStates[switchFace][currentState];
  var spaceClassName =
    currentState === 0
      ? "flex-center-button space-button"
      : "flex-center-button red-space-button";

  const onSwitch = () => {
    if (currentState !== 0) {
      setAllWords([...allWords, currentWord]);
      setCurrentWord("");
    }

    setSwitchFace((prevSwitchFace) => (prevSwitchFace === 1 ? 0 : 1));
    setButtonClass((prevClass) =>
      prevClass === "light-blue-button"
        ? "dark-blue-button"
        : "light-blue-button"
    );
    if (currentState !== 0) {
      setCurrentState(0);
    }
  };

  const onSpace = () => {
    // WORD SHOULD BE SENT TO BACKEND TO BE SEARCHED FOR
    console.log("Searching for: " + currentWord);
    console.log("Current sentence: " + currentSentence);
    console.log("All words: " + allWords);

    setCurrentSentence(currentSentence + " ");
    if (currentState === 0) {
      setCurrentState(1);
    }
    // IF PERIOD BUTTON IS DEPRESSED
    else {
      console.log("RESETTING ALL STATES");
      setAllWords();
      setCurrentWord("");
      setCurrentState(0);
    }
  };

  const onRightArrow = () => {
    // LA to LARA + SELF LOOP | RAK
    setRightArrowCount(rightArrowCount + 1);

    if (currentState === 1) {
      setCurrentState(2);
    }
  };

  const onLeftArrow = () => {
    // LARA to LA | LAK
    if (rightArrowCount === 1) {
      setCurrentState(0);
    }
    setRightArrowCount(rightArrowCount - 1);
  };

  const onDepress = (label) => {
    console.log("Depressed: " + label);
    // IF DEPRESS FOLLOWS WORD SEARCH UPDATE STATES
    if (currentState !== 0) {
      let updatedWords = [...allWords, currentWord];
      console.log("Updated words: " + updatedWords);
      setAllWords(updatedWords);
      setCurrentWord("");
    }

    // WHEN BACKSPACE IS PRESSED
    if (label === "DEL") {
      // REMOVE LAST CHARACTER FROM RELEVANT STATES
      if (currentSentence.length > 0) {
        setCurrentSentence(currentSentence.slice(0, -1));
      }
      if (currentWord.length > 0) {
        setCurrentSentence(currentWord.slice(0, -1));
      }
      // IF CURRENT WORD IS EMPTY, REMOVE LAST WORD FROM ALL WORDS AND UPDATE CURRENT WORD
      else {
        if (allWords.length > 0) {
          var lastWord = allWords.pop();
          setCurrentWord(lastWord);
        }
      }
    }
    // WHEN SENTENCE IS COMPLETED
    else if (label === ".") {
      // SHOULD SEND TO BACKEND FOR GPT PROCESSING

      // RESET STATES
      setCurrentSentence("");
      setCurrentWord("");
      setAllWords([]);
    }
    // WHEN A CHARACTER IS TYPED
    else {
      // APPEND TO RELEVANT STATES
      setCurrentSentence(currentSentence + label);
      setCurrentWord(currentWord + label);
    }

    // ENSURE THAT WE ARE IN BASE STATE AFTER TYPING ANY CHARACTER
    setCurrentState(0);
  };

  const buttons = buttonLabels.map((label) => {
    let className;
    let onClick = onDepress.bind(this, label);
    switch (label) {
      case "DEL":
        className = "flex-center-button red-button";
        break;
      case ".":
        className = "flex-center-button red-button";
        break;
      case "~":
        className = "flex-center-button wildcard-button";
        break;
      case "<-":
        className = "flex-center-button purple-button";
        onClick = onLeftArrow;
        break;
      case "->":
        className = "flex-center-button purple-button";
        onClick = onRightArrow;
        break;
      case "+":
        return (
          <Switch
            key="Switch"
            buttonClass={getOppositeColor(buttonClass)}
            buttonLabels={allStates[switchFace === 0 ? 1 : 0][0]}
            onSwitchClick={onSwitch}
          />
        );
      default:
        className = `flex-center-button ${buttonClass}`; // Use state for class
        break;
    }

    return (
      <button className={className} key={label} onClick={onClick}>
        {label}
      </button>
    );
  });

  return (
    <div>
      <div className="grid-container">{buttons}</div>
      <button className={spaceClassName} onClick={onSpace}>
        {currentState === 0 ? "Space" : "."}
      </button>
    </div>
  );
}

export default App;
