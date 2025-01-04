<template>
    <v-app id="Traffic Fine">
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
              prepend-avatar="/citizen_logo.png"
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
              <v-list-item prepend-icon="mdi-update" title="Edit Profile" ripple @click="goToHome"></v-list-item>
              <v-list-item prepend-icon="mdi-file-document-edit" title="Update Document" ripple @click="goToHome"></v-list-item>
              <v-list-item prepend-icon="mdi-numeric" title="Important Numbers" ripple @click="goToHome"></v-list-item>
            </v-list>
          </v-navigation-drawer>
  
        
          <v-main>
            <v-container fluid class="fill-height gradient-background">
              <v-row justify="center" align="center">
                <v-col cols="12" sm="10" md="8" lg="6">
                  <v-card class="fine-card" elevation="10">
                    <v-card-title class="text-h4 font-weight-bold text-center py-4 primary white--text">
                      Your Traffic Fines
                    </v-card-title>
  
                    <v-card-text class="pa-6">
                      <div v-if="loading" class="loading-container">
                        <v-card class="loading-card" elevation="4">
                          <v-card-text class="text-center pa-4">
                            <v-progress-circular
                              indeterminate
                              color="primary"
                              size="64"
                              width="4"
                              class="mb-4 pulse-animation"
                            ></v-progress-circular>
                            <h2 class="text-h6 font-weight-bold mb-2">Fetching your fines</h2>
                            <p class="text-body-2 text-medium-emphasis">Please wait while we gather all your fines</p>
                            <v-skeleton-loader
                              class="mt-4"
                              type="list-item-two-line, list-item-two-line"
                              :loading="true"
                            ></v-skeleton-loader>
                          </v-card-text>
                        </v-card>
                      </div>
  
                      <v-expansion-panels v-else accordion hover>
                        <v-expansion-panel
                          v-for="(fine, index) in fines"
                          :key="index"
                          class="mb-4"
                        >
                          <v-expansion-panel-header class="title">
                            <v-row no-gutters align="center">
                              <v-col cols="auto" class="mr-2">
                                <v-icon color="red" size="36">mdi-alert</v-icon>
                              </v-col>
                              <v-col class="d-flex align-center">
                                Case {{ fine.case_number }}
                              </v-col>
                              <v-col cols="auto">
                                <v-chip
                                  :color="fine.status ? 'success' : 'warning'"
                                  small
                                >
                                  {{ fine.status ? 'Paid' : 'Unpaid' }}
                                </v-chip>
                              </v-col>
                            </v-row>
                          </v-expansion-panel-header>
                          <v-expansion-panel-content>
                            <v-card flat>
                              <v-card-text>
                                <v-row>
                                  <v-col cols="6">
                                    <div class="subtitle-1">Cause:</div>
                                    <div class="text-h5 font-weight-bold">{{ fine.cause }}</div>
                                  </v-col>
                                  <v-col cols="6">
                                    <div class="subtitle-1">Due Payment:</div>
                                    <div class="text-h6">{{ formatCurrency(fine.due_payment) }}</div>
                                  </v-col>
                                </v-row>
                              </v-card-text>
                              <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                  :color="fine.status ? 'success' : 'primary'"
                                  :disabled="fine.status"
                                  @click="redirectToPayment(index)"
                                  elevation="2"
                                >
                                  <v-icon left>{{ fine.status ? 'mdi-check' : 'mdi-cash-multiple' }}</v-icon>
                                  {{ fine.status ? 'Paid' : 'Pay Now' }}
                                </v-btn>
                              </v-card-actions>
                            </v-card>
                          </v-expansion-panel-content>
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
    data() {
      return {
        fines: [],
        loading: true,
        drawer: true,
        rail: true,
      };
    },
    methods: {
      async fetchFines() {
        try {
          const response = await fetch(`http://localhost:5000/trafficfine`);
          if (!response.ok) {
            throw new Error("Failed to fetch fines.");
          }
          const data = await response.json();
          this.fines = data.map((fine) => ({
            ...fine,
            status: Boolean(fine.status),
          }));
        } catch (error) {
          console.error("Error fetching fines:", error);
          alert("Failed to fetch fines. Please try again later.");
        } finally {
          await new Promise((resolve) => setTimeout(resolve, 1500));
          this.loading = false;
        }
      },
      redirectToPayment(index) {
        const fine = this.fines[index];
        this.$router.push(`/payment?amount=${fine.due_payment}&updateStatusEndpoint=/update_fine_status/${fine.id}&redirectRoute=/trafficfine&type=traffic_fine`);
      },
      formatCurrency(amount) {
        return new Intl.NumberFormat("en-BD", { style: "currency", currency: "BDT" }).format(amount);
      },
      goToHome() {
        this.$router.push("/home");
      },
      logout() {
        alert("Logged out!");
        this.$router.push("/signin");
      },
    },
    mounted() {
      this.fetchFines();
    },
  };
  </script>
  
  <style>
  .background-container {
    background: linear-gradient(135deg, black, #1a1a1a);
    padding-top: 64px; 
  }
  
  .fine-card {
    background: linear-gradient(135deg, #a7a5a4 0%, #2b4162 100%);
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  }
  
  .fine-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
  }

  </style>
  