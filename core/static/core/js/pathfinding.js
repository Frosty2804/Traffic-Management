import { GeoJSONPathFinder } from "geojson-path-finder";

// Create a simple GeoJSON road network (mockup for demonstration)
const geojson = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: {},
      geometry: {
        type: "LineString",
        coordinates: [
          [-74.006, 40.7128], // New York City
          [-73.9352, 40.73061], // Somewhere in NY
          [-73.7226, 41.0952], // Another point in NY
          [-71.0589, 42.3601], // Boston
        ],
      },
    },
  ],
};

// Create the map
const map = L.map("map").setView([42.3601, -71.0589], 7); // Center over Boston

// Add OpenStreetMap tile layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);

// Create an instance of GeoJSONPathFinder
const pathFinder = new GeoJSONPathFinder(geojson);

// Define start and end points
const start = [-74.006, 40.7128]; // Starting coordinates (New York City)
const end = [-71.0589, 42.3601]; // Ending coordinates (Boston)

// Find the path
const path = pathFinder.findPath(start, end);

// Log the result
console.log("Path found:", path);

// Visualize the path on the map
if (path) {
  const line = L.polyline(path, { color: "red" }).addTo(map);
  map.fitBounds(line.getBounds());
} else {
  console.log("No path found.");
}
