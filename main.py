from data_cleaning.cleaner import DataCleaner # data_cleaning is treated as a python package
from uae_info.uaeInfo import UAEInfo 
from data_saving.dataSaver import DataSaver
from database_utils.databaseConfig import Database





if __name__ == "__main__":
    raw_dataset = "/Users/pedramjalali/documents/data_analysis/uae_properties/dataset/raw_data/uae_properties.csv"

    cleaner = DataCleaner(raw_data_path=raw_dataset, uae_cities=UAEInfo.uae_cities())
    data = cleaner.read_raw_data()



    # EXTRACT CITY NAME FROM ADDRESS COLUMN AND ADD IT TO THE NEW COLUMN CITY
    
    
    #print(data.describe)
    #print(data.columns)




    # DATA CLEANING
    cleaner.create_city_column() 
    cleaner.remove_city_from_address() 
    cleaner.numeric_columns()
    cleaner.object_columns()
    cleaner.date_columns()
    cleaner.convert_to_date_type()
    cleaner.impute_missing_values()
    cleaner.drop_missing_rent_values()
    cleaner.drop_duplicate_rows()
    cleaner.convert_columns_to_lowercase()


    
    


    # OUTLIER DETECTION
    """

    - Every numeric value column contains high-end and ignorable outliers meaning the distribution is 
    positively skewed. The majority of the data is clustered toward lower values, 
    with a few extremely high values pulling the upper end.

    - Outliers are not an issue in any case.

    """

    #for column in data.columns:
        #cleaner.outlier_detection(column)


    # SAVING THE NEW CLEANED DATASET TO 'dataset/cleaned_data/'
    saver = DataSaver()
    saver.save_clean_data(cleaner.df)


    # LOADING THE SAVED CLEANED DATA TO POSTGRESQL DB

    load_to_db = Database()
    load_to_db.create_database()
    load_to_db.create_engine()
    load_to_db.load_to_db()
