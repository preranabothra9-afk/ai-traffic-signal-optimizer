import { lanes } from "./data/DummyData.js";
import LaneCard from "./components/LaneCard";
import "./index.css";

function App() {
  return (
    <div className="app">
      <h1 className="title">AI Traffic Signal Optimiser 🚦</h1>

      <div className="lane-grid">
        {lanes.map((lane, index) => (
          <LaneCard key={index} {...lane} />
        ))}
      </div>
    </div>
  );
}

export default App;
