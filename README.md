# YouTube Trending Video Analysis

## Overview
This project implements a data pipeline that fetches trending YouTube video statistics using the YouTube Data API. The data is then stored in an S3 bucket as a JSON file, and the AWS Glue Crawler scans the data to create a schema in AWS Glue. The schema is then queried using AWS Athena to retrieve specific statistics like the maximum like count of trending videos for specific days.


## Architecture
![Architecture](images/architecture.png)

## Components

###  Data Source
The data is sourced from the [YouTube Data API v3](https://developers.google.com/youtube/v3), specifically from the Search endpoint and the videos endpoint, using a developer API key. The pipeline queries trending video metadata and statistics such as title, channel name, like count, and more.

- API Endpoint Base URL: `https://www.googleapis.com/youtube/v3`

- API_KEY: AIzaSyDjio9u6s6C-Ob3Ox2q77fANRhXZNnSokY

### EventBridge Rule:
Triggers the Lambda function every hour to fetch the latest trending videos from YouTube.


### Lambda Function:
Fetches video statistics from the YouTube API (trending videos, likes, channel title, hash tags, published date etc.).
Saves the data as a nested JSON in S3.


### S3 Bucket:
Stores the raw JSON data fetched by Lambda.
Organized by partition (year, month, day, hour).


### AWS Glue Crawler:
Scans the S3 bucket and generates a schema.
Automatically creates a table in the Glue Catalog for querying via Athena.


### Athena Queries:
SQL queries are run on the Glue Catalog data.
The data is queried in a partitioned way to get specific results, such as the video with the maximum like count for a particular day.


## Tools and Technologies 
1. Programming Language - Python
2. Scripting Language - SQL
3. AWS
   - lambda
   - Event Bridge
   - S3
   - AWS Glue
   - Amazon Athena
   - IAM


## Code and Query
1. [lambda.py](codes-n-query/lambda.py)









