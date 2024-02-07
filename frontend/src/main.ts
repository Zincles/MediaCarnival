import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./Router.ts";

//createApp(App).mount('#app')

createApp(App).use(router).mount("#app");
