import tkinter as tk
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk
from lastsong import getDF,calculateProb
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import os
from io import BytesIO

def get_playlist_image(playlist_link):
    playlist_id = playlist_link.split('/')[-1]
    scope = "user-library-read"
    user = os.environ.get('SPOT_USER') #Environmental variable is set up
    token = util.prompt_for_user_token(user, scope)
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth=token,auth_manager=auth_manager)
    # Get the playlist information, including the image URL
    playlist = sp.playlist(playlist_id)
    image_url = playlist['images'][0]['url']
    
    # Download the image from the URL and open it with PIL
    response = requests.get(image_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    
    # Resize the image to fit in the GUI
    maxsize = (400, 400)
    img.thumbnail(maxsize, Image.ANTIALIAS)
    
    # Convert the PIL image to a Tkinter-compatible image and return it
    img_tk = ImageTk.PhotoImage(img)
    return img_tk

def process_playlist_link(playlistlink, result_label, image_label):
    try:
        # Get the playlist image and display it
        image = get_playlist_image(playlistlink)
        image_label.config(image=image)
        image_label.image = image
        
        # Calculate and display the result
        data = getDF(playlistlink)
        df = data[0]
        tracks_in_playlist = data[1]
        result_str = str(calculateProb(df,tracks_in_playlist))
        result_label.config(text=result_str)
    except Exception as e:
        result_label.config(text=str(e))

# Create the GUI
root = tk.Tk()
root.title("Playlist Processor")
root.geometry("600x500")

# Add a background image
bg_image = Image.open("spotifybackground.png")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add a header label
header_label = tk.Label(root, text="Playlist Processor", font=("Arial Bold", 24),bg='#1ED760')
header_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

# Create the input field
playlist_link_var = tk.StringVar()
playlist_link_label = tk.Label(root, text="Enter Playlist Link:", font=("Arial", 14),bg='#1ED760')
playlist_link_label.grid(row=1, column=0, padx=20, pady=(20, 5), sticky="w")
playlist_link_entry = tk.Entry(root, textvariable=playlist_link_var, width=40, font=("Arial", 12))
playlist_link_entry.grid(row=1, column=1, padx=20, pady=(20, 5))

# Create the submit button
submit_button = tk.Button(root, text="Process Playlist", command=lambda: process_playlist_link(playlist_link_var.get(), result_label, playlist_image_label), font=("Arial", 14), bg="#ff6961", fg="white")
submit_button.grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 10))

# Add a result label
result_label = tk.Label(root, text="", font=("Arial", 12),bg='#1ED760')
result_label.grid(row=3, column=0, columnspan=2, padx=20, pady=(10, 0))

# Add a playlist image label
playlist_image_label = tk.Label(root, image=None)
playlist_image_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(10, 20))

# Run the GUI
root.mainloop()

