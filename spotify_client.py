"""
Spotify Client Helper Module
Provides centralized authentication and Spotipy client initialization.
"""

import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

DEFAULT_SCOPE = (
    "playlist-read-private "
    "playlist-read-collaborative "
    "playlist-modify-private "
    "playlist-modify-public "
    "user-library-modify "
    "user-library-read"
)

def get_spotify_client(scope: str = DEFAULT_SCOPE) -> spotipy.Spotify:
    """
    Initializes and returns an authenticated Spotipy client.
    Credentials are read from environment variables:
      - SPOTIPY_CLIENT_ID
      - SPOTIPY_CLIENT_SECRET
      - SPOTIPY_REDIRECT_URI (defaults to http://localhost:1234/)
    """
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:1234/")

    if not client_id or not client_secret or "your_spotify_" in client_id:
        print("[ERROR] Spotify API credentials not configured.")
        print("Please create a .env file from .env.example and set your SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET.")
        sys.exit(1)

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        open_browser=True
    )
    return spotipy.Spotify(auth_manager=auth_manager)
