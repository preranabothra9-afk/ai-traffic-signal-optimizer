import LaneCard from "./components/LaneCard";
import "./index.css";
import { useEffect, useState } from "react";

function App() {
  const [systemState, setSystemState] = useState(null);
  useEffect(() => {
    const fetchState = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/state");
        const data = await res.json();
        setSystemState(data);
      } catch (err) {
        console.error("Failed to fetch backend state", err);
      }
    };

    fetchState(); 
    const interval = setInterval(fetchState, 1000);

    return () => clearInterval(interval);
    }, []);

 
    if (!systemState) {
      return <h2 style={{ textAlign: "center" }}>Loading traffic state...</h2>;
    }

    const { lanes, mode } = systemState;

  return (
    <div className="app">
      <h1 className="title">AI Traffic Signal Optimiser 🚦</h1>
      <h3 className="mode">Mode: {mode}</h3>

      {/* 🔴 ADD THIS BLOCK HERE */}
      {mode === "EMERGENCY" && (
        <div className="emergency-banner">
          🚨 EMERGENCY MODE ACTIVE
        </div>
      )}

      <div className="lane-grid">
        {Object.entries(lanes).map(([laneName, laneData]) => (
          <LaneCard
            key={laneName}
            name={laneName}
            count={laneData.count}
            signal={laneData.signal}
            greenTime={laneData.green_time}
          />
        ))}
      </div>
    </div>
  );

}

export default App;
