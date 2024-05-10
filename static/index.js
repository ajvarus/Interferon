const app = Vue.createApp({
  delimiters: ["[[", "]]"],
  data() {
    return {
      isBoxVisible: false,
      message: "",
      messages: {
        type1:
          "This feature is currently under development. If you have signed up, we'll send you an email when it's available.",
        type2:
          "This feature is currently only available to users who have signed up. If you have, please login to continue.",
      },
    };
  },
  methods: {
    messageBoxShow(event) {
      const buttonText = event.target.textContent;

      if (buttonText === "Not the one you think.") {
        this.message = this.messages["type2"];
      } else {
        this.message = this.messages["type1"];
      }

      this.isBoxVisible = true;
    },
    messageBoxHide() {
      this.isBoxVisible = false;
    },
  },
});

app.mount("#app");
