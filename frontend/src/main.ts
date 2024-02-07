import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./Router.ts";

import { IconPack, library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { fas } from "@fortawesome/free-solid-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";
library.add(fas as IconPack, fab as IconPack);

let app = createApp(App);
app.component("font-awesome-icon", FontAwesomeIcon); // 导入FontAwesome图标。为了偷懒，索性全部导入了。
app.use(router);
app.mount("#app");
