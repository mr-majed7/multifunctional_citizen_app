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
  name: 'App',

  components: {
  },
  mounted() {
    localStorage.setItem('user_id', '123e4567-e89b-12d3-a456-426614174000');
    localStorage.setItem('nid_number', '1234567890123');
  }
}
</script>

