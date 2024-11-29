import React, { useState } from "react";

function SongCard({ song }) {
  const [rating, setRating] = useState(0);

  const handleRating = (value) => {
    setRating(value);
    console.log(`Rated "${song.name}" by ${song.artists.join(", ")}: ${value} stars`);
  };

  return (
    <div className="card h-100 shadow-sm">
      <div className="card-body">
        <h5 className="card-title text-primary">{song.name}</h5>
        <h6 className="card-subtitle mb-2 text-muted">By: {song.artists.join(", ")}</h6>
        <ul className="list-group list-group-flush mb-3">
          <li className="list-group-item"><strong>Danceability:</strong> {song.danceability}</li>
          <li className="list-group-item"><strong>Energy:</strong> {song.energy}</li>
          <li className="list-group-item"><strong>Valence:</strong> {song.valence}</li>
        </ul>
        <div>
          <strong>Rate this song:</strong>
          <div>
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                onClick={() => handleRating(star)}
                className={`btn ${star <= rating ? "btn-warning" : "btn-outline-warning"} btn-sm`}
              >
                ★
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default SongCard;
