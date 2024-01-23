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
    }
  };

  useEffect(() => {
    console.log("loading webgazer");
    loadWebGazer();
  }, []);

  // const canvas = webgazer.getVideoElementCanvas();
  // if (canvas) {
  //   console.log("captured");
  //   const capturedStream = canvas.captureStream(30); // 30 FPS
  //   console.log(capturedStream);
  //   setStream(capturedStream);
  //   if (videoRef.current) {
  //     console.log(videoRef);
  //     videoRef.current.srcObject = stream;
  //   }
  // }

  return <Calibration prediction={prediction}></Calibration>;
};

export default EyeBlinkTracker;
