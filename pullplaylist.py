import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import requests
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import googleapiclient.errors
from dotenv import load_dotenv
from pytube import Playlist

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

def get_tracks(PlaylistItems):

    tracks = {}
    for item in PlaylistItems["items"]:

        for artist in item["track"]["artists"]:
            tracks.update({item["track"]["name"]:artist["name"]})
    
    return tracks
def yt_authentication():
    scopes = ["https://www.googleapis.com/auth/youtube"]
    path = "client_secret_646657873122-7aldfsd5cl41110oj2si2gilpq6iuupi.apps.googleusercontent.com (1).json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(path,scopes)
    credentials = flow.run_local_server(port=0)

    youtube = build('youtube','v3',credentials = credentials)
    return youtube


def create_YT_playlist(playlist_name,youtube):
    request = youtube.playlists().insert(
        part = 'snippet, status',
        body = {
            "snippet": {
                "title": f"{playlist_name}",
                "description":"list of songs to be downloaded",
                "default language":"en"
            },
            "status":{
                "privacyStatus" : "private"
            }
        }
    )
    response= request.execute()
    id = response['id']
    return id 


def search_for_songs(tracks_and_artists,youtube):
    song_ids = []
    list_keys = list(tracks_and_artists.keys())
    list_values = list(tracks_and_artists.values())
    for idx,_ in enumerate(tracks_and_artists):
        request = youtube.search().list(
            part = "snippet",
            q = list_keys[idx] + list_values[idx],
            maxResults = 1
        )
        response = request.execute()
        for item in response["items"]:
            id = item["id"]
            videoID = id["videoId"]
            song_ids.append(videoID)
    return song_ids


def add_songs_to_playlist(song_ids,playlistId,youtube):
    for song_id in song_ids:
        request = youtube.playlistItems().insert(
            part = "snippet",
            body = {
                "snippet":{
                    "playlistId" : playlistId,
                    "resourceId" : {
                        "kind" : "youtube#video",
                        "videoId": song_id
                    }
                }
            }
        ).execute()



def download_playlist(id):
    url = f"https://www.youtube.com/playlist?list={id}"
    p = Playlist(url)
    for video in p.videos:
        video.streams.first().download(output_path="/Users/abhinavpappu/Downloads")
        
    

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
    youtube = yt_authentication()
    playlist_id = create_YT_playlist(playlist_name=selected_playlist,youtube=youtube)
    print("playlist_id",playlist_id)
    song_ids = search_for_songs(tracks_and_artists=playlist_tracks,youtube =youtube)
    add_songs_to_playlist(song_ids=song_ids, playlistId=playlist_id,youtube=youtube )
    download_playlist(playlist_id)

if __name__ == '__main__':
    main()

