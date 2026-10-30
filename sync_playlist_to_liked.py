"""
Sync Playlist Tracks to Liked Songs
Compares tracks in a playlist against current Liked Songs and a Removed Tracks blacklist.
Automatically likes missing tracks on Spotify, respecting the removal blacklist.
"""

import os
import pandas as pd
from spotify_client import get_spotify_client

def sync_playlist_to_liked(
    playlist_csv: str = os.path.join("data", "playlist_tracks.csv"),
    liked_csv: str = os.path.join("data", "liked_tracks.csv"),
    removed_csv: str = os.path.join("data", "removed_tracks.csv")
):
    """
    Finds tracks present in a playlist that are NOT in Liked Songs,
    filters out tracks in the Removed Tracks list, and likes them on Spotify.
    """
    if not os.path.exists(playlist_csv):
        print(f"[ERROR] '{playlist_csv}' not found. Run 'list_playlist_tracks.py' first.")
        return
    if not os.path.exists(liked_csv):
        print(f"[ERROR] '{liked_csv}' not found. Run 'list_liked_tracks.py' first.")
        return

    df_playlist = pd.read_csv(playlist_csv, index_col=0)
    df_liked = pd.read_csv(liked_csv, index_col=0)
    df_removed = pd.read_csv(removed_csv, index_col=0) if os.path.exists(removed_csv) else pd.DataFrame(columns=df_liked.columns)

    set_playlist = set(df_playlist.index)
    set_liked = set(df_liked.index)
    set_removed = set(df_removed.index)

    # Tracks present in playlist but not currently in liked songs
    only_playlist = set_playlist - set_liked
    print(f"[ANALYSIS] Tracks in playlist not currently liked: {len(only_playlist)}")

    # Filter out tracks in the removed blacklist
    to_add_liked = list(only_playlist - set_removed)
    print(f"[ACTION] Tracks to add to Spotify Liked Songs: {len(to_add_liked)}")

    if not to_add_liked:
        print("[SUCCESS] No new tracks need to be added to Liked Songs.")
        return

    sp = get_spotify_client()
    print("[INFO] Adding tracks to Spotify Liked Songs in batches of 50...")

    # Spotify API accepts up to 50 tracks per batch for user library modifications
    for i in range(0, len(to_add_liked), 50):
        batch = to_add_liked[i:i + 50]
        sp.current_user_saved_tracks_add(tracks=batch)
        print(f"       Liked batch {i + 1} - {i + len(batch)} of {len(to_add_liked)}")

    print(f"[SUCCESS] Successfully added {len(to_add_liked)} tracks to your Spotify Liked Songs!")

if __name__ == "__main__":
    sync_playlist_to_liked()
