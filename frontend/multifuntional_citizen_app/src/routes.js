

import { createRouter, createWebHistory } from "vue-router";
import Manageprofile from "./components/Manageprofile.vue";
import VoteSystem from "./components/VoteSystem.vue";



const routes = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/votesystem", component: VoteSystem },
    { path: "/manageprofile", component: Manageprofile },

  ],
});

export default routes;