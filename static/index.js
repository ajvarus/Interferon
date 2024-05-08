function messageBoxToggle(clickedButtonId, boxToHideId) {
  const clickedButton = document.getElementById(clickedButtonId);
  const boxToHide = document.getElementById(boxToHideId);

  // Add click event listener to the button
  clickedButton.addEventListener("click", function () {
    // Toggle the visibility of the target element
    boxToHide.classList.toggle("is-hidden");
  });
}

messageBoxToggle("indexMessageDeleteButton", "indexMessageBox");
messageBoxToggle("indexKeygenButton", "indexMessageBox");

function logout() {
  const logoutButton = document.getElementById("logoutButton");

  logoutButton.addEventListener("click", function () {
    fetch("/auth/logout", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json", // Specify content type as JSON
      },
      body: JSON.stringify({}),
    })
      .then((response) => {
        if (response.ok) {
          window.location.href = "{{ base_url }}/";
        } else {
          console.error("Logout failed:", response.statusText);
        }
      })
      .catch((error) => {
        console.error("Logout failed:", error);
      });
  });
}
