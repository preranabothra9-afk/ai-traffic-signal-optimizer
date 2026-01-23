import { useEffect, useState } from "react";
import { fetchSystemState } from "../services/api";

export default function ControlPanel() {
  const [stats, setStats] = useState({
    avgWait: 0,
    efficiency: 0,
    co2: 0,
    mode: "AUTO",
  });

  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const state = await fetchSystemState();

        if (!state || !state.lanes) return;

        const lanes = Object.values(state.lanes);
        const counts = lanes.map((l) => l.count ?? 0);
        const greenLanes = lanes.filter((l) => l.signal === "green").length;

        const avgWait =
          counts.reduce((a, b) => a + b, 0) / counts.length;

        const efficiency = Math.min(100, greenLanes * 25);
        const co2 = Math.min(50, Math.round(avgWait * 0.5));

        setStats({
          avgWait: Math.round(avgWait),
          efficiency,
          co2,
          mode: state.mode ?? "AUTO",
        });
      } catch (err) {
        console.error("ControlPanel error:", err);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, []);

  const sendEmergency = async (lane) => {
    try {
      await fetch("http://127.0.0.1:5000/emergency/detect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lane }),
      });
      setShowPopup(false);
    } catch {
      alert("Backend not reachable");
    }
  };

  const cancelEmergency = async () => {
    try {
      await fetch("http://127.0.0.1:5000/emergency/clear", {
        method: "POST",
      });
    } catch {
      alert("Backend not reachable");
    }
  };

  return (
    <div className="bg-gray-800 p-4 rounded-xl space-y-4">
      <h2 className="text-lg font-semibold">Optimization Stats</h2>

      <div>Avg Wait Time: <b>{stats.avgWait}s</b></div>
      <div>Efficiency: <b>{stats.efficiency}%</b></div>
      <div>CO₂ Reduction: <b>{stats.co2}%</b></div>

      <div className="space-y-2">
        <button className="w-full bg-green-500 py-2 rounded-lg font-semibold">
          {stats.mode} MODE
        </button>

        <button
          onClick={() => setShowPopup(true)}
          className="w-full bg-red-600 hover:bg-red-700 py-2 rounded-lg font-semibold text-white"
        >
          🚨 EMERGENCY
        </button>

        {stats.mode === "EMERGENCY" && (
          <button
            onClick={cancelEmergency}
            className="w-full bg-gray-600 hover:bg-gray-700 py-2 rounded-lg font-semibold text-white"
          >
            ❌ Cancel Emergency
          </button>
        )}
      </div>

      {showPopup && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
          <div className="bg-gray-900 p-6 rounded-xl space-y-4 w-72">
            <h3 className="text-lg font-bold text-center text-red-400">
              Select Emergency Direction
            </h3>

            <div className="grid grid-cols-2 gap-3">
              <button onClick={() => sendEmergency("north")} className="bg-red-600 py-2 rounded">North</button>
              <button onClick={() => sendEmergency("south")} className="bg-red-600 py-2 rounded">South</button>
              <button onClick={() => sendEmergency("east")} className="bg-red-600 py-2 rounded">East</button>
              <button onClick={() => sendEmergency("west")} className="bg-red-600 py-2 rounded">West</button>
            </div>

            <button
              onClick={() => setShowPopup(false)}
              className="w-full bg-gray-700 py-2 rounded"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
