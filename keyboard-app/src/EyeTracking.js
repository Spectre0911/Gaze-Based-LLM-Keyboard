import React, {
  useEffect,
  useRef,
  useState,
  componentDidMount,
  componentWillUnmount,
} from "react";

import App from "./App";
import Calibration from "./Calibration";

const EyeBlinkTracker = () => {
  const videoRef = useRef(null);
  const webgazer = window.webgazer;
  // const webgazer = require("webgazer");
  const [prediction, setPrediction] = useState({ x: 0, y: 0 });
  const [videoCanvas, setVideoCanvas] = useState(null);
  const [stream, setStream] = useState(null);
  const videoElement = document.querySelector("video");
  const loadWebGazer = async () => {
    if (window.webgazer) {
      webgazer.showVideo(false);
      webgazer.util.bound(prediction);
      webgazer.applyKalmanFilter(true);
      webgazer
        .setGazeListener(function (data, elapsedTime) {
          if (data == null) {
            return;
          }
          var xprediction = data.x; //these x coordinates are relative to the viewport
          var yprediction = data.y; //these y coordinates are relative to the viewport
          setPrediction({ x: xprediction, y: yprediction });
        })
        .begin();
      webgazer.showPredictionPoints(true);
      webgazer.saveDataAcrossSessions(false);
    }
  };

  useEffect(() => {
    console.log("loading webgazer");
    loadWebGazer();
  }, []);

  return <Calibration prediction={prediction}></Calibration>;
};

export default EyeBlinkTracker;
