document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]",
    ).value;

    fetch("/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Invalid credentials.");
        }
        return response.json();
      })
      .then((data) => {
        if (data.access) {
          localStorage.setItem("accessToken", data.access);
          localStorage.setItem("refreshToken", data.refresh);
          window.location.href = "/supervisor/dashboard/";
        }
      })
      .catch((error) => {
        const errorContainer = document.createElement("div");
        errorContainer.classList.add("alert", "alert-danger");
        const errorList = document.createElement("ul");
        const listItem = document.createElement("li");
        listItem.textContent = error.message;
        errorList.appendChild(listItem);
        errorContainer.appendChild(errorList);
        document.body.prepend(errorContainer);
      });
  });
