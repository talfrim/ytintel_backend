import json

from backend.business_logic.youtube_communicator import youtube_communicator


# returns up to 5 channels JSON data that matches the query.
# in this implementation, the server just needs a search query and it responds with all the channels data
def search_channels(q):
    id_list = youtube_communicator.get_channels_ids_by_name(q)
    channel_jsons = []
    if len(id_list) > 0:
        for channel_id in id_list:
            channel_preview = youtube_communicator.get_channel_preview_by_id(channel_id)
            channel_jsons.append(channel_preview.get_dict())
        return json.dumps(channel_jsons)



