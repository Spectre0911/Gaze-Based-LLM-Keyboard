import React, { useEffect, useState } from "react";
import { sendDataToFlask } from "./services/sendDataToFlask";
import { sendSentenceToGPT } from "./services/sendSentenceToGPT";
import "./App.css";
import TriggerButton from "./triggerButton";
import Cursor from "./Cursor";

const createHashMap = (array) => {
  let hashMap = {};

  array.forEach((subArray, subArrayIndex) => {
    subArray.forEach((item, i) => {
      if (!hashMap[item]) {
        hashMap[item] = i;
      }
    });
  });

  return hashMap;
};

function App({
  pred,
  trialMode,
  trialSentence,
  setCalibrationComplete,
  setRecalibrate,
}) {
  const [coordinateMap, setCoordinateMap] = useState({});
  const [currentState, setCurrentState] = useState(0);
  const [buttonClass, setButtonClass] = useState("dark-blue-button");
  const [rightArrowCount, setRightArrowCount] = useState(0);
  const [currentWord, setCurrentWord] = useState("");
  const [currentWordChoices, setCurrentWordChoices] = useState([]);
  const [currentSentence, setCurrentSentence] = useState("");
  const [allWords, setAllWords] = useState([]);
  const [lookingAt, setLookingAt] = useState("");
  const [buttons, setButtons] = useState([]);
  const [selected, setSelected] = useState(Array(13).fill(false));
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
  const [firstDepress, setFirstDepress] = useState(false);
  const [startTime, setStartTime] = useState(null);

  var spaceClassName =
    currentState === 0
      ? "flex-center-button space-button"
      : currentState === 3
      ? "flex-center-button green-space-button"
      : "flex-center-button red-space-button";
  const spaceStates = ["SPACE", ".", ".", currentSentence];
  const spaceName = spaceStates[currentState];
  const boardStates = [
    [
      "E",
      "R",
      "T",
      "O",
      "A",
      "%",
      "S",
      "L",
      "N",
      "I",
      "DEL ",
      spaceName,
      "DEL",
    ],
    ["E", "R", "T", "O", "A", "%", "S", "L", "N", "I", "DEL ", spaceName, "->"],
    ["E", "R", "T", "O", "A", "%", "S", "L", "N", "I", "<-", spaceName, "->"],
    ["E", "R", "T", "O", "A", "%", "S", "L", "N", "I", spaceName],
  ];

  const letterIndexMap = createHashMap(boardStates);
  const trialSentenceWords = trialSentence.split(" ");
  const [trialIndex, setTrialIndex] = useState(0);
  const [correctionsMade, setCorrectionsMade] = useState(0);
  var buttonLabels = boardStates[currentState];

  function findLetterForPoint(point, map) {
    let validKeys = boardStates[currentState];
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
    let vertAlign;
    let horAlign;

    switch (label) {
      case "DEL":
      case "DEL ":
        className += " red-button";
        onClick = onDepress.bind(this, "DEL");
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
      case "SPACE":
      case ".":
      case currentSentence:
        className = spaceClassName;
        onClick = onSpace;
        break;
      default:
        className += ` ${buttonClass}`;
        onClick = onDepress.bind(this, label);
    }
    if (i === 0 || i === 4 || i === 7 || i === 10) {
      if (currentState !== 3) {
        horAlign = "flex-start";
      }
      vertAlign = "center";
    } else if (i === 6 || i === 9 || i === 12 || i === 3) {
      vertAlign = "center";
      horAlign = "flex-end";
    }
    if (i > 9) {
      vertAlign = "flex-end";
    }

    if (i < 4) {
      className += " first-row-button";
      vertAlign = "flex-start";
    }

    if (i === 4 || i === 6 || i === 7 || i === 9) {
      className += " n-row-edge-button";
    }

    if (i === 5 || i === 8) {
      className += " n-row-button";
    }

    return { className, onClick, vertAlign, horAlign };
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
      if (event.code === "Enter") {
        handleSpaceBar();
      }
      if (event.code === "KeyC") {
        setRecalibrate(true);
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [selectedLetter, currentState, currentWord]);

  useEffect(() => {
    const letter = findLetterForPoint(cursorPosition, coordinateMap);
    setLookingAt(letter);
    // Highlight the letter on the keyboard
    if (letter) {
      setSelectedLetter(letter);
      setSelected(() =>
        Array(13)
          .fill(false)
          .map((_, index) => letterIndexMap[letter] === index)
      );
    }
  }, [cursorPosition, coordinateMap]);

  useEffect(() => {
    if (currentState !== 3) {
      return;
    }
    setFirstDepress(false);
    // Set buffering true at the start of the effect
    setBuffering(true);
    let duration = (Date.now() - startTime) / 1000;
    let wordsPerMinute = (allWords.length + 1) / (duration / 60);
    // Combine words to form the sentence for GPT
    const sentence = [...allWords, currentWord].join(" ");

    // Define the asynchronous function inside the useEffect
    const sendSentence = async () => {
      try {
        const response = await sendSentenceToGPT({
          sentence,
          duration,
          trialMode,
          trialSentence,
          correctionsMade,
        });
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
        setStartTime(null);
        if (trialMode) {
          setCalibrationComplete(false);
        }
      }
    };

    // Call the async function
    sendSentence();
  }, [currentState]);

  const updateCoords = (label, data) => {
    setCoordinateMap((prevMap) => ({
      ...prevMap,
      [label]: data,
    }));
  };

  // WHEN SPACE BUTTON IS DEPRESSED
  const onSpace = async () => {
    var nextState = 1;
    setTrialIndex(trialIndex + 1);
    // Send currentWord to the backend
    if (currentState === 0) {
      try {
        let payload = {
          currentWord: currentWord,
          currentSentence: currentSentence,
        };
        const response = await sendDataToFlask(payload);
        if (response) {
          console.log("Response from backend:", response);
          if (response[1].length === 1) {
            setCurrentWordChoices([currentWord]);
            setCurrentWord(response[1][0].toUpperCase());
            setRightArrowCount(1);
            nextState = 2;
          } else {
            setCurrentWordChoices([...response[1]]);
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
      setCurrentWord("");
      setRightArrowCount(0);
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

  const onDepress = (label) => {
    // Prevent any key from being depressed when information is being collected from GPT
    if (buffering) {
      return;
    }

    if (!firstDepress) {
      setFirstDepress(true);
      setStartTime(Date.now());
    }

    let shouldResetState = true; // A flag to determine if state should be reset at the end

    // If a key is depressed after the sentence is returned from GPT, reset the sentence
    if (currentState === 3) {
      setCurrentSentence("");
      setCurrentState(0); // This state reset is specific to this condition
      shouldResetState = false; // Prevent further resetting
    }

    // Handling arrows keys
    if (label === "->") {
      onRightArrow();
    } else if (label === "<-") {
      onLeftArrow();
    } else {
      // Depressing any key when the arrows are present, should take the user back to the main screen
      setRightArrowCount(0);
    }
    // Handling DEL keys
    if (label === "DEL" || label === "DEL ") {
      setCorrectionsMade(correctionsMade + 1);
      // Deals with edge case when space has been depressed, but user wants to go back to previous word to change spelling
      if (trialMode && trialIndex > 0 && currentState == 1) {
        setTrialIndex(trialIndex - 1);
      } else if (currentWord.length > 0) {
        setCurrentWord(currentWord.slice(0, -1));
      } else {
        // If no word exists, get the last word (if one exists)
        if (allWords.length > 0) {
          var lastWord = allWords.pop(); // Directly modify allWords and use the popped word
          setAllWords(allWords); // Update allWords state after modification
          setCurrentWord(lastWord);
          if (trialIndex > 0) {
            setTrialIndex(trialIndex - 1);
          }
        }
      }
    }
    // Handling SPACE / Period keys
    else if (label === "SPACE" || label === ".") {
      shouldResetState = false;
      onSpace();
    }
    // Handles character depression
    else {
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
    const buttons = buttonLabels.map((label) => {
      i += 1;

      let strokeLabel = label;

      const { className, onClick, vertAlign, horAlign } = getButtonConfig(
        strokeLabel,
        i
      );

      let currentTrialWord;
      if (trialMode) {
        currentTrialWord = trialSentenceWords[trialIndex];
      }

      return (
        <TriggerButton
          className={className}
          frontLabel={label}
          onClick={onClick}
          sendCoords={updateCoords}
          selected={selected[i]}
          verticalAlign={vertAlign}
          horizontalAlign={horAlign}
          currentWord={currentWord}
          trialWord={currentTrialWord}
          currentWordChoices={currentWordChoices}
          rightArrowCount={rightArrowCount}
          buffering={buffering}
        />
      );
    });

    setButtons(buttons);
  }, [currentWord, currentState, lookingAt, buffering]);

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
          {buttons.slice(4, buttons.length - (currentState === 3 ? 1 : 3))}
        </div>

        <div className="space-row">
          {buttons.slice(
            buttons.length - (currentState === 3 ? 1 : 3),
            buttons.length
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
