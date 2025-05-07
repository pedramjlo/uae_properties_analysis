from data_cleaning.cleaner import DataCleaner # data_cleaning is treated as a python package



if __name__ == "__main__":
    raw_dataset = "/Users/pedramjalali/documents/data_analysis/uae_properties/raw_data/uae_properties.csv"

    cleaner = DataCleaner(raw_data_path=raw_dataset)
    data = cleaner.read_raw_data()




    # cleaner.create_city_column()

    # print(data["City"].unique())

    print(data.describe)