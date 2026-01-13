const LaneCard = ({ name, count, signal, greenTime }) => {
  return (
    <div className={`lane-card ${signal === "green" ? "active" : ""}`}>

      <h3>{name} Lane</h3>

      <p><strong>Vehicles:</strong> {count}</p>

      <div className="signal-box">
        <span className={`light red ${signal === "red" ? "on" : ""}`}></span>
        <span className={`light green ${signal === "green" ? "on" : ""}`}></span>
      </div>

      {signal === "green" && (
        <p className="green-time">Green Time: {greenTime}s</p>
      )}
    </div>
  );
};

export default LaneCard;
