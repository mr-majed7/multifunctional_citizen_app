<template>
    <v-app>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title>
                <v-text-field
                  label="Enter your NID"
                  v-model="userNID"
                  outlined
                  dense
                ></v-text-field>
                <v-btn
                  color="primary"
                  class="ml-4"
                  :disabled="!userNID"
                  @click="fetchBills"
                >
                  Fetch Bills
                </v-btn>
              </v-card-title>
  
              <v-divider></v-divider>
  
              <v-card-text>
                <div v-if="bills.length > 0">
                  <v-expansion-panels>
                    <v-expansion-panel v-for="(bill, index) in bills" :key="index">
                      <v-expansion-panel-header>
                        {{ bill.type.toUpperCase() }} Bill - Due: {{ bill.dueDate }}
                      </v-expansion-panel-header>
  
                      <v-expansion-panel-content>
                        <v-list dense>
                          <v-list-item>
                            <v-list-item-title>Amount Due:</v-list-item-title>
                            <v-list-item-subtitle>{{ bill.amount }} BDT</v-list-item-subtitle>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-title>Status:</v-list-item-title>
                            <v-list-item-subtitle>
                              {{ bill.status ? "Paid" : "Pending" }}
                            </v-list-item-subtitle>
                          </v-list-item>
                        </v-list>
  
                        <v-btn
                          color="success"
                          :disabled="bill.status"
                          @click="redirectToPayment(index)"
                        >
                          {{ bill.status ? "Paid" : "Pay Now" }}
                        </v-btn>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </div>
                <div v-else-if="userNID && !loading">
                  <v-alert type="info" border="left" prominent>
                    No bills found for the entered NID.
                  </v-alert>
                </div>
  
                <v-progress-circular
                  v-if="loading"
                  indeterminate
                  color="primary"
                  class="mt-4"
                ></v-progress-circular>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
  
        <v-snackbar v-model="snackbar" :timeout="3000" top>
          {{ snackbarMessage }}
          <template v-slot:action>
            <v-btn color="white" text @click="snackbar = false">Close</v-btn>
          </template>
        </v-snackbar>
      </v-container>
    </v-app>
  </template>
  
  <script>
  export default {
    data() {
      return {
        userNID: "",
        bills: [],
        loading: false,
        snackbar: false,
        snackbarMessage: "",
        countdown: 5,
        interval: null,
      };
    },
    methods: {
      fetchBills() {
        this.loading = true;
        setTimeout(() => {
          this.loading = false;
          this.bills = [
            {
              type: "gas",
              amount: 1200,
              dueDate: "2024-12-31",
              status: false,
            },
            {
              type: "electricity",
              amount: 2500,
              dueDate: "2024-12-20",
              status: false,
            },
            {
              type: "water",
              amount: 500,
              dueDate: "2024-12-25",
              status: true,
            },
          ];
        }, 1000);
      },
      redirectToPayment(index) {
        const bill = this.bills[index];
        this.$router.push(`/payment?amount=${bill.amount}`);
      },
    },
  };
  </script>
  
  <style>
  .v-btn {
    margin-top: 10px;
  }
  </style>
  