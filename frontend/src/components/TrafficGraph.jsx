import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { useEffect, useState } from "react";
import { fetchTrafficData } from "../services/api";

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  Filler
);

const MAX_POINTS = 10;

export default function TrafficGraph() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      const lanes = await fetchTrafficData();

      setHistory((prev) => {
        const next = [...prev, lanes];
        return next.slice(-MAX_POINTS);
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const labels = history.map((_, i) => `${(MAX_POINTS - i)}s`);

  const laneColors = {
    North: "rgba(0, 200, 0, 1)",
    East: "rgba(255, 200, 0, 1)",
    South: "rgba(255, 0, 0, 1)",
    West: "rgba(0, 150, 255, 1)",
  };

  const datasets = ["North", "East", "South", "West"].map((lane) => ({
    label: `${lane} Lane`,
    data: history.map(
      (frame) => frame.find((l) => l.lane === lane)?.vehicles ?? 0
    ),
    borderColor: laneColors[lane],
    backgroundColor: laneColors[lane].replace("1)", "0.15)"),
    tension: 0.4,
    fill: true,
    pointRadius: 3,
  }));

  return (
    <div className="bg-gray-800 p-4 rounded-xl">
      <h2 className="text-lg font-semibold mb-2">Traffic Analysis (Live)</h2>
      <Line
        data={{ labels, datasets }}
        options={{
          responsive: true,
          animation: false,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Vehicle Count",
              },
            },
            x: {
              title: {
                display: true,
                text: "Time (seconds ago)",
              },
            },
          },
        }}
      />
    </div>
  );
}
