<template>
  <v-app>
    <v-main>
      <v-container>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>

import NIDVerify from './components/NIDVerify.vue';

export default {
  components: {
    NIDVerify,
  }
}

</script>