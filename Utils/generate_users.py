from typing import List
import Data.constants as c
from UserProfileSystem.UserProfile import UserProfile
from Data.Song import Song
from Data.SongStore import SongStore
import random
import csv

def generate_users(num_users: int, songs: List[Song], num_songs=10): 
    new_users = []
    for user_id in range(num_users): 
        new_user = UserProfile(user_id=user_id)
        #def __init__(self: "UserProfile",user_id: str,danceability=0.0, energy=0.0, valence=0.0, acousticness=0.0, tempo=0.0, loudness=0.0, song_count=0) -> None:
        # danceability = random_generate(c.DANCEABILITY_MIN, c.DANCEABILITY_MAX)
        # energy = random_generate(c.ENERGY_MIN, c.ENERGY_MAX)
        # valence = random_generate(c.VALENCE_MIN, c.VALENCE_MAX)
        # acousticness = random_generate(c.ACOUSTICNESS_MIN, c.ACOUSTICNESS_MAX)
        # tempo = random_generate(c.TEMPO_MIN_USEFUL, c.TEMPO_MAX_USEFUL)
        # loudness = random_generate(c.LOUDNESS_MIN_USEFUL, c.LOUDNESS_MAX)
        # song_count = 0
        # new_user = UserProfile(user_id=user_id, danceability=danceability, energy=energy, valence=valence, acousticness=acousticness, tempo=tempo, loudness=loudness, song_count=song_count)
        for _ in range(num_songs): 
            song_id = random.randint(0, len(songs))
            new_user.update_profile_with_song(songs[song_id])
        new_users.append(new_user.write_to_csv_dict())

    with open('mock_users.csv', 'w', newline='') as csvfile:
        fieldnames = ['user_id','danceability','energy','valence','acousticness','tempo','loudness','genres','artists','popular_tracks','song_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_users)
        


def random_generate(start:float, end:float) -> float: 
    return random.uniform(start, end)

def execute(): 
    DEFAULT_DATA_FILENAME = 'tracks_features.csv'
    print("Loading songs")
    song_store: SongStore = SongStore(file_name=DEFAULT_DATA_FILENAME)
    print("Getting songs to a list")
    songs = song_store.get_all_songs()
    print("Writing to CSV")
    generate_users(100, songs, num_songs=50)
    print("End of program")

execute()

