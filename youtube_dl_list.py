from flask import Flask,request
import youtube_dl
import threading

app = Flask(__name__)


class Videos:

    def __init__(self):
        self.videos = []


    def add(self, video):
        self.videos.append(video)


    def remove(self, video):
        self.videos.remove(video)


    def get_video(self):
        return self.videos.pop()


    def while_video(self):
        print("videos: " + str(self.videos))
        if self.videos != []:
            return True
        return False

    def get_list(self):
        for index in range(len(self.videos)-1, -1, -1):
            yield self.videos[index]


videos = Videos()

@app.route('/')
def list():
    output = ""
    for vid in videos.get_list():
        output += "\n" + vid
    return output


@app.route('/add', methods=['POST','GET'])
def  download_video():
    vid = request.args.get('v', type = str)
    if vid is not None and vid != '':
        videos.add(str(vid))

    return "Success"


@app.route('/download')
def download():
    ydl_opts = {}
    errors = []
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        while videos.while_video():
            vid = videos.get_video()
            print("vid: " + vid)
            try:
                ydl.download([vid])
                videos.remove(vid)
            except:
                errors.append("ERROR: " + str(vid))

    if errors == []:
        return "DONE"
    else:
        return str(errors)


@app.route('/remove', methods=['GET'])
def remove():
    vid = request.args.get('v', type = str)
    if vid is not None and vid != '':
        try:
            videos.remove(str(vid))
        except:
            return "Could not remove " + str(vid)

    return "Success"



