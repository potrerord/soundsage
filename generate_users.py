from typing import List
import Data.constants as c
from UserProfileSystem.UserProfile import UserProfile
from Data.Song import Song
from Data.SongStore import SongStore
import random
import csv

def generate_random_users(num_users: int, songs: List[Song], num_songs=10): 
    '''
    Generates random users based on specified number of users and number of songs
    '''
    # Store new users to an array
    new_users = []
    # Generate user id using real number
    for user_id in range(num_users): 
        new_user = UserProfile(user_id=user_id)
        # Generate num_songs
        for _ in range(num_songs): 
            # Randomly select from the runtime songstore
            song_id = random.randint(0, len(songs))
            # Update profile 
            new_user.update_profile_with_song(songs[song_id])
        # Transform user data into csv friendly dictionary. 
        new_users.append(new_user.write_to_csv_dict())

    # Write to mock user file Currently set to always refresh mock users at runtime if executed
    with open('mock_users.csv', 'w', newline='') as csvfile:
        fieldnames = ['user_id','danceability','energy','valence','acousticness','tempo','loudness','genres','artists','popular_tracks','song_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_users)
        


def random_generate(start:float, end:float) -> float: 
    return random.uniform(start, end)

def random_execute(num_users, num_songs): 
    DEFAULT_DATA_FILENAME = 'tracks_features.csv'
    print("Loading songs")
    song_store: SongStore = SongStore(file_name=DEFAULT_DATA_FILENAME)
    print("Getting songs to a list")
    songs = song_store.get_all_songs()
    print("Writing to CSV")
    generate_random_users(num_users, songs, num_songs)
    print("End of program")

def generate_real_users(songs, user_id): 
    new_user = UserProfile(user_id=user_id)
    for song in songs: 
        new_user.update_profile_with_song(song)
    csv_dict = [new_user.write_to_csv_dict()]

    with open('real_users.csv', 'a', newline='') as csvfile:
        fieldnames = ['user_id','danceability','energy','valence','acousticness','tempo','loudness','genres','artists','popular_tracks','song_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_dict)

def real_execute(user_file_name, user_id):
    '''
    takes in a real user file information CSV and tranform to CSV file 
    '''
    print("Loading songs")
    song_store = SongStore(file_name=user_file_name)
    print("Getting songs to a list")
    songs = song_store.get_all_songs()
    print("Writing to CSV")
    generate_real_users(songs, user_id)
    print("End of program")



# Uncomment for generate 100 random users with 50 songs each. 
# random_execute(100, 50)

# Uncomment for generate based on real user info
user_file_name = "adn-spotify-playlist_features-runaway.csv"
user_id = 'anthony'
real_execute(user_file_name, user_id)
