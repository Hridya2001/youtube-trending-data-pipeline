SELECT 
  item.snippet.title AS video_title,
  MAX(CAST(item.statistics.likeCount AS bigint)) AS max_like_count
FROM 
  youtube_database.trending_raw_data
CROSS JOIN UNNEST(items) AS t(item)
WHERE 
  year = '2025'
  AND month = '05'
  AND day = '03'
  AND item.statistics.likeCount IS NOT NULL
GROUP BY 
  item.snippet.title
ORDER BY 
  max_like_count DESC
LIMIT 24;
