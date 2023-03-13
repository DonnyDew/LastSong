import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pandas as pd

def getDF(playlist_link):
    scope = "user-library-read"
    user = os.environ.get('SPOT_USER') #Environmental variable is set up
    token = util.prompt_for_user_token(user, scope)
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth=token,auth_manager=auth_manager)

    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    data = {'AlbumName': [],
            'IsLast': [],
            'TotalTracks': [],
            'TracksInAlbum': [],
            }
    tracks_in_playlist = 0
    album_last_songs = {} # initialize dictionary to store last song names for each album
    
    offset = 0
    while True:
        results = sp.playlist_tracks(playlist_URI, offset=offset)
        items = results['items']
        tracks_in_playlist += len(items)
        
        for track in items:
            track_uri = track["track"]["uri"]
            track_info = sp.track(track_uri)
            album_type = track_info['album']['album_type'] 

            if album_type == "album":
                track_name = track["track"]["name"] 
                album = track["track"]["album"]["name"] 
                total_tracks = track_info['album']['total_tracks']
                albumID = track_info['album']['id']

                if albumID in album_last_songs:
                    last_song = album_last_songs[albumID] # retrieve last song name from dictionary
                    isLast = int(track_name == last_song)
                else:
                    last_song = find_last_song(albumID)
                    album_last_songs[albumID] = last_song # add album ID and last song name to dictionary
                    isLast = int(track_name == last_song)

                # add the data for the current track to the dictionary
                if album not in data['AlbumName']:
                    data['AlbumName'].append(album)
                    data['IsLast'].append(isLast)
                    data['TotalTracks'].append(total_tracks)
                    data['TracksInAlbum'].append(1)
                else:
                    index = data['AlbumName'].index(album)
                    data['IsLast'][index] = data['IsLast'][index] or isLast
                    data['TotalTracks'][index] = total_tracks
                    data['TracksInAlbum'][index] += 1
        
        if results['next'] is None:
            break
            
        offset += len(items)

    # create a new DataFrame from the dictionary and return it
    return pd.DataFrame(data), tracks_in_playlist


def find_last_song(album_id):
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    album = sp.album(album_id)
    tracks = album['tracks']['items']
    last_track = tracks[-1]
    return last_track['name']
def calculateProb(df,tracks_in_playlist):
    num_last_tracks = sum(df['IsLast'] == 1)
    prop_last_tracks = num_last_tracks / tracks_in_playlist
    
    df["isLast"] = df["TracksInAlbum"] / df["TotalTracks"]
    prob_last_tracks = df["isLast"].mean()
    return f"The proportion of last tracks is {prop_last_tracks*100:.2f}% compared to the expected of {prob_last_tracks*100:.2f}%"
