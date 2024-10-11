document.addEventListener("DOMContentLoaded", function () {
  checkLoginStatus();

  document
    .getElementById("logoutButton")
    .addEventListener("click", function () {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      window.location.href = "/home";
    });

  document
    .getElementById("vehicleForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      const numberPlate = document.getElementById("number_plate").value;
      const startLocation = document.getElementById("start_location").value;
      const endLocation = document.getElementById("end_location").value;

      Promise.all([
        fetchCoordinates(startLocation),
        fetchCoordinates(endLocation),
      ])
        .then(([startData, endData]) => {
          const data = {
            number_plate: numberPlate,
            start_latitude: startData.lat,
            start_longitude: startData.lon,
            stop_latitude: endData.lat,
            stop_longitude: endData.lon,
          };

          return fetch("/api/vehicles/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify(data),
          });
        })
        .then((response) => {
          if (response.ok) {
            alert("Vehicle entry created successfully!");
            window.location.reload();
          } else {
            return response.json().then((errorData) => {
              alert(
                "Failed to create vehicle entry: " + JSON.stringify(errorData),
              );
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("An error occurred while creating the vehicle entry.");
        });
    });

  function fetchCoordinates(locationName) {
    const accessKey = "24d74a23652290361b43cc60a6499e4a";
    const url = `https://api.positionstack.com/v1/forward?access_key=${accessKey}&query=${locationName}`;

    return fetch(url)
      .then((response) => response.json())
      .then((data) => {
        if (data.data && data.data.length > 0) {
          return { lat: data.data[0].latitude, lon: data.data[0].longitude };
        } else {
          throw new Error("Location not found");
        }
      });
  }

  function checkLoginStatus() {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      window.location.href = "/auth/login/";
    }
  }
});
