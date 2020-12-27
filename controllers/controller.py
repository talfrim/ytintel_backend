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

# returns up to 5 channels' data, by a search query for channels.
@app.route('/channels/searchChannels', methods=['GET'])
def get_channels():
    q = request.args.get('q')
    if q is not None:
        x = q
        res = channels.search_channels(x)
        if res is not None:
            return res
    return "error", 500



''' VIDEOS '''

# returns videos ids list by playlist id,
# which the client receives from channel's data.
@app.route('/videos/videosIds', methods=['GET'])
def get_videos_ids_by_playlist():
    pl_id = request.args.get('playlistId')
    if pl_id is not None:
        res = videos.get_videos_ids_by_playlist(pl_id)
        if res is not None:
            return res
    return "Server error", 500


# returns video preview info by video id.
@app.route('/videos/videoPreviewInfoById', methods=['GET'])
def get_videos_info_by_id():
    vid_id = request.args.get('videoId')
    if vid_id is not None:
        res = videos.get_video_info_by_id(vid_id)
        if res is not None:
            return res
    return "Server error", 500


if __name__ == "__main__":
    app.run()


