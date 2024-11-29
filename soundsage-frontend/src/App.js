import React, { useState, useEffect } from "react";
import axios from "axios";
import SongList from "./components/SongList";

// "proxy": "http://127.0.0.1:8080",
function App() {
  const [songs, setSongs] = useState([]);
    
  useEffect(() => {
    async function fetchData() {
      // Fetch from flask
    try {
      const response = await fetch("/recommendations");
      const data = await response.json();
      console.log("Printing out data")
      console.log(data);
      console.log("Printing out data recommendations")
      console.log(data.recommendations);
      setSongs(data.recommendations)
    } catch (error) {
      console.log(error);
    }
    }
    fetchData();
  }, []);

  // useEffect(() => {
  //   // Fetch from flask
  //   fetch("/recommendations")
  //     .then((response) => {
  //       console.log("This is the response")
  //       data = response.json()
  //       console.log(data)
  //       setSongs(data.recommendations)
  //     })
  //     // .then((data) => {
  //     //   console.log("This is the data being presented")
  //     //   console.log(recommendations)
  //     //   setSongs(recommendations)
  //     // })
  //     .catch((error) => console.error("Error loading songs:", error));
  // }, []);

  // Use Flask server to fetch data
  // useEffect(() => {
  //   axios.post("/recommendations").then((response) => {
  //     console.log("This is the response")
  //     console.log(response)
  //     console.log(response.data.recommendations)
  //       setSongs(response.data.recommendations);
  //     }
  //     ).
  //     catch((error) => {
  //           console.error("Error fetching songs:", error);
  //         });
  //     }, []);

  // Use FastAPI to fetch data
  // useEffect(() => {
  //   // Fetch song data from your FastAPI backend
  //   axios.post("http://127.0.0.1:8080/recommendations", { user_id: "1" })
  //     .then((response) => {
  //       setSongs(response.data.recommendations);
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching songs:", error);
  //     });
  // }, []);

  // Use static JSON file
  // useEffect(() => {
  //   // Fetch static JSON file
  //   fetch("/songs.json")
  //     .then((response) => {
  //       console.log(response)
  //       response.json()
  //     })
  //     .then((data) => setSongs(data))
  //     .catch((error) => console.error("Error loading songs:", error));
  // }, []);

  return (
    <div className="container mt-5">
      <h1 className="text-center">Recommended Songs</h1>
      <SongList songs={songs} />
    </div>
  );
}

export default App;
