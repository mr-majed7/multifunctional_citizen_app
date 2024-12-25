import DocumentCorrection from "@/components/DocumentCorrection.vue";
import ENominationPage from "@/components/Enomination.vue";
import Feedback from "@/components/Feedback.vue";
import HomePage from "@/components/HomePage.vue";
import IncomeTax from "@/components/IncomeTax.vue";
import NIDVerify from "@/components/NIDVerify.vue";
import ProcessPayment from "@/components/ProcessPayment.vue";
import Signin from "@/components/Signin.vue";
import SignUp from "@/components/SignUp.vue";
import UtilityBill from "@/components/UtilityBill.vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/nidverify", name: "NIDVerify", component: NIDVerify },
    { path: "/utbill", name: "UtilityBill", component: UtilityBill },
    { path: "/payment", name: "ProcessPayment", component: ProcessPayment },
    { path: "/income_tax", name: "IncomeTax", component: IncomeTax },
    {
      path: "/doc_correction",
      name: "DocumentCorrection",
      component: DocumentCorrection,
    },
    { path: "/", name: "signin", component: Signin },
    { path: "/signup", name: "signup", component: SignUp },
    { path: "/home", name: "home", component: HomePage },
    { path: "/feedback", name: "Feedback", component: Feedback },
    { path: "/e-nomination", name: "ENomination", component: ENominationPage },
  ],
});

export default routes;
