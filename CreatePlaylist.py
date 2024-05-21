import os 
import requests
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv

def yt_authentication():
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    path = "client_secret_646657873122-7aldfsd5cl41110oj2si2gilpq6iuupi.apps.googleusercontent.com (1).json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(path,scopes)
    credentials = flow.run_local_server(port=0)

    youtube = build('youtube','v3',credentials = credentials)
    return youtube




def create_YT_playlist(tracks_artists,youtube):
    youtube.playlists().insert(
        part = 'snippet, status',
        body = {


        }

    )

    
    


def main():
    load_dotenv()
    tracks_artists = {'Sirens': 'Icarus', 'Sacrifice': 'Kx5', 'Reminiscing': 'INDI', 'Go Back (feat. Julia Church)': 'Julia Church', 'hakuna matata': 'Gunna', 'flight fm': 'Joy Orbison'}
    youtube = yt_authentication()
    create_YT_playlist(tracks_artists=tracks_artists,youtube=youtube)

if __name__ == '__main__':
    main()
