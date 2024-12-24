import { createRouter, createWebHistory } from "vue-router";
import Signin from '@/components/Signin.vue';
import SignUp from '@/components/SignUp.vue'; 
import HomePage from '@/components/HomePage.vue';
import Feedback from '@/components/Feedback.vue';

const routes = [
  {
    path: '/',
    name: 'signin',
    component: Signin,
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp,
  },
  {
    path: '/home',
    name: 'home',
    component: HomePage, 
  },
  {
    path: '/feedback',
    name: 'Feedback',
    component: Feedback,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: [],
});

export default routes;
