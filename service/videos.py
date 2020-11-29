import json

from backend.business_logic.youtube_communicator import youtube_communicator


# returns all data for previewing the video according to id provided
def get_video_info_by_id(vid_id):
    video = youtube_communicator.get_videos_data_from_id_list([vid_id])[0]  # video object
    comment_list = youtube_communicator.get_comments_for_video(vid_id)  # all comments for video
    for comment in comment_list:
        comment.analyze_sentiment()
        if comment_list.sentiment == 1:
            video.add_good_comment()
        else:
            video.add_bad_comment()
    video.calc_good_comments_rate()
    video_dict = video.get_dict()
    return json.dumps(video_dict)


# if multiple videos support is needed- currently no
def get_videos_data(vid_id_list):
    return json.dumps([get_video_info_by_id(vid_id) for vid_id in vid_id_list])


#  returns video ids "list" (as str)
def get_videos_ids_by_playlist(pl_id):
    video_ids = youtube_communicator.get_videos_ids_from_playlist_id(pl_id)
    if video_ids is not None:
        return json.dumps(video_ids)
