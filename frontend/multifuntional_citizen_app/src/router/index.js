import complaints from "@/components/complaints.vue";
import DocumentCorrection from "@/components/DocumentCorrection.vue";
import EmergencyCon from "@/components/EmergencyCon.vue";
import ENominationPage from "@/components/Enomination.vue";
import Feedback from "@/components/Feedback.vue";
import HomePage from "@/components/HomePage.vue";
import IncomeTax from "@/components/IncomeTax.vue";
import Listfiles from "@/components/Listfiles.vue";
import Manageprofile from "@/components/Manageprofile.vue";
import NIDVerify from "@/components/NIDVerify.vue";
import PassportApplication from "@/components/PassportApplication.vue";
import ProcessPayment from "@/components/ProcessPayment.vue";
import PropertyTax from "@/components/PropertyTax.vue";
import Signin from "@/components/Signin.vue";
import SignUp from "@/components/SignUp.vue";
import TINRegistration from "@/components/TINRegistration.vue";
import Trafficfine from "@/components/Trafficfine.vue";
import Upload from "@/components/Upload.vue";
import UtilityBill from "@/components/UtilityBill.vue";
import VoteSystem from "@/components/VoteSystem.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
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
    {
      path: "/trafficfine",
      name: "Trafficfine",
      component: Trafficfine,
    },

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
    {
      path: "/passportapplication",
      name: "PassportApplication",
      component: PassportApplication,
    },
    {
      path: "/propertytax",
      name: "PropertyTax",
      component: PropertyTax,
    },
    { path: "/", name: "signin", component: Signin },
    { path: "/signup", name: "signup", component: SignUp },
    { path: "/home", name: "home", component: HomePage },
    { path: "/feedback", name: "Feedback", component: Feedback },
    { path: "/e-nomination", name: "ENomination", component: ENominationPage },
    { path: "/votesystem", component: VoteSystem },
    { path: "/manageprofile", component: Manageprofile },
    { path: "/emergencycon", component: EmergencyCon },
    { path: "/complaints", component: complaints },
  ],
});

export default router;
