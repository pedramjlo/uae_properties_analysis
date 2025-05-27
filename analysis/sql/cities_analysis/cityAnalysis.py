import os
import sys
import pandas as pd
from sqlalchemy import Column, Integer, String, Float, func
from sqlalchemy.orm import declarative_base, sessionmaker

# Allow relative import of your custom Database class
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from loading_db.loadtoDB import Database

# Define ORM base
Base = declarative_base()

# Database connection
db = Database()
engine = db.create_engine()

# Define the ORM model
class UAEProperties(Base):
    __tablename__ = "uae_properties"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    rent = Column(Float)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

def get_average_rent_per_city():
    """Query average rent per city and return as DataFrame."""
    try:
        query = (
            session.query(UAEProperties.city, func.avg(UAEProperties.rent).label("avg_rent"))
            .group_by(UAEProperties.city)
        )
        results = query.all()
        df = pd.DataFrame(results, columns=["city", "avg_rent"])
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Run the query and display the DataFrame
    df = get_average_rent_per_city()
    print(df)

    # Close session
    session.close()
