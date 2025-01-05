<template>
  <v-app>
    <v-container fluid class="fill-height gradient-background">
      <v-row justify="center" align="center">
        <v-col cols="12" sm="10" md="8" lg="6">
          <v-card class="bill-card" elevation="10">
            <v-card-title class="text-h4 font-weight-bold text-center py-4 primary white--text">
              Your Utility Bills
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
                    <h2 class="text-h6 font-weight-bold mb-2">Fetching your bills</h2>
                    <p class="text-body-2 text-medium-emphasis">Please wait while we gather all your bills</p>
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
                  v-for="(bill, index) in bills"
                  :key="index"
                  class="mb-4"
                >
                  <v-expansion-panel-header class="title">
                    <v-row no-gutters align="center">
                      <v-col cols="auto" class="mr-2">
                        <v-icon :color="getBillColor(bill.type)" size="36">{{ getBillIcon(bill.type) }}</v-icon>
                      </v-col>
                      <v-col class="d-flex align-center">
                        {{ bill.type.toUpperCase() }} Bill
                      </v-col>
                      <v-col cols="auto">
                        <v-chip
                          :color="bill.status ? 'success' : 'warning'"
                          small
                        >
                          {{ bill.status ? 'Paid' : 'Pending' }}
                        </v-chip>
                      </v-col>
                    </v-row>
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <v-card flat>
                      <v-card-text>
                        <v-row>
                          <v-col cols="6">
                            <div class="subtitle-1">Amount Due:</div>
                            <div class="text-h5 font-weight-bold">{{ formatCurrency(bill.amount) }}</div>
                          </v-col>
                          <v-col cols="6">
                            <div class="subtitle-1">Due Date:</div>
                            <div class="text-h6">{{ formatDate(bill.dueDate) }}</div>
                          </v-col>
                        </v-row>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                          :color="bill.status ? 'success' : 'primary'"
                          :disabled="bill.status"
                          @click="redirectToPayment(index)"
                          elevation="2"
                        >
                          <v-icon left>{{ bill.status ? 'mdi-check' : 'mdi-cash-multiple' }}</v-icon>
                          {{ bill.status ? 'Paid' : 'Pay Now' }}
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
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      bills: [],
      loading: true,
    };
  },
  methods: {
    async fetchBills() {
    const nidNumber = localStorage.getItem("nid_number");
    if (!nidNumber) {
      alert("NID number is missing!");
      return;
    }

    try {
      const response = await fetch(`https://multifunctional-citizen-app-api.onrender.com/get_bills/${nidNumber}`);
      if (!response.ok) {
        throw new Error("Failed to fetch bills.");
      }
      const data = await response.json();

      this.bills = data.map(bill => ({
        ...bill,
        dueDate: new Date(bill.due_date).toISOString(),
        amount: parseFloat(bill.amount),
        status: Boolean(bill.status)
      }));
      console.log("Fetched bills:", this.bills);
    } catch (error) {
      console.error("Error fetching bills:", error);
      alert("Failed to fetch bills. Please try again later.");
    } finally {
      await new Promise(resolve => setTimeout(resolve, 1500));
      this.loading = false;
    }
  },
    redirectToPayment(index) {
      const bill = this.bills[index];
      this.$router.push(`/payment?amount=${bill.amount}&updateStatusEndpoint=/update_bill_status/${bill.bill_id}&redirectRoute=/utbill&type=utility_bill`);
    },
    getBillIcon(type) {
      const icons = {
        gas: "mdi-fire",
        electricity: "mdi-lightning-bolt",
        water: "mdi-water",
      };
      return icons[type] || "mdi-file-document-outline";
    },
    getBillColor(type) {
      const colors = {
        gas: "orange",
        electricity: "yellow darken-2",
        water: "blue",
      };
      return colors[type] || "grey";
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat("en-BD", { style: "currency", currency: "BDT" }).format(amount);
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString("en-BD", { year: "numeric", month: "long", day: "numeric" });
    },
  },
  mounted() {
    this.fetchBills();
  },
};
</script>

<style scoped>
.bill-card {
  background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.bill-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
}

.v-expansion-panel {
  background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
  border-radius: 8px !important;
  margin-bottom: 16px;
}

.v-expansion-panel::before {
  box-shadow: none;
}

.v-expansion-panel-header {
  padding: 16px;
}

.v-card {
  background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
}

.v-expansion-panel-content__wrap {
  padding: 0;
}

.v-btn {
  text-transform: none;
  font-weight: 600;
  letter-spacing: 0.5px;
}

loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.loading-card {
  width: 100%;
  max-width: 500px; 
  border-radius: 16px;
  overflow: hidden;
}

.pulse-animation {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.05);
    opacity: 1;
  }
  100% {
    transform: scale(0.95);
    opacity: 0.7;
  }
}


</style>
