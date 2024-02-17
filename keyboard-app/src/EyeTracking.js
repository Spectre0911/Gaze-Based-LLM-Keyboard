import React, { useEffect, useState } from "react";

import App from "./App";
import Calibration from "./Calibration";
import CenterCursor from "./CenterCursor";

const EyeTracker = () => {
  const webgazer = window.webgazer;
  // const webgazer = require("webgazer");
  const [prediction, setPrediction] = useState({ x: 0, y: 0 });
  const [calibrationComplete, setCalibrationComplete] = useState(false);

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
    loadWebGazer();
  }, []);

  if (calibrationComplete) {
    return <App pred={prediction} />;
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
