import pandas as pd
import numpy as np
import re
import logging




logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)



class UAEInfo:
    
    @staticmethod
    def uae_cities():
        return [
        "Dubai",
        "Abu Dhabi",
        "Sharjah",
        "Al Ain",
        "Ajman",
        "Ras Al Khaimah",
        "Fujairah",
        "Umm Al Quwain",
        "Kalba",
        "Dibba Al-Fujairah",
        "Madinat Zayed",
        "Khor Fakkan",
        "Al Dhannah",
        "Ghayathi",
        "Dhaid",
        "Jebel Ali",
        "Liwa Oasis",
        "Hatta",
        "Ar-Rams",
        "Dibba Al-Hisn",
        "Al Jazirah Al Hamra",
        "Al Mirfa",
        "Masfut",
        "Masafi",
        "Al Madam",
        "Al Manama",
        "Al Khawaneej",
        "Al Awir",
        "Al Faqa",
        "Al Lisaili",
        "Sweihan",
        "Dalma",
        "Falaj Al Mualla",
        "Sila",
        "Al Badiyah",
        "Al Jeer",
        "Al Hamriyah",
        "Al Ajban",
        "Al Yahar",
        "Al Bataeh",
        "Al Ruwayyah",
        "Al Nakhil",
        "Al Nuaimia",
        "Al Gharbia",
        "Al Aryam",
        "Al Qusaidat",
        "Al Qor",
        "Al Salamah",
        "Al Shuwaib",
        "Al Rafaah",
        "Al Rashidya",
        "Asimah",
        "Dadna",
        "Digdaga",
        "Ghalilah",
        "Ghayl",
        "Ghub",
        "Habshan",
        "Huwaylat",
        "Khatt",
        "Khor Khwair",
        "Lahbab",
        "Manama",
        "Marawah",
        "Mirbah",
        "Mleiha",
        "Nahil",
        "Qidfa",
        "Sha'am",
        "Wadi Shah",
        "Zubarah"
    ]




class DataCleaner:
    def __init__(self, raw_data: pd.DataFrame):
        self.raw_data = raw_data
        self.df = None

    def read_raw_data(self):
        try:
            self.df = pd.read_csv(self.raw_data, encoding="ISO-8859-1", engine='python')
            logging.info("Read the dataset successfully.")
            return pd.DataFrame(self.df)
        except FileNotFoundError:
            logging.error("Error: The file was not found.")
        except pd.errors.EmptyDataError:
            logging.error("Error: The file is empty.")
        except pd.errors.ParserError:
            logging.error("Error: The file could not be parsed.")

    
    




    def numeric_columns(self):
        try:
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            logging.info(f"Found the numerical values: {numeric_cols}")
            return numeric_cols
        except Exception as e:
            logging.warning(f"Failed to get some numerical columns, {e}")


    def object_columns(self):
        try:
            object_cols = self.df.select_dtypes(include=['object']).columns
            logging.info(f"Found the object(string + date) values: {object_cols}")
        except Exception as e:
            logging.warning(f"Failed to get some object(string + date) columns, {e}")


    def date_columns(self):
        try:
            date_cols = self.df.select_dtypes(include=['datetime']).columns
            logging.info(f"Found the object date values: {date_cols}")
        except Exception as e:
            logging.warning(f"Failed to get some object date columns, {e}")


    def convert_to_date_type(self):
        try:
            self.df['Posted_date'] = pd.to_datetime(self.df['Posted_date'], errors='coerce')
            logging.info("Successfully converted 'Posted_date' to datetime.")
        except Exception as e:
            logging.warning(f"Failed to convert 'Posted_date' to datetime type: {e}")

    
    

    """
    # USING IQR METHOD
    def outlier_detection(self, column):
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            logging.warning(f"Column '{column}' is not numeric. Skipping outlier detection.")
            return pd.DataFrame()

        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1

        outliers = self.df[
            (self.df[column] < Q1 - 1.5 * IQR) |
            (self.df[column] > Q3 + 1.5 * IQR)
        ]
        percentage = (len(outliers) / len(self.df)) * 100
        logging.info(f"{percentage:.2f}% of the values in column '{column}' are outliers.")
        return outliers
    """
    
    

    """
    Only Latitude and Longitude column contain missing values
    """
    def impute_missing_values(self):
        try:
            self.df["Latitude"].fillna(0, inplace=True)
            self.df["Longitude"].fillna(0, inplace=True)
            logging.info("Imputed missing values in Longitude and Latitude with 0")
        except Exception as e:
            logging.warning(f"Failed to impute missing values, {e}")



    """
    DROP ROWS WHERE RENT VALUES ARE MISSING SINCE IT MAKES THE ANALYSIS USELESS
    """
    def drop_missing_rent_values(self):
        try:
            """
            A minimum threshold of 700 AED has been set for rent rates; 
            any record falling below this threshold is dropped.
            """
            self.df = self.df[self.df["Rent"].notnull() & (self.df["Rent"] > 700)]
            logging.info("Dropped rows with missing Rent values and below 700 AED.")
        except Exception as e:
            logging.warning(f"Failed to drop rows with missing Rent values. {e}")

    

    def drop_duplicate_rows(self):
        total_rows = self.df.shape[0]
        duplicate_rows = self.df.duplicated().sum()
        
        try:
            if duplicate_rows == 0:
                logging.info("No duplicate rows were found")
            else:
                self.df = self.df.drop_duplicates()
                removed_rows = total_rows - self.df.shape[0]
                logging.info(f"{removed_rows} rows were removed")
        except Exception as e:
            logging.error(f"Failed to drop duplicate rows, {e}")
            


    # SQL standard naming
    def convert_columns_to_lowercase(self):
        try:
            self.df.columns = self.df.columns.str.lower()
            logging.info("Columns names converted to lowercase")
        except Exception as e:
            logging.error(f"Failed to convert columns to lowercase, {e}")


    def clean_all(self):
        self.read_raw_data()
        self.remove_city_from_address()
        self.numeric_columns()
        self.object_columns()
        self.date_columns()
        self.convert_to_date_type()
        self.impute_missing_values()
        self.drop_missing_rent_values()
        self.drop_duplicate_rows()
        self.convert_columns_to_lowercase()
        return self.df
            

