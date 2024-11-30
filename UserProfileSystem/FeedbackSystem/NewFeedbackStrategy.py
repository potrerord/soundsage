import json
import os
import Data.constants as c


class NewFeedbackStrategy:
    ADJUSTMENT_FACTOR: float = 0.01
    profile_file: str
    weight_factors: dict[str, int]

    def __init__(
            self: "NewFeedbackStrategy",
            profile_file: str = "user_profiles.json",
            weight_factors: dict[str, int] = None,
    ) -> None:
        # Initialize profile file and weight factors
        self.profile_file = profile_file
        self.weight_factors = weight_factors if weight_factors else {
            'danceability': 1,
            'energy': 1,
            'valence': 1,
            'acousticness': 1,
            'instrumentalness': 1,
            'liveness': 1,
            'popularity': 1,
            'speechiness': 1,
            'tempo': 1,
            'loudness': 1
        }

    def load_profiles_from_json(self):
        """Load the list of user profiles from the JSON file."""
        if os.path.exists(self.profile_file):
            with open(self.profile_file, "r", encoding="utf-8") as file:
                return json.load(file)  # Returns a list of profiles
        return []

    def save_profiles_to_json(self, profiles):
        """Save the list of user profiles to the JSON file."""
        with open(self.profile_file, "w", encoding="utf-8") as file:
            json.dump(profiles, file, indent=4)
        print(f"User profiles saved to {self.profile_file}.")

    def save_user_profile(self, user_id, user_profile):
        """Save or update a specific user's profile in the JSON file."""
        # Load existing profiles
        profiles = self.load_profiles_from_json()

        # Check if the user's profile already exists
        user_profile_data = user_profile.__dict__
        for idx, profile in enumerate(profiles):
            if profile["user_id"] == user_id:
                # Update the existing profile
                profiles[idx] = user_profile_data
                break
        else:
            # Add a new profile
            profiles.append(user_profile_data)

        # Save the updated profiles list back to the file
        self.save_profiles_to_json(profiles)

    def update_user_profile_based_on_feedback(self, user_profile, user_id, song, feedback_score):
        """Update the user profile based on feedback score and save it."""

        # Ensure user profile exists
        if not user_profile:
            raise ValueError("User profile not found.")

        # Define feature ranges (add all relevant features here)
        feature_ranges = {
            "acousticness": (c.ACOUSTICNESS_MIN, c.ACOUSTICNESS_MAX),
            "danceability": (c.DANCEABILITY_MIN, c.DANCEABILITY_MAX),
            "energy": (c.ENERGY_MIN, c.ENERGY_MAX),
            "instrumentalness": (c.INSTRUMENTALNESS_MIN, c.INSTRUMENTALNESS_MAX),
            "liveness": (c.LIVENESS_MIN, c.LIVENESS_MAX),
            "loudness": (c.LOUDNESS_MIN_USEFUL, c.LOUDNESS_MAX),
            "speechiness": (c.SPEECHINESS_MIN, c.SPEECHINESS_MAX),
            "tempo": (c.TEMPO_MIN_USEFUL, c.TEMPO_MAX_USEFUL),
            "valence": (c.VALENCE_MIN, c.VALENCE_MAX),
        }

        # Track features and their ratings
        # feature_updates = {feature: getattr(song, feature) for feature in self.weight_factors.keys()}
        feature_updates = {
            "acousticness": song.acousticness,
            "danceability": song.danceability,
            "energy": song.energy,
            "instrumentalness": song.instrumentalness,
            "liveness": song.liveness,
            "loudness": song.loudness,
            "speechiness": song.speechiness,
            "tempo": song.tempo,
            "valence": song.valence,
        }

        # Apply feedback (positive or negative) to the features
        for feature, feature_value in feature_updates.items():
            # if feature_value is None or feature not in feature_ranges:
            #     continue  # Skip features with missing values or undefined ranges

            # Get the range for this feature
            min_value, max_value = feature_ranges[feature]

            # Adjust the user's profile feature based on feedback score (1-5 scale)
            # Increase or decrease based on feedback: feedback_score ranges from 1 (negative) to 5 (positive)
            adjustment_factor: float = (feedback_score - 3) * self.ADJUSTMENT_FACTOR  # Feedback score adjustment scaled

            # Get the current feature value from the user profile
            current_value = getattr(user_profile, feature)

            # Adjust the feature based on feedback score, respecting the feature's natural range
            new_feature_value = current_value + adjustment_factor * feature_value
            new_feature_value = min(max(new_feature_value, min_value), max_value)  # Clamp to feature range

            # Update the user's profile with the adjusted feature value
            setattr(user_profile, feature, new_feature_value)

        # Save or update the user profile in the JSON file
        self.save_user_profile(user_id, user_profile)

        return user_profile
