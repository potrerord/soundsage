'''
Use multiple strategies to improve recommendation accuracy
Explore-exploit strategy: similar to reinforcement learning: 
Explore Random diverse song with probability e, and most similar exploit with probability 1 - e
Set a trade-off decay rate for exploration. 

weighted updates to the user profile vector. 

'''
from Data import Song
import numpy as np
import random
    

def explore_exploit(loaded_songs: List[Song], recommendations: List[Song], epsilon, top_n): 
    '''
    Explore-exploit strategy: similar to reinforcement learning: 
    Explore Random diverse song with probability e, and most similar exploit with probability 1 - e
    Set a trade-off decay rate for exploration. 
    
    Loaded songs: List of loaded songs from the CSV file. 
    recommendations: recommendations made by either KNN or cosine similarity. List of songs. 
        Randomly sample 10 to start. 
    Epsilon: probability of choosing a random song from the loaded songs, else choose from the recommendation list. 
        Sample top 10
    Epsilon decays after each recommendation made on the current user. Should be a feature of user object
    '''
    choice = np.random.choice([0,1], p=[epsilon, 1-epsilon])
    if choice == 0: 
        recommend_songs = random.sample(loaded_songs, top_n)
    else: 
        recommend_songs = recommendations[:top_n]
    epsilon = epsilon * 0.999999
    return recommend_songs, epsilon