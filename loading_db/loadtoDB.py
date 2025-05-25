import os
import logging
import pandas as pd

import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine

from dotenv import load_dotenv

from urllib.parse import quote_plus

# Dynamically get the root directory of the project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




logging.basicConfig(
    level=logging.INFO,  # Set the minimum log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    # filename='app.log'  # Log to a file (optional)
)

load_dotenv()



class Database:
    def __init__(self, file_path=os.path.join(PROJECT_ROOT, "dataset", "cleaned_data/cleaned_uae_properties_data.csv")):
        self.user = os.getenv('DB_USER')
        self.password = quote_plus(os.getenv('DB_PASSWORD'))
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.dbname = "uae_properties"
        self.connection_url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        self.target_dataset = pd.read_csv(file_path)


    def create_database(self):
        # CHECK TO ESTABLISH CONNECTION TO THE DB
        try:
            conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host, port=self.port)
            conn.autocommit = True  # To allow database creation
            cur = conn.cursor()
            logging.info("Connection established successfully")
        except Exception as e:
            logging.error(f"Failed to establish connection to the db, {e}")

        # CHECK WHETHER THE DB EXISTS
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.dbname,))
        exists = cur.fetchone()

        # CREATE THE DB IF IT DOESNT EXIST
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.dbname)))
            logging.info(f"Database '{self.dbname}' created successfully.")
        else:
            logging.info(f"Database '{self.dbname}' already exists.")


        # CLOSING THE CONNECTION
        cur.close()
        conn.close()
        logging.info("Connection closed.")


    def create_engine(self):
        try:
            
            engine = create_engine(self.connection_url)
            logging.info("PostgreSQL engine created.")
            return engine
        except Exception as e:
            logging.error("Failed to create PostgreSQL engine", exc_info=True)
            raise 


    def load_to_db(self):
        engine = self.create_engine()
        try:
            # Load to PostgreSQL (if table exists, replace or append)
            self.target_dataset.to_sql("uae_properties", engine, index=False, if_exists='replace')  # or 'append'
            logging.info("Data loaded to the database successfully ")
        except Exception as e:
            logging.error(f"Failed to load the data to PostgreSQL, {e}")
            

    def get_connection(self):
        return psycopg2.connect(
        host=os.getenv(self.host),
        database=os.getenv(self.dbname),
        user=os.getenv(self.user),
        password=os.getenv(self.password),
        port=os.getenv(self.port, 5432)
    )
