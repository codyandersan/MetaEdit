from lyrics_extractor import SongLyrics


GCS_API_KEY = "AIzaSyC32HWPe2FtRgkFsWFB0lK5jxSCTN-Ymag"
GCS_ENGINE_ID = "30b4eebe2f43f45f9"

extract_lyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)


data = extract_lyrics.get_lyrics("Shape of You")
print(data)
