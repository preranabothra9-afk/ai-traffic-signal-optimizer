import "./LaneCard.css";

function LaneCard({ name, count, signal, greenTime }) {
  return (
    <div className={`lane-card ${signal}`}>
      <h2>{name.toUpperCase()}</h2>

      <div className="signal">
        {signal === "green" ? "🟢 GREEN" : "🔴 RED"}
      </div>

      <p>Vehicles: <b>{count}</b></p>

      {signal === "green" && (
        <p>Green Time: <b>{greenTime}s</b></p>
      )}
    </div>
  );
}

export default LaneCard;
