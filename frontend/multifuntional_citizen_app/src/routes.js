import { createRouter, createWebHistory } from "vue-router";

import TINRegistration from '@/components/TINRegistration.vue'; 
import Upload from '@/components/Upload.vue';
import Listfiles from '@/components/Listfiles.vue';

const routes = [

  {
    path: '/tinregistration',
    name: 'TINRegistration',
    component: TINRegistration,
  },
  {
    path: '/upload',
    name: 'Upload',
    component: Upload, 
  },
  {
    path: '/listfiles',
    name: 'Listfiles',
    component: Listfiles,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

export default router;