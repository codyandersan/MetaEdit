import os

from flask import Flask, send_file, request, render_template, jsonify
from helper import process, empty_tmp
from lyrics import get_lyrics

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/download", methods=["GET"])
def get_song():
    """
    Retrieves a song based on the provided song_id and downloads it directly.
    """

    empty_tmp()

    song_id = request.args.get("song_id")
    fpath = process(song_id)  # Call the process method with the song_id
    return send_file(fpath, as_attachment=True)

@app.route("/lyrics", methods=["GET"])
def get_lyrics_endpoint():
    title = request.args.get("title")
    artist = request.args.get("artist")

    lyrics = get_lyrics(title, artist)

    return jsonify({"lyrics": lyrics})


# Get PORT from environment variable
# if __name__ == "__main__":
#     port = os.getenv("PORT")
#     app.run(port=port)
