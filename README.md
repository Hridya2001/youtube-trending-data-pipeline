# YouTube Trending Video Analysis

## Overview
This project implements a data pipeline that fetches trending YouTube video statistics using the YouTube Data API. The data is then stored in an S3 bucket as a JSON file, and the AWS Glue Crawler scans the data to create a schema in AWS Glue. The schema is then queried using AWS Athena to retrieve specific statistics like the maximum like count of trending videos for specific days.


## Architecture
![Architecture](images/architecture.png)

## Components & Process

- Data Source: The data is sourced from the [YouTube Data API v3](https://developers.google.com/youtube/v3), specifically from the Search endpoint and the videos endpoint, using a developer API key. The pipeline queries trending video metadata and statistics such as title, channel name, like count, and more.

     API Endpoint Base URL: `https://www.googleapis.com/youtube/v3`

     API_KEY: AIzaSyDjio9u6s6C-Ob3Ox2q77fANRhXZNnSokY

- EventBridge Rule: Triggers the Lambda function every hour to fetch the latest trending videos from YouTube.


- AWS Lambda: Fetches video statistics from the YouTube API (trending videos, likes, channel title, hash tags, published date etc.).
Saves the data as a nested JSON in S3.


- S3 Bucket: Stores the raw JSON data fetched by Lambda.
Organized by partition (year, month, day, hour).


- AWS Glue Crawler: Scans the S3 bucket and generates a schema.
Automatically creates a table in the Glue Catalog for querying via Athena.


- Athena Queries: SQL queries are run on the Glue Catalog data.
The data is queried in a partitioned way to get specific results, such as the video with the maximum like count for a particular day.


## Tools and Technologies 
1. Programming Language - Python
2. Scripting Language - SQL
3. AWS
   - Lambda
   - Event Bridge
   - S3
   - AWS Glue
   - Amazon Athena
   - IAM


## Code and Query
1. [lambda.py](codes-n-query/lambda.py)
   
This Lambda function fetches metadata and statistics of trending YouTube videos using the YouTube Data API v3. It first searches for the top 10 videos related to the keyword “Trending” and retrieves their video IDs. Then, it fetches detailed information for each video—such as title, channel name, view count, like count, and thumbnail URLs—and organizes the data into a structured JSON format. Finally, it stores this data in an S3 bucket using a time-based partitioned folder structure (year/month/day/hour) for easy querying with AWS Glue and Athena.
2. [athena.txt](codes-n-query/athena-sql-query)

This query retrieves the titles of trending YouTube videos along with their maximum like counts for a specific date (May 3, 2025). The data is filtered by partition keys (year, month, day) and handles nested JSON by unnesting the items array.


## Policies and IAM Permissions
Make sure to grant the following IAM roles and permissions:

1. Lambda Execution Role
To allow your Lambda function to:
Call the YouTube Data API (handled via requests, no IAM policy needed)
Write to S3

Policies added:
AmazonS3FullAccess

2. AWS Glue Crawler Role
To allow the Glue Crawler to:
Read from your S3 bucket
Write metadata to Glue Data Catalog

Policies added:
AmazonS3ReadOnlyAccess 
AWSGlueServiceRole

3. EventBridge Scheduler Execution Policy
Policy Name: Amazon-EventBridge-Scheduler-Execution-Policy-84bed0da-3e5b-47d6-a1a0-96e8a1091ac8
Purpose: Lets EventBridge invoke Lambda functions based on a schedule (every hour in your case).

Usually grants:
lambda:InvokeFunction
Trust relationship with scheduler.amazonaws.com

## Troubleshooting
Common Errors:
HIVE_PARTITION_SCHEMA_MISMATCH: This occurs when the Glue crawler cannot match the schema of partitioned data.

Solution: Re-run the Glue Crawler with updated partition fields.

Lambda Timeout: If the Lambda function times out, increase the timeout setting in the Lambda configuration.

Athena Errors: If the partitioning is mismatched, ensure that the partitions in your query match the S3 data and Glue schema.


## Conclusion
This project demonstrates a fully automated and serverless data pipeline that ingests real-time trending YouTube video statistics using the YouTube Data API, processes and stores it in Amazon S3, catalogs the data with AWS Glue, and enables powerful analytics using Amazon Athena.

By leveraging services like AWS Lambda (for data fetching), EventBridge (for scheduled execution), S3 (as a raw data lake), Glue Crawlers (for schema inference and cataloging), and Athena (for serverless querying), the pipeline ensures hourly data freshness with minimal manual intervention.

This setup is ideal for real-time analytics, trend monitoring, and building dashboards or ML pipelines downstream. The modular and scalable design makes it easy to extend with sentiment analysis, alerting systems, or data warehousing solutions like Redshift or Snowflake in the future.









