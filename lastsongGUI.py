import tkinter as tk
from PIL import Image, ImageTk
from lastsong import getDF, calculateProb

def process_playlist_link(playlistlink, result_label):
    try:
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

# Create the submit button and result label
result_label = tk.Label(root, text="", font=("Arial", 10),bg='#1ED760')
result_label.pack()
submit_button = tk.Button(root, text="Process Playlist", font=("Arial", 14),bg="#ff6961", fg="white")
submit_button.pack()

# Bind the button to the lambda function that calls process_playlist_link with the current playlist_link_var and result_label values
submit_button.config(command=lambda: process_playlist_link(playlist_link_var.get(), result_label))

# Run the GUI
root.mainloop()
