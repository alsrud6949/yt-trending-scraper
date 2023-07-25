from init import credentials, unsafe_characters, snippet_features, category_dict, OUTPUT_BUCKET
import pandas as pd
import time
from googleapiclient.discovery import build

def get_youtube_api():
    # get youtube api credentials
    # credentials - from init.py
    # if your credentials does not include data api, make sure include it or make other one

    yt_data = build('youtube', 'v3', credentials=credentials)
    return yt_data

def prepare_feature(feature):
    # Removes any character from the unsafe characters list and surrounds the whole item in quotes
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return feature

def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
    return prepare_feature("|".join(tags_list))

def get_trending(region, category):
    youtube = get_youtube_api()

    # https://developers.google.com/youtube/v3/docs/videos/list?hl=ko
    response = youtube.videos().list(
        part='id,snippet,statistics,contentDetails',
        chart='mostPopular',
        regionCode=region,
        videoCategoryId=category,
        maxResults=50
    ).execute()
    result = response['items']
    return result

def get_videos(items):
    rank = 0
    result = []
    for item in items:
        rank += 1
        video_id = item.get('id')
        result_dict = {'rank':rank,'video_id':video_id}

        snippet = item.get('snippet')
        snippet = {key: prepare_feature(snippet.get(key, "")) if key in snippet_features else snippet.get(key, "") for
                   key in snippet.keys()}
        snippet['thumbnails'] = snippet['thumbnails'].get('default').get('url')
        snippet['tags'] = get_tags(snippet.get("tags", [""]))
        result_dict.update(snippet)

        contentDetails = item.get('contentDetails')
        video_length = {'video_length': contentDetails.get("duration")}
        result_dict.update(video_length)

        statistics = item.get('statistics')
        result_dict.update(statistics)

        del result_dict['localized']

        result.append(result_dict)

    result_df = pd.DataFrame(result)

    return result_df

def get_channel_stats(channels):
    youtube = get_youtube_api()

    channel_lists = [channels[i:i+50] for i in range(0, len(channels), 50)]
    total_result = pd.DataFrame()
    for channel_list_of_list in channel_lists:
        # https://developers.google.com/youtube/v3/docs/videos/list?hl=ko
        response = youtube.channels().list(
            part='id,snippet,statistics',
            id=','.join(channel_list_of_list)
        ).execute()

        items = response.get('items')
        result = []
        for item in items:
            channel_id = item.get('id')
            result_dict = {'channelId':channel_id}
            snippet = item.get('snippet')
            result_dict.update(snippet)
            statistics = item.get('statistics')
            result_dict.update(statistics)

            result_dict['thumbnails'] = result_dict['thumbnails'].get('default').get('url')
            del result_dict['localized']
            result.append(result_dict)
        result_df = pd.DataFrame(result)
        total_result = total_result.append(result_df)

    return total_result

def main(region):
    trending_date = time.strftime("%Y-%m-%d")
    channel_list = []
    for c_id, category in category_dict.items():
        try:
            trending = get_trending(region, c_id)
        except:
            trending = None
        if trending:
            trending_video = get_videos(trending)

            channels = trending_video['channelId'].unique()
            channel_list.extend(channels)

            trending_video.to_csv(f'gs://{OUTPUT_BUCKET}/{region}/{trending_date}/{category}_trending.csv',index=False)
    try:
        channels = get_channel_stats(list(set(channel_list)))
        channels.to_csv(f'gs://{OUTPUT_BUCKET}/{region}/{trending_date}/channels.csv',index=False)
    except:
        pass

if __name__ == '__main__':
    main('KR')