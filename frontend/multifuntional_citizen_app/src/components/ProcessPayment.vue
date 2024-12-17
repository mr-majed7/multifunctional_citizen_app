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
                  <p>Payment Receipt:</p>
                  <ul>
                    <li><strong>Amount Paid:</strong> {{ paidAmount }} BDT</li>
                    <li><strong>Payment Date:</strong> {{ paymentDate }}</li>
                    <li><strong>Payment ID:</strong> {{ paymentId }}</li>
                  </ul>
                  <v-btn color="primary" text @click="downloadReceipt">
                    Download Receipt
                  </v-btn>
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
import jsPDF from "jspdf";
export default {
  data() {
    return {
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
  },
  methods: {
    processPayment() {
      this.dialog = true;
      this.paymentState = "processing";
      setTimeout(() => {
        this.paymentState = "success";
        this.paidAmount = this.amount;
        this.paymentDate = new Date().toLocaleString();
        this.paymentId = Math.random().toString(36).slice(2, 12).toUpperCase();
        this.startCountdown();
      }, 3000);
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
      this.$router.push("/");
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

<style>
.v-btn {
  margin-top: 10px;
}
.text-center {
  text-align: center;
}
</style>
