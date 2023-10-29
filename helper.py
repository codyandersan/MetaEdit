import os
import requests
import music_tag
from lyrics import get_lyrics

def append_metadata(song_path, title, artist, artwork_path, lyrics=None):
    # Load the song file
    f = music_tag.load_file(song_path)

    # Set the title, artist, and lyrics
    f["title"] = title
    f["artist"] = artist
    f["lyrics"] = lyrics

    # Set the artwork
    with open(artwork_path, "rb") as img_in:
        try:
            f["artwork"] = img_in.read()
        except:
            pass
    # Save the metadata
    f.save()


def fetch_song_details(song_id):
    url = f"https://jiosaavn-api-codyandersan.vercel.app/songs?id={song_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def extract_song_info(song_details):
    quality_map = {
        "12kbps": 12,
        "48kbps": 48,
        "96kbps": 96,
        "160kbps": 160,
        "320kbps": 320,
    }

    if song_details["status"] == "SUCCESS":
        song_name = song_details["data"][0]["name"]
        image_link = max(
            song_details["data"][0]["image"],
            key=lambda x: int(x["quality"].split("x")[0]),
        )["link"]
        download_url = max(
            song_details["data"][0]["downloadUrl"],
            key=lambda x: quality_map[x["quality"]],
        )["link"]
        primary_artists = song_details["data"][0]["primaryArtists"]
        has_lyrics = bool(song_details["data"][0]["hasLyrics"])

        return song_name, image_link, download_url, primary_artists, has_lyrics
    else:
        return None


def download(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print("Downloaded successfully!")
    else:
        print("Failed to download.")


def process(song_id):
    print("Fetching song details")
    song_details = fetch_song_details(song_id)

    print("Extracting song info")
    info = extract_song_info(song_details)

    fpath = f"/tmp/{info[0]} — {info[3].split(',')[0]}.m4a"

    print("Downloading song")
    download(info[2], fpath)

    print("Downloading artwork")
    download(info[1], "/tmp/artwork.png")

    if info[4]:
        print("Fetching lyrics")
        lyrics = get_lyrics(info[0], info[3])
    else:
        lyrics = None

    print("Appending metadata")
    append_metadata(fpath, info[0], info[3], "/tmp/artwork.png", lyrics=lyrics)

    print("Done!")

    return fpath

def empty_tmp():
    for file in os.listdir("/tmp"):
        file_path = os.path.join("/tmp", file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")


if __name__ == "__main__":
    process("SNkDIrfg")

