

import { createRouter, createWebHistory } from "vue-router";
import Manageprofile from "./components/Manageprofile.vue";
import VoteSystem from "./components/VoteSystem.vue";
import EmergencyCon from "./components/EmergencyCon.vue";



const routes = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/votesystem", component: VoteSystem },
    { path: "/manageprofile", component: Manageprofile },
    { path: "/emergencycon", component: EmergencyCon },

  ],
});

export default routes;