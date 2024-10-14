import urllib.request
import json


def get_recommendation_seeds(): 
    artist_list = []
    genre_list = []

    # TODO: Programatically/hard code artist/genres. 
    seed_artist = ''
    seed_genres = ''
    seed_tracks = ''
    # Limit of tracks of songs. 
    limit = 10
    market = ''

    # TODO: Add seed artists and recommendations at the end of the list. 
    url = ('https://api.spotify.com/v1/recommendations?seed_artists=' + seed_artist 
        + '&seed_genres=' + seed_genres + '&seed_tracks=' + seed_tracks)

    response = urllib.request.urlopen(url)
    data = response.read().decode('UTF-8')

    file = open("data.json","w")
    file.write(data)

    new_data = json.loads(data)
    # get_articles = new_data['articles']

    # new_data_articles = json.dumps(get_articles)

    # TODO: Write it out to a CSV file instead of JSON. Use 
    # # JSON first to verify data fetched correctly. 
    f = open("data.json", "r")
    new_data = json.loads(f.read())

def main(): 
    get_recommendation_seeds()