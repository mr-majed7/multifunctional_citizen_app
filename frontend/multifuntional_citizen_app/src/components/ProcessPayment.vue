<template>
    <v-app>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>
                <span class="text-h5">Payment Information</span>
              </v-card-title>
  
              <v-divider></v-divider>
  
              <v-card-text>
                <v-form ref="paymentForm" v-model="valid">
                  <v-text-field
                    label="Cardholder Name"
                    v-model="cardholderName"
                    :rules="[rules.required]"
                    outlined
                    dense
                  ></v-text-field>
  
                  <v-text-field
                    label="Card Number"
                    v-model="cardNumber"
                    :rules="[rules.required, rules.cardNumber]"
                    outlined
                    dense
                  ></v-text-field>
  
                  <v-row>
                    <v-col cols="6">
                      <v-text-field
                        label="Expiry Date (MM/YY)"
                        v-model="expiryDate"
                        :rules="[rules.required, rules.expiryDate]"
                        outlined
                        dense
                      ></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field
                        label="CVV"
                        v-model="cvv"
                        :rules="[rules.required, rules.cvv]"
                        outlined
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
  
                  <v-btn
                    color="success"
                    :disabled="!valid"
                    block
                    @click="processPayment"
                  >
                    Pay {{ amount }} BDT
                  </v-btn>
                </v-form>
              </v-card-text>
            </v-card>
  
            <v-dialog v-model="dialog" max-width="400">
              <v-card>
                <v-card-title>
                  <span class="text-h6">
                    {{ paymentState === "processing" ? "Processing Payment" : "Payment Successful" }}
                  </span>
                </v-card-title>
  
                <v-card-text>
                  <div v-if="paymentState === 'processing'" class="text-center">
                    <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    <p>Processing your payment, please wait...</p>
                  </div>
                  <div v-else-if="paymentState === 'success'">
                    Redirecting back to the app in {{ countdown }} seconds...
                  </div>
                </v-card-text>
  
                <v-card-actions>
                  <v-btn v-if="paymentState === 'success'" color="primary" text @click="redirectToApp">
                    Redirect Now
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-col>
        </v-row>
      </v-container>
    </v-app>
  </template>
  
  <script>
  export default {
    data() {
      return {
        cardholderName: "",
        cardNumber: "",
        expiryDate: "",
        cvv: "",
        valid: false,
        dialog: false,
        paymentState: "processing", // "processing" or "success"
        countdown: 5,
        interval: null,
        amount: 0, // Default value for amount
        rules: {
          required: (value) => !!value || "Field is required",
          cardNumber: (value) =>
            /^[0-9]{16}$/.test(value) || "Invalid card number",
          expiryDate: (value) =>
            /^(0[1-9]|1[0-2])\/\d{2}$/.test(value) || "Invalid expiry date",
          cvv: (value) => /^[0-9]{3}$/.test(value) || "Invalid CVV",
        },
      };
    },
    created() {
      // Get the 'amount' from query parameters
      const queryAmount = this.$route.query.amount;
      this.amount = queryAmount ? parseFloat(queryAmount) : 0;
    },
    methods: {
      processPayment() {
        // Simulate payment processing
        this.dialog = true;
        this.paymentState = "processing";
        setTimeout(() => {
          this.paymentState = "success";
          this.startCountdown();
        }, 3000); // Simulate a delay of 3 seconds for processing
      },
      startCountdown() {
        this.interval = setInterval(() => {
          if (this.countdown > 0) {
            this.countdown--;
          } else {
            clearInterval(this.interval);
            this.redirectToApp();
          }
        }, 1000);
      },
      redirectToApp() {
        this.dialog = false;
        this.$router.push("/"); // Redirect using vue-router
      },
    },
  };
  </script>
  
  <style>
  .v-btn {
    margin-top: 10px;
  }
  .text-center {
    text-align: center;
  }
  </style>
  