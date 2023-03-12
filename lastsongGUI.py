import tkinter as tk
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk
from lastsong import process_playlist_link
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