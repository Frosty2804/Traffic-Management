document.addEventListener("DOMContentLoaded", function () {
  checkLoginStatus();

  // Logout functionality
  document
    .getElementById("logoutButton")
    .addEventListener("click", function () {
      localStorage.removeItem("jwt");
      window.location.href = "/home";
    });

  // Handle vehicle form submission (POST)
  document
    .getElementById("vehicleForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      const startLocation = document.getElementById("start_location").value;
      const destination = document.getElementById("destination").value;

      // Look up coordinates for start location
      fetch(`/api/locations/?query=${encodeURIComponent(startLocation)}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to fetch start location coordinates");
          }
          return response.json();
        })
        .then((startData) => {
          // Log startData for debugging
          console.log("Start Location Data:", startData);

          // Set start coordinates
          document.getElementById("start_latitude").value = startData.latitude;
          document.getElementById("start_longitude").value =
            startData.longitude;

          // Look up coordinates for destination
          return fetch(
            `/api/locations/?query=${encodeURIComponent(destination)}`,
          );
        })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to fetch destination coordinates");
          }
          return response.json();
        })
        .then((destinationData) => {
          // Log destinationData for debugging
          console.log("Destination Location Data:", destinationData);

          // Set destination coordinates
          document.getElementById("stop_latitude").value =
            destinationData.latitude;
          document.getElementById("stop_longitude").value =
            destinationData.longitude;

          // Log coordinates before submission
          console.log("Coordinates Before Submission:", {
            start_latitude: startData.latitude,
            start_longitude: startData.longitude,
            stop_latitude: destinationData.latitude,
            stop_longitude: destinationData.longitude,
          });

          // Validate coordinates
          if (
            !startData.latitude ||
            !startData.longitude ||
            !destinationData.latitude ||
            !destinationData.longitude
          ) {
            alert("Invalid coordinates received. Please check your locations.");
            return;
          }

          // Prepare data for submission
          const formData = new FormData(document.getElementById("vehicleForm"));
          const data = Object.fromEntries(formData);

          // Add coordinates to the data object
          data.start_latitude = startData.latitude;
          data.start_longitude = startData.longitude;
          data.stop_latitude = destinationData.latitude;
          data.stop_longitude = destinationData.longitude;

          // Submit the vehicle form
          fetch("/api/vehicles/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("jwt")}`,
            },
            body: JSON.stringify(data),
          })
            .then((response) => {
              if (response.ok) {
                alert("Vehicle entry created successfully!");
                window.location.reload(); // Reload the page to reflect changes
              } else {
                return response.json().then((errorData) => {
                  alert(
                    "Failed to create vehicle entry: " +
                      JSON.stringify(errorData),
                  );
                });
              }
            })
            .catch((error) => {
              console.error("Error:", error);
              alert("An error occurred while creating the vehicle entry.");
            });
        })
        .catch((error) => {
          console.error("Error:", error);
          alert(error.message);
        });
    });
});
