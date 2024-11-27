from collections import Counter
from typing import TextIO

from UserProfileSystem.UserProfile import UserProfile
import csv
import os

import Data.constants as c


class UserProfileStore:
    DATA_DIRNAME: str = "Data"

    user_profiles_csv: str

    def __init__(
            self: "UserProfileStore",
            user_profiles_csv: str,
    ) -> None:
        self.user_profiles_csv = os.path.join(self.DATA_DIRNAME, user_profiles_csv)

    def _read_csv(
            self: "UserProfileStore",
    ) -> list[dict[str, str]]:
        """Read the CSV file of user profiles and return data as a list
        of dictionaries.
        
        Returns:
            A list of dictionaries representing user profiles read from
            the given file.
            
        Raises:
            FileNotFoundError: If the CSV file does not exist.
        """

        try:
            file: TextIO
            with open(self.user_profiles_csv, mode='r', newline='', encoding='utf-8') as file:
                reader: csv.DictReader = csv.DictReader(file)
                row: dict[str, str]
                return [row for row in reader]
        except FileNotFoundError as e:
            print(f"Error reading user profiles from '{self.user_profiles_csv}'. Exiting...")
            raise e

    def _write_csv(
            self: "UserProfileStore",
            rows: list[dict[str, str]],
    ) -> None:
        """Write the given list of rows back to the CSV file.
        
        Parameters:
            rows (list[dict[str, str]]): A list of dictionaries 
                representing user profiles read from the given file.
        """
        file: TextIO
        with open(self.user_profiles_csv, mode='w', newline='', encoding='utf-8') as file:
            fieldnames: list[dict[str, str]] = rows[0].keys() if rows else []  # Get headers from first row
            writer: csv.DictWriter = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def get_user_profile(
            self: "UserProfileStore",
            user_id: str,
    ) -> UserProfile | None:
        """Fetch a user profile by user_id.
        
        Parameters:
            user_id (str): The user_id of the user profile to fetch.
        
        Returns:
            The fetched user profile by user_id.
        """
        rows: list[dict[str, str]] = self._read_csv()
        
        row: dict[str, str]
        for row in rows:
            if row['user_id'] == user_id:
                # Create UserProfile instance from CSV data
                user_profile = UserProfile(user_id=row['user_id'])
                user_profile.danceability = float(row['danceability'])
                user_profile.energy = float(row['energy'])
                user_profile.valence = float(row['valence'])
                user_profile.acousticness = float(row['acousticness'])
                user_profile.tempo = float(row['tempo'])
                user_profile.loudness = float(row['loudness'])

                # Restore genres, artists, and popular tracks (handle as strings or lists)
                user_profile.genres = Counter(eval(row['genres']))
                user_profile.artists = Counter(eval(row['artists']))
                user_profile.popular_tracks = Counter(eval(row['popular_tracks']))
                user_profile.song_count = int(row['song_count'])

                return user_profile
        return None  # User profile not found

    def update_user_profile(
            self: "UserProfileStore",
            user_id: str,
            user_profile: UserProfile,
    ) -> None:
        """Updates a user profile."""
        rows = self._read_csv()
        updated = False

        for i, row in enumerate(rows):
            if row['user_id'] == user_id:
                # Update the row with the new values
                rows[i] = {
                    'user_id': user_profile.user_id,
                    'danceability': user_profile.danceability,
                    'energy': user_profile.energy,
                    'valence': user_profile.valence,
                    'acousticness': user_profile.acousticness,
                    'tempo': user_profile.tempo,
                    'loudness': user_profile.loudness,
                    'genres': str(user_profile.genres),
                    'artists': str(user_profile.artists),
                    'popular_tracks': str(user_profile.popular_tracks),
                    'song_count': user_profile.song_count,
                }
                updated = True
                break

        if not updated:
            # If not found, add the new profile as a new row
            rows.append({
                'user_id': user_profile.user_id,
                'danceability': user_profile.danceability,
                'energy': user_profile.energy,
                'valence': user_profile.valence,
                'acousticness': user_profile.acousticness,
                'tempo': user_profile.tempo,
                'loudness': user_profile.loudness,
                'genres': str(user_profile.genres),
                'artists': str(user_profile.artists),
                'popular_tracks': str(user_profile.popular_tracks),
                'song_count': user_profile.song_count,
            })

        self._write_csv(rows)

    def remove_user_profile(
            self: "UserProfileStore",
            user_id: str,
    ) -> None:
        """Removes a user profile from the CSV file."""
        rows = self._read_csv()
        rows = [row for row in rows if row['user_id'] != user_id]
        self._write_csv(rows)
