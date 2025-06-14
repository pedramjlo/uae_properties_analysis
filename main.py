import pandas as pd

from data_cleaning.cleaner import DataCleaner # data_cleaning is treated as a python package
from data_saving.dataSaver import DataSaver
from database_utils.databaseConfig import Database
from feature_engineering.feature_engineering import FeatureEngineering



class Pipeline:
    def __init__(self, raw_data: pd.DataFrame):
        self.raw_data = raw_data
        self.cleaned_data = None

    def data_cleaner(self):
        cleaner = DataCleaner(raw_data=self.raw_data)
        self.cleaned_data = cleaner.clean_all()


    def feature_engineering(self):
        fe = FeatureEngineering(df=self.cleaned_data)
        fe.run_feature_engineering


    def data_saver(self):
        saver = DataSaver()
        saver.save_clean_data(df=self.cleaned_data)


    def load_data_to_db(self):
        db = Database()
        db.run_db()

    



if __name__ == "__main__":
    raw_dataset = "/Users/pedramjalali/documents/data_analysis/uae_properties/dataset/raw_data/uae_properties.csv"

    pl = Pipeline(raw_data=raw_dataset)
    pl.data_cleaner()
    pl.data_saver()
    pl.load_data_to_db()




    
    




    
