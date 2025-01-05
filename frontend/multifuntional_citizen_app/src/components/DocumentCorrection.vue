<template>
  <v-container fluid class="correction-request-container">
    <v-card class="correction-card">
            <v-card-title class="text-h4 font-weight-bold text-center py-4 primary white--text">
            Document Correction Request
            </v-card-title>
            <v-card-text>
            <v-form v-if="step === 1" @submit.prevent="editForm">
                <h2 class="text-h5 mb-4">Select Document Type</h2>
                <v-select
                v-model="selectedDocumentType"
                :items="documentTypes"
                label="Document Type"
                outlined
                ></v-select>
                <v-btn
                color="primary"
                class="mt-4"
                :disabled="!selectedDocumentType"
                type="submit"
                >Continue</v-btn>
            </v-form>

            <v-form v-if="step === 2" ref="form" v-model="valid" @submit.prevent="reviewForm">
                <v-text-field
                v-model="documentNumber"
                :label="`${selectedDocumentType} Number`"
                outlined
                required
                ></v-text-field>
                <v-text-field
                v-model="formData.name"
                label="Name"
                outlined
                required
                :rules="[nameRule]"
                ></v-text-field>
                <v-text-field
                v-model="formData.fathersName"
                label="Father's Name"
                outlined
                required
                :rules="[nameRule]"
                ></v-text-field>
                <v-text-field
                v-model="formData.mothersName"
                label="Mother's Name"
                outlined
                required
                :rules="[nameRule]"
                ></v-text-field>
                <v-text-field
                v-model="formData.dateOfBirth"
                label="Date of Birth (DD-MM-YYYY)"
                outlined
                required
                :rules="[dateRule]"
                ></v-text-field>
                <v-textarea
                v-model="formData.address"
                label="Address"
                outlined
                required
                ></v-textarea>
                <v-textarea
                v-model="formData.description"
                label="Description of Corrections Needed"
                outlined
                required
                ></v-textarea>
                <v-btn
                color="primary"
                class="mt-4"
                :disabled="!valid"
                type="submit"
                >
                Review Request
                </v-btn>
            </v-form>

            <div v-if="step === 3">
                <h2 class="text-h5 mb-4">Review Your Details</h2>
                <v-list>
                <v-list-item>
                    <v-list-item-content>
                    <v-list-item-title class="font-weight-medium">Document Type:</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">{{ selectedDocumentType }}</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item>
                    <v-list-item-content>
                    <v-list-item-title class="font-weight-medium">{{ selectedDocumentType }} Number:</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">{{ documentNumber }}</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item v-for="(value, key) in formData" :key="key">
                    <v-list-item-content>
                    <v-list-item-title class="font-weight-medium">{{ formatLabel(key) }}:</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">{{ value }}</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
                </v-list>
                <v-btn
                color="primary"
                class="mt-4 mr-2"
                @click="submitForm"
                >
                Submit Correction Request
                </v-btn>
                <v-btn
                color="secondary"
                class="mt-4"
                @click="editForm"
                >
                Edit Form
                </v-btn>
            </div>
            </v-card-text>
            <v-dialog v-model="showConfirmation" max-width="500px">
        <v-card>
          <v-card-title class="text-h5 font-weight-bold">
            Document Correction Request Received
          </v-card-title>
          <v-card-text>
            <p class="mb-4">Your Document Correction request has been successfully submitted.</p>
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title class="font-weight-medium">Ticket Number:</v-list-item-title>
                <v-list-item-subtitle class="text-h6">
                  {{ ticketNumber }}
                  <v-btn icon small @click="copyTicketNumber" class="ml-2">
                    <v-icon>mdi-content-copy</v-icon>
                  </v-btn>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title class="font-weight-medium">Description of Issue:</v-list-item-title>
                <v-list-item-subtitle>{{ formData.description }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" text @click="goToHome">
              <v-icon left>mdi-home</v-icon>
              Go to Home
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="closeConfirmation">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </v-container>
</template>
  
<script>
import axios from 'axios';

export default {
  name: 'DocumentCorrection',
  data() {
    return {
      step: 1,
      selectedDocumentType: '',
      documentTypes: ['NID', 'Passport', 'Birth Certificate'],
      documentNumber: '',
      valid: false,
      formData: {
        name: '',
        fathersName: '',
        mothersName: '',
        dateOfBirth: '',
        address: '',
        description: '',
      },
      nameRule: v => /^[A-Za-z\s]+$/.test(v) || 'Only letters and spaces are allowed',
      dateRule: v => {
        const isValidFormat = /^\d{2}-\d{2}-\d{4}$/.test(v);
        if (!isValidFormat) return 'Enter a valid date in DD-MM-YYYY format';

        const [day, month, year] = v.split('-').map(Number);

        const date = new Date(`${year}-${month}-${day}`);
        return (
          date.getFullYear() === year &&
          date.getMonth() + 1 === month &&
          date.getDate() === day
        ) || 'Enter a valid date in DD-MM-YYYY format';
      },
      showConfirmation: false,
      ticketNumber: '',
    };
  },
  methods: {
    reviewForm() {
      if (this.$refs.form.validate()) {
        this.step = 3;
      }
    },
    async submitForm() {
      console.log('Submitting correction request:', {
        document_type: this.selectedDocumentType,
        document_number: this.documentNumber,
        ...this.formData,
      });
      
      this.ticketNumber = this.generateTicketNumber();
      const user_id = localStorage.getItem('user_id')
      
      try {
        const response = await axios.post(
          `https://multifunctional-citizen-app-api.onrender.com/service_req/${user_id}/Document%20Correction`,
          {
            document_type: this.selectedDocumentType,
            document_number: this.documentNumber,
            form_data: this.formData,
            ticket_no: this.ticketNumber,
          }
        );

        if (response.status === 200) {
          console.log('Request submitted successfully:', response.data);
          this.$emit('success', response.data.message || 'Request submitted successfully');
        }
      } catch (error) {
        if (error.response) {
          console.error('Error response:', error.response.data);
          alert(`Error: ${error.response.data.error || 'Unable to submit request'}`);
        } else if (error.request) {
          console.error('Error request:', error.request);
          alert('Error: No response from the server. Please try again later.');
        } else {
          console.error('Error:', error.message);
          alert('Error: Something went wrong. Please try again.');
        }
      }

      this.showConfirmation = true;
    },
    editForm() {
      this.step = 2;
    },
    formatLabel(key) {
      return key.split(/(?=[A-Z])/).join(" ").replace(/\b\w/g, l => l.toUpperCase());
    },
    generateTicketNumber() {
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
      let result = '';
      for (let i = 0; i < 8; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
      }
      return `DCR-${result}`;
    },
    copyTicketNumber() {
      navigator.clipboard.writeText(this.ticketNumber);
    },
    closeConfirmation() {
      this.showConfirmation = false;
      this.resetForm();
    },
    resetForm() {
      this.step = 1;
      this.selectedDocumentType = '';
      this.documentNumber = '';
      this.formData = {
        name: '',
        fathersName: '',
        mothersName: '',
        dateOfBirth: '',
        address: '',
        description: '',
      };
    },
    goToHome() {
      this.$router.push('/');
    },
  },
};
</script>
  
  <style scoped>
  .correction-request-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
  }
  
  .correction-card {
    width: 100%;
    max-width: 600px;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
  }
  
  .v-card__title {
    background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
  }
  
  .v-list-item {
    background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
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