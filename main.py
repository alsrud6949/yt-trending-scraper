from init import youtube
import pandas as pd

def main(region):
    # https://developers.google.com/youtube/v3/docs/videos/list?hl=ko
    response = youtube.videos().list(
        part='id,snippet,statistics',
        chart='mostPopular',
        regionCode=region,
        maxResults=50
    ).execute()

    items = response.get('items')
    rank = 0
    result = []
    for item in items:
        rank += 1
        video_id = item.get('id')
        result_dict = {'rank':rank,'video_id':video_id}
        snippet = item.get('snippet')
        result_dict.update(snippet)
        statistics = item.get('statistics')
        result_dict.update(statistics)

        result_dict['thumbnails'] = result_dict['thumbnails'].get('default').get('url')
        del result_dict['localized']
        result.append(result_dict)

    result_df = pd.DataFrame(result)

    return result_df

if __name__ == '__main__':
    trending = main('KR')