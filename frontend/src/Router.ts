import { createRouter, createWebHistory } from "vue-router";
import Index from "./pages/Index.vue";
import About from "./pages/About.vue";
import FileBrowser from "./pages/FileBrowser.vue";

const routes = [
  { path: "/", component: Index },
  { path: "/about", component: About },
  { path: "/file_browser", component: FileBrowser },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
