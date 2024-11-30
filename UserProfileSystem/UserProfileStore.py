import os
import json
import csv
from collections import Counter
from typing import Optional, TextIO
from UserProfileSystem.UserProfile import UserProfile  # <-- Make sure this import is present

from UserProfileSystem.UserProfile import UserProfile

import Data.constants as c


class UserProfileStore:
    DATA_DIRNAME: str = "Data"
    csv_file: str
    user_profiles_json: str

    def __init__(
            self: "UserProfileStore",
            csv_file: str,
            json_file: str,
    ) -> None:
        self.csv_file = csv_file
        self.user_profiles_json = json_file

    def _read_csv(self: "UserProfileStore") -> list[dict[str, str]]:
        """Reads the CSV file and returns a list of dictionaries."""
        try:
            file: TextIO
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader: csv.DictReader = csv.DictReader(file)

                row: dict[str, str]
                return [row for row in reader]
            
        except FileNotFoundError:
            return []  # If file doesn't exist, return an empty list

    def _write_csv(
            self: "UserProfileStore",
            rows: list[dict[str, str]],
    ) -> None:
        """Writes the given list of rows back to the CSV file."""
        file: TextIO
        with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = rows[0].keys() if rows else []  # Get headers from first row
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _read_json(self) -> dict[str, UserProfile]:
        if not os.path.exists(self.user_profiles_json):
            return {}
        with open(self.user_profiles_json, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_json(self, user_profiles: dict[str, UserProfile]) -> None:
        with open(self.user_profiles_json, 'w', encoding='utf-8') as f:
            json.dump(user_profiles, f, default=str, indent=4)

    def _update_aggregated_data(self, user_profile: UserProfile) -> None:
        """Aggregate user profile data."""
        user_profile.danceability = self._aggregate_value(user_profile.danceability)
        user_profile.energy = self._aggregate_value(user_profile.energy)
        user_profile.valence = self._aggregate_value(user_profile.valence)
        user_profile.acousticness = self._aggregate_value(user_profile.acousticness)
        user_profile.tempo = self._aggregate_value(user_profile.tempo)
        user_profile.loudness = self._aggregate_value(user_profile.loudness)

    def _aggregate_value(self, value: float) -> float:
        """Perform aggregation on a given value."""
        # Example aggregation logic, replace with your actual aggregation method
        return value  # For now, just returns the value (could be a sum, average, etc.)


    def get_user_profile(self: "UserProfileStore", user_id: str) -> UserProfile | None:
        """Fetch a user profile by user_id."""
        if os.path.exists(self.user_profiles_json):  # Check if the JSON file exists
            user_profiles = self._read_json()

            # If the aggregated data exists in the JSON, return the UserProfile with pre-aggregated values
            if user_id in user_profiles:
                user_data = user_profiles[user_id]
                # Convert the dictionary into a UserProfile object
                user_profile = UserProfile(user_id)
                user_profile.danceability = user_data['danceability']
                user_profile.energy = user_data['energy']
                user_profile.valence = user_data['valence']
                user_profile.acousticness = user_data['acousticness']
                user_profile.tempo = user_data['tempo']
                user_profile.loudness = user_data['loudness']
                user_profile.genres = Counter(user_data['genres'])
                user_profile.artists = Counter(user_data['artists'])
                user_profile.popular_tracks = Counter(user_data['popular_tracks'])
                user_profile.song_count = user_data['song_count']
                return user_profile
            
        print(f"\nJSON file not found: {self.user_profiles_json}")
        # Fallback to reading from CSV and performing aggregation if JSON doesn't have the profile
        rows = self._read_csv()
        print("\nPrinting out rows in user profile csv read")
        print(rows)
        for row in rows:
            if row['id'] == user_id:
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

                # Aggregating data before returning
                self._update_aggregated_data(user_profile)

                # Save the aggregated data into the JSON file for future use
                if os.path.exists(self.user_profiles_json):
                    user_profiles = self._read_json()
                else:
                    user_profiles = {}

                user_profiles[user_id] = {
                    'danceability': user_profile.danceability,
                    'energy': user_profile.energy,
                    'valence': user_profile.valence,
                    'acousticness': user_profile.acousticness,
                    'tempo': user_profile.tempo,
                    'loudness': user_profile.loudness,
                    'genres': dict(user_profile.genres),
                    'artists': dict(user_profile.artists),
                    'popular_tracks': dict(user_profile.popular_tracks),
                    'song_count': user_profile.song_count
                }

                self._write_json(user_profiles)
                return user_profile
        print(f"\nUser profile not found.")
        return None  # User profile not found

    def update_user_profile(self, user_id: str, user_profile: UserProfile) -> None:
        """Update or add a user profile."""
        if os.path.exists(self.user_profiles_json):  # If JSON file exists, use it
            user_profiles = self._read_json()
            user_profiles[user_id] = user_profile
            self._write_json(user_profiles)
        else:
            print(f"\nJSON file not found: {self.user_profiles_json}")
            # If JSON file doesn't exist, fallback to CSV
            rows = self._read_csv()
            updated = False
            for i, row in enumerate(rows):
                if row['user_id'] == user_id:
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

        # After updating CSV or JSON, ensure we also update the aggregated data in JSON
        user_profiles = self._read_json()
        user_profiles[user_id] = user_profile
        self._write_json(user_profiles)


    def remove_user_profile(self: "UserProfileStore", user_id: str):
        """Removes a user profile from the CSV file."""
        rows = self._read_csv()
        rows = [row for row in rows if row['user_id'] != user_id]
        self._write_csv(rows)
