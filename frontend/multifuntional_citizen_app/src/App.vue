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
    localStorage.setItem('user_id', 1);
    localStorage.setItem('nid_number', '123457890123');
  }
}
</script>

