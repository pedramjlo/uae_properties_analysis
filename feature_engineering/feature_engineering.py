import pandas as pd
import re
import logging
from uae_info.uaeInfo import UAEInfo


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





class FeatureEngineering:
    def __init__(self, df: pd.DataFrame):
        self.df = df


    """
    City names from the Address column are extracted and added to a new column City
    """
    def create_city_column(self):
        column_name = "City"
        uae_cities = UAEInfo.uae_cities()
        if "Address" in self.df.columns:
            if column_name not in self.df.columns:
                try:
                    # Match city only if it appears after a comma at the end of the string
                    pattern = r",\s*(" + "|".join(map(re.escape, uae_cities)) + r")\s*$"
                    self.df[column_name] = self.df["Address"].str.extract(pattern, flags=re.IGNORECASE)
                    logging.info(f"Extracted city names to column {column_name}.")
                except Exception as e:
                    logging.error(f"Failed to extract city names: {e}")
            else:
                logging.warning(f"Column {column_name} already exists!")
        else:
            logging.error("Column 'Address' does not exist.")


    
    """
    After extracting the city name from the address column and adding it to the new City column,
    it's removed from Address 
    """
    def remove_city_from_address(self):
        uae_cities = UAEInfo.uae_cities()
        if "Address" in self.df.columns:
            for city in uae_cities:
                removing_pattern = fr",?\s*{city}\s*" 
                self.df["Address"] = self.df["Address"].str.replace(removing_pattern, '', regex=True)
            logging.info("City names removed from Address column")
        else:
            logging.error("The column 'Address' does not exist.")


    def run_feature_engineering(self):
        self.create_city_column()
        self.remove_city_from_address()
        return self.df