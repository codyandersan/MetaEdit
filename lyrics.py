from googlesearch import search
from bs4 import BeautifulSoup
import requests


# to search


def get_lyrics_random_api(title):
    url = f"https://some-random-api.com/others/lyrics?title={title}"
    response = requests.get(url)
    lyrics = response.json()["lyrics"]
    return lyrics

def get_lyricsgoal(title, artist):
    """
    Retrieves the lyrics for a given song title and artist.

    Args:
        title (str): The title of the song.
        artist (str): The name of the artist.

    Returns:
        Lyrics in text format
    """

    query = f"{title} {artist.split(',')[0]} lyrics site:lyricsgoal.com"

    url = list(search(query, tld="com", num=1, stop=1, pause=0.5))[0]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    lyrics_div = soup.find("div", class_="song_lyrics")
    children = lyrics_div.findChildren()

    lyrics = ""

    for child in children:
        #if child is p
        if child.name == "p":
            lyrics = "\n".join([lyrics, child.text])

    return lyrics.lstrip("\n")

def get_lyrics(title, artist):
    try:
        lyrics = get_lyricsgoal(title, artist)
    except:
        print(f"Can't find lyrics on lyricsgoal.com!")

        try:
            lyrics = get_lyrics_random_api(title)
        except:
            return "Lyrics not found"
    return lyrics

if __name__ == "__main__":
    lyrics = get_lyrics("tum hi ho", "arijit singh")
    print(lyrics)
    with open("lyrics.txt", "w") as f:
        f.write(lyrics)