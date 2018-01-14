from flask import Flask,request
import youtube_dl
import threading

app = Flask(__name__)

videos = []

@app.route('/')
def list():
    return str(videos)

@app.route('/add', methods=['POST','GET'])
def  download_video():
    vid = request.args.get('v', type = str)
    if vid is not None:
        videos.append(str(vid))

    return "Success"

@app.route('/download')
def download():
    ydl_opts = {}
    errors = []
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for vid in videos:
            try:
                ydl.download([vid])
                videos.remove(vid)
            except:
                errors.append("ERROR: " + str(vid))

    if errors == []:
        return "DONE"
    else:
        return str(errors)

