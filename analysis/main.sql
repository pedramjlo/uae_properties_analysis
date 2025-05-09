SELECT * FROM uae_properties;

-- AVAILABLE CITIES IN THE DATASET
SELECT DISTINCT "City"
FROM uae_properties;


-- MEDIAN RENT PER CITY (ANNUAL & MONTHLY)
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




-- TOP 20 MOST EXPENSIVE LOCATIONS (ACCROSS THE COUNTRY)
WITH EXPENSIVE_LOCATION_PER_CITY as (
    SELECT
        "City",
        "Location",
        "Address",
        MAX("Rent") as "highest_annual_rent"
    FROM uae_properties
    GROUP BY "City", "Location",  "Address"
)
SELECT 
    "City",
    "Location",
     "Address",
    "highest_annual_rent"
FROM EXPENSIVE_LOCATION_PER_CITY
ORDER BY "highest_annual_rent" DESC
LIMIT 20;



-- TOP 20 MOST AFFORDABLE LOCATIONS (ACCROSS THE COUNTRY)
WITH AFFORDABLE_LOCATION_PER_CITY as (
    SELECT
        "City",
        "Location",
        "Address",
        MIN("Rent") as "lowest_annual_rent"
    FROM uae_properties
    GROUP BY "City", "Location", "Address"
)
SELECT 
    "City",
    "Location",
    "Address",
    "lowest_annual_rent"
FROM AFFORDABLE_LOCATION_PER_CITY
ORDER BY "lowest_annual_rent" ASC;


-- AVERAGE AREA BY PROPERTY TYPE IN SQUAREFEET UNIT AND THE NUMBER OF BEDROOMS
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
ORDER BY a."City", a."Type", a."average_area_in_sqrft" DESC;


-- MOST EXPENSIVE LOCATION IN EVERY CITY (ON AVERAGE RENT RATE)
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



-- MOST AFFORDABLE LOCATION IN EVERY CITY (ON AVERAGE RENT RATE)
WITH MOST_AFFORDABLE_LOCATION AS (
    SELECT 
        "City",
        "Location",
        ROUND(AVG("Rent"), 2) AS average_rent,
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
    average_rent
FROM MOST_AFFORDABLE_LOCATION
WHERE row_number = 1
ORDER BY "City" ASC;
