import { useEffect, useState } from "react";
import { fetchTrafficData } from "../services/api";

export default function LeftPanel() {
  const [lanes, setLanes] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      const data = await fetchTrafficData();
      setLanes(data);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-4">
      {lanes.map((lane) => (
        <div
          key={lane.lane}
          className="bg-gray-800 p-4 rounded-xl border-l-4"
        >
          <h2 className="text-lg font-semibold">{lane.lane} Lane</h2>
          <p>Vehicles: {lane.vehicles}</p>
          <p>Wait Time: {lane.wait_time}s</p>
          <p>Signal: {lane.signal}</p>
        </div>
      ))}
    </div>
  );
}
