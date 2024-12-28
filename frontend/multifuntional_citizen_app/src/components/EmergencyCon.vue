<template>
    <v-container>
      <h2>Emergency Contact Information</h2>
      <v-card>
          <v-card-title>Emergency Numbers</v-card-title>
          <v-list dense>
             <v-list-item v-for="contact in predefinedContacts" :key="contact.service" class="d-flex align-center">
                  <v-list-item-content>
                      <v-list-item-title>{{ contact.service }} Service</v-list-item-title>
                  </v-list-item-content>
                  <v-list-item-content>
                       <v-list-item-title>{{ contact.phone_number }}</v-list-item-title>
                  </v-list-item-content>
                  <v-list-item-action>
                        <v-btn icon @click="callNumber(contact.phone_number)">
                           <v-icon>mdi-phone</v-icon>
                        </v-btn>
                  </v-list-item-action>
              </v-list-item>
          </v-list>
      </v-card>

  
     
      <!-- <v-card>
        <v-card-title>Emergency Numbers</v-card-title>
        <v-list>
          
          <v-list-item v-for="contact in predefinedContacts" :key="contact.service">
            <v-list-item-content>
              <v-list-item-title>{{ contact.service }}</v-list-item-title>
              <v-list-item-subtitle>{{ contact.phone_number }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn icon @click="callNumber(contact.phone_number)">
                <v-icon>mdi-phone</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-card> -->
      <v-divider class="my-5"></v-divider>
  
      
      <v-card class="mt-5">
        <v-card-title>Personal Emergency Contacts</v-card-title>
        <v-form @submit.prevent="addContact">
          <v-text-field v-model="newContact.name" label="Name" required></v-text-field>
          <v-text-field v-model="newContact.phone_number" label="Phone Number" required></v-text-field>
          <v-text-field v-model="newContact.relationship" label="Relationship" required></v-text-field>
          <v-btn type="submit" color="primary" class="mt-3">Add Contact</v-btn>
        </v-form>
  
        <v-list class="mt-5">
          <v-list-item
            v-for="contact in personalContacts"
            :key="contact.id"
          >
            <v-list-item-content>
              <v-list-item-title>{{ contact.name }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ contact.phone_number }} - {{ contact.relationship }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn icon @click="deleteContact(contact.id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
              
  
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-card>
    </v-container>
  </template>
  
  
  
  <script>
  import axios from 'axios';
  
  axios.defaults.baseURL = 'http://localhost:5000';
  
  export default {
    data() {
      return {
        predefinedContacts: [],
        personalContacts: [],
        newContact: {
          name: '',
          phone_number: '',
          relationship: '',
        },
        userId: 1,
      };
    },
    methods: {
      fetchPredefinedContacts() {
        axios.get('/emergency/predefined')
          .then(response => {
            this.predefinedContacts = response.data;
          })
          .catch(error => {
            console.error('Error fetching predefined contacts:', error.response ? error.response.data : error);
            alert('Failed to load predefined contacts.');
          });
      },
      fetchPersonalContacts() {
        axios.get(`/emergency/personal/${this.userId}`)
          .then(response => {
            this.personalContacts = response.data.contacts || [];
          })
          .catch(error => {
            console.error('Error fetching personal contacts:', error.response ? error.response.data : error);
            alert('Failed to load personal contacts.');
          });
      },
      addContact() {
        const contact = { ...this.newContact, user_id: this.userId };
        axios.post('/emergency/personal', contact)
          .then(response => {
            alert(response.data.message);
            this.fetchPersonalContacts();
            this.newContact = { name: '', phone_number: '', relationship: '' };
          })
          .catch(error => {
            console.error('Error adding contact:', error.response ? error.response.data : error);
            alert('Failed to add contact.');
          });
      },
      deleteContact(contactId) {
        axios.delete(`/emergency/personal/${this.userId}/${contactId}`)
          .then(response => {
            alert(response.data.message);
            this.fetchPersonalContacts();
          })
          .catch(error => {
            console.error('Error deleting contact:', error.response ? error.response.data : error);
            alert('Failed to delete contact.');
          });
      },
      callNumber(phoneNumber) {
        alert(`Calling ${phoneNumber}...`);
      },
    },
    mounted() {
      this.fetchPredefinedContacts();
      this.fetchPersonalContacts();
    },
  };
  </script>
  

  <style scoped>
  .mt-5 {
    margin-top: 20px;
  }
  </style>
  