from flask import Flask, send_file, request, render_template
from helper import process, empty_tmp

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


if __name__ == "__main__":
    app.run()
