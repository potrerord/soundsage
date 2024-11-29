import React, { useState, useEffect } from "react";
import axios from "axios";
import SongList from "./components/SongList";

function App() {
  const [songs, setSongs] = useState([]);

  // useEffect(() => {
  //   // Fetch song data from your FastAPI backend
  //   axios.post("http://127.0.0.1:8000/recommendations", { user_id: "1" })
  //     .then((response) => {
  //       setSongs(response.data.recommendations);
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching songs:", error);
  //     });
  // }, []);

  useEffect(() => {
    // Fetch static JSON file
    fetch("/songs.json")
      .then((response) => response.json())
      .then((data) => setSongs(data))
      .catch((error) => console.error("Error loading songs:", error));
  }, []);

  return (
    <div className="container mt-5">
      <h1 className="text-center">Recommended Songs</h1>
      <SongList songs={songs} />
    </div>
  );
}

export default App;
