from flask import Flask,request
import youtube_dl

app = Flask(__name__)

videos = []

@app.route('/')
def list():
    return str(videos)

@app.route('/add', methods=['POST','GET'])
def  download_video():
    vid = request.args.get('v', type = str)
    if vid is not None:
        videos.append(vid)

    return "Success"

@app.route('/download')
def download():
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for vid in videos:
            try:
                ydl.download([vid])
                videos.remove(vid)
            except:
                return "ERROR: " + str(vid)

    return "DONE"

