-- Active: 1744916696249@@localhost@5432@uae_properties
-- ALL_CITIES 
SELECT DISTINCT "city"
FROM uae_properties;


-- name: MEDIAN_rent_PER_city
WITH MEDIAN_rent_PER_city AS (
    SELECT 
        "city", 
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "rent") AS "median_annual_rent"
    FROM uae_properties
    GROUP BY "city"
)
SELECT 
    "city", 
    "median_annual_rent" as "median_annual_rent",
    ROUND(("median_annual_rent" / 12)::numeric, 2) AS "median_monthly_rent",
    RANK() OVER (ORDER BY "median_annual_rent" DESC) AS Rank
FROM MEDIAN_rent_PER_city;




-- name: TOP_20_MOST_EXPENSIVE_lOCATIONS
WITH EXPENSIVE_lOCATION_PER_city as (
    SELECT
        "city",
        "location",
        "address",
        "rent" as "annual_rent"
    FROM uae_properties
    GROUP BY "city", "location",  "address", "annual_rent"
)
SELECT 
    "city",
    "location",
     "address",
    "annual_rent"
FROM EXPENSIVE_lOCATION_PER_city
ORDER BY "annual_rent" DESC
LIMIT 20;



-- name: MOST_AFFORDABLE_lOCATIONS
WITH AFFORDABLE_lOCATION_PER_city as (
    SELECT
        "city",
        "location",
        "address",
        "rent" as "annual_rent"
    FROM uae_properties
    GROUP BY "city", "location", "address", "annual_rent"
)
SELECT 
    "city",
    "location",
    "address",
    "annual_rent"
FROM AFFORDABLE_lOCATION_PER_city
ORDER BY "annual_rent" ASC;



-- name: AVERAGE_AREA_BY_PROPERTY_type
WITH AVERAGE_AREA_BY_type AS (
    SELECT 
        "city",
        "type",
        ROUND(AVG("area_in_sqft"), 3) AS average_area_in_sqrft
    FROM uae_properties
    GROUP BY "city", "type"
),
AVERAGE_BEDROOMS_BY_type AS (
    SELECT 
        "city",
        "type",
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "beds") AS median_beds_number
    FROM uae_properties
    WHERE "type" NOT IN ('Residential Plot') AND "beds" <> 0
    GROUP BY "city", "type"
)
SELECT
    a."city",
    a."type",
    a."average_area_in_sqrft",
    b."median_beds_number"
FROM AVERAGE_AREA_BY_type a
JOIN AVERAGE_BEDROOMS_BY_type b 
    ON a."type" = b."type"
    AND a."city" = b."city"
ORDER BY a."city", a."type", a."average_area_in_sqrft" DESC
LIMIT 20;


-- name: MOST_EXPENSIVE_lOCATIONS_BY_city 
WITH MOST_EXPENSIVE_lOCATION AS (
    SELECT 
        "city",
        "location",
        ROUND(AVG("rent"), 2) AS average_rent,
        ROW_NUMBER() OVER (
            PARTITION BY "city"
            ORDER BY AVG("rent") DESC
        ) AS row_number
    FROM uae_properties
    GROUP BY "city", "location"
)
SELECT 
    "city",
    "location",
    average_rent
FROM MOST_EXPENSIVE_lOCATION
WHERE row_number = 1
ORDER BY "city" ASC;



-- name: MOST_AFFORDABLE_lOCATIONS_BY_city
WITH MOST_AFFORDABLE_lOCATION AS (
    SELECT 
        "city",
        "location",
        ROUND(AVG("rent"), 2) AS "average_annual_rent",
        ROW_NUMBER() OVER (
            PARTITION BY "city"
            ORDER BY AVG("rent") ASC
        ) AS row_number
    FROM uae_properties
    GROUP BY "city", "location"
)
SELECT 
    "city",
    "location",
    "average_annual_rent"
FROM MOST_AFFORDABLE_lOCATION
WHERE row_number = 1
ORDER BY "city" ASC;



