import json
import boto3
import requests
import datetime
from collections import OrderedDict

s3 = boto3.client('s3')

def lambda_handler(event, context):
    YOUTUBE_API_KEY = " "
    SEARCH_QUERY = "Trending"
    MAX_RESULTS = 10
    BUCKET_NAME = "hridya-api-data-bucket"

    print("Lambda execution started...")

    try:
        # Step 1: Fetch video IDs from YouTube search
        print("Calling YouTube Search API...")
        search_url = (
            f"https://www.googleapis.com/youtube/v3/search"
            f"?part=snippet&type=video&q={SEARCH_QUERY}&maxResults={MAX_RESULTS}&key={YOUTUBE_API_KEY}"
        )
        search_response = requests.get(search_url)
        search_response.raise_for_status()
        search_data = search_response.json()

        video_ids = [item["id"]["videoId"] for item in search_data["items"]]
        print(f"Fetched {len(video_ids)} video IDs: {video_ids}")

        if not video_ids:
            print("No videos found from YouTube search. Exiting Lambda.")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No videos found to process.'})
            }

        # Step 2: Fetch detailed video stats
        video_ids_str = ",".join(video_ids)
        videos_url = (
            f"https://www.googleapis.com/youtube/v3/videos"
            f"?part=snippet,statistics&id={video_ids_str}&key={YOUTUBE_API_KEY}"
        )
        print("Calling YouTube Videos API...")
        videos_response = requests.get(videos_url)
        videos_response.raise_for_status()
        videos_data = videos_response.json()
        print(f"Fetched details for {len(videos_data.get('items', []))} videos.")

        # Step 3: Reorganize data
        ordered_items = []
        for item in videos_data.get("items", []):
            snippet = item.get("snippet", {})
            statistics = item.get("statistics", {})
            thumbnails = snippet.get("thumbnails", {})
            localized = snippet.get("localized", {})

            ordered_item = OrderedDict([
                ("kind", item.get("kind")),
                ("etag", item.get("etag")),
                ("id", item.get("id")),
                ("snippet", OrderedDict([
                    ("publishedAt", snippet.get("publishedAt")),
                    ("channelId", snippet.get("channelId")),
                    ("title", snippet.get("title")),
                    ("description", snippet.get("description")),
                    ("thumbnails", OrderedDict([
                        ("default", thumbnails.get("default")),
                        ("medium", thumbnails.get("medium")),
                        ("high", thumbnails.get("high")),
                        ("standard", thumbnails.get("standard")),
                        ("maxres", thumbnails.get("maxres"))
                    ])),
                    ("channelTitle", snippet.get("channelTitle")),
                    ("categoryId", snippet.get("categoryId")),
                    ("liveBroadcastContent", snippet.get("liveBroadcastContent")),
                    ("defaultLanguage", snippet.get("defaultLanguage")),
                    ("localized", OrderedDict([
                        ("title", localized.get("title")),
                        ("description", localized.get("description"))
                    ])),
                    ("defaultAudioLanguage", snippet.get("defaultAudioLanguage")),
                    ("tags", snippet.get("tags"))
                ])),
                ("statistics", OrderedDict([
                    ("viewCount", statistics.get("viewCount")),
                    ("likeCount", statistics.get("likeCount")),
                    ("favoriteCount", statistics.get("favoriteCount")),
                    ("commentCount", statistics.get("commentCount"))
                ]))
            ])
            ordered_items.append(ordered_item)

        final_data = OrderedDict([
            ("kind", videos_data.get("kind")),
            ("etag", videos_data.get("etag")),
            ("items", ordered_items),
            ("pageInfo", videos_data.get("pageInfo"))
        ])

        # Step 4: Save to S3
        now = datetime.datetime.utcnow()
        s3_key = (
            f"raw-data/year={now.year}/month={now.month:02d}/"
            f"day={now.day:02d}/hour={now.hour:02d}/youtube_trending_stats_{now.strftime('%Y-%m-%dT%H-%M-%SZ')}.json"
        )
        print(f"Uploading data to S3: s3://{BUCKET_NAME}/{s3_key}")
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(final_data),
            ContentType='application/json'
        )
        print("Upload successful.")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f"Trending video stats saved to S3 as {s3_key}",
                'bucket': BUCKET_NAME
            })
        }

    except Exception as e:
        print(f"ERROR: Lambda failed with exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

