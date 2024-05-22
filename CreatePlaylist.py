import os 
import requests
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv

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




    


def main():
    load_dotenv()
    playlist_name = "March 2024"
    tracks_artists = {'Sirens': 'Icarus', 'Sacrifice': 'Kx5', 'Reminiscing': 'INDI', 'Go Back (feat. Julia Church)': 'Julia Church', 'hakuna matata': 'Gunna', 'flight fm': 'Joy Orbison'}
    youtube = yt_authentication()
    playlist_id = create_YT_playlist(playlist_name=playlist_name,youtube=youtube)
    print("playlist_id",playlist_id)
    song_ids = search_for_songs(tracks_and_artists=tracks_artists,youtube =youtube)
    add_songs_to_playlist(song_ids=song_ids, playlistId=playlist_id,youtube=youtube )

if __name__ == '__main__':
    main()
