from data_cleaning.cleaner import DataCleaner # data_cleaning is treated as a python package
from uae_info.uaeInfo import UAEInfo 

from data_visualiser.dataVisualiser import PlotCreator



if __name__ == "__main__":
    raw_dataset = "/Users/pedramjalali/documents/data_analysis/uae_properties/raw_data/uae_properties.csv"

    cleaner = DataCleaner(raw_data_path=raw_dataset, uae_cities=UAEInfo.uae_cities())
    data = cleaner.read_raw_data()



    # EXTRACT CITY NAME FROM ADDRESS COLUMN AND ADD IT TO THE NEW COLUMN CITY
    #cleaner.create_city_column() 
    #cleaner.remove_city_from_address() 
    
    #print(data.describe)
    #print(data.columns)



    #print(data.describe)

    # CHECK FOR DATA TYPES
    cleaner.numeric_columns()
    cleaner.object_columns()
    cleaner.date_columns()
    cleaner.convert_to_date_type()


    


    # OUTLIERS
    """

    - Every numeric value column contains high-end and ignorable outliers meaning the distribution is 
    positively skewed. The majority of the data is clustered toward lower values, 
    with a few extremely high values pulling the upper end.

    - Outliers are not an issue in any case.

    """

    #for column in data.columns:
        #cleaner.outlier_detection(column)



    

    