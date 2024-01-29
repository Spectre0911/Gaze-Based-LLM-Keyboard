import React, { useEffect, useState } from "react";
import { sendDataToFlask } from "./services/sendDataToFlask";
import Switch from "./Switch";
import "./App.css";
import TriggerButton from "./triggerButton";
import SpaceTriggerButton from "./SpaceTrigger";

function getOppositeColor(currentColor) {
  return currentColor === "light-blue-button"
    ? "dark-blue-button"
    : "light-blue-button";
}

function findLetterForPoint(point, map) {
  for (const [letter, coords] of Object.entries(map)) {
    if (
      point.x >= coords.topLeft.x &&
      point.x <= coords.topRight.x &&
      point.y >= coords.topLeft.y &&
      point.y <= coords.bottomLeft.y
    ) {
      return letter;
    }
  }
}

function twoDimZip(a, b) {
  return a.map(function (ai, i) {
    return ai.map(function (e, j) {
      return [e, b[i][j]];
    });
  });
}

const lightBlueStates = [
  ["I", "T", "A", "N", "+", "E", "DEL", "%", "AUTO"],
  ["I", "T", "A", "N", "+", "E", "DEL", "%", "->"],
  ["I", "T", "A", "N", "+", "E", "<-", "%", "->"],
  ["I", "T", "A", "N", "+", "E", "<-", "%", "->"],
];

const darkBlueStates = [
  ["D", "O", "S", "L", "+", "R", "DEL", "%", "AUTO"],
  ["D", "O", "S", "L", "+", "R", "DEL", "%", "->"],
  ["D", "O", "S", "L", "+", "R", "<-", "%", "->"],
  ["D", "O", "S", "L", "+", "R", "<-", "%", "->"],
];

const createHashMap = (arrays) => {
  let hashMap = {};

  arrays.forEach((array, arrayIndex) => {
    array.forEach((subArray, subArrayIndex) => {
      subArray.forEach((item, i) => {
        if (!hashMap[item]) {
          hashMap[item] = i;
        }
      });
    });
  });

  return hashMap;
};

const letterIndexMap = createHashMap([lightBlueStates, darkBlueStates]);
console.log(letterIndexMap);

