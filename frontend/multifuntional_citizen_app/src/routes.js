import { createRouter, createWebHistory } from "vue-router";
import EmergencyCon from "./components/EmergencyCon.vue";
import Manageprofile from "./components/Manageprofile.vue";
import VoteSystem from "./components/VoteSystem.vue";
import complaints from "./components/complaints.vue";

const routes = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/votesystem", component: VoteSystem },
    { path: "/manageprofile", component: Manageprofile },
    { path: "/emergencycon", component: EmergencyCon },
    { path: "/complaints", component: complaints },
  ],
});

export default routes;
