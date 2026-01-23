export default function LiveIntersection() {
  return (
    <div className="bg-gray-800 p-4 rounded-xl">
      <h2 className="text-lg mb-2">Live Intersection</h2>

      <img
        src="http://127.0.0.1:5000/video"
        alt="Live Traffic"
        className="w-full h-72 rounded-lg object-cover"
      />
    </div>
  );
}
