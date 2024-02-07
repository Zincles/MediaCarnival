import { createRouter, createWebHistory } from 'vue-router';
import Index from './pages/Index.vue';
import About from './pages/About.vue';

const routes = [
  { path: '/', component: Index },
  { path: '/about', component: About },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;