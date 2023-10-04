import json
from artist import Artist

class Track:
    def __init__(self, title: str, album: str | None, artists: list[Artist]) -> None:
        self.title = title
        self.album = album
        self.artists = []
        for artist in artists:
            if isinstance(artist, Artist):
                self.artists.append(artist)
            elif isinstance(artist, dict):
                self.artists.append(Artist(**artist))

    def __str__(self) -> str:
        return f"Title: {self.title} - Album: {self.album} - Artists: {self.artists}"

    def __repr__(self) -> str:
        return f"Track({str(self)})"

def read_tracks_json(input_file="tracks.json") -> list[Track]:
    with open(input_file, "r", encoding="utf-8") as f:
        json_tracks = json.load(f)

    tracks = [Track(**track) for track in json_tracks]
    return tracks

def write_tracks_json(tracks: list[Track], output_file="tracks.json") -> None:
    json_tracks = json.dumps(tracks, default=lambda x: x.__dict__, ensure_ascii=False)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json_tracks)