function App({ pred }) {
  const [coordinateMap, setCoordinateMap] = useState({});
  const [switchFace, setSwitchFace] = useState(0);
  const [currentState, setCurrentState] = useState(0);
  const [buttonClass, setButtonClass] = useState("light-blue-button");
  const [rightArrowCount, setRightArrowCount] = useState(0);
  const [currentWord, setCurrentWord] = useState("");
  const [currentWordChoices, setCurrentWordChoices] = useState([]);
  const [currentSentence, setCurrentSentence] = useState("");
  const [allWords, setAllWords] = useState([]);
  const [lookingAt, setLookingAt] = useState("");
  const [buttons, setButtons] = useState([]);
  const [selected, setSelected] = useState(Array(10).fill(false));
  const [selectedLetter, setSelectedLetter] = useState("");

  const allStates = [lightBlueStates, darkBlueStates];
  const zippedStates = twoDimZip(lightBlueStates, darkBlueStates);
  var buttonLabels = zippedStates[currentState];

  var spaceClassName =
    currentState === 0
      ? "flex-center-button space-button"
      : currentState === 3
      ? "flex-center-button green-space-button"
      : "flex-center-button red-space-button";

  const getButtonConfig = (label) => {
    let className = "flex-center-button";
    let onClick;
    let flip = false;

    switch (label) {
      case "DEL":
        className += " red-button";
        onClick = onDepress.bind(this, label);
        break;
      case "AUTO":
        className += " green-auto-button";
        onClick = onDepress.bind(this, label);
        break;
      case "%":
        className += " wildcard-button";
        onClick = onDepress.bind(this, label);
        break;
      case "<-":
        className += " purple-button";
        onClick = onLeftArrow;
        break;
      case "->":
        className += " purple-button";
        onClick = onRightArrow;
        break;
      default:
        className += ` ${buttonClass}`;
        onClick = onDepress.bind(this, label);
        flip = true;
    }

    return { className, onClick, flip };
  };

  useEffect(() => {
    const handleSpaceBar = () => {
      onDepress(selectedLetter);
    };
    const handleKeyDown = (event) => {
      if (event.code === "Space") {
        handleSpaceBar();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [selectedLetter]);

  useEffect(() => {
    const letter = findLetterForPoint(pred, coordinateMap);
    setLookingAt(letter);
    // Highlight the letter on the keyboard
    if (letter) {
      setSelected((_) => {
        const newSelected = Array(10).fill(false);
        const index = letterIndexMap[letter];
        newSelected[index] = true;
        setSelectedLetter(letter);
        return newSelected;
      });
    }
  }, [pred, coordinateMap]);

  const updateCoords = (label, data) => {
    setCoordinateMap((prevMap) => ({
      ...prevMap,
      [label]: data,
    }));
  };

  // WHEN SPACE BUTTON IS DEPRESSED
  const onSpace = async () => {
    console.log("Searching for: " + currentWord);
    console.log("Current sentence: " + currentSentence);
    var nextState = 1;
    // Send currentWord to the backend
    if (currentState === 0) {
      try {
        const response = await sendDataToFlask({
          currentWord: currentWord,
          currentSentence: currentSentence,
        });
        console.log("Response recieved");
        console.log("Response from backend:", response);
        setCurrentWordChoices([currentWord, ...response[1]]);
        if (response[1].length === 1) {
          setCurrentWord(response[1][0].toUpperCase());
          setRightArrowCount(1);
          nextState = 2;
        }
      } catch (error) {
        console.error("Error sending word to backend:", error);
      }
      // Append space to current sentence
      setCurrentState(nextState);
    } else if (currentState === 1 || currentState === 2) {
      setCurrentSentence([...allWords, currentWord].join(" "));
      setCurrentState(3);
      setAllWords([]);
      setCurrentWord("");
    } else if (currentState === 3) {
      setCurrentSentence("");
      setCurrentState(0);
    }
  };

  // WHEN RIGHT ARROW IS CLICKED
  const onRightArrow = () => {
    if (rightArrowCount < currentWordChoices.length - 1) {
      setCurrentWord(currentWordChoices[rightArrowCount + 1].toUpperCase());
      console.log(
        "Current word: " + currentWordChoices[rightArrowCount + 1].toUpperCase()
      );
      setRightArrowCount(rightArrowCount + 1);
    }

    if (currentState === 1) {
      setCurrentState(2);
    }
  };

  // WHEN LEFT ARROW IS CLICKED
  const onLeftArrow = () => {
    if (rightArrowCount === 1) {
      setCurrentState(1);
    } else if (rightArrowCount === 0) {
      setCurrentState(0);
    }
    setCurrentWord(currentWordChoices[rightArrowCount - 1].toUpperCase());
    console.log(
      "Current word: " + currentWordChoices[rightArrowCount - 1].toUpperCase()
    );
    setRightArrowCount(rightArrowCount - 1);
  };

  // WHEN SWITCH IS CLICKED
  const onSwitch = () => {
    setRightArrowCount(0);
    setCoordinateMap({});

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

  // WHEN ANY TRIGGER IS DEPRESSED
  const onDepress = (label) => {
    console.log(label);
    // RESET RIGHT ARROW CLICKS
    setRightArrowCount(0);
    if (label === "DEL") {
      if (currentWord.length > 0) {
        setCurrentWord(currentWord.slice(0, -1));
      } else {
        if (allWords.length > 0) {
          var lastWord = allWords[allWords.length - 1];
          setAllWords(allWords.slice(0, -1));
          setCurrentWord(lastWord);
        }
      }
    } else if (label === "+") {
      onSwitch();
    } else if (label === "SPACE") {
      console.log("SPACE");
      onSpace();
    } else if (label == "AUTO") {
    } else {
      // IF RETURNING FROM A SPACE
      if (currentState != 0) {
        // WRITE THE CURRENT WORD TO THE LIST OF WORDS
        setAllWords([...allWords, currentWord]);
        // OVERWRITE THE CURRENT WORD
        setCurrentWord(label);
      } else {
        setCurrentWord(currentWord + label);
      }
    }

    // ENSURE THAT WE ARE IN BASE STATE AFTER TYPING ANY CHARACTER
    setCurrentState(0);
  };

  // Initially create the buttons
  useEffect(() => {
    var i = -1;
    const buttons = buttonLabels.map((labels) => {
      var [frontLabel, backLabel] = labels;
      i += 1;

      if (frontLabel === "+") {
        return (
          <Switch
            key="Switch"
            buttonClass={getOppositeColor(buttonClass)}
            buttonLabels={allStates[switchFace === 0 ? 1 : 0][0]}
            currentWord={currentWord}
            onSwitch={onSwitch}
            sendCoords={updateCoords}
            selected={selected[i]}
          />
        );
      }

      let strokeLabel = frontLabel;

      if (switchFace === 1) {
        strokeLabel = backLabel;
      }

      const { className, onClick, flip } = getButtonConfig(strokeLabel);

      return (
        <TriggerButton
          className={className}
          frontLabel={backLabel}
          backLabel={frontLabel}
          onClick={onClick}
          sendCoords={updateCoords}
          flipCard={flip}
          flipped={switchFace === 0 ? true : false}
          selected={selected[i]}
        />
      );
    });

    setButtons(buttons);
  }, [switchFace, currentWord, currentState, lookingAt]);

  return (
    <div>
      <div className="grid-container">{buttons}</div>
      <TriggerButton
        className={spaceClassName}
        frontLabel={
          currentState === 0
            ? "SPACE"
            : currentState == 3
            ? currentSentence
            : "."
        }
        onClick={onSpace}
        sendCoords={updateCoords}
        flipCard={false}
        flipped={false}
        selected={selected[9]}
      />{" "}
      ;
    </div>
  );
}

export default App;
