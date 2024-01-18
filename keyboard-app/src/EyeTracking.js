import React, {
  useEffect,
  useRef,
  useState,
  componentDidMount,
  componentWillUnmount,
} from "react";
import App from "./App";

const EyeBlinkTracker = () => {
  const videoRef = useRef(null);
  const webgazer = window.webgazer;
  const [prediction, setPrediction] = useState({ x: 0, y: 0 });

  const loadWebGazer = async () => {
    if (window.webgazer) {
      webgazer.showVideo(true);
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
    loadWebGazer();
  }, []);

  return <App pred={prediction}></App>;
};

export default EyeBlinkTracker;
