from ytmusicapi import YTMusic
import os

from artist import Artist
from track import Track, write_tracks_json


def ytplaylist_to_artist(artists: list) -> list[Artist]:
    output_artists = []
    for artist in artists:
        name = artist["name"]
        output_artists.append(Artist(name))

    return output_artists


def ytplaylist_to_track(tracks: list) -> list[Track]:
    output_tracks = []

    for track in tracks:
        title = track["title"]

        album = track["album"]
        if album is not None:
            album_name = album["name"]
        else:
            album_name = None

        artists = track["artists"]
        output_artists = ytplaylist_to_artist(artists)

        output_tracks.append(Track(title, album_name, output_artists))

    return output_tracks


def check_tracks(
    tracks: list[Track],
    show_album_none=True,
    show_more_than_one_artist=True,
    show_zero_artists=True,
) -> None:
    album_none_text = "Album is None"
    more_than_one_artist_text = "More than one artist"
    zero_artists_text = "Zero artists"

    album_none_count = 0
    more_than_one_artist_count = 0
    zero_artists_count = 0

    for track in tracks:
        album_none = track.album is None
        more_than_one_artist = len(track.artists) > 1
        zero_artists = len(track.artists) == 0

        if (
            (album_none and show_album_none)
            or (more_than_one_artist and show_more_than_one_artist)
            or (zero_artists and show_zero_artists)
        ):
            print(f"{str(track)}:", end=" ")
            if album_none and show_album_none:
                album_none_count += 1
                print(album_none_text, end=", ")
            if more_than_one_artist and show_more_than_one_artist:
                more_than_one_artist_count += 1
                print(more_than_one_artist_text, end=", ")
            if zero_artists and show_zero_artists:
                zero_artists_count += 1
                print(zero_artists_text, end=", ")
            print()

    if show_album_none:
        print(f"{album_none_text}: {album_none_count}")
    if show_more_than_one_artist:
        print(f"{more_than_one_artist_text}: {more_than_one_artist_count}")
    if show_zero_artists:
        print(f"{zero_artists_text}: {zero_artists_count}")


if __name__ == "__main__":
    YTMUSIC_OAUTH_PATH = os.getenv("YTMUSIC_OAUTH_PATH")
    if YTMUSIC_OAUTH_PATH is None:
        YTMUSIC_OAUTH_PATH = "oauth.json"

    yt = YTMusic(YTMUSIC_OAUTH_PATH)

    liked_songs = yt.get_liked_songs(limit=0)

    liked_songs_count = liked_songs["trackCount"]

    liked_songs = yt.get_liked_songs(limit=liked_songs_count)
    liked_tracks = liked_songs["tracks"]

    tracks = ytplaylist_to_track(liked_tracks)

    check_tracks(
        tracks,
        show_album_none=True,
        show_more_than_one_artist=False,
        show_zero_artists=True,
    )
    write_tracks_json(tracks, output_file="output/tracks.json")
