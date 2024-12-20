<template>
  <v-app id="income-tax-app">
    <v-container fluid class="fill-height">
      <v-row align="center" justify="center">
        <v-col cols="12" sm="10" md="8" lg="6">
          <v-card class="tax-card" elevation="10">
            <v-card-title class="text-h4 font-weight-bold text-center py-4 primary white--text">
              Income Tax Filing
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
                  v-model="formData.nidNumber"
                  label="NID Number"
                  :rules="[v => !!v || 'NID Number is required']"
                  required
                  outlined
                  dense
                  ></v-text-field>

                <v-text-field 
                  v-model="formData.timePeriod"
                  label="Time Period (e.g., FY 2023-24)"
                  :rules="[v => !!v || 'Time Period is required']"
                  required
                  outlined
                  dense
                ></v-text-field>

                <v-text-field 
                  v-model="formData.incomeSource"
                  label="Income Source"
                  :rules="[v => !!v || 'Income Source is required']"
                  required
                  outlined
                  dense
                ></v-text-field>

                <v-text-field 
                  v-model="formData.totalIncome"
                  label="Total Income"
                  type="number"
                  :rules="[
                    v => !!v || 'Total Income is required',
                    v => v > 0 || 'Total Income must be greater than 0'
                  ]"
                  required
                  outlined
                  dense
                  prefix="BDT"
                ></v-text-field>

                <v-text-field 
                  v-model="formData.taxAmount"
                  label="Total Tax Amount"
                  type="number"
                  :rules="[
                    v => !!v || 'Tax Amount is required',
                    v => v >= 0 || 'Tax Amount must be 0 or greater'
                  ]"
                  required
                  outlined
                  dense
                  prefix="BDT"
                ></v-text-field>

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

              <div v-else>
                <h2 class="text-h5 mb-4">Review Your Details</h2>
                <v-list>
                  <v-list-item v-for="(value, key) in formData" :key="key">
                    <v-list-item-content>
                      <v-list-item-title class="font-weight-medium">{{ formatLabel(key) }}:</v-list-item-title>
                      <v-list-item-subtitle class="text-h6">
                        {{ formatValue(key, value) }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
                <v-btn
                  color="primary"
                  @click="proceedToPayment"
                  class="mt-4"
                  elevation="2"
                >
                  <v-icon left>mdi-cash-multiple</v-icon>
                  Proceed to Payment
                </v-btn>
                <v-btn
                  color="secondary"
                  @click="editForm"
                  class="mt-4 ml-2"
                  elevation="2"
                >
                  <v-icon left>mdi-pencil</v-icon>
                  Edit Form
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
export default {
  name: "IncomeTaxApp",
  data() {
    return {
      valid: false,
      showReview: false,
      formData: {
        name: "",
        nidNumber: "",
        timePeriod: "",
        incomeSource: "",
        totalIncome: 0,
        taxAmount: 0,
      },
    };
  },
  methods: {
    submitForm() {
      if (this.$refs.form.validate()) {
        this.showReview = true;
      }
    },
    proceedToPayment() {
      this.$router.push(`/payment?amount=${this.formData.taxAmount}&redirectRoute=/`);
    },
    editForm() {
      this.showReview = false;
    },
    formatLabel(key) {
      return key.split(/(?=[A-Z])/).join(" ").replace(/\b\w/g, l => l.toUpperCase());
    },
    formatValue(key, value) {
      if (key === 'totalIncome' || key === 'taxAmount') {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'BDT' }).format(value);
      }
      return value;
    }
  },
};
</script>

<style scoped>
.tax-card {
  background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.tax-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
}

.v-list-item {
  background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.v-list-item:last-child {
  border-bottom: none;
}

.v-btn {
  text-transform: none;
  font-weight: 600;
  letter-spacing: 0.5px;
}
</style>