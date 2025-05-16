-- Active: 1744916696249@@localhost@5432@uae_properties
-- ALL_CITIES 
SELECT DISTINCT "City"
FROM uae_properties;


-- name: MEDIAN_RENT_PER_CITY
WITH MEDIAN_RENT_PER_CITY AS (
    SELECT 
        "City", 
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "Rent") AS "median_annual_rent"
    FROM uae_properties
    GROUP BY "City"
)
SELECT 
    "City", 
    "median_annual_rent" as "median_annual_rent",
    ROUND(("median_annual_rent" / 12)::numeric, 2) AS "median_monthly_rent",
    RANK() OVER (ORDER BY "median_annual_rent" DESC) AS Rank
FROM MEDIAN_RENT_PER_CITY;




-- name: TOP_20_MOST_EXPENSIVE_LOCATIONS
WITH EXPENSIVE_LOCATION_PER_CITY as (
    SELECT
        "City",
        "Location",
        "Address",
        "Rent" as "annual_rent"
    FROM uae_properties
    GROUP BY "City", "Location",  "Address", "annual_rent"
)
SELECT 
    "City",
    "Location",
     "Address",
    "annual_rent"
FROM EXPENSIVE_LOCATION_PER_CITY
ORDER BY "annual_rent" DESC
LIMIT 20;



-- name: MOST_AFFORDABLE_LOCATIONS
WITH AFFORDABLE_LOCATION_PER_CITY as (
    SELECT
        "City",
        "Location",
        "Address",
        "Rent" as "annual_rent"
    FROM uae_properties
    GROUP BY "City", "Location", "Address", "annual_rent"
)
SELECT 
    "City",
    "Location",
    "Address",
    "annual_rent"
FROM AFFORDABLE_LOCATION_PER_CITY
ORDER BY "annual_rent" ASC;



-- name: AVERAGE_AREA_BY_PROPERTY_TYPE
WITH AVERAGE_AREA_BY_TYPE AS (
    SELECT 
        "City",
        "Type",
        ROUND(AVG("Area_in_sqft"), 3) AS average_area_in_sqrft
    FROM uae_properties
    GROUP BY "City", "Type"
),
AVERAGE_BEDROOMS_BY_TYPE AS (
    SELECT 
        "City",
        "Type",
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "Beds") AS median_beds_number
    FROM uae_properties
    WHERE "Type" NOT IN ('Residential Plot') AND "Beds" <> 0
    GROUP BY "City", "Type"
)
SELECT
    a."City",
    a."Type",
    a."average_area_in_sqrft",
    b."median_beds_number"
FROM AVERAGE_AREA_BY_TYPE a
JOIN AVERAGE_BEDROOMS_BY_TYPE b 
    ON a."Type" = b."Type"
    AND a."City" = b."City"
ORDER BY a."City", a."Type", a."average_area_in_sqrft" DESC
LIMIT 20;


-- name: MOST_EXPENSIVE_LOCATIONS_BY_CITY 
WITH MOST_EXPENSIVE_LOCATION AS (
    SELECT 
        "City",
        "Location",
        ROUND(AVG("Rent"), 2) AS average_rent,
        ROW_NUMBER() OVER (
            PARTITION BY "City"
            ORDER BY AVG("Rent") DESC
        ) AS row_number
    FROM uae_properties
    GROUP BY "City", "Location"
)
SELECT 
    "City",
    "Location",
    average_rent
FROM MOST_EXPENSIVE_LOCATION
WHERE row_number = 1
ORDER BY "City" ASC;



-- name: MOST_AFFORDABLE_LOCATIONS_BY_CITY
WITH MOST_AFFORDABLE_LOCATION AS (
    SELECT 
        "City",
        "Location",
        ROUND(AVG("Rent"), 2) AS "average_annual_rent",
        ROW_NUMBER() OVER (
            PARTITION BY "City"
            ORDER BY AVG("Rent") ASC
        ) AS row_number
    FROM uae_properties
    GROUP BY "City", "Location"
)
SELECT 
    "City",
    "Location",
    "average_annual_rent"
FROM MOST_AFFORDABLE_LOCATION
WHERE row_number = 1
ORDER BY "City" ASC;



