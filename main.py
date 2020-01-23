
import sys

import spotipy
import spotipy.util as util

if len(sys.argv) > 2:
    username = sys.argv[1]
    artist_name = sys.argv[2]
else:
    print("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
    sys.exit()

scope = 'playlist-modify-private, playlist-modify-public, user-library-read'
token = util.prompt_for_user_token(username, scope)

playlist = 'spotify:user:jonas.hogne:playlist:6D1u6A4DmGiKceXhGlJyDM'
track = ['spotify:track:6rqhFgbbKwnb9MLmUQDhG6']

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, playlist, track, position=None)
    print(results)
else:
    print("Can't get token for", username)

artist_id = sp.search(q=artist_name, type='artist')['artists']['items'][0]['id']

results = sp.artist_albums(artist_id, album_type='album,single')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
    tracks = sp.album_tracks(album['id'])['items']
    for i in tracks:
        print(i['name'])
    print()
