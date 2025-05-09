SELECT * FROM uae_properties;

-- AVAILABLE CITIES IN THE DATASET
SELECT DISTINCT "City"
FROM uae_properties;


-- AVERAGE RENT PER CITY (ANNUAL)
WITH AVERAGE_RENT_PER_CITY AS (
    SELECT 
        "City", 
        AVG("Rent") as "average_annual_rent"
    FROM uae_properties
    GROUP BY "City", "Address"
)
SELECT 
    "City", 
    ROUND("average_annual_rent", 2) as "average_annual_rent",
    RANK() OVER (ORDER BY "average_annual_rent" DESC) AS Rank
FROM AVERAGE_RENT_PER_CITY;




-- TOP 20 MOST EXPENSIVE LOCATIONS
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



-- TOP 20 MOST AFFORDABLE LOCATIONS
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


SELECT 
    "Area_in_sqft"
FROM uae_properties
WHERE "Beds" = 12;