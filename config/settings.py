import os

# Dynamically get the root directory of the project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path=os.path.join(PROJECT_ROOT, "cleaned_data", "cleaned_uae_properties_data.csv")