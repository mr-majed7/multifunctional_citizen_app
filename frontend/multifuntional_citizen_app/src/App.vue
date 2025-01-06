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



export default {
  components: {
  },
  mounted() {
    localStorage.setItem('user_id', 4);
    localStorage.setItem('nid_number', '9581710416');
  }
}
</script>

