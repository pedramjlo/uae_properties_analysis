import pandas as pd
import numpy as np
import re
import logging
from geopy.geocoders import Nominatim


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

class DataCleaner:
    def __init__(self, raw_data_path, uae_cities):
        self.raw_data_path = raw_data_path
        self.uae_cities = uae_cities
        self.df = None

    def read_raw_data(self):
        try:
            self.df = pd.read_csv(self.raw_data_path, encoding="ISO-8859-1", engine='python')
            logging.info("Read the dataset successfully.")
            return self.df
        except FileNotFoundError:
            logging.error("Error: The file was not found.")
        except pd.errors.EmptyDataError:
            logging.error("Error: The file is empty.")
        except pd.errors.ParserError:
            logging.error("Error: The file could not be parsed.")

    
    """
    City names from the Address column are extracted and added to a new column City
    """
    def create_city_column(self):
        column_name = "City"
        if "Address" in self.df.columns:
            if column_name not in self.df.columns:
                try:
                    self.df[column_name] = self.df["Address"].str.extract([city for city in self.uae_cities])
                    logging.info(f"The new column {column_name} was created.")
                except Exception as e:
                    logging.error(e)
            else:
                logging.error(f"The column {column_name} already exists!")
        else:
            logging.error(f"The column {column_name} does not exist.")


    """
    After extracting the city name from the address column and adding it to the new City column,
    it's removed from Address 
    """
    def remove_city_from_address(self):
        if "Address" in self.df.columns:
            for city in self.uae_cities:
                removing_pattern = fr",?\s*{city}\s*" 
                self.df["Address"] = self.df["Address"].str.replace(removing_pattern, '', regex=True)
            logging.info("City names removed from Address column")
        else:
            logging.error("The column 'Address' does not exist.")


    def convert_string_values(self):
        string_columns = ['Address', 'City', 'Type', 'Rent_per_sqft', 'Frequency', 'Furnishing', 'Purpose', 'Location']
        try:
            self.df[string_columns] = self.df[string_columns].astype(str)
            logging.info("Successfully converted specified columns to string type")
        except Exception as e:
            logging.error(f"Failed to convert some columns into strings: {e}")
        return self.df


    def convert_to_integer(self):
        try:
            numeric_cols = ['Rent', 'Beds',	'Baths', ]
            self.df[numeric_cols] = self.df[numeric_cols].apply(pd.to_numeric, errors='coerce').astype('Int64')
            logging.info("Successfully converted specified columns to integer type")
        except Exception as e:
            logging.error(f"Failed to convert some columns into integers: {e}")
        return self.df

