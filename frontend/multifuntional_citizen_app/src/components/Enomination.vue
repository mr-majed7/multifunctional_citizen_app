<template>
    <v-app id="e-nomination-app">
      <v-app-bar color="#0d1117" dark app>
        <v-toolbar-title>Citizen App - E-Nomination</v-toolbar-title>
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
              prepend-avatar="@/assets/citizen_logo.png"
              title="Welcome To Citizen App"
            >
              <template v-slot:append>
                <v-btn icon variant="text" @click.stop="rail = !rail">
                  <v-icon>{{ rail ? "mdi-chevron-left" : "mdi-chevron-right" }}</v-icon>
                </v-btn>
              </template>
            </v-list-item>
  
            <v-divider></v-divider>
  
            <v-list dense nav>
              <v-list-item prepend-icon="mdi-home-city" title="Edit Profile" @click="goToHome"></v-list-item>
              <v-list-item prepend-icon="mdi-account" title="Update Document"></v-list-item>
              <v-list-item prepend-icon="mdi-account-group-outline" title="Important Numbers"></v-list-item>
            </v-list>
          </v-navigation-drawer>

          <v-main>
            <v-container fluid class="fill-height">
              <v-row align="center" justify="center">
                <v-col :cols="cols" :sm="cols" :md="cols" :lg="cols" :xl="cols" class="nomination-card-container">
                  <v-card class="nomination-card" elevation="10">
                    <v-card-title class="text-h4 font-weight-bold text-center py-4 primary white--text">
                      E-Nomination for Property
                    </v-card-title>
  
                    <v-card-text class="pa-6">
                      <v-form @submit.prevent="submitForm" ref="form" v-model="valid">
                        <v-divider class="mb-4"></v-divider>
                        <h3 class="text-h6 font-weight-bold">Property Details</h3>
  
                        <v-text-field 
                          v-model="formData.propertyId"
                          label="Property ID"
                          :rules="[rules.required]"
                          required
                          outlined
                          dense
                        ></v-text-field>
  
                        <v-text-field 
                          v-model="formData.propertyAddress"
                          label="Property Address"
                          :rules="[rules.required]"
                          required
                          outlined
                          dense
                        ></v-text-field>
  
                        <v-divider class="my-4"></v-divider>
                        <h3 class="text-h6 font-weight-bold">Beneficiary Details</h3>
  
                        <v-text-field 
                          v-model="formData.beneficiaryName"
                          label="Beneficiary Name"
                          :rules="[rules.required]"
                          required
                          outlined
                          dense
                        ></v-text-field>
  
                        <v-text-field 
                          v-model="formData.beneficiaryRelation"
                          label="Relation with Beneficiary"
                          :rules="[rules.required]"
                          required
                          outlined
                          dense
                        ></v-text-field>
  
                        <v-text-field 
                          v-model="formData.beneficiaryContact"
                          label="Contact Number"
                          :rules="[rules.required, rules.phone]"
                          required
                          outlined
                          dense
                        ></v-text-field>
  
                        <v-divider class="my-4"></v-divider>
                        <h3 class="text-h6 font-weight-bold">Proof of Identification</h3>
  
                        <v-file-input 
                          v-model="formData.proofOfId"
                          label="Upload Proof of Identification"
                          :rules="[rules.required]"
                          required
                          dense
                        ></v-file-input>

                        <v-divider class="my-4"></v-divider>
                        <h3 class="text-h6 font-weight-bold">Declaration</h3>
  
                        <v-checkbox 
                          v-model="formData.declaration"
                          label="I hereby declare that the above information is true and accurate."
                          :rules="[rules.requiredCheckbox]"
                          required
                        ></v-checkbox>
  
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
    name: "ENominationPage",
    data() {
      return {
        drawer: true,
        rail: true,
        valid: false,
        cols: 6,
        formData: {
          propertyId: "",
          propertyAddress: "",
          beneficiaryName: "",
          beneficiaryRelation: "",
          beneficiaryContact: "",
          proofOfId: null,
          declaration: false,
        },
        rules: {
          required: value => !!value || "Field is required",
          phone: value => /\d{10}/.test(value) || "Enter a valid 10-digit number",
          requiredCheckbox: value => value || "You must agree to the declaration",
        },
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
          alert("Nomination submitted successfully!");
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
  
  .nomination-card-container {
    margin-bottom: 24px;
  }
  
  .nomination-card {
    background: linear-gradient(135deg, #a7a5a4 0%, #2b4162 100%);
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  }
  
  .nomination-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
  }
  
  .full-height {
    height: 100vh;
  }
  
  .v-navigation-drawer {
    position: fixed;
    top: 64px; 
    left: 0;
    height: calc(100vh - 64px); 
    margin: 0 !important;
    padding: 0 !important;
  }
  </style>
  