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

// "{'i', 's', 't', 'o', 'a', 'l', 'e', 'n', 'r'}

const lightBlueStates = [
  ["A", "T", "R", "L", "E", "%", "S", "O", "N", "I", "DEL", "DEL"],
  ["A", "T", "R", "L", "E", "%", "S", "O", "N", "I", "DEL", "->"],
  ["A", "T", "R", "L", "E", "%", "S", "O", "N", "I", "<-", "->"],
];

const darkBlueStates = [
  ["X", "X", "X", "X", "X", "%", "N", "X", "X", "X", "DEL", "DEL"],
  ["X", "X", "X", "X", "X", "%", "N", "X", "X", "->", "DEL", "DEL"],
  ["X", "X", "X", "X", "X", "%", "N", "<-", "X", "->", "DEL", "DEL"],
  ["X", "X", "X", "X", "X", "%", "N", "X", "X", "X", "DEL", "DEL"],
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

  const getButtonConfig = (label, i) => {
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
    if (i < 4) {
      className += " first-row-button";
    }

    return { className, onClick, flip };
  };

  useEffect(() => {
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
    var nextState = 1;
    // Send currentWord to the backend
    if (currentState === 0) {
      try {
        let payload = {
          currentWord: currentWord,
          currentSentence: currentSentence,
        };
        const response = await sendDataToFlask(payload);
        setCurrentWordChoices([currentWord]);
        if (response) {
          console.log("Response from backend:", response);
          setCurrentWordChoices([...currentWordChoices, ...response[1]]);
          if (response[1].length === 1) {
            setCurrentWord(response[1][0].toUpperCase());
            setRightArrowCount(1);
            nextState = 2;
          }
        }
      } catch (error) {
        console.error("Error sending word to backend:", error);
      }
      // Append space to current sentence
      setCurrentState(nextState);
    } else if (currentState === 1 || currentState === 2) {
      setCurrentState(3);
    } else {
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

      if (currentState === 1) {
        setCurrentState(2);
      }
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

  const onDepress = (label) => {
    // Prevent any key from being depressed when information is being collected from GPT
    if (buffering) {
      return;
    }

    let shouldResetState = true; // A flag to determine if state should be reset at the end

    // If a key is depressed after the sentence is returned from GPT, reset the sentence
    if (currentState == 3) {
      setCurrentSentence("");
      setCurrentState(0); // This state reset is specific to this condition
      shouldResetState = false; // Prevent further resetting
    }

    // Logic for handling arrows keys
    if (label == "->") {
      onRightArrow();
    } else if (label == "<-") {
      onLeftArrow();
    } else {
      // Depressing any key when the arrows are present, should take the user back to the main screen
      setRightArrowCount(0);
    }

    if (label === "DEL") {
      if (currentWord.length > 0) {
        setCurrentWord(currentWord.slice(0, -1));
      } else {
        // If no word exists, get the last word (if one exists)
        if (allWords.length > 0) {
          var lastWord = allWords.pop(); // Directly modify allWords and use the popped word
          setAllWords(allWords); // Update allWords state after modification
          setCurrentWord(lastWord);
        }
      }
    } else if (label === "+") {
      onSwitch();
    } else if (label === "SPACE" || label === ".") {
      shouldResetState = false;
      onSpace();
    } else if (label == "AUTO") {
      // AUTO does not imply specific handling besides state reset, which is managed by the flag
    } else {
      if (currentState != 0) {
        // Write the current word to the list of words
        setAllWords([...allWords, currentWord]);
        setCurrentWord(label); // Overwrite the current word with the new letter
      } else {
        setCurrentWord(currentWord + label); // Add the new letter to the current word
      }
    }

    // Reset currentState to 0 if applicable
    if (shouldResetState) {
      setCurrentState(0);
    }
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

      const { className, onClick, flip } = getButtonConfig(strokeLabel, i);

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
    <div style={{ position: "relative" }}>
      <div>
        <Cursor
          cursorPosition={cursorPosition}
          setCursorPosition={setCursorPosition}
          screenSize={screenSize}
          setScreenSize={setScreenSize}
          pred={pred}
        />
        <div className="first-row">{buttons.slice(0, 4)}</div>

        <div className="grid-container">
          {buttons.slice(4, buttons.length - 2)}
        </div>

        <div className="space-row">
          {buttons[buttons.length - 2]}
          <TriggerButton
            className={spaceClassName}
            frontLabel={spaceStates[currentState]}
            onClick={onSpace}
            sendCoords={updateCoords}
            flipCard={false}
            flipped={switchFace === 0 ? true : false}
            selected={selected[9]}
            buffering={buffering}
          />
          {buttons[buttons.length - 1]}
        </div>
      </div>
    </div>
  );
}

export default App;
