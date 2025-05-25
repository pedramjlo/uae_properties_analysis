import os
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


logging.basicConfig(
    level=logging.INFO,  # Set the minimum log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    # filename='app.log'  # Log to a file (optional)
)



PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class AnalysisUtility:
    def __init__(self):
        self.parent_analysis_dir = "analysis"
        self.cities_analysis_parent_dir = "cities_analysis"


    """
    creating a parent directory for cities analysis exclusively
    where city-level analysis is done
    """
    def create_city_analysis_dir(self):
        analysis_dir = os.path.join(PROJECT_ROOT, self.parent_analysis_dir)
        create_dir_at = os.path.join(analysis_dir, self.cities_analysis_parent_dir)
        
        try:
            if not os.path.exists(self.cities_analysis_parent_dir):
                os.makedirs(create_dir_at, exist_ok=True)
                logging.info(f"the target dir {self.cities_analysis_parent_dir} was created.")
            else:
                logging.warning(f"the target dir {self.cities_analysis_parent_dir} already exists.")
        except Exception as e:
            logging.error(f"Failed to create {self.cities_analysis_parent_dir}; {e}")


    """
    creating directories named after each for more specific analysis inside teh parent city analysis directory
    """

    def create_every_city_dir(self, cities_list):
        cities_analysis_dir = os.path.join(PROJECT_ROOT, self.parent_analysis_dir, self.cities_analysis_parent_dir)
        for city_dir in cities_list:
            dir_path = os.path.join(cities_analysis_dir, city_dir)
            if os.path.isdir(dir_path):
                logging.warning(f"{dir_path} already exists!")
            else:
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"{dir_path} created.")





at = AnalysisUtility()
at.create_city_analysis_dir()
at.create_every_city_dir(cities_list=['london', 'paris', 'berlin'])