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
                              <v-item v-for="n in 5" :key="n - 1">
                                <template v-slot:default="{ toggle }">
                                  <v-btn
                                    :active="formData[question.model] != null && formData[question.model] === n - 1"
                                    :icon="`mdi-numeric-${n - 1}`"
                                    height="40"
                                    variant="text"
                                    width="40"
                                    border
                                    @click="formData[question.model] = n - 1"
                                  ></v-btn>
                                </template>
                              </v-item>
                            </v-item-group>
                          </v-card>
                        </div>
  
                        <v-textarea
                          v-model="formData.feedback_text"
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


                <v-col :cols="4">
                  <v-card elevation="10" class="faq-card">
                    <v-card-title class="text-h5 font-weight-bold">
                      Frequently Asked Questions
                    </v-card-title>
                    <v-card-text>
                      <v-expansion-panels>
                        <v-expansion-panel
                          v-for="(faq, index) in faqList"
                          :key="index"
                          :title="faq.question"
                          :text="faq.answer"
                        >
                        </v-expansion-panel>
                      </v-expansion-panels>
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
          feedback_text: "",
        },
        surveyQuestions: [
          { text: "How satisfied are you with developing using Vuetify?", model: "experience" },
          { text: "How would you rate the usability?", model: "usability" },
          { text: "Would you recommend this service to others?", model: "recommendation" },
        ],
        faqList: [
          { question: "How can I view my bills?", answer: "Go to the Utility Bill Management section to view and pay your bills." },
          { question: "How do I reset my password?", answer: "Go to Profile Management and select 'Reset Password'." },
          { question: "Can I apply for a passport?", answer: "Yes, you can apply for a passport through the Passport Application section." },
          { question: "How do I register on the Citizen App?", answer: "To register, click on the 'Register' button on the login screen. Provide your NID, email address, and mobile number. Verify your account using the code sent to you and set a password to complete the process." },
          { question: "How can I reset my password if I forget it?", answer: "Click on 'Forgot Password' on the login screen. Enter your registered email or NID to receive a reset link. Follow the link to create a new password." },          
          { question: "What services are linked to my NID?", answer: "Your NID links to services like utility bill management (electricity, gas, water), TIN registration, and document access, ensuring accurate billing and service availability." },
          { question: "How do I pay my utility bills using the app?", answer: "Navigate to 'Utility Bill Management,' select the bill type, enter details, confirm the payment, and choose a payment method. A receipt will be generated upon completion." },
          { question: "Can I correct errors in government documents through the app?", answer: "Yes, use the 'Document Correction' section to submit requests. Upload the incorrect document and provide correct information to receive updates on your request." },
          { question: "How do I access support if I face issues?", answer: "Visit the 'Support and Feedback' section to submit tickets or feedback. Alternatively, explore the FAQ for common queries." },
          { question: "What documents can I store and access through the app?", answer: "Store and access property deeds, tax receipts, and utility bills. Some documents may require a fee for access or download." },
          { question: "How can I apply for a passport using the app?", answer: "In the 'Passport Application' section, fill out the form with your details and upload required documents. Receive updates on your application's status." },
          { question: "How does the voting system work in the app?", answer: "Authenticate with your NID during the voting period to access the interface. Cast or modify your vote until the voting window closes." },
          { question: "What is the purpose of the emergency contact feature?", answer: "The emergency contact feature provides quick access to police, fire, and medical numbers, and allows saving personal emergency contacts for critical situations." }
        ],
      };
    },
    methods: {
      logout() {
        alert("Logged out!");
        this.$router.push("/");
      },
      goToHome() {
        this.$router.push("/home");
      },
      async submitForm() {
        if (this.$refs.form.validate()) {
          try {
            const response = await fetch("http://localhost:5000/feedback", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(this.formData),
            });

            if (response.ok) {
              const data = await response.json();
              alert(data.message || "Feedback submitted successfully!");
            } else {
              const errorData = await response.json();
              alert(errorData.error || "Failed to submit feedback.");
            }
          } catch (error) {
            console.error(error);
            alert("An error occurred while submitting feedback.");
          }
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
  margin-bottom: 24px; 
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

</style>