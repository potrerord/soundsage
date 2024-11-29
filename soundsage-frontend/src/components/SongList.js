import React from "react";
import SongCard from "./SongCard.js";

function SongList({ songs }) {
  return (
    <div className="row">
      {songs.map((song, index) => (
        <div className="col-md-6 mb-4" key={index}>
          <SongCard song={song} />
        </div>
      ))}
    </div>
  );
}

export default SongList;
