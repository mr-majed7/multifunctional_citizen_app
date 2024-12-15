import HelloWorld from "./components/HelloWorld.vue";
import NIDVerify from "./components/NIDVerify.vue";

import { createRouter, createWebHistory } from "vue-router";
import ProcessPayment from "./components/ProcessPayment.vue";
import UtilityBill from "./components/UtilityBill.vue";

const routes = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/nidverify", component: NIDVerify },
    { path: "/home", component: HelloWorld },
    { path: "/utbill", component: UtilityBill },
    { path: "/payment", component: ProcessPayment },
  ],
});

export default routes;
