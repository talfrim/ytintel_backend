import json

from backend.service import channels, videos
from flask import Flask, jsonify, request
app = Flask(__name__)


''' ALIVE TEST '''

@app.route('/alive')
def alive():
    return "I'm alive"


''' CHANNELS '''

@app.route('/channels/searchChannels', methods=['GET'])
def get_channels():
    q = request.args.get('q')
    if q is not None:
        res = channels.search_channels(q)
        if res is not None:
            return res
    return "server error", 500



''' VIDEOS '''


# returns video id list from playlist id,
# client supposed to send it from channel's data response it gets
@app.route('/videos/videosIds', methods=['GET'])
def get_videos_ids_by_playlist():
    pl_id = request.args.get('playlistId')
    if pl_id is not None:
        res = videos.get_videos_ids_by_channel(pl_id)
        if res is not None:
            return res
    return "Server error", 500


# returns video preview info by video od
@app.route('/videos/videoPreviewInfoById', methods=['GET'])
def get_videos_info_by_id():
    vid_id = request.args.get('videoId')
    if vid_id is not None:
        res = videos.get_video_info_by_id(vid_id)
        if res is not None:
            return res
    return "Server error", 500


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


