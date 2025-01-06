<template>
    <v-app>
      <v-app-bar color="#0d1117" dark app>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer" class="d-md-none"></v-app-bar-nav-icon>
        <v-toolbar-title>Citizen App</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn class="mx-2 d-none d-sm-flex" color="primary" variant="tonal" ripple @click="logout">
          Logout
        </v-btn>
        <v-btn class="mx-2 d-none d-sm-flex" color="primary" variant="tonal" ripple @click="goToHome">
          Home
        </v-btn>
        <v-btn class="mx-2 d-none d-sm-flex" color="primary" variant="tonal" ripple @click="giveFeedback">
          Feedback
        </v-btn>
        <v-menu v-if="$vuetify.display.xs">
          <template v-slot:activator="{ props }">
            <v-btn icon v-bind="props">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="logout">
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
            <v-list-item @click="goToHome">
              <v-list-item-title>Home</v-list-item-title>
            </v-list-item>
            <v-list-item @click="giveFeedback">
              <v-list-item-title>Feedback</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-app-bar>
  
      <v-navigation-drawer
        v-model="drawer"
        :rail="rail"
        :permanent="$vuetify.display.mdAndUp"
        :temporary="$vuetify.display.smAndDown"
        class="elevation-2 full-height no-gap"
        @click="rail = false"
      >
        <v-list-item
          prepend-avatar="/citizen_logo.png"
          title="Welcome To Citizen App"
        >
          <template v-slot:append>
            <v-btn icon variant="text" @click.stop="rail = !rail">
              <v-icon>{{ rail ? 'mdi-chevron-right' : 'mdi-chevron-left' }}</v-icon>
            </v-btn>
          </template>
        </v-list-item>
  
        <v-divider></v-divider>
  
        <v-list dense nav>
          <v-list-item prepend-icon="mdi-update" title="Edit Profile" ripple @click="$router.push('/manageprofile')"></v-list-item>
          <v-list-item prepend-icon="mdi-file-document-edit" title="Update Document" ripple @click="$router.push('/doc_correction')"></v-list-item>
          <v-list-item prepend-icon="mdi-numeric" title="Important Numbers" ripple @click="$router.push('/emergencycon')"></v-list-item>
        </v-list>
      </v-navigation-drawer>
  
      <v-main>
        <v-container fluid class="background-container pa-0">
          <v-row dense>
            <v-col
              v-for="(image, index) in images"
              :key="index"
              cols="12"
              sm="6"
              md="4"
              class="d-flex flex-column align-center pa-2"
            >
              <v-card class="pa-0 large-square-card" outlined>
                <v-img
                  :src="require(`@/assets/${image.src}`)"
                  :lazy-src="require(`@/assets/${image.src}`)"
                  class="m-0"
                  cover
                >
                  <template v-slot:placeholder>
                    <v-row class="fill-height ma-0" align="center" justify="center">
                      <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    </v-row>
                  </template>
                </v-img>
              </v-card>
  
              <v-btn
                color="primary"
                ripple
                @click="navigateToPage(image.path)"
                class="mt-2 responsive-btn"
              >
                {{ image.name }}
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script>
  export default {
    data() {
      return {
        drawer: null,
        rail: true,
        images: [
          { src: "utbill.png", name: "Utility Payment", path: "/utbill" },
          { src: "votesystem.png", name: "Vote", path: "/votesystem" },
          { src: "Documents.png", name: "Documents", path: "/listfiles" },
          { src: "Income_tax.png", name: "Income Tax", path: "/income_tax" },
          { src: "Property_tax.png", name: "Property Tax", path: "/propertytax" },
          { src: "E_nomination.png", name: "E-Nomination", path: "/e-nomination" },
          { src: "Passport.jpg", name: "Passport Application", path: "/passportapplication" },
          { src: "traffic_fine.jpg", name: "Traffic Fine", path: "/trafficfine" },
          { src: "Complaint.jpg", name: "Complaint", path: "/complaints" }
        ],
      };
    },
    methods: {
      logout() {
        alert("Logged out!");
        this.$router.push("/");
      },
      goToHome() {
        alert("Navigating to Home!");
        this.$router.push("/home");
      },
      giveFeedback() {
        this.$router.push('/feedback');
      },
      navigateToPage(path) {
        if (path) {
          this.$router.push(path);
        } else {
          console.error("Path not defined for this image.");
          alert("Path not defined for this image!");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .no-gap {
    margin: 0;
    padding: 0;
  }
  
  .background-container {
    background: url("../assets/background.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background: linear-gradient(135deg, #344f36 0%, #701717 100%);
    min-height: 100vh;
  }
  
  .full-height {
    height: 100vh;
  }
  
  .v-app-bar {
    margin: 0;
    padding: 0;
    width: 100%
  }
  
  .large-square-card {
    width: 100%;
    max-width: 300px;
    aspect-ratio: 1 / 1;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  
  .v-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .responsive-btn {
    width: 100%;
    max-width: 300px;
  }
  
  @media (max-width: 600px) {
    .large-square-card {
      max-width: 250px;
    }
  
    .responsive-btn {
      max-width: 250px;
    }
  }
  
  @media (max-width: 400px) {
    .large-square-card {
      max-width: 200px;
    }
  
    .responsive-btn {
      max-width: 200px;
    }
  }
  </style>