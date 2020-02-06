import sys

import spotipy
import spotipy.util as util
import argparse

def authorize(username):
    scope = 'playlist-modify-private playlist-modify-public playlist-read-private'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
    else:
        print("Can't get token for", username)
    return sp    

def get_all_results(results, sp):
    items = results['items']
    while results['next']:
        results = sp.next(results)
        items.extend(results['items'])
    return items

def add_to_playlist(username, playlist_id, tracks, sp):
    chunks = [tracks[x:x+100] for x in range(0,len(tracks), 100)]
    for i in chunks:
        sp.user_playlist_add_tracks(username, playlist_id, i, position=None)

def get_fields(field, l):
    return [i[field] for i in l]

def get_playlist_id(playlist_name, username, sp):
    playlists = sp.user_playlists(username)
    names = get_fields('name', playlists['items'])
    playlist_id = ''
    for i in playlists['items']:
        if i['name'] == playlist_name:
            playlist_id = i['id']
            break

    if playlist_id == '':
        playlist_id = sp.user_playlist_create(username, playlist_name, public=True, description='')['id']
    
    return playlist_id

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--username", required=True, help="Spotify username")
    parser.add_argument("-p","--playlist", required=True, help="Playlist name")
    parser.add_argument("-a","--artists", required=True, nargs="+", help="Artist names")

    args = parser.parse_args()
    return (args.username, args.playlist, args.artists)

def main():
    username, playlist_name, artist_names = get_arguments()

    sp = authorize(username)
    playlist_id = get_playlist_id(playlist_name, username, sp)

    # Gets the first aritst id when searching for artists with each prompt
    artist_ids = []
    for name in artist_names:
        artist_ids.append(sp.search(q=name, type='artist')['artists']['items'][0]['id'])

    albums = []
    for artist_id in artist_ids:
        albums += get_all_results(sp.artist_albums(artist_id, album_type='album,single'), sp)
        
    tracks = []
    for album in albums:
        album_tracks = sp.album_tracks(album['id'])['items']
        tracks += get_fields('id', album_tracks)

    playlist_tracks = get_all_results(sp.user_playlist_tracks(username,playlist_id), sp)
    orig_tracks = [x['track']['id'] for x in playlist_tracks]
    add_to_playlist(username, playlist_id, list(set(tracks) - set(orig_tracks)), sp)

if __name__ == '__main__':
    main()