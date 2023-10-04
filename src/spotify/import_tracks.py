from collections.abc import Callable
import os.path
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from track import Track, read_tracks_json


def compose_query(track: Track) -> str:
    query_list = []
    if track.title is not None:
        query_list.append(f"track:{track.title}")

    if track.album is not None:
        query_list.append(f"album:{track.album}")

    if track.artists is not None:
        first_artist = track.artists[0]
        query_list.append(f"artist:{first_artist.name}")

    query = " ".join(query_list)

    return query


def search(track: Track, limit=1, type=None):
    if type is None:
        return

    query = compose_query(track)

    search_result = spotify.search(q=query, limit=1, type="track")

    return search_result


# Returns track, list of artists, album ids
def search_track(track: Track) -> dict | None:
    search_result = search(track, type="track")

    found_tracks = search_result["tracks"]["items"]
    if len(found_tracks) == 0:
        return None

    ids = dict()

    found_track = found_tracks[0]
    track_id = found_track["id"]
    track_name = found_track["name"]

    album = found_track["album"]
    album_id = album["id"]
    album_name = album["name"]

    artist_ids = list()
    artist_names = list()

    artists = found_track["artists"]
    for artist in artists:
        artist_id = artist["id"]
        artist_name = artist["name"]

        artist_ids.append(artist_id)
        artist_names.append(artist_name)

    ids["track_id"] = track_id
    ids["album_id"] = album_id
    ids["artist_ids"] = artist_ids

    print("---")
    print(f"Original track: {track}")
    print(f"Found track: {track_name} - {album_name} - {artist_names}")
    print("---")

    return ids


def print_set(info: str, print_set: set) -> None:
    print(info)
    print("\n".join(print_set))


def add_tracks(track_ids: set) -> None:
    print_set("Adding tracks", track_ids)
    # Maximum: 50 IDs
    add_ids(track_ids, 50, spotify.current_user_saved_tracks_add)


def add_albums(album_ids: set) -> None:
    print_set("Adding albums", album_ids)
    # Maximum: 20 IDs
    add_ids(album_ids, 20, spotify.current_user_saved_albums_add)


def add_artists(artist_ids: set) -> None:
    print_set("Adding artist", artist_ids)
    # Maximum: 50 IDs
    add_ids(artist_ids, 50, spotify.user_follow_artists)


def add_ids(ids: set, max: int, request_method: Callable[[list], None]) -> None:
    paged_ids = [ids[i : i + max] for i in range(0, len(ids), max)]
    for ids_page in paged_ids:
        request_method(ids_page)


def cache_ids_json(ids: dict, output_file="spotify_ids_cache.json") -> None:
    json_ids = json.dumps(ids, ensure_ascii=False)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json_ids)


if __name__ == "__main__":
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope="user-library-modify user-follow-modify")
    )

    cache_file_path = "output/spotify_ids_cache.json"
    if os.path.isfile(cache_file_path):
        with open(cache_file_path, "r", encoding="utf-8") as f:
            ids = json.load(f)

        add_tracks(ids["track_ids"])
        add_albums(ids["album_ids"])
        add_artists(ids["artist_ids"])
        exit(0)

    tracks = read_tracks_json(input_file="output/tracks.json")

    track_ids = set()
    album_ids = set()
    artist_ids = set()

    for track in tracks:
        found_ids = search_track(track)
        if found_ids is None:
            continue

        track_ids.add(found_ids["track_id"])
        album_ids.add(found_ids["album_id"])
        artist_ids.update(found_ids["artist_ids"])

    cache_ids_json(
        ids={
            "track_ids": list(track_ids),
            "album_ids": list(album_ids),
            "artist_ids": list(artist_ids),
        },
        output_file=cache_file_path,
    )
    add_tracks(track_ids)
    add_albums(album_ids)
    add_artists(artist_ids)
