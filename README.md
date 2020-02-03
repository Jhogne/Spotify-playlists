# Spotify-playlists

Spotify-playlists allows the user to easily create long playlists by adding all tracks from a list of artists to a playlist.

## Setup
1. Install the dependency [spotipy](https://github.com/plamere/spotipy) and python3
2. Create a new app and export the variables required by spotipy
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-redirect-uri'
```
3. Run program with the following syntax
```
python3 main.py 'your-username' 'playlist-name' 'artist1' 'artist2' 'artist3'
```
and follow the instructions that are printed.

## Usage
The program will add all the tracks from all artists given (>1) and add all their tracks to a playlist with the given name. The tracks will be added to a playlist with the given name, if it doesn't exist a new playlist with the given name will be created.
