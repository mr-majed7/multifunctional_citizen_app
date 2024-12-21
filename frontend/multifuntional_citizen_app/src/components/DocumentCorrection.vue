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
        </v-card>
    </v-container>

</template>
  
<script>
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

            // Parse the date components
            const [day, month, year] = v.split('-').map(Number);

            // Check if the date is logical
            const date = new Date(`${year}-${month}-${day}`);
            return (
                date.getFullYear() === year &&
                date.getMonth() + 1 === month &&
                date.getDate() === day
            ) || 'Enter a valid date in DD-MM-YYYY format';
            },
    };
  },
  methods: {
    reviewForm() {
      if (this.$refs.form.validate()) {
        this.step = 3;
      }
    },
    submitForm() {
      console.log('Submitting correction request:', {
        documentType: this.selectedDocumentType,
        documentNumber: this.documentNumber,
        ...this.formData,
      });
      this.step = 1;
      this.selectedDocumentType = '';
      this.documentNumber = '';
      this.$vuetify.snackbar.success('Correction request submitted successfully!');
    },
    editForm() {
      this.step = 2;
    },
    formatLabel(key) {
      return key.split(/(?=[A-Z])/).join(" ").replace(/\b\w/g, l => l.toUpperCase());
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