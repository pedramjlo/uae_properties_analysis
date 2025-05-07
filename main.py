from data_cleaning.cleaner import DataCleaner # data_cleaning is treated as a python package
from uae_info.uaeInfo import UAEInfo 



if __name__ == "__main__":
    raw_dataset = "/Users/pedramjalali/documents/data_analysis/uae_properties/raw_data/uae_properties.csv"

    cleaner = DataCleaner(raw_data_path=raw_dataset, uae_cities=UAEInfo.uae_cities())
    data = cleaner.read_raw_data()




    cleaner.create_city_column() # creates the city column and add the extracted city from the address column
    cleaner.remove_city_from_address() # removes the city name from the address column 
    #cleaner.find_missing_latitude()
    
    #print(data.describe)
    #print(data.columns)


    cleaner.convert_string_values()
    cleaner.convert_to_integer()
    cleaner.convert_to_float()
    cleaner.convert_to_date()

    print(data.describe)
    


    """
    - both latitude and longitude columns contain 719 out of 73742 against None for every other column
    - 
    """
    # print(data.shape[0])
