import pandas as pd
import numpy as np
import faiss
from sklearn.preprocessing import StandardScaler

from DataPreprocessing import get_cleaned_dataframe

def load_data():
    """Load the cleaned Spotify data from a CSV file."""
    return get_cleaned_dataframe()  # or pd.read_pickle('cleaned_spotify_data.pkl')

def calculate_similarity(data, features):
    """Calculate the FAISS index based on selected features."""
    # Filter only numeric features
    feature_data = data[features].select_dtypes(include=[np.number]).values.astype('float32')  # Convert to float32 for FAISS
    print("Feature Data Shape (for FAISS):", feature_data.shape)

    # Normalize the features
    scaler = StandardScaler()
    feature_data_scaled = scaler.fit_transform(feature_data)

    # Create a FAISS index
    index = faiss.IndexFlatL2(feature_data_scaled.shape[1])  # L2 distance
    index.add(feature_data_scaled)  # Add vectors to the index

    return index

def recommend_tracks(index, data, liked_tracks, features, num_recommendations=5):
    """Recommend tracks based on a user's liked tracks."""
    # Get the track indices of liked tracks
    liked_track_indices = data[data['track_id'].isin(liked_tracks)].index.tolist()
    
    if not liked_track_indices:
        print("No liked tracks found in the data.")
        return []

    # Retrieve the feature vectors for the liked tracks
    liked_vectors = data.loc[liked_track_indices, features].select_dtypes(include=[np.number]).values.astype('float32')
    print("Liked Vectors Shape (for search):", liked_vectors.shape)

    # Ensure the liked vectors have the same number of features as the index
    if liked_vectors.shape[1] != index.d:
        raise ValueError(f"Mismatched dimensions: index has {index.d} features but liked_vectors has {liked_vectors.shape[1]} features.")

    # Search for similar tracks
    D, I = index.search(liked_vectors, num_recommendations)  # D: distances, I: indices
    
    # Collect recommended track IDs
    recommended_tracks = set()
    for indices in I:
        recommended_tracks.update(data.iloc[indices]['track_id'].tolist())

    # Remove liked tracks from recommendations
    recommended_tracks = list(recommended_tracks - set(liked_tracks))
    
    return recommended_tracks[:num_recommendations]  # Return the top recommended track IDs

# Main execution
merged_spotify_data = load_data()
features = ['danceability', 'loudness', 'energy', 'liveness', 'speechiness', 'valence', 'track_popularity', 'artist_popularity']
similarity_index = calculate_similarity(merged_spotify_data, features)

liked_tracks_example = ['07A5yehtSnoedViJAZkNnc', '08y9GfoqCWfOGsKdwojr5e']  # Replace with actual track IDs the user liked
recommended_tracks = recommend_tracks(similarity_index, merged_spotify_data, liked_tracks_example, features)
print("Recommended Tracks:", recommended_tracks)
