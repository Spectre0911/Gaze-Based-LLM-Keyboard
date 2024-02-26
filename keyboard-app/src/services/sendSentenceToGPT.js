export const sendSentenceToGPT = async (data) => {
  const processingStartTime = Date.now(); // Capture start time
  try {
    const response = await fetch("http://127.0.0.1:5000/api/onPeriod", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const processingEndTime = Date.now(); // Capture end time
    const processingDuration = processingEndTime - processingStartTime; // Calculate duration
    console.log(`Response received in ${processingDuration} ms`); // Log duration
    return await response.json();
  } catch (error) {
    console.log(data);
    console.error("Error sending data to Flask:", error);
  }
};
