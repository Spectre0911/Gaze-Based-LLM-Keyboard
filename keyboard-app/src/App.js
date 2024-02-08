import React, { useEffect, useState } from "react";
import { sendDataToFlask } from "./services/sendDataToFlask";
import { sentSentenceToGPT } from "./services/sendSentenceToGPT";
import Switch from "./Switch";
import "./App.css";
import TriggerButton from "./triggerButton";
import Cursor from "./Cursor";

function getOppositeColor(currentColor) {
  return currentColor === "light-blue-button"
    ? "dark-blue-button"
    : "light-blue-button";
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
  ["I", "T", "A", "N", "+", "E", "DEL", "%", "AUTO"],
];

const darkBlueStates = [
  ["D", "O", "S", "L", "+", "R", "DEL", "%", "AUTO"],
  ["D", "O", "S", "L", "+", "R", "DEL", "%", "->"],
  ["D", "O", "S", "L", "+", "R", "<-", "%", "->"],
  ["D", "O", "S", "L", "+", "R", "DEL", "%", "AUTO"],
];

const createHashMap = (arrays) => {
  let hashMap = {};
  hashMap["SPACE"] = 9;
  hashMap["."] = 9;
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
  const [screenSize, setScreenSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });
  const [cursorPosition, setCursorPosition] = useState({
    x: screenSize.width / 2,
    y: screenSize.height / 2,
  });
  const [buffering, setBuffering] = useState(false);
  const allStates = [lightBlueStates, darkBlueStates];
  const zippedStates = twoDimZip(lightBlueStates, darkBlueStates);
  const spaceStates = ["SPACE", ".", ".", currentSentence];
  var buttonLabels = zippedStates[currentState];
  var spaceClassName =
    currentState === 0
      ? "flex-center-button space-button"
      : currentState === 3
      ? "flex-center-button green-space-button"
      : "flex-center-button red-space-button";

  function findLetterForPoint(point, map) {
    let validKeys = [
      ...allStates[switchFace][currentState],
      spaceStates[currentState],
    ];
    let validKeysSet = new Set(validKeys);

    for (const [letter, coords] of Object.entries(map)) {
      if (!validKeysSet.has(letter)) {
        continue;
      }
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
    console.log(`You are in state ${currentState}`);

    const handleSpaceBar = () => {
      onDepress(selectedLetter);

      setCursorPosition({
        x: screenSize.width / 2,
        y: screenSize.height / 2,
      });
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
  }, [selectedLetter, currentState]);

  useEffect(() => {
    const letter = findLetterForPoint(cursorPosition, coordinateMap);
    setLookingAt(letter);

    // Highlight the letter on the keyboard
    if (letter) {
      setSelectedLetter(letter);
      setSelected(() =>
        Array(10)
          .fill(false)
          .map((_, index) => letterIndexMap[letter] === index)
      );
    }
  }, [cursorPosition, coordinateMap]);

  useEffect(() => {
    if (currentState !== 3) {
      return;
    }
    // Set buffering true at the start of the effect
    setBuffering(true);

    // Combine words to form the sentence for GPT
    const sentence = [...allWords, currentWord].join(" ");

    // Define the asynchronous function inside the useEffect
    const sendSentence = async () => {
      try {
        const response = await sentSentenceToGPT({ sentence });
        // After the async operation, update the state based on the response
        setCurrentSentence(response);
        setAllWords([]);
        setCurrentWord("");
      } catch (error) {
        console.error("Error sending sentence to GPT:", error);
        // Handle any errors appropriately
      } finally {
        // Ensure buffering is turned off after the operation completes or fails
        setBuffering(false);
      }
    };

    // Call the async function
    sendSentence();
  }, [currentState]); // Depen

  const updateCoords = (label, data) => {
    setCoordinateMap((prevMap) => ({
      ...prevMap,
      [label]: data,
    }));
  };

  // WHEN SPACE BUTTON IS DEPRESSED
  const onSpace = async () => {
    console.log("Before SPACE: " + currentState);

    var nextState = 1;
    // Send currentWord to the backend
    if (currentState === 0) {
      try {
        const response = await sendDataToFlask({
          currentWord: currentWord,
          currentSentence: currentSentence,
        });
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
      setCurrentState(3);
    } else {
      console.log("RETURNING TO HOME STATE");
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
      console.log("FORCE TRANSITION");
      setCurrentState(0);
    }
  };

  // WHEN ANY TRIGGER IS DEPRESSED
  const onDepress = (label) => {
    // Prevent any key from being depressed when information is being collected from GPT
    if (buffering) {
      return;
    }
    // If a key is depressed after the sentence is returned from GPT, reset the sentence
    if (currentState == 3) {
      setCurrentSentence("");
      setCurrentState(0);
    }

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
    } else if (label === "SPACE" || label === ".") {
      onSpace();
    } else if (label == "AUTO") {
    } else if (label == "->") {
      onRightArrow();
    } else if (label == "<-") {
      onLeftArrow();
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

  // Create the buttons / Rerender when state change
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
      <Cursor
        cursorPosition={cursorPosition}
        setCursorPosition={setCursorPosition}
        screenSize={screenSize}
        setScreenSize={setScreenSize}
        pred={pred}
      />

      <div className="grid-container">{buttons}</div>
      <TriggerButton
        className={spaceClassName}
        frontLabel={spaceStates[currentState]}
        onClick={onSpace}
        sendCoords={updateCoords}
        flipCard={false}
        flipped={false}
        selected={selected[9]}
        buffering={buffering}
      />
    </div>
  );
}

export default App;
