import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import requests

load_dotenv()#loads environoment variables

def print_playlists(up):
    for playlist in up["items"]:
        name = playlist["name"]
        print(name)
    return

def get_playlist_id(name, up):
    for playlist in up["items"]:
        if name == playlist["name"]:
            return playlist["id"]
    print("!!Playlist Not found!!")
    return 

def print_tracks(PlaylistItems):
    for item in PlaylistItems["items"]:
        print(item["track"]["name"])


#returns a dictionary of key value pairs of songs and artists
def get_tracks(PlaylistItems):
    tracks = {}
    for item in PlaylistItems["items"]:

        for artist in item["track"]["artists"]:
            tracks.update({item["track"]["name"]:artist["name"]})
    
    return tracks


def main():
    scope = "playlist-read-private user-library-read"
    sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id= os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret= os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri= os.getenv("SPOTIPY_REDIRECT_URI"),
    scope = scope
    ))

    user_playlists = sp.current_user_playlists()
    print_playlists(user_playlists)#prints outs all of the current users playlists

    selected_playlist = input("Select a playlist you want to download:")
    playlist_id = get_playlist_id(selected_playlist, user_playlists)
    
    playlist_items = sp.playlist_tracks(playlist_id)
    
    playlist_tracks = get_tracks(playlist_items)
    


if __name__ == '__main__':
    main()

