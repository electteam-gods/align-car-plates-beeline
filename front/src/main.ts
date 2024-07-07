import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura";
import FileUpload from "primevue/fileupload";

const app = createApp(App);
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: "dark",
    },
  },
});

app.component("FileUpload", FileUpload);

app.mount("#app");
