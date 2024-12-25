import { createRouter, createWebHistory } from "vue-router";
import DocumentCorrection from "./components/DocumentCorrection.vue";
import IncomeTax from "./components/IncomeTax.vue";
import ProcessPayment from "./components/ProcessPayment.vue";
import UtilityBill from "./components/UtilityBill.vue";

const routes = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/nidverify", component: NIDVerify },
    { path: "/home", component: HelloWorld },
    { path: "/utbill", component: UtilityBill },
    { path: "/payment", component: ProcessPayment },
    { path: "/income_tax", component: IncomeTax },
    { path: "/doc_correction", component: DocumentCorrection },
  ],
});

export default routes;
