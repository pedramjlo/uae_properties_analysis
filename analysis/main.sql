SELECT * FROM uae_properties;

-- AVAILABLE CITIES IN THE DATASET
SELECT DISTINCT "City"
FROM uae_properties;


-- AVERAGE RENT PER CITY (PER MONTH)
WITH AVERAGE_RENT_PER_CITY AS (
    SELECT 
        "City", 
        AVG("Rent") as "Average_rent"
    FROM uae_properties
    GROUP BY "City"
)
SELECT 
    "City", 
    ROUND("Average_rent", 2),
    RANK() OVER (ORDER BY "Average_rent" DESC) AS Rank
FROM AVERAGE_RENT_PER_CITY;




-- TOP 20 MOST EXPENSIVE LOCATIONS
WITH EXPENSIVE_LOCATION_PER_CITY as (
    SELECT
        "City",
        "Location",
        MAX("Rent") as "Highest_Rent",
    FROM uae_properties
    GROUP BY "City", "Location"
)
SELECT 
    "City",
    "Location",
    "Highest_Rent"
FROM EXPENSIVE_LOCATION_PER_CITY
ORDER BY "Highest_Rent" DESC;


-- TOP 20 MOST AFFORDABLE LOCATIONS
WITH AFFORDABLE_LOCATION_PER_CITY as (
    SELECT
        "City",
        "Location",
        MIN("Rent") as "Lowest_Rent"
    FROM uae_properties
    GROUP BY "City", "Location"
)
SELECT 
    "City",
    "Location",
    "Lowest_Rent"
FROM AFFORDABLE_LOCATION_PER_CITY
ORDER BY "Lowest_Rent" ASC;

