import pandas as pd
import numpy as np
import re
import logging


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
                    # Match city only if it appears after a comma at the end of the string
                    pattern = r",\s*(" + "|".join(map(re.escape, self.uae_cities)) + r")\s*$"
                    self.df[column_name] = self.df["Address"].str.extract(pattern, flags=re.IGNORECASE)
                    logging.info(f"Extracted city names to column {column_name}.")
                except Exception as e:
                    logging.error(f"Failed to extract city names: {e}")
            else:
                logging.error(f"Column {column_name} already exists!")
        else:
            logging.error("Column 'Address' does not exist.")

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


    def check_numeric_columns(self):
        try:
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            logging.info(f"Found the numerical values: {numeric_cols}")
        except Exception as e:
            logging.warning(f"Failed to get some numerical columns, {e}")


    def check_object_columns(self):
        try:
            obejct_cols = self.df.select_dtypes(include=['object']).columns
            logging.info(f"Found the object(string + date) values: {obejct_cols}")
        except Exception as e:
            logging.warning(f"Failed to get some object(string + date) columns, {e}")
