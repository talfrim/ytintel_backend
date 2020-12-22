import json

from business_logic.youtube_communicator import youtube_communicator


# returns all data for previewing the video according to id provided
def get_video_info_by_id(vid_id):
    video = youtube_communicator.get_videos_data_from_id_list([vid_id])[0]  # video object
    comment_list = youtube_communicator.get_comments_for_video(vid_id)  # all comments for video

    # analyzing comments
    video.comment_list = comment_list
    video.analyze_comments()
    top_comments_lst = comment_list[:10]  # getting top 10 comments
    video.set_top_comments_lst(top_comments_lst)

    # turn to dict and  return json
    video_dict = video.get_dict()  # turn into dictionary so it can be jsonfied
    return json.dumps(video_dict)


# if multiple videos support is needed- currently no
def get_videos_data(vid_id_list):
    return json.dumps([get_video_info_by_id(vid_id) for vid_id in vid_id_list])


#  returns video ids "list" (as str)
def get_videos_ids_by_playlist(pl_id):
    video_ids = youtube_communicator.get_videos_ids_from_playlist_id(pl_id)
    if video_ids is not None:
        return json.dumps(video_ids)
