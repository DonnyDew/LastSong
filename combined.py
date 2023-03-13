import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk

def getDF(playlist_link):
    SPOTIPY_CLIENT_ID = str(os.environ.get('SPOTIPY_CLIENT_ID'))
    SPOTIPY_CLIENT_SECRET = str(os.environ.get('SPOTIPY_CLIENT_SECRET'))
    SPOTIPY_REDIRECT_URI = str(os.environ.get('SPOTIPY_REDIRECT_URI'))

    os.environ['SPOTIPY_CLIENT_ID'] = SPOTIPY_CLIENT_ID
    os.environ['SPOTIPY_CLIENT_SECRET'] = SPOTIPY_CLIENT_SECRET
    os.environ['SPOTIPY_REDIRECT_URI'] = SPOTIPY_REDIRECT_URI

    scope = "user-library-read"
    user = os.environ.get('SPOT_USER') #Environmental variable is set up

    token = util.prompt_for_user_token(user, scope)

    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth=token,auth_manager=auth_manager)

    
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    df = []
    tracks_in_playlist = 0
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        track_uri = track["track"]["uri"]
        track_info = sp.track(track_uri)
        album_type = track_info['album']['album_type'] 
        if album_type == "album":
            tracks_in_playlist += 1
            track_name = track["track"]["name"] #
            track_pop = track_info['popularity']
            track_num = track_info["track_number"]
            album = track["track"]["album"]["name"] #
            total_tracks = track_info['album']['total_tracks']
            isLast = 0
            if track_num == total_tracks:
                isLast = 1
            
            track_artists = track_info['artists'] 
            
            if (len(track_artists) > 1):
                for i in range(1,len(track_artists)):
                    artist_names = artist_names + "," + track_artists[i]["name"]
            else:
                artist_names =  track_info['artists'][0]["name"] 
            
            
            track_dict = {"TrackName":track_name,"TrackNum":track_num,
                        "ArtistNames":artist_names,"TotalTracks":total_tracks,"IsLast":isLast,
                        "AlbumName":album
                        }
            df.append(track_dict)

    df= pd.DataFrame(df)
    data = {'AlbumName': [],
            'ArtistNames': [],
            'IsLast': [],
            'TotalTracks': [],
            'TracksInAlbum': [],
            }

    # iterate over each unique album in the original DataFrame
    for album_name in df['AlbumName'].unique():
        # select only the rows corresponding to the current album
        album_df = df[df['AlbumName'] == album_name]

        # concatenate the track names into a single string
        track_names = ', '.join(album_df['TrackName'].tolist())

        # determine the artist names and total tracks for the album
        artist_names = album_df['ArtistNames'].iloc[0]
        total_tracks = album_df['TotalTracks'].iloc[0]

        # determine if any of the tracks in the album are the last one
        is_last = 1 if 1 in album_df['IsLast'].tolist() else 0

        # determine the number of tracks in the album
        tracks_in_album = len(album_df)

        # add the data for the current album to the dictionary
        data['AlbumName'].append(album_name)
        data['ArtistNames'].append(artist_names)
        data['IsLast'].append(is_last)
        data['TotalTracks'].append(total_tracks)
        data['TracksInAlbum'].append(tracks_in_album)
        
        # create a new DataFrame from the dictionary and return it
    return pd.DataFrame(data),tracks_in_playlist



def calculateProb(df,tracks_in_playlist):
    num_last_tracks = sum(df['IsLast'] == 1)
    prop_last_tracks = num_last_tracks / tracks_in_playlist
    
    df["isLast"] = df["TracksInAlbum"] / df["TotalTracks"]
    chanceLast = df["isLast"].mean()
   
    total_tracks_in_albums = df['TracksInAlbum'].sum()
    prob_last_tracks = (chanceLast * total_tracks_in_albums) / tracks_in_playlist
    return f"The proportion of last tracks is {prop_last_tracks*100:.2f}% compared to the expected of {prob_last_tracks*100:.2f}%"
    
def process_playlist_link(playlistlink):
    try:
        data = getDF(playlistlink)
        df = data[0]
        tracks_in_playlist = data[1]
        result_str = str(calculateProb(df,tracks_in_playlist))
        print(result_str)
        messagebox.showinfo("Result", result_str)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    

# Create the GUI
root = tk.Tk()
root.title("Playlist Processor")
root.geometry("500x300")

# Add a background image
bg_image = Image.open("spotifybackground.png")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add a header label
header_label = tk.Label(root, text="Playlist Processor", font=("Arial Bold", 24),bg='#1ED760')
header_label.pack(pady=(20, 10))

# Create the input field
playlist_link_var = tk.StringVar()
playlist_link_label = tk.Label(root, text="Enter Playlist Link:", font=("Arial", 14),bg='#1ED760')
playlist_link_label.pack(pady=(20, 5))
playlist_link_entry = tk.Entry(root, textvariable=playlist_link_var, width=40, font=("Arial", 12))
playlist_link_entry.pack(pady=(5, 20))

# Create the submit button
submit_button = tk.Button(root, text="Process Playlist", command=lambda: process_playlist_link(playlist_link_var.get()),font=("Arial", 14),bg="#ff6961", fg="white")
submit_button.pack()

# Run the GUI
root.mainloop()
    


        
    
    

    



