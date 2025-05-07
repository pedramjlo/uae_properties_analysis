from uae_info.uaeInfo import UAEInfo
import pandas as pd
import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

class DataCleaner:
    def __init__(self, raw_data_path):
        self.raw_data_path = raw_data_path
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
                    self.df[column_name] = self.df["Address"].str.extract([city for city in UAEInfo.uae_cities()])
                    logging.info(f"The new column {column_name} was created.")
                except Exception as e:
                    logging.error(e)
            else:
                logging.error(f"The column {column_name} already exists!")
        else:
            logging.error(f"The column {column_name} does not exist.")
