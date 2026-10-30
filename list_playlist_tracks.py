"""
Export Playlist Tracks to CSV
Fetches all tracks from a designated Spotify playlist and saves metadata to a CSV file.
"""

import os
import sys
import pandas as pd
from spotify_client import get_spotify_client

def export_playlist_tracks(
    playlist_id: str = None,
    output_csv: str = os.path.join("data", "playlist_tracks.csv")
) -> pd.DataFrame:
    """
    Retrieves all tracks from a specific Spotify playlist and exports metadata to CSV.
    
    If playlist_id is not provided, it reads SPOTIPY_PLAYLIST_ID from the environment.
    """
    if not playlist_id:
        playlist_id = os.getenv("SPOTIPY_PLAYLIST_ID")

    if not playlist_id or "your_target_playlist" in playlist_id:
        print("[ERROR] No target Playlist ID specified.")
        print("Please set SPOTIPY_PLAYLIST_ID in your .env file or pass it as an argument.")
        sys.exit(1)

    # Clean URL if full Spotify URL was provided
    if "spotify.com/playlist/" in playlist_id:
        playlist_id = playlist_id.split("playlist/")[1].split("?")[0]

    sp = get_spotify_client()
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    print(f"[INFO] Fetching tracks for playlist '{playlist_id}'...")
    results = sp.playlist_items(playlist_id)
    tracks = results.get("items", [])

    while results.get("next"):
        results = sp.next(results)
        tracks.extend(results.get("items", []))
        print(f"       Fetched {len(tracks)} tracks so far...")

    print(f"[INFO] Total playlist tracks retrieved: {len(tracks)}")

    records = []
    for item in tracks:
        track = item.get("track", {})
        if not track or not track.get("id"):
            continue

        artists = track.get("artists", [])
        artist_1_id = artists[0]["id"] if len(artists) > 0 else None
        artist_1_name = artists[0]["name"] if len(artists) > 0 else None
        artist_2_id = artists[1]["id"] if len(artists) > 1 else None
        artist_2_name = artists[1]["name"] if len(artists) > 1 else None

        album = track.get("album", {})
        records.append({
            "track id": track.get("id"),
            "track name": track.get("name"),
            "album id": album.get("id"),
            "album name": album.get("name"),
            "artist 1 id": artist_1_id,
            "artist 1 name": artist_1_name,
            "artist 2 id": artist_2_id,
            "artist 2 name": artist_2_name
        })

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"[SUCCESS] Saved {len(df)} tracks to '{output_csv}'.")
    return df

if __name__ == "__main__":
    target_id = sys.argv[1] if len(sys.argv) > 1 else None
    export_playlist_tracks(target_id)
