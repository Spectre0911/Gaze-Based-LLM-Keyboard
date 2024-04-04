import React, { useEffect, useState } from "react";
import App from "./App";
import CenterCursor from "./CenterCursor";
import _ from "lodash";
import TrialComplete from "./trialComplete";

const trialMode = true;
/*
8.8
7.2
7.4
7.2
8.8
*/
const trialSentences = [
  "The quick brown fox jumps over the lazy dog",
  "Sphinx of black quartz judge my vow",
  "The five boxing wizards jump quickly",
  "How vexingly quick daft zebras jump",
];

const EyeTracker = () => {
  const webgazer = window.webgazer;
  const GazeCloudAPI = window.GazeCloudAPI;
  const [prediction, setPrediction] = useState({ x: 0, y: 0 });
  const [calibrationComplete, setCalibrationComplete] = useState(false);
  const [recalibrate, setRecalibrate] = useState(false);
  const [trialOrder, setTrialOrder] = useState([0, 1, 2, 3, 0]);
  const [trialIndex, setTrialIndex] = useState(-2);
  const mode = 0;

  useEffect(() => {
    setRecalibrate(false);
    if (!calibrationComplete && trialIndex < trialOrder.length) {
      setTrialIndex((prev) => {
        console.log(prev);
        return prev + 1;
      });
    }
  }, [calibrationComplete]);

  useEffect(() => {
    // setTrialOrder(_.shuffle(trialOrder));
    setTrialOrder([0, 1, 2, 3, 0]);
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

  const stopWebGazer = async () => {
    await webgazer.clearData();
  };

  useEffect(() => {
    console.log("in here");
    if (mode == 0) {
      stopWebGazer();
      loadWebGazer();
    } else if (mode == 1) {
      GazeCloudAPI.StartEyeTracking();
    } else {
      setCalibrationComplete(true);
    }
  }, [trialIndex, recalibrate]);

  if (trialIndex >= trialOrder.length) {
    return <TrialComplete />;
  }

  if (calibrationComplete && !recalibrate) {
    let trialSentence = trialMode
      ? trialSentences[trialOrder[trialIndex]]
      : null;
    return (
      <App
        pred={prediction}
        trialMode={trialMode}
        trialSentence={trialSentence}
        setCalibrationComplete={setCalibrationComplete}
        setRecalibrate={setRecalibrate}
      />
    );
  } else {
    if (recalibrate) {
      setTrialIndex(trialIndex - 1);
    }
    return (
      <CenterCursor
        prediction={prediction}
        setCalibrationComplete={setCalibrationComplete}
        order={trialOrder}
        setRecalibrate={setRecalibrate}
      />
    );
  }
};

export default EyeTracker;
