const BASE_URL = "http://127.0.0.1:5000";

export async function fetchTrafficData() {
  const res = await fetch(`${BASE_URL}/state`);
  const data = await res.json();

  return Object.entries(data.lanes).map(([lane, info]) => ({
    lane: lane.charAt(0).toUpperCase() + lane.slice(1),
    vehicles: info.count,
    signal: info.signal.toUpperCase(),
    wait_time: info.green_time,
  }));
}

// ✅ ADD THIS FUNCTION
export async function fetchSystemState() {
  const res = await fetch(`${BASE_URL}/state`);
  if (!res.ok) throw new Error("Failed to fetch system state");
  return res.json();
}
