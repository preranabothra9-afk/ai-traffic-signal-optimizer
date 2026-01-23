import Header from "./components/Header";
import LeftPanel from "./components/LeftPanel";
import LiveIntersection from "./components/LiveIntersection";
import ControlPanel from "./components/ControlPanel";
import TrafficGraph from "./components/TrafficGraph";

export default function App() {
  return (
    <div className="min-h-screen p-4">
      <Header />

      <div className="grid grid-cols-12 gap-4 mt-4">
        <div className="col-span-3">
          <LeftPanel />
        </div>

        <div className="col-span-6">
          <LiveIntersection />
        </div>

        <div className="col-span-3">
          <ControlPanel />
        </div>
      </div>

      <div className="mt-6">
        <TrafficGraph />
      </div>
    </div>
  );
}
