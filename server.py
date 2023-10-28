from flask import Flask, send_file, request
from helper import process
import os

app = Flask(__name__)


@app.route("/download", methods=["GET"])
def get_song():
    """
    Retrieves a song based on the provided song_id and downloads it directly.
    """
    # delete song.mp3 and artwork.png

    if os.path.exists("/tmp/song.mp3"):
        os.remove("/tmp/song.mp3")
    if os.path.exists("/tmp/artwork.png"):
        os.remove("/tmp/artwork.png")

    song_id = request.args.get("song_id")
    process(song_id)  # Call the process method with the song_id
    return send_file("/tmp/song.mp3", as_attachment=True)


if __name__ == "__main__":
    app.run()
