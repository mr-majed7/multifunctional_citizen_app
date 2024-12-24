<template>
    <v-app id="feedback-app">
      <v-app-bar color="#0d1117" dark app>
        <v-toolbar-title>Citizen App Feedback</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn class="mx-2" color="primary" variant="tonal" ripple @click="goToHome">
          Home
        </v-btn>
        <v-btn class="mx-2" color="primary" variant="tonal" ripple @click="logout">
          Logout
        </v-btn>
      </v-app-bar>
  
      <v-container fluid class="background-container">
        <v-layout>
          <v-navigation-drawer
          v-model="drawer"
            :rail="rail"
            permanent
            class="elevation-2 full-height no-gap"
            @click="rail = false"

          >
            <v-list-item
              prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
              title="John Leider"
              subtitle="Admin"
            >
              <template v-slot:append>
                <v-btn icon variant="text" @click.stop="rail = !rail">
                  <v-icon>{{ rail ? "mdi-chevron-left" : "mdi-chevron-right" }}</v-icon>
                </v-btn>
              </template>
            </v-list-item>
  
            <v-divider></v-divider>
  
            <v-list dense nav>
              <v-list-item prepend-icon="mdi-home-city" title="Home" @click="goToHome"></v-list-item>
              <v-list-item prepend-icon="mdi-account" title="My Account"></v-list-item>
              <v-list-item prepend-icon="mdi-account-group-outline" title="Users"></v-list-item>
            </v-list>
          </v-navigation-drawer>
  
          <v-main>
            <v-container fluid class="fill-height">
              <v-row align="center" justify="center">
                <v-col :cols="cols" :sm="cols" :md="cols" :lg="cols" :xl="cols" class="survey-card-container">
                  <v-card class="feedback-card" elevation="10">
                    <v-card-title class="text-h4 font-weight-bold text-center py-4 primary white--text">
                      Feedback Survey
                    </v-card-title>
  
                    <v-card-text class="pa-6">
                      <v-form @submit.prevent="submitForm" ref="form" v-model="valid" v-if="!showReview">
                        <v-text-field 
                          v-model="formData.name"
                          label="Name"
                          :rules="[v => !!v || 'Name is required']"
                          required
                          outlined
                          dense
                        ></v-text-field>
  
                        
                        <v-text-field 
                          v-model="formData.email"
                          label="Email"
                          :rules="[v => !!v || 'Email is required']"
                          required
                          outlined
                          dense
                        ></v-text-field>
  
                        <div v-for="(question, index) in surveyQuestions" :key="index" class="mt-4">
                          <v-card
                            class="px-2 mx-auto"
                            max-width="300"
                            rounded="lg"
                            :text="question.text"
                            theme="dark"
                            variant="flat"
                          >
                            <v-item-group
                              v-model="formData[question.model]"
                              class="d-flex justify-sm-space-between px-6 pt-2 pb-6"
                            >
                              <v-item v-for="n in 5" :key="n">
                                <template v-slot:default="{ toggle }">
                                  <v-btn
                                    :active="formData[question.model] != null && formData[question.model] + 1 >= n"
                                    :icon="`mdi-numeric-${n}`"
                                    height="40"
                                    variant="text"
                                    width="40"
                                    border
                                    @click="toggle"
                                  ></v-btn>
                                </template>
                              </v-item>
                            </v-item-group>
                          </v-card>
                        </div>
  
                        <v-textarea
                          v-model="formData.feedback"
                          label="Additional Feedback"
                          hint="Optional"
                          outlined
                          dense
                          rows="4"
                        ></v-textarea>
  
                        <v-btn
                          color="primary"
                          type="submit"
                          :disabled="!valid"
                          class="mt-4"
                          elevation="2"
                        >
                          <v-icon left>mdi-check</v-icon>
                          Submit
                        </v-btn>
                      </v-form>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-main>
        </v-layout>
      </v-container>
    </v-app>
  </template>
  
  <script>
  export default {
    name: "FeedbackPage",
    data() {
      return {
        drawer: true,
        rail: true,
        valid: false,
        showReview: false,
        cols: 6, 
        formData: {
          name: "",
          email: "",
          experience: null,
          usability: null,
          recommendation: null,
          feedback: "",
        },
        surveyQuestions: [
          { text: "How satisfied are you with developing using Vuetify?", model: "experience" },
          { text: "How would you rate the usability?", model: "usability" },
          { text: "Would you recommend this service to others?", model: "recommendation" },
        ],
      };
    },
    methods: {
      logout() {
        alert("Logged out!");
        this.$router.push("/signin");
      },
      goToHome() {
        this.$router.push("/");
      },
      submitForm() {
        if (this.$refs.form.validate()) {
          alert("Feedback submitted!");
        }
      },
    },
  };
  </script>

<style>
.background-container {
  background: linear-gradient(135deg, black, #1a1a1a);
  padding-top: 64px; 
}

.survey-card-container {
  margin-bottom: 24px; /
}

.feedback-card {
  background: linear-gradient(135deg, #a7a5a4 0%, #2b4162 100%);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.feedback-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
}



.no-margin {
  margin: 0;
}

.no-gap {
  margin: 0;
  padding: 0;
}

.v-app-bar {
margin: 0;
padding: 0;
width: 100%;
}

.full-height {
  height: 100vh;
}
.v-navigation-drawer {
position: fixed;
top: 64px; 
left: 0; 
height: calc(100vh - 64px); 
padding: 0 !important;
}
</style>