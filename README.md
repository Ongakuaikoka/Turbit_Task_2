This project ingests and visualizes turbine data using a containerized full-stack setup.

What It Does

- Load CSV time series data (Turbine1 & Turbine2) into MongoDB
- FastAPI backend with queryable endpoint:
  - Filter by `turbine_id` and `timestamp` range
- React frontend with:
  - Power curve plot (Power vs Wind Speed)
  - Adjustable time range selection
  - Turbine dropdown
- Full Docker support (MongoDB, FastAPI, React)
---

Quick Start

1. Clone the Repo
  `git clone https://github.com/Ongakuaikoka/Turbit_Task_2.git`
  `cd Turbit_Task_2`

2. Start the services
  `docker-compose up --build`

3. Load Data into MongoDB
   `docker-compose exec fastapi_app python load_csv.py`

**API Endpoint**
GET /turbine-data

Query params:
turbine_id (e.g., Turbine1)
from_time (e.g., 2020-01-01T00:00)
to_time (optional)
