import React, { Component, useEffect, useRef } from "react";
import TriggerButton from "./triggerButton";
import { sendDataToFlask } from "./services/sendDataToFlask";

const SpaceTriggerButton = ({
  className,
  label,
  sendCoords,
  setCurrentWord,
  setAllWords,
  setCurrentSentence,
  setCurrentState,
  setCurrentWordChoices,
  setRightArrowCount,
  currentWord,
  currentSentence,
  currentState,
}) => {
  const buttonRef = useRef(null);

  useEffect(() => {
    for (let i = 0; i < 10000; i++) {
      console.log(label);
    }
  });

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

      setCurrentSentence(currentSentence + " ");
      setCurrentState(nextState);
    } else if (currentState === 1 || currentState === 2) {
      setCurrentSentence(currentSentence + currentWord);
      setCurrentState(3);
      setAllWords([]);
      setCurrentWord("");
    } else if (currentState === 3) {
      setCurrentSentence("");
      setCurrentState(0);
    }
  };

  return (
    <TriggerButton
      ref={buttonRef}
      onClick={onSpace}
      key={label}
      label={label}
      className={className}
      sendCoords={sendCoords}
    />
  );
};

export default SpaceTriggerButton;
