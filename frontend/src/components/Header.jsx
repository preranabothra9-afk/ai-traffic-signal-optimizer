export default function Header() {
  return (
    <div className="bg-gray-800 rounded-xl p-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold text-green-400">
        AI Traffic Signal Optimizer
      </h1>
      <span className="text-sm text-gray-300">
        Status: <span className="text-green-400">Live</span>
      </span>
    </div>
  );
}
