import React, { useState } from "react";

function App() {
  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const [isListening, setIsListening] = useState(false);

  const handleStart = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    setIsListening(true);
    recognition.start();

    recognition.onresult = async (event) => {
      const speechToText = event.results[0][0].transcript;
      setTranscript(speechToText);
      const res = await fetch("https://conci-api.onrender.com/process_intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: speechToText }),
      });
      const data = await res.json();
      setResponse(data.reply);
      const utterance = new SpeechSynthesisUtterance(data.reply);
      speechSynthesis.speak(utterance);
    };

    recognition.onend = () => setIsListening(false);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Hey Conci 👋</h1>
      <p>{transcript || "Click below and speak a request..."}</p>
      <p><strong>{response}</strong></p>
      <button onClick={handleStart} disabled={isListening}>
        {isListening ? "Listening..." : "Activate Conci"}
      </button>
    </div>
  );
}

export default App;
