import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the minimum log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    # filename='app.log'  # Log to a file (optional)
)




class DataCleaner:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        

    def read_raw_data(self):
        try:
            logging.info("read the dataset successfully")
            return pd.read_csv(self.raw_data, encoding="ISO-8859-1", engine='python')
        except FileNotFoundError:
            logging.error("Error: The file was not found.")
        except pd.errors.EmptyDataError:
            logging.error("Error: The file is empty.")
        except pd.errors.ParserError:
            logging.error("Error: The file could not be parsed.")






