<template>
  <v-app>
    <v-main>
      <v-container>
        <router-view></router-view>
        <HelloWorld></HelloWorld>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>

import HelloWorld from './components/HelloWorld.vue';
export default {
  components: {
    HelloWorld
  }
}

</script>