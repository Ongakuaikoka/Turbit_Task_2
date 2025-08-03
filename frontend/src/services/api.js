import axios from "axios";

const API_BASE = "http://localhost:8000";

export const fetchTurbineData = (params) => {
  return axios.get(`${API_BASE}/turbine-data`, { params });
};
