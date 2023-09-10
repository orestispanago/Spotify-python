import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

USER = ""
CLIENT_ID = ""
CLIENT_SECRET = ""


# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
playlists = session.user_playlists(USER)["items"]

for playlist in playlists:
    playlist_name = playlist["name"]
    uri = playlist["uri"].split(":")[-1]
    tracks = session.playlist_tracks(uri)["items"]
    rows = []
    for track in tracks:
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
    df.to_csv(f"{playlist_name}.csv", index=False)
