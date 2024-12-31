import { createRouter, createWebHistory } from "vue-router";
import Signin from '@/components/Signin.vue';
import SignUp from '@/components/SignUp.vue'; 
import HomePage from '@/components/HomePage.vue';
import Feedback from '@/components/Feedback.vue';
import ENominationPage from '@/components/Enomination.vue'; 
import Trafficfine from '@/components/Trafficfine.vue';  


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
  {
    path: '/e-nomination',
    name: 'ENomination',
    component: ENominationPage, 
  },
  {
    path: '/trafficfine',
    name: 'Trafficfine',
    component: Trafficfine, 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes ,
});

export default router;
