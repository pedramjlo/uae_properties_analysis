from data_cleaning.cleaner import DataCleaner



if __name__ == "__main__":
    raw_dataset = "/Users/pedramjalali/documents/data_analysis/uae_properties/raw_data/uae_properties.csv"

    cleaner = DataCleaner(raw_data=raw_dataset)
    cleaner.read_raw_data()