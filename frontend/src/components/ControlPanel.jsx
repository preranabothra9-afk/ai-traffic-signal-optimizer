import { useEffect, useState } from "react";
import { fetchSystemState } from "../services/api";

export default function ControlPanel() {
  const [stats, setStats] = useState({
    avgWait: 0,
    efficiency: 0,
    co2: 0,
    mode: "AUTO",
  });

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const state = await fetchSystemState();

        if (!state || !state.lanes) return;

        const lanes = Object.values(state.lanes);

        const counts = lanes.map((l) => l.count ?? 0);
        const greenLanes = lanes.filter(
          (l) => l.signal === "green"
        ).length;

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

  return (
    <div className="bg-gray-800 p-4 rounded-xl space-y-4">
      <h2 className="text-lg font-semibold">Optimization Stats</h2>

      <div>Avg Wait Time: <b>{stats.avgWait}s</b></div>
      <div>Efficiency: <b>{stats.efficiency}%</b></div>
      <div>CO₂ Reduction: <b>{stats.co2}%</b></div>

      <button className="w-full bg-green-500 py-2 rounded-lg font-semibold">
        {stats.mode} MODE
      </button>

      <button className="w-full bg-gray-600 py-2 rounded-lg">
        Manual Control
      </button>
    </div>
  );
}
