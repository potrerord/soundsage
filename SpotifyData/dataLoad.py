import pandas as pd 
import ast

tracks_data = pd.read_csv("tracks.csv")
artists_data = pd.read_csv("artists.csv")

tracks_data['artist_ids'] = tracks_data['id_artists'].apply(lambda x: ast.literal_eval(x))


tracks_exploded = tracks_data.explode('artist_ids')
merged_data = pd.merge(tracks_exploded, artists_data, left_on='artist_ids', right_on='artist_id', how='left')
print(merged_data.head())
merged_data.to_csv("merged_spotify_data.csv")

# aggregated_data = merged_data.groupby('artist_ids').agg({
#     'danceability': 'first',  # Keep original track features
#     'loudness': 'first',
#     'instrumentalness': 'first',
#     'artist_popularity': 'mean',  # Example of averaging artist popularity for tracks with multiple artists
#     # Add more columns as needed
# }).reset_index()

# print(aggregated_data.head())