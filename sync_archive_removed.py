"""
Sync Archive & Track Removals
Compares current Liked Tracks against a Master Library Archive and a Removed Tracks list.
Automatically archives newly liked tracks and logs unliked tracks to the removed list.
"""

import os
import pandas as pd

def sync_archive_and_removals(
    liked_csv: str = os.path.join("data", "liked_tracks.csv"),
    master_csv: str = os.path.join("data", "master_library.csv"),
    removed_csv: str = os.path.join("data", "removed_tracks.csv")
):
    """
    Performs set difference analysis across:
      1. Liked Tracks (current snapshot)
      2. Master Library (permanent active archive)
      3. Removed Tracks (historical log of unliked / deleted tracks)

    Workflow:
      - Tracks in Liked but missing from Master (and not previously logged in Removed)
        are added to the Master Library.
      - Tracks in Master but absent from Liked are moved from Master to Removed Tracks.
    """
    if not os.path.exists(liked_csv):
        print(f"[ERROR] '{liked_csv}' not found. Run 'list_liked_tracks.py' first.")
        return

    df_liked = pd.read_csv(liked_csv, index_col=0)
    df_master = pd.read_csv(master_csv, index_col=0) if os.path.exists(master_csv) else pd.DataFrame(columns=df_liked.columns)
    df_removed = pd.read_csv(removed_csv, index_col=0) if os.path.exists(removed_csv) else pd.DataFrame(columns=df_liked.columns)

    set_liked = set(df_liked.index)
    set_master = set(df_master.index)
    set_removed = set(df_removed.index)

    # Tracks present only in liked songs
    only_liked = set_liked - set_master
    # Tracks present only in master library (removed from liked songs)
    only_master = set_master - set_liked

    print(f"[ANALYSIS] Liked only (new tracks): {len(only_liked)}")
    print(f"[ANALYSIS] Master only (missing from current likes): {len(only_master)}")

    # Exclude tracks already intentionally marked as removed
    to_add_master = only_liked - set_removed
    print(f"[ACTION] New tracks to add to Master Library: {len(to_add_master)}")

    # 1. Add new tracks to master library
    if to_add_master:
        new_rows = df_liked[df_liked.index.isin(to_add_master)]
        df_master = pd.concat([df_master, new_rows])

    # 2. Move deleted tracks to removed archive
    if only_master:
        removed_rows = df_master[df_master.index.isin(only_master)]
        df_removed = pd.concat([df_removed, removed_rows])
        # Drop duplicates in removed archive
        df_removed = df_removed[~df_removed.index.duplicated(keep="first")]
        # Remove from active master library
        df_master = df_master[~df_master.index.isin(only_master)]
        print(f"[ACTION] Moved {len(only_master)} tracks to '{removed_csv}'.")

    # 3. Save updated CSV files
    df_master.to_csv(master_csv)
    df_removed.to_csv(removed_csv)
    print(f"[SUCCESS] Updated Master Library ({len(df_master)} total) and Removed Archive ({len(df_removed)} total).")

if __name__ == "__main__":
    sync_archive_and_removals()
