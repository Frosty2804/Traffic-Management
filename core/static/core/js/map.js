// Initialize the map centered over Goa
var map = L.map("map").setView([15.2993, 74.0377], 12); // Centered over Goa

// OpenStreetMap tile layer
var mapLink = "<a href='http://openstreetmap.org'>OpenStreetMap</a>";
L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
    attribution: "Leaflet &copy; " + mapLink + ", contributors",
    maxZoom: 18,
}).addTo(map);

// Coordinates for the routes
var routes = {};

// Populate the routes object and the route selector
const vehicles = [
    {% for vehicle in vehicles %}
    {
        id: "{{ vehicle.number_plate }}", // Using number_plate as ID
        start: [{{ vehicle.start_latitude }}, {{ vehicle.start_longitude }}],
        end: [{{ vehicle.stop_latitude }}, {{ vehicle.stop_longitude }}],
    },
    {% endfor %}
];

vehicles.forEach((vehicle, index) => {
    routes[vehicle.id] = {
        start: vehicle.start,
        end: vehicle.end,
    };

    // Populate route selector options
    var option = document.createElement("option");
    option.value = vehicle.id;
    option.textContent = vehicle.id; // Display number plate or any other identifier
    document.getElementById("routeSelector").appendChild(option);
});

// Initialize routing control
var control = L.Routing.control({
    waypoints: [],
    routeWhileDragging: true,
    router: L.Routing.osrmv1({
        serviceUrl: "https://router.project-osrm.org/route/v1", // Use OSRM service
    }),
}).addTo(map);

// Function to update the route based on selection
function updateRoute(selectedRoute) {
    var route = routes[selectedRoute];
    control.setWaypoints([
        L.latLng(route.start[0], route.start[1]), // Start point
        L.latLng(route.end[0], route.end[1]), // End point
    ]);
    fetchTrafficLights(selectedRoute); // Fetch traffic lights for the selected route
}

// Handle route selection change
document
    .getElementById("routeSelector")
    .addEventListener("change", function () {
        updateRoute(this.value);
    });

// Initialize with the first route if available
if (vehicles.length > 0) {
    updateRoute(vehicles[0].id); // Use the number plate as the initial route
}

// Listen for route found event to get the main road name
control.on("routesfound", function (e) {
    var routes = e.routes;
    if (routes.length > 0) {
        // Get the first instruction which usually indicates the main road
        var firstInstruction = routes[0].instructions[0].text;

        // Log the main road name to the console
        console.log("Main road along the route: " + firstInstruction);
    }
});

// Function to fetch traffic light coordinates from Overpass API
function fetchTrafficLights(route) {
    let bounds;

    // Set bounds based on the selected route
    if (route === "panjim-margao") {
        bounds = "15.2967,73.8278,15.499,74.0207"; // Panjim to Margao
    } else if (route === "mapusa-mumbai") {
        bounds = "15.5501,73.7518,19.076,72.8777"; // Mapusa to Mumbai
    }

    const overpassUrl = `https://overpass-api.de/api/interpreter?data=[out:json];node["highway"="traffic_signals"](${bounds});out body;`;

    fetch(overpassUrl)
        .then((response) => response.json())
        .then((data) => {
            const trafficLights = data.elements.map((light) => [
                light.lat,
                light.lon,
            ]);
            // Clear previous markers before adding new ones
            map.eachLayer((layer) => {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });
            trafficLights.forEach((coords) => {
                L.marker(coords)
                    .addTo(map)
                    .bindPopup("Traffic Light")
                    .openPopup();
            });
        })
        .catch((error) =>
            console.error("Error fetching traffic lights:", error)
        );
}
