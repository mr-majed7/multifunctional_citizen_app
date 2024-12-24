<template>
  <v-app>
    <v-main>
      <Listfiles/>
      <router-view />
       <!-- <Upload/> -->
    </v-main>
  </v-app>
</template>

<script>
import Listfiles from './components/Listfiles.vue'
import Upload from './components/Upload.vue';

export default {
  name: 'App',

  components: {
    Listfiles,
    Upload
  },

  data: () => ({
    //
  }),
}
</script>