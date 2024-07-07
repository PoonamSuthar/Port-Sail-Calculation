WITH voyage_events AS (
    SELECT
        id,
        event,
        DATEADD(day, dateStamp - 43831, '1900-01-01') + timeStamp AS utc_datetime,
        voyage_From,
        lat,
        lon,
        LEAD(event) OVER (PARTITION BY voyage_Id ORDER BY utc_datetime) AS next_event,
        LEAD(DATEADD(day, dateStamp - 43831, '1900-01-01') + timeStamp) OVER (PARTITION BY voyage_Id ORDER BY utc_datetime) AS next_utc_datetime,
        LEAD(lat) OVER (PARTITION BY voyage_Id ORDER BY utc_datetime) AS next_lat,
        LEAD(lon) OVER (PARTITION BY voyage_Id ORDER BY utc_datetime) AS next_lon,
        voyage_Id
    FROM voyages
    WHERE allocatedVoyageId IS NULL AND imo_num = '9434761' AND voyage_Id = '6'
)
SELECT
    id,
    event,
    utc_datetime,
    voyage_From,
    lat,
    lon,
    next_event,
    next_utc_datetime,
    voyage_Id,
    DATEDIFF(second, utc_datetime, next_utc_datetime) / 3600.0 AS duration_hours,
    GEOGRAPHY::Point(lat, lon).STDistance(GEOGRAPHY::Point(next_lat, next_lon)) / 1852 AS distance_nautical_miles
FROM voyage_events
WHERE event = 'SOSP' AND next_event = 'EOSP';
