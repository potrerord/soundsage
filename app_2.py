import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Load a real dataset (e.g., Spotify's Million Playlist Dataset)
# This example assumes you have song features and user interactions data.
# For demonstration, we'll use a synthetic dataset as a placeholder.

# Example data preparation (real dataset)
# Columns: user_id, song_id, interaction (1 if user liked the song, 0 if not)
data = pd.DataFrame({
    'user_id': np.random.randint(0, 100, 1000),
    'song_id': np.random.randint(0, 200, 1000),
    'interaction': np.random.randint(0, 2, 1000)
})

# Encode users and songs as integers
user_ids = data['user_id'].unique()
song_ids = data['song_id'].unique()

user_to_index = {user_id: i for i, user_id in enumerate(user_ids)}
song_to_index = {song_id: i for i, song_id in enumerate(song_ids)}

data['user_id'] = data['user_id'].map(user_to_index)
data['song_id'] = data['song_id'].map(song_to_index)

num_users = len(user_ids)
num_songs = len(song_ids)

# Split data into training and test sets
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Neural network model
embedding_size = 50  # Size of the embedding vectors

# User embedding
user_input = keras.Input(shape=(1,), name='user_input')
user_embedding = layers.Embedding(input_dim=num_users, output_dim=embedding_size, name='user_embedding')(user_input)
user_embedding = layers.Flatten()(user_embedding)

# Song embedding
song_input = keras.Input(shape=(1,), name='song_input')
song_embedding = layers.Embedding(input_dim=num_songs, output_dim=embedding_size, name='song_embedding')(song_input)
song_embedding = layers.Flatten()(song_embedding)

# Concatenate user and song embeddings
concat = layers.Concatenate()([user_embedding, song_embedding])

# Add additional features if available (e.g., song metadata, user preferences)
# Example: additional_input = keras.Input(shape=(num_additional_features,), name='additional_input')
# concat = layers.Concatenate()([concat, additional_input])

# Dense layers
dense = layers.Dense(128, activation='relu')(concat)
dense = layers.Dense(64, activation='relu')(dense)
output = layers.Dense(1, activation='sigmoid')(dense)

# Build and compile the model
model = keras.Model(inputs=[user_input, song_input], outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    [train_data['user_id'], train_data['song_id']],
    train_data['interaction'],
    epochs=10,
    batch_size=32,
    validation_split=0.2
)

# Evaluate the model
eval_results = model.evaluate([test_data['user_id'], test_data['song_id']], test_data['interaction'])
print(f"Test Loss: {eval_results[0]}, Test Accuracy: {eval_results[1]}")


# Function to recommend songs for a given user
def recommend_songs(user_id, num_recommendations=5):
    user_index = user_to_index.get(user_id)
    if user_index is None:
        raise ValueError("User ID not found")

    # Predict scores for all songs
    song_indices = np.arange(num_songs)
    user_indices = np.full(num_songs, user_index)
    predictions = model.predict([user_indices, song_indices]).flatten()

    # Get top recommendations
    top_song_indices = predictions.argsort()[-num_recommendations:][::-1]
    top_song_ids = [list(song_to_index.keys())[i] for i in top_song_indices]
    return top_song_ids


# Example recommendation
user_id = 10  # Replace with an actual user ID from the dataset
print("Recommended songs:", recommend_songs(user_id))

# Enhancements for real-world applications:
# 1. Incorporate song metadata (e.g., genre, artist, tempo) as additional inputs.
# 2. Use implicit feedback (e.g., skip behavior, play counts) for more nuanced interactions.
# 3. Fine-tune embedding sizes and model architecture based on data characteristics.
# 4. Employ collaborative filtering with matrix factorization for scalability.
