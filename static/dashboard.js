const app = Vue.createApp({
  delimiters: ["[[", "]]"],
  data() {
    return {
      base_url: document.getElementById("app").getAttribute("data-base-url"),
    };
  },
  methods: {
    logout() {
      console.log("in vue");
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
            window.location.href = this.base_url;
          } else {
            console.error("Logout failed:", response.statusText);
          }
        })
        .catch((error) => {
          console.error("Logout failed:", error);
        });
    },
  },
});

app.mount("#app");
