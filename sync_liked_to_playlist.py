"""
Sync Liked Songs to Playlist
Exports all saved tracks from the user's Spotify library directly into a designated target playlist.
"""

import os
import sys
from spotify_client import get_spotify_client

def sync_liked_to_playlist(playlist_id: str = None, avoid_duplicates: bool = True):
    """
    Retrieves all liked tracks and uploads them to the target playlist in batches of 100.
    """
    if not playlist_id:
        playlist_id = os.getenv("SPOTIPY_PLAYLIST_ID")

    if not playlist_id or "your_target_playlist" in playlist_id:
        print("[ERROR] No target Playlist ID specified.")
        print("Please set SPOTIPY_PLAYLIST_ID in your .env file or pass it as an argument.")
        sys.exit(1)

    if "spotify.com/playlist/" in playlist_id:
        playlist_id = playlist_id.split("playlist/")[1].split("?")[0]

    sp = get_spotify_client()

    print("[INFO] Fetching liked tracks from user library...")
    results = sp.current_user_saved_tracks(limit=50)
    saved_tracks = results.get("items", [])
    while results.get("next"):
        results = sp.next(results)
        saved_tracks.extend(results.get("items", []))

    track_ids = [item["track"]["id"] for item in saved_tracks if item.get("track", {}).get("id")]
    print(f"[INFO] Found {len(track_ids)} liked tracks.")

    if avoid_duplicates:
        print("[INFO] Checking existing tracks in destination playlist to avoid duplicates...")
        existing_results = sp.playlist_items(playlist_id)
        existing_items = existing_results.get("items", [])
        while existing_results.get("next"):
            existing_results = sp.next(existing_results)
            existing_items.extend(existing_results.get("items", []))
        
        existing_ids = set(item["track"]["id"] for item in existing_items if item.get("track", {}).get("id"))
        track_ids = [t_id for t_id in track_ids if t_id not in existing_ids]
        print(f"[INFO] {len(track_ids)} new tracks to add after deduplication.")

    if not track_ids:
        print("[SUCCESS] Playlist is already up to date. No new tracks to add.")
        return

    print(f"[INFO] Adding {len(track_ids)} tracks to playlist in batches of 100...")
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i + 100]
        sp.playlist_add_items(playlist_id, batch)
        print(f"       Added batch {i + 1} - {i + len(batch)} of {len(track_ids)}")

    print(f"[SUCCESS] Successfully synchronized {len(track_ids)} tracks to playlist '{playlist_id}'.")

if __name__ == "__main__":
    target_id = sys.argv[1] if len(sys.argv) > 1 else None
    sync_liked_to_playlist(target_id)
