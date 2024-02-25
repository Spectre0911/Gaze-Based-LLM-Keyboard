import React, { useEffect, useState } from "react";

import App from "./App";
import CenterCursor from "./CenterCursor";
import _ from "lodash";

const trialMode = true;
const trialSentences = [
  "The quick brown fox jumps over the lazy dog",
  "Sphinx of black quartz judge my vow",
  "The five boxing wizards jump quickly",
  "How vexingly quick daft zebras jump",
];

const EyeTracker = () => {
  const webgazer = window.webgazer;
  const GazeCloudAPI = window.GazeCloudAPI;
  // const webgazer = require("webgazer");
  const [prediction, setPrediction] = useState({ x: 0, y: 0 });
  const [calibrationComplete, setCalibrationComplete] = useState(false);
  const [trialOrder, setTrialOrder] = useState([0, 1, 2, 3]);
  const [trialIndex, setTrialIndex] = useState(0);
  const mode = 0;

  useEffect(() => {
    GazeCloudAPI.ApiKey = "AppKeyTrial";
  }, []);

  useEffect(() => {
    setTrialOrder(_.shuffle(trialOrder));
  }, []);

  GazeCloudAPI.OnCalibrationComplete = function () {
    console.log("gaze Calibration Complete");
    setCalibrationComplete(true);
  };

  GazeCloudAPI.OnResult = function (GazeData) {
    setPrediction({ x: GazeData.docX, y: GazeData.docY });
  };

  const loadWebGazer = async () => {
    if (window.webgazer) {
      await webgazer.showVideo(false);
      await webgazer.applyKalmanFilter(true);
      await webgazer
        .setGazeListener(function (data, elapsedTime) {
          if (data == null) {
            return;
          }
          var xprediction = data.x; //these x coordinates are relative to the viewport
          var yprediction = data.y; //these y coordinates are relative to the viewport
          setPrediction({ x: xprediction, y: yprediction, ts: elapsedTime });
        })
        .begin();
      await webgazer.showPredictionPoints(true);
      await webgazer.saveDataAcrossSessions(false);
    }
  };

  useEffect(() => {
    if (mode == 0) {
      loadWebGazer();
    } else if (mode == 1) {
      GazeCloudAPI.StartEyeTracking();
    } else {
      setCalibrationComplete(true);
    }
  }, []);

  if (calibrationComplete) {
    return (
      <App
        pred={prediction}
        trialSentence={trialMode ? trialSentences[trialOrder[trialIndex]] : " "}
      />
    );
  } else {
    return (
      <CenterCursor
        prediction={prediction}
        setCalibrationComplete={setCalibrationComplete}
      />
    );
  }
};

export default EyeTracker;
