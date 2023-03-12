# Playlist Processor
This Python script analyzes a Spotify playlist and determines the proportion of songs that are last in an album within the playlist compared to the expected proportion based on the artists' album lengths.

## Requirements
The following packages are required to run the script:
* `spotipy`
* `pandas`
* `tkinter`
* `Pillow`

## How to use
1. Obtain a Spotify playlist link
2. Run the script and enter the playlist link in the GUI
3. The script will display a message box showing the proportion of last tracks in the playlist compared to the expected proportion

## Explanation of the code
The script consists of three main functions:
* `getDF`: takes a Spotify playlist link and returns a Pandas DataFrame containing information about each track in the playlist
* `calculateProb`: takes the DataFrame returned by getDF and the number of tracks in the playlist, and returns a string describing the proportion of last tracks in the playlist compared to the expected proportion
* `process_playlist_link`: takes a Spotify playlist link, calls getDF and calculateProb, and displays the result in a message box
The GUI is created using the tkinter package, with a background image and header label added. When the "Submit" button is clicked, process_playlist_link is called with the input playlist link as an argument.

## How it works
The script uses the Spotify API via the `spotipy package` to obtain information about each track in the playlist. For each album, the proportion of "last tracks" (tracks that are the last on their respective albums) is calculated, and the expected proportion of last tracks in the playlist is determined based on the proportions of each album in the playlist. The actual proportion of last tracks in the playlist is then compared to the expected proportion, and the result is displayed in a message box.

