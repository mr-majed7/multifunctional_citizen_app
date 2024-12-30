import { createRouter, createWebHistory } from "vue-router";
import EmergencyCon from "./components/EmergencyCon.vue";
import Manageprofile from "./components/Manageprofile.vue";
import VoteSystem from "./components/VoteSystem.vue";
import complaints from "./components/complaints.vue";

import Listfiles from "@/components/Listfiles.vue";
import TINRegistration from "@/components/TINRegistration.vue";
import Upload from "@/components/Upload.vue";

const routes = [
  {
    path: "/tinregistration",
    name: "TINRegistration",
    component: TINRegistration,
  },
  {
    path: "/upload",
    name: "Upload",
    component: Upload,
  },
  {
    path: "/listfiles",
    name: "Listfiles",
    component: Listfiles,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/votesystem", component: VoteSystem },
    { path: "/manageprofile", component: Manageprofile },
    { path: "/emergencycon", component: EmergencyCon },
    { path: "/complaints", component: complaints },
  ],
  routes: routes,
});

export default router;
