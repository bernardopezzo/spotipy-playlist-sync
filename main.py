"""
Spotify Playlist & Library Synchronizer (CLI Entry Point)
A complete toolset to backup, synchronize, and archive Spotify playlists and Liked Songs.
"""

import sys
import argparse
from list_liked_tracks import export_liked_tracks
from list_playlist_tracks import export_playlist_tracks
from sync_liked_to_playlist import sync_liked_to_playlist
from sync_archive_removed import sync_archive_and_removals
from sync_playlist_to_liked import sync_playlist_to_liked

def interactive_menu():
    """Displays an interactive command-line menu."""
    while True:
        print("\n" + "=" * 50)
        print("    SPOTIFY PLAYLIST & LIBRARY SYNCHRONIZER")
        print("=" * 50)
        print("1. Export Liked Tracks to CSV (data/liked_tracks.csv)")
        print("2. Export Playlist Tracks to CSV (data/playlist_tracks.csv)")
        print("3. Sync Liked Tracks into Destination Playlist")
        print("4. Sync Master Archive & Track Removals")
        print("5. Sync Playlist Tracks into Liked Songs (respecting removals)")
        print("6. Run Full Workflow (Export -> Archive -> Sync)")
        print("0. Exit")
        print("=" * 50)

        choice = input("Select an option (0-6): ").strip()
        if choice == "1":
            export_liked_tracks()
        elif choice == "2":
            pid = input("Enter Spotify Playlist ID or URL (leave blank for .env default): ").strip() or None
            export_playlist_tracks(pid)
        elif choice == "3":
            pid = input("Enter Target Playlist ID or URL (leave blank for .env default): ").strip() or None
            sync_liked_to_playlist(pid)
        elif choice == "4":
            sync_archive_and_removals()
        elif choice == "5":
            sync_playlist_to_liked()
        elif choice == "6":
            print("\n>>> STEP 1: Exporting Liked Tracks...")
            export_liked_tracks()
            print("\n>>> STEP 2: Syncing Master Library and Removed Archive...")
            sync_archive_and_removals()
            print("\n>>> STEP 3: Syncing Liked Tracks to Target Playlist...")
            sync_liked_to_playlist()
            print("\n[SUCCESS] Full workflow complete!")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("[WARN] Invalid option, please choose between 0 and 6.")

def parse_args():
    parser = argparse.ArgumentParser(description="Spotify Library and Playlist Synchronizer")
    parser.add_argument("--export-liked", action="store_true", help="Export saved tracks to CSV")
    parser.add_argument("--export-playlist", type=str, nargs="?", const="", help="Export playlist tracks to CSV")
    parser.add_argument("--sync-to-playlist", type=str, nargs="?", const="", help="Sync liked tracks to target playlist")
    parser.add_argument("--sync-archive", action="store_true", help="Sync master library and removed archive")
    parser.add_argument("--playlist-to-liked", action="store_true", help="Add playlist tracks to liked songs")
    parser.add_argument("--all", action="store_true", help="Run complete sync workflow")
    return parser.parse_args()

def main():
    args = parse_args()

    # If no flags passed, launch interactive menu
    if not any(vars(args).values()):
        interactive_menu()
        return

    if args.export_liked:
        export_liked_tracks()
    if args.export_playlist is not None:
        pid = args.export_playlist if args.export_playlist != "" else None
        export_playlist_tracks(pid)
    if args.sync_to_playlist is not None:
        pid = args.sync_to_playlist if args.sync_to_playlist != "" else None
        sync_liked_to_playlist(pid)
    if args.sync_archive:
        sync_archive_and_removals()
    if args.playlist_to_liked:
        sync_playlist_to_liked()
    if args.all:
        print("\n>>> STEP 1: Exporting Liked Tracks...")
        export_liked_tracks()
        print("\n>>> STEP 2: Syncing Master Library and Removed Archive...")
        sync_archive_and_removals()
        print("\n>>> STEP 3: Syncing Liked Tracks to Target Playlist...")
        sync_liked_to_playlist()
        print("\n[SUCCESS] Full workflow complete!")

if __name__ == "__main__":
    main()
