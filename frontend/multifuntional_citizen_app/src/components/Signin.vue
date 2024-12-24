<template>
    <v-app>
      <v-container fluid class="fill-height background-image">
        <v-row justify="center" align="center">
          <v-col cols="12" sm="10" md="8" lg="6">
            <v-row class="d-flex justify-center align-center" style="max-height: 200px;">
              <v-img
                class="mx-auto my-5 logo-margin"
                max-width="100"
                src="@/assets/citizen_logo.png"
                rounded="lg"
              ></v-img>
            </v-row>
  
           
            <v-card
              class="mx-auto pa-12 pb-8"
              elevation="8"
              width="448"
              rounded="lg"
            >
              <div class="text-subtitle-1 text-medium-emphasis">Account</div>
  
              <v-text-field
                density="compact"
                placeholder="Email address"
                prepend-inner-icon="mdi-email-outline"
                variant="outlined"
                v-model="email"
              ></v-text-field>
  
              <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                Password
                <a
                  class="text-caption text-decoration-none text-blue"
                  href="#"
                  rel="noopener noreferrer"
                  target="_blank"
                >
                  Forgot login password?
                </a>
              </div>
  
              <v-text-field
                :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                :type="visible ? 'text' : 'password'"
                density="compact"
                placeholder="Enter your password"
                prepend-inner-icon="mdi-lock-outline"
                variant="outlined"
                @click:append-inner="visible = !visible"
                v-model="password"
              ></v-text-field>
  
              <v-btn
                class="mb-8"
                color="blue"
                size="large"
                variant="tonal"
                block
                @click="handleLogin"
              >
                Log In
              </v-btn>
  
              <v-card-text class="text-center">
                <router-link to="/signup" class="text-blue text-decoration-none">
                  Sign up now <v-icon icon="mdi-chevron-right"></v-icon>
                </router-link>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-app>
  </template>
  
  <script>
  export default {
    data: () => ({
      visible: false,
      email: '',
      password: '',
    }),
    methods: {
      handleLogin() {
        if (this.email === 'user@example.com' && this.password === 'password123') {
          this.$router.push('/home'); 
        } else {
          alert('Invalid login credentials. Please try again!');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .background-image {
    background: url('@/assets/flag.png') no-repeat center center fixed;
    background-size: cover;
    height: 100vh; 
  }
  
  .fill-height {
    height: 100vh;
  }
  
  .logo-margin {
    margin-left: 30px; 
  }
  </style>
  