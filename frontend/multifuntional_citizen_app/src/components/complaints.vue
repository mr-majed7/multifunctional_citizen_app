<template>
    <v-container>
      <v-card class="pa-4">
        <v-card-title>
          Submit a Complaint
        </v-card-title>
        <v-form ref="complaintForm" v-model="valid">
          <v-text-field
            v-model="newComplaint.title"
            label="Title of Complaint"
            :rules="[rules.required, rules.maxLength(150)]"
            required
          ></v-text-field>
          <v-textarea
            v-model="newComplaint.description"
            label="Description of Complaint"
            :rules="[rules.required, rules.maxLength(500)]"
            required
          ></v-textarea>
          <v-btn :disabled="!valid" color="primary" @click="submitComplaint">
            Submit
          </v-btn>
        </v-form>
      </v-card>
  
      <v-divider class="my-4"></v-divider>
  
      <v-card class="pa-4">
        <v-card-title>
          Your Complaints
        </v-card-title>
        <v-list>
          <v-list-item v-for="complaint in complaints" :key="complaint.id">
            <v-list-item-content>
              <v-list-item-title>{{ complaint.title }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ complaint.description }}
              </v-list-item-subtitle>
              <v-chip :color="complaint.status === 'Resolved' ? 'green' : 'orange'">
                {{ complaint.status }}
              </v-chip>
              <span class="text-caption grey--text">
                Submitted on: {{ formatDate(complaint.created_at) }}
              </span>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn icon color="red" @click="deleteComplaint(complaint.id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-card>
  
      <v-snackbar v-model="snackbar.visible" :color="snackbar.color">
        {{ snackbar.message }}
      </v-snackbar>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        valid: false,
        newComplaint: {
          title: '',
          description: '',
          user_id: null, 
        },
        
        complaints: [],
        snackbar: {
          visible: false,
          message: '',
          color: '',
        },
        rules: {
          required: (value) => !!value || 'This field is required.',
          maxLength: (max) => (value) => value.length <= max || `Must be ${max} characters or less.`,
        },
      };
    },
    async mounted() {
        try {
         const response = await axios.get('/me'); // Replace with actaul user login credentials
         this.newComplaint.user_id = response.data.id; 
         console.log('User ID set:', this.newComplaint.user_id);
       } catch (error) {
         console.error('Failed to fetch user info:', error);
         this.snackbar.message = 'Failed to fetch user information.';
         this.snackbar.color = 'red';
         this.snackbar.visible = true;
       }
    },

    methods: {
      async fetchComplaints() {
        try {
          const response = await axios.get(`/complaints/${this.newComplaint.user_id}`);
          this.complaints = response.data;
        } catch (error) {
          this.showSnackbar('Failed to fetch complaints.', 'red');
        }
      },
      async submitComplaint() {
        if (this.$refs.complaintForm.validate()) {
          console.log('Submitting complaint:', this.newComplaint);
          try {
            const response = await axios.post('/complaints', this.newComplaint);
            console.log('Complaint submission response:', response);
            //await axios.post('/complaints', this.newComplaint);
            this.showSnackbar('Complaint submitted successfully!', 'green');
            this.newComplaint.title = '';
            this.newComplaint.description = '';
            this.fetchComplaints();
          } catch (error) {
            console.error('Error during complaint submission:', error);
            this.showSnackbar('Failed to submit complaint.', 'red');
          }
        }
      },
      async deleteComplaint(complaintId) {
        try {
          await axios.delete(`/complaints/${complaintId}`);
          this.showSnackbar('Complaint deleted successfully.', 'green');
          this.fetchComplaints();
        } catch (error) {
          this.showSnackbar('Failed to delete complaint.', 'red');
        }
      },
      formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
      },
      showSnackbar(message, color) {
        this.snackbar.message = message;
        this.snackbar.color = color;
        this.snackbar.visible = true;
      },
    },
    mounted() {
      this.fetchComplaints();
    },
  };
  </script>
  
  <style scoped>
  .text-caption {
    display: block;
    margin-top: 4px;
  }
  </style>
  