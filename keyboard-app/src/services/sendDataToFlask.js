export const sendDataToFlask = async (data) => {
  try {
    const response = await fetch("http://127.0.0.1:5000/onSpace", {
      mode: "no-cors",
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    return await response.json();
  } catch (error) {
    console.error("Error sending data to Flask:", error);
  }
};
