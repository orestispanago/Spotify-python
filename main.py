import pandas as pd
import spotipy

USER = ""
CLIENT_ID = ""
CLIENT_SECRET = ""


def list_to_df(tracks_list, export_csv_name=None):
    rows = []
    for track in tracks_list:
        row = {
            "track": track["track"]["name"],
            "artist": track["track"]["artists"][0]["name"],
            "album": track["track"]["album"]["name"],
            "released": track["track"]["album"]["release_date"],
            "added": track["added_at"],
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df = df.drop_duplicates("track")
    if export_csv_name:
        df.to_csv(export_csv_name, index=False)


def download_playlists(session):
    playlists = session.user_playlists(USER)["items"]
    for playlist in playlists:
        playlist_name = playlist["name"]
        uri = playlist["uri"].split(":")[-1]
        tracks = session.playlist_tracks(uri)["items"]
        list_to_df(tracks, export_csv_name=f"playlists/{playlist_name}.csv")


def download_liked_songs(session):
    liked_songs = []
    offset = 0
    saved_tracks = session.current_user_saved_tracks(limit=50, offset=offset)[
        "items"
    ]
    while len(saved_tracks) != 0:
        liked_songs.extend(saved_tracks)
        offset += 50
        saved_tracks = session.current_user_saved_tracks(
            limit=50, offset=offset
        )["items"]
    list_to_df(liked_songs, export_csv_name="playlists/Liked songs.csv")


token = spotipy.util.prompt_for_user_token(
    USER,
    "user-library-read",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:5500",
)


session = spotipy.Spotify(auth=token)

download_playlists(session)
download_liked_songs(session)
