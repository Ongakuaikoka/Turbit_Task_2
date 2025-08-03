
import pandas as pd
import os
import logging

from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URI = f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}"
DB_NAME = os.getenv("MONGO_DB")
COLLECTION_NAME = "turbine_data"

def load_and_clean_csv(path, turbine_id):
    df = pd.read_csv(path, delimiter=";", header=0)
    df = df.drop(index=0)

    df.columns = [col.strip().replace("\\ufeff", "") for col in df.columns]
    df.rename(columns={"Dat/Zeit": "timestamp"}, inplace=True)

    for col in df.columns:
        if col != "timestamp":
            try:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(",", ".")
                    .str.strip()
                )
                df[col] = pd.to_numeric(df[col], errors="coerce")
            except Exception as e:
                logger.warning(f"Skipping column '{col}' due to error: {e}")
                df.drop(columns=[col], inplace=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d.%m.%Y, %H:%M")
    df["turbine_id"] = turbine_id

    return df

def main():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        df1 = load_and_clean_csv("Turbine1.csv", "Turbine1")
        df2 = load_and_clean_csv("Turbine2.csv", "Turbine2")
        df = pd.concat([df1, df2], ignore_index=True)

        collection.drop()
        collection.insert_many(df.to_dict("records"))

        logger.info(f"Inserted {len(df)} records into '{COLLECTION_NAME}'")
    except Exception as e:
        logger.error("Error loading turbine data", exc_info=True)

if __name__ == "__main__":
    main()
