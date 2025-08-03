from fastapi import FastAPI, Query, HTTPException
from pymongo import MongoClient
from dateutil import parser
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

import os
import logging

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # (!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(level=logging.INFO)

# Mongo connection
client = MongoClient(
    f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}"
)
db = client[os.getenv("MONGO_DB")]
collection = db["turbine_data"]

@app.get("/turbine-data")
def get_turbine_data(
    turbine_id: str = Query(...),
    from_time: str = Query(None, description="Format: YYYY-MM-DDTHH:MM"),
    to_time: str = Query(None, description="Format: YYYY-MM-DDTHH:MM"),
):
    try:
        query = {"turbine_id": turbine_id}
        
        if from_time or to_time:
            query["timestamp"] = {}
            if from_time:
                query["timestamp"]["$gte"] = parser.parse(from_time)
            if to_time:
                query["timestamp"]["$lte"] = parser.parse(to_time)

        fields = {"_id": 0, "timestamp": 1, "Wind": 1, "Leistung": 1}
        data = list(collection.find(query, fields).limit(10000))

        return data

    except Exception as e:
        logging.error(f"Error querying turbine data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve data")
