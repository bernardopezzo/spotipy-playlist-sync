"""
Export Liked Tracks to CSV
Fetches all saved (liked) songs from the user's Spotify library and saves them to a CSV file.
"""

import os
import pandas as pd
from spotify_client import get_spotify_client

def export_liked_tracks(output_csv: str = os.path.join("data", "liked_tracks.csv")) -> pd.DataFrame:
    """
    Retrieves all liked tracks for the authenticated user and exports metadata to CSV.
    
    Columns exported:
      - track id, track name, album id, album name
      - artist 1 id, artist 1 name, artist 2 id, artist 2 name
    """
    sp = get_spotify_client()
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    print("[INFO] Fetching saved tracks from your Spotify library...")
    results = sp.current_user_saved_tracks(limit=50)
    tracks = results.get("items", [])
    
    while results.get("next"):
        results = sp.next(results)
        tracks.extend(results.get("items", []))
        print(f"       Fetched {len(tracks)} tracks so far...")

    print(f"[INFO] Total liked tracks retrieved: {len(tracks)}")

    records = []
    for idx, item in enumerate(tracks, start=1):
        track = item.get("track", {})
        if not track:
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
    export_liked_tracks()
