<template>
    <v-app id="income-tax-app">
      <v-container>
        <v-card class="pa-5">
          <v-card-title>
            <h1>Income Tax Filing</h1>
          </v-card-title>
  
          <v-card-text>
            <section v-if="step === 'form'">
              <h2>Complete Your Income Tax Form</h2>
              <v-form @submit.prevent="submitForm">
                <v-text-field 
                  label="Name" 
                  v-model="formData.name" 
                  required
                />
  
                <v-text-field 
                  label="Time Period (e.g., FY 2023-24)" 
                  v-model="formData.timePeriod" 
                  required
                />
  
                <v-text-field 
                  label="Income Source" 
                  v-model="formData.incomeSource" 
                  required
                />
  
                <v-text-field 
                  label="Total Income" 
                  type="number" 
                  v-model="formData.totalIncome" 
                  required
                />
  
                <v-text-field 
                  label="Total Tax Amount" 
                  type="number" 
                  v-model="formData.taxAmount" 
                  required
                />
  
                <v-btn color="primary" type="submit">Submit</v-btn>
              </v-form>
            </section>
  
            <section v-else-if="step === 'review'">
              <h2>Review Your Details</h2>
              <v-list>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title><strong>Name:</strong> {{ formData.name }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title><strong>Time Period:</strong> {{ formData.timePeriod }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title><strong>Income Source:</strong> {{ formData.incomeSource }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title><strong>Total Income:</strong> {{ formData.totalIncome }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title><strong>Total Tax Amount:</strong> {{ formData.taxAmount }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
              <v-btn color="primary" @click="proceedToPayment">Proceed to Payment</v-btn>
            </section>
          </v-card-text>
        </v-card>
      </v-container>
    </v-app>
  </template>
  
  <script>
  import ProcessPayment from "./ProcessPayment.vue";
  
  export default {
    name: "IncomeTaxApp",
    components: { ProcessPayment },
    data() {
      return {
        step: "form",
        formData: {
          name: "",
          timePeriod: "",
          incomeSource: "",
          totalIncome: 0,
          taxAmount: 0,
        },
      };
    },
    methods: {
      submitForm() {
        this.step = "review";
      },
      proceedToPayment() {
        this.$router.push(`/payment?&amount=${this.formData.taxAmount}`);
      },
    },
  };
  </script>
  
  <style>
  #income-tax-app {
    margin: 20px;
  }
  </style>
  