SELECT
  event_type,
  COUNT(*) AS cnt
FROM curated_events
GROUP BY event_type;