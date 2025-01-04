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
    localStorage.setItem('user_id', 100);
    localStorage.setItem('nid_number', '1234567890123');
  }
}
</script>

