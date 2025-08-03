import React, { useState } from "react";
import axios from "axios";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Label,
} from "recharts";
import { fetchTurbineData } from "../services/api";
import "./PowerCurve.css";

const API_BASE = "http://localhost:8000";

const PowerCurve = () => {
  const [turbine, setTurbine] = useState("Turbine1");
  const [fromTime, setFromTime] = useState("2016-01-01T00:00");
  const [toTime, setToTime] = useState("2016-01-02T00:00");
  const [data, setData] = useState([]);

  const fetchData = async () => {
    try {
      const res = await fetchTurbineData({ turbine_id: turbine, from_time: fromTime, to_time: toTime });
      const grouped = {};
      res.data.forEach((item) => {
        const wind = Math.round(item.Wind * 10) / 10;
        if (!grouped[wind]) {
          grouped[wind] = { totalPower: 0, count: 0 };
        }
        grouped[wind].totalPower += item.Leistung;
        grouped[wind].count += 1;
      });

      const averaged = Object.entries(grouped).map(([wind, stats]) => ({
        Wind: parseFloat(wind),
        Leistung: stats.count ? stats.totalPower / stats.count : 0,
      }));

      averaged.sort((a, b) => a.Wind - b.Wind);

      setData(averaged);

    } catch (err) {
      console.warn("Fetch failed:", err);
    }
  };

  return (
    <div className="container">
      <h1>Power Curve Viewer</h1>
      <div className="controls">
        <select value={turbine} onChange={(e) => setTurbine(e.target.value)}>
          <option value="Turbine1">Turbine 1</option>
          <option value="Turbine2">Turbine 2</option>
        </select>

        <input type="datetime-local" value={fromTime} onChange={(e) => setFromTime(e.target.value)} />
        <input type="datetime-local" value={toTime} onChange={(e) => setToTime(e.target.value)} />
        <button onClick={fetchData}>Load</button>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 30, right: 30, left: 20, bottom: 40 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="Wind"
            type="number"
            domain={['auto', 'auto']}
            tickFormatter={(value) => `${Math.round(value)}`}
            tick={{ fontSize: 12 }}
          >
            <Label value="Wind Speed (m/s)" offset={-10} position="insideBottom" />
          </XAxis>
          <YAxis 
            type="number"
            domain={[0, 'auto']}
            label={{ value: "Power (kW)", angle: -90, position: "insideLeft" }}
          />
          <Tooltip />
          <Line type="monotone" dataKey="Leistung" stroke="#8884d8" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PowerCurve;
