# TODO async?


import requests
import time

from business_logic.ChannelPreview import ChannelPreview
from business_logic.Video import Video
from business_logic.Comment import Comment
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")
base_url = "https://youtube.googleapis.com/youtube/v3/"

""" CHANNELS """

# This function returns a list of up to 5 top channel ids according to the name entered
def get_channels_ids_by_name(name):
    req_url = base_url + "search?part=snippet&maxResults=5&q=" + name + \
              "&type=channel&fields=items%2Fsnippet%2FchannelId&key=" + api_key
    res = requests.get(req_url)
    if int(res.status_code) == 200:
        return extract_ids_from_ids_results(res.json())


# This methods returns ChannelPreview object according to the id entered
def get_channel_preview_by_id(channel_id):
    req_url = base_url + "channels?part=snippet%2CcontentDetails%2Cstatistics&id=" \
              + channel_id + "&key=" + api_key  # only snippet, add statistics if we want (for subscribers, etc)
    res = requests.get(req_url)
    if int(res.status_code) == 200:
        res_json = res.json()
        channel_data = res_json["items"][0]
        return ChannelPreview(channel_data["id"],
                              channel_data["snippet"]["title"],
                              channel_data["snippet"]["description"],
                              channel_data["snippet"]["thumbnails"]["medium"]["url"],
                              channel_data["statistics"]["videoCount"],
                              channel_data["statistics"]["subscriberCount"],
                              channel_data["contentDetails"]["relatedPlaylists"]["uploads"])


""" VIDEOS """


# we use the uploads playlist id of a channel to get an id's list of it's videos.
# * This request can give only basic info on each video (id, title, desc, thumbnail),
#   and not statistics or comments, so additional calls required (we take only ids list
#   from here). For the info we need, "list (multiple video IDs)" in "video" segment
#   will probably work (and one more is needed for comments).
# * If we want to support more than 50 videos per channel, we should use page tokens
#   that means adding a pageToke parameter and each time giving the next page token
#   that we receive in the response.
def get_videos_ids_from_playlist_id(playlist_id, max_videos="50"):
    req_url = base_url + "playlistItems?part=contentDetails&maxResults=" + max_videos + \
              "&playlistId=" + playlist_id + "&key=" + api_key
    res = requests.get(req_url)
    if int(res.status_code) == 200:
        res_json = res.json()
        video_lst = res_json["items"]
        id_list = list(map(lambda vid: vid["contentDetails"]["videoId"], video_lst))  # get the id for each video
        return id_list


# This method returns a list of video object from a id_list request
def get_videos_data_from_id_list(id_list):
    ids_str = ','.join(id_list)
    req_url = base_url + "videos?part=snippet%2CcontentDetails%2Cstatistics&id=" + ids_str + "&key=" + api_key
    res = requests.get(req_url)
    if int(res.status_code) == 200:
        response_json = res.json()
        response_list = response_json["items"]
        video_list = list(map(lambda vid: Video(
            vid["id"],
            vid["snippet"]["title"],
            vid["snippet"]["thumbnails"]["medium"]["url"],
            vid["snippet"]["categoryId"],
            vid["statistics"]["viewCount"],
            vid["statistics"]["likeCount"],
            vid["statistics"]["dislikeCount"],
            vid["statistics"]["commentCount"]
        ), response_list))
        return video_list

# !!!DEPRECATED - use get_comments_forVideo!!!
# This method return a list of all comments for channel (comment objects),
# if more then 100 desired, using page tokens needed
def get_all_toplevel_comments_for_channel(channel_id, page_token="", max_results="100"):
    req_url = base_url + "commentThreads?part=snippet%2Creplies&allThreadsRelatedToChannelId=" + channel_id + \
              "&maxResults=" + max_results + "&pageToken=" + page_token + "&key=" + api_key
    res = requests.get(req_url)
    if int(res.status_code) == 200:
        response_json = res.json()
        response_list = response_json["items"]
        comment_list = list(map(lambda comm: Comment(
            comm["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
            comm["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
            comm["snippet"]["topLevelComment"]["snippet"]["likeCount"],
            comm["snippet"]["videoId"]
            if "videoId" in comm["snippet"] else None  # if it is not a comment on video, pun None instead
        ), response_list))
        comment_list = [comm for comm in comment_list if
                        comm is None]  # removing all none values (for comments who are on the channel and not on video)
        return comment_list

# returns all comments for videos
def get_comments_for_video(video_id, page_limit=4):
    initial_req_url = base_url + "commentThreads?part=snippet%2Creplies&maxResults=100&videoId=" + video_id + "&key=" + api_key
    res = requests.get(initial_req_url)
    has_more_comments = True
    comment_list = []
    page_count = 1
    while has_more_comments and page_count <= page_limit:
        if int(res.status_code) == 200:
            response_json = res.json()
            response_list = response_json["items"]
            page_comment_list = list(map(lambda comm: Comment(
                comm["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                comm["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                comm["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                comm["snippet"]["videoId"]
            ), response_list))
            comment_list = comment_list + page_comment_list

            '''next request'''
            has_more_comments = True if "nextPageToken" in response_json else False
            if has_more_comments:
                page_count += 1
                next_page_token = response_json["nextPageToken"]
                req_url = base_url + "commentThreads?part=snippet%2Creplies&maxResults=100&pageToken=" + next_page_token + "&videoId=" + video_id + "&key=" + api_key
                res = requests.get(req_url)
        else:
            return None  # don't go to infinite loop when status is not 200
    return comment_list


""" UTIL """

def extract_ids_from_ids_results(results_json):
    result_list = []
    for obj in results_json["items"]:
        result_list.append(obj["snippet"]["channelId"])
    return result_list

