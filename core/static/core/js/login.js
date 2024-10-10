document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]",
    ).value; // Get the CSRF token

    fetch("/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken, // Include CSRF token
      },
      body: JSON.stringify({ username, password }), // Send username and password as JSON
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json(); // Parse the JSON response
      })
      .then((data) => {
        // Handle successful login
        if (data.access) {
          // Check if access token is present
          // Optionally store tokens in local storage or a global variable
          localStorage.setItem("accessToken", data.access);
          localStorage.setItem("refreshToken", data.refresh);

          // Redirect to the supervisor dashboard
          window.location.href = "/supervisor/dashboard/";
        } else {
          // Handle errors (if any)
          const errorContainer = document.createElement("div");
          errorContainer.classList.add("alert", "alert-danger");
          const errorList = document.createElement("ul");

          if (data.errors && data.errors.non_field_errors) {
            data.errors.non_field_errors.forEach((error) => {
              const listItem = document.createElement("li");
              listItem.textContent = error;
              errorList.appendChild(listItem);
            });
          } else {
            const listItem = document.createElement("li");
            listItem.textContent = "An unknown error occurred.";
            errorList.appendChild(listItem);
          }

          errorContainer.appendChild(errorList);
          document.body.prepend(errorContainer);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
