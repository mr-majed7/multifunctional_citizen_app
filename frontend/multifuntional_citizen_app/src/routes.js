import { createRouter, createWebHistory } from "vue-router";
import HomePage from '@/components/HomePage.vue';

const routes = [
  {
    path: '/home',
    name: 'home',
    component: HomePage, 
  },
]
const router = createRouter({
  history: createWebHistory(),
  routes: [],
});

export default routes;
