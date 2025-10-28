import spotipy
from spotipy.oauth2 import SpotifyOAuth

# you'll fill these in with your real values once you make the spotify app
CLIENT_ID = "YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
REDIRECT_URI = "http://localhost:8888/callback"

SCOPE = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-currently-playing"
)

def get_spotify_client():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
        )
    )
    return sp


def spotify_pause():
    sp = get_spotify_client()
    sp.pause_playback()
    return "paused spotify."


def spotify_resume():
    sp = get_spotify_client()
    sp.start_playback()
    return "resumed playback."


def spotify_next():
    sp = get_spotify_client()
    sp.next_track()
    return "skipped to next track."


def spotify_current_track():
    sp = get_spotify_client()
    data = sp.current_user_playing_track()

    if not data or not data.get("item"):
        return "nothing is playing right now."

    track = data["item"]["name"]
    artist_names = [a["name"] for a in data["item"]["artists"]]
    artist_str = ", ".join(artist_names)

    is_paused = not data["is_playing"]

    status = "paused" if is_paused else "playing"
    return f"current track: {track} by {artist_str} ({status})."


def spotify_play_search(query: str):
    """
    try to play a track/artist/playlist just by text.
    ex: 'play travis scott' or 'play my chill playlist'
    """
    sp = get_spotify_client()

    # search for the query
    results = sp.search(q=query, type="track,playlist,artist", limit=1)

    # try track first
    tracks = results.get("tracks", {}).get("items", [])
    if tracks:
        uri = tracks[0]["uri"]
        sp.start_playback(uris=[uri])
        return f"playing {tracks[0]['name']} by {tracks[0]['artists'][0]['name']}."

    # then playlist
    playlists = results.get("playlists", {}).get("items", [])
    if playlists:
        uri = playlists[0]["uri"]
        sp.start_playback(context_uri=uri)
        return f"playing playlist {playlists[0]['name']}."

    # then artist (will start artist radio)
    artists = results.get("artists", {}).get("items", [])
    if artists:
        uri = artists[0]["uri"]
        sp.start_playback(context_uri=uri)
        return f"starting radio for {artists[0]['name']}."

    return "couldn't find anything to play with that search."