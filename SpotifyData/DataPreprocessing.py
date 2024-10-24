import pandas as pd 
import re 

spotify_data = pd.read_csv("merged_spotify_data.csv")

def clean_track_name(name):
    # Replace non-ASCII characters with a space or remove them
    name = re.sub(r'[^\x00-\x7F]+', '', name)  # Removes non-ASCII characters
    return name

def bnasic_preprocessing(spotify_data):
    #spotify_data = pd.read_csv("merged_spotify_data.csv")

    spotify_data.drop(spotify_data.columns[[0,22]],axis=1,inplace=True)
    spotify_data.rename(columns = {'id':'track_id','name_x':'track_name','popularity_x':'track_popularity','name_y':'artist_name','popularity_y':'artist_popularity'}, inplace = True)
    spotify_data.dropna(inplace=True)

    spotify_data['track_name'] = spotify_data['track_name'].apply(clean_track_name)
    spotify_data.drop(['id_artists','artists'],inplace=True,axis=1)

def get_cleaned_dataframe():
    bnasic_preprocessing(spotify_data)
    return spotify_data
