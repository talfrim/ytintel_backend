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


# returns up to 100 video previews only summary of comments
@app.route('/videos/videosPrev', methods=['GET'])
def get_videos_info():
    channel_id = request.args.get('channel_id')
    if channel_id is not None:
        res = videos.get_videos_prev_by_channel(channel_id)
        if res is not None and int(res.status_code) == 200:
            return res
    return "Server error", 500


@app.route('/videos/videoComments', methods=['GET'])
# returns the comments we want to show for specific video
def get_video_comments():
    video_id = request.args.get('video_id')
    if video_id is not None:
        res = videos.get_commetns_for_video(video_id)
        if res is not None and int(res.status_code) == 200:
            return res
    return "Server error", 500







if __name__ == "__main__":
    app.run()


