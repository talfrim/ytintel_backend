import json

from service import channels, videos
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

''' ALIVE TEST '''

@app.route('/alive')
def alive():
    return "I'm alive"


''' CHANNELS '''

@app.route('/channels/searchChannels', methods=['GET'])
def get_channels():
    q = request.args.get('q')
    if q is not None:
        print(q)
        print(type(q))
        x = q
        res = channels.search_channels(x)
        if res is not None:
            return res
    return "error", 500



''' VIDEOS '''


# returns video id list from playlist id,
# client supposed to send it from channel's data response it gets
@app.route('/videos/videosIds', methods=['GET'])
def get_videos_ids_by_playlist():
    pl_id = request.args.get('playlistId')
    if pl_id is not None:
        res = videos.get_videos_ids_by_playlist(pl_id)
        if res is not None:
            return res
    return "Server error", 500


# returns video preview info by video id
@app.route('/videos/videoPreviewInfoById', methods=['GET'])
def get_videos_info_by_id():
    vid_id = request.args.get('videoId')
    if vid_id is not None:
        res = videos.get_video_info_by_id(vid_id)
        if res is not None:
            return res
    return "Server error", 500


# ***DO NOT USE***- videos come with comments by default now.
@app.route('/videos/videoComments', methods=['GET'])
# returns the comments we want to show for specific video
def get_video_comments():
    video_id = request.args.get('videoId')
    if video_id is not None:
        res = videos.get_commetns_for_video(video_id)
        if res is not None:
            return res
    return "Server error", 500







if __name__ == "__main__":
    app.run()


