<template>
  <v-app>
    <v-container fluid class="fill-height gradient-background">
      <v-row justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="payment-card" elevation="10">
            <v-card-title class="text-h4 font-weight-bold text-center py-4">
              Payment Information
            </v-card-title>

            <v-card-text>
              <v-form ref="form" v-model="valid" @submit.prevent="processPayment">
                <v-text-field
                  v-model="cardholderName"
                  label="Cardholder Name"
                  :rules="[rules.required]"
                  outlined
                  dense
                  class="mb-2"
                ></v-text-field>

                <v-text-field
                  v-model="cardNumber"
                  label="Card Number"
                  :rules="[rules.required, rules.cardNumber]"
                  outlined
                  dense
                  class="mb-2"
                ></v-text-field>

                <v-row>
                  <v-col cols="6">
                    <v-text-field
                      v-model="expiryDate"
                      label="Expiry Date (MM/YY)"
                      :rules="[rules.required, rules.expiryDate]"
                      outlined
                      dense
                    ></v-text-field>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field
                      v-model="cvv"
                      label="CVV"
                      :rules="[rules.required, rules.cvv]"
                      outlined
                      dense
                    ></v-text-field>
                  </v-col>
                </v-row>

                <v-btn
                  color="primary"
                  :disabled="!valid"
                  block
                  x-large
                  class="mt-4"
                  type="submit"
                >
                  Pay {{ amount }} BDT
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title class="text-h5 text-center">
          {{ paymentState === "processing" ? "Processing Payment" : "Payment Successful" }}
        </v-card-title>

        <v-card-text class="text-center">
          <div v-if="paymentState === 'processing'" class="payment-processing">
            <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
            <p class="mt-4">Processing your payment, please wait...</p>
          </div>
          <div v-else-if="paymentState === 'success'" class="payment-success">
            <v-icon color="success" size="64">mdi-check-circle</v-icon>
            <h3 class="mt-4 mb-2">Payment Receipt</h3>
            <v-list dense>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Amount Paid:</v-list-item-title>
                  <v-list-item-subtitle>{{ paidAmount }} BDT</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Payment Date:</v-list-item-title>
                  <v-list-item-subtitle>{{ paymentDate }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Payment ID:</v-list-item-title>
                  <v-list-item-subtitle>{{ paymentId }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
            <v-btn color="primary" text @click="downloadReceipt" class="mt-4">
              <v-icon left>mdi-download</v-icon>
              Download Receipt
            </v-btn>
          </div>
        </v-card-text>

        <v-card-actions v-if="paymentState === 'success'">
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="redirect">
            Redirect Now ({{ countdown }}s)
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="redirectLoading" persistent max-width="300">
    <v-card>
      <v-card-text class="text-center pa-4">
        <v-progress-circular indeterminate color="primary" size="64" class="mb-4"></v-progress-circular>
        <p class="text-h6">Redirecting...</p>
        <p>Please wait while we redirect you to your app</p>
      </v-card-text>
    </v-card>
  </v-dialog>
  </v-app>
</template>

<script>
import axios from "axios";
import jsPDF from "jspdf";

export default {
  data() {
    return {
      dialog: false,
      redirectLoading: false,
      cardholderName: "",
      cardNumber: "",
      expiryDate: "",
      cvv: "",
      valid: false,
      dialog: false,
      paymentState: "processing",
      countdown: 5,
      interval: null,
      amount: 0,
      paidAmount: 0,
      paymentDate: "",
      paymentId: "",
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
    const queryAmount = this.$route.query.amount;
    this.amount = queryAmount ? parseFloat(queryAmount) : 0;
    this.updateStatusUrl = this.$route.query.updateStatusEndpoint;
    console.log(this.updateStatusUrl);
  },
  methods: {
    async updateStatus(url){
      try {
        console.log(url);
        const response = await axios.put(`http://localhost:5000/${url}`);
        if (!response.ok) {
          throw new Error("Failed to update status.");
        }else{
          return true;
        }
      } catch (error) {
        console.error("Error updating status:", error);
      }
    },
    processPayment() {
      if (this.$refs.form.validate()) {
        if (this.updateStatusUrl != undefined){
          this.updateStatus(this.updateStatusUrl);
        }
          this.dialog = true;
          this.paymentState = "processing";
          setTimeout(() => {
            this.paymentState = "success";
            this.paidAmount = this.amount;
            this.paymentDate = new Date().toLocaleString();
            this.paymentId = Math.random().toString(36).slice(2, 12).toUpperCase();
            this.startCountdown();
          }, 3000);
      }
    },
    startCountdown() {
      this.interval = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          clearInterval(this.interval);
          this.redirect();
        }
      }, 1000);
    },
    redirect() {
      this.redirectLoading = true;
      this.dialog = false;
      setTimeout(() => {
        this.$router.push(`${this.$route.query.redirectRoute}`);
      }, 3000);
    },
    maskCardNumber(cardNumber) {
      if (cardNumber.length === 16) {
        return `${cardNumber.slice(0, 4)} ******** ${cardNumber.slice(-4)}`;
      }
      return "Invalid Card Number";
    },
    downloadReceipt() {
      if (!this.paidAmount || !this.paymentDate || !this.paymentId) {
        console.error("Receipt data is missing!");
        return;
      }

      try {
        const doc = new jsPDF();
        let y = 20;

        doc.setFontSize(16);
        doc.text("Payment Receipt", 20, y);
        y += 10;

        doc.setFontSize(12);
        doc.text(`Cardholder Name: ${this.cardholderName}`, 20, y);
        y += 10;
        doc.text(`Card Number: ${this.maskCardNumber(this.cardNumber)}`, 20, y);
        y += 10;
        doc.text(`Amount Paid: ${this.paidAmount} BDT`, 20, y);
        y += 10;
        doc.text(`Payment Date: ${this.paymentDate}`, 20, y);
        y += 10;
        doc.text(`Payment ID: ${this.paymentId}`, 20, y);

        doc.save(`Payment_Receipt_${this.paymentId}.pdf`);
      } catch (error) {
        console.error("Error generating receipt PDF:", error);
      }
    }
  },
};
</script>

<style scoped>

.payment-card {
  background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
  border-radius: 16px;
  overflow: hidden;
}

.v-card__title {
  background-color: #f3f4f6;
  color: #1e293b;
}

.v-btn {
  text-transform: none;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.v-dialog {
  border-radius: 16px;
}
</style>