const LaneCard = ({ name, count, signal, greenTime }) => {
  return (
    <div className={`lane-card ${signal === "green" ? "active" : ""}`}>

      <h3>{name} Lane</h3>

      <p><strong>Vehicles:</strong> {count}</p>

      <div className="signal">
        {signal === "green" ? (
            <span className="green-dot"></span>
        ) : (
            <span className="red-dot"></span>
        )}
      </div>


      {signal === "green" && (
        <p>Green Time: {greenTime}s</p>
       )}

    </div>
  );
};

export default LaneCard;
