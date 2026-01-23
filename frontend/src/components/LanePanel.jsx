const lanes = [
  { name: "North", flow: "High", vehicles: 15, green: "10s", color: "green" },
  { name: "East", flow: "Moderate", vehicles: 8, green: "25s", color: "yellow" },
  { name: "South", flow: "Congested", vehicles: 22, green: "45s", color: "red" },
  { name: "West", flow: "Low", vehicles: 5, green: "15s", color: "blue" },
];

export default function LanePanel() {
  return (
    <div className="space-y-4">
      {lanes.map((lane) => (
        <div
          key={lane.name}
          className="bg-gray-800 rounded-xl p-4 border-l-4"
          style={{ borderColor: lane.color }}
        >
          <h2 className="text-lg font-semibold">{lane.name} Lane</h2>
          <p>Traffic Flow: <b>{lane.flow}</b></p>
          <p>Vehicles: {lane.vehicles}</p>
          <p>Green Time: {lane.wait}</p>
        </div>
      ))}
    </div>
  );
}
