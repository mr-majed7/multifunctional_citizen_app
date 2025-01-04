<template>
    <v-container>
      <v-card class="mx-auto" max-width="600">
        <v-card-title>File Upload</v-card-title>
        <v-card-text>
          <v-file-input
            v-model="file"
            label="Select a file"
            accept="/"
            outlined
          ></v-file-input>
          <v-btn color="primary" @click="uploadFile" :disabled="!file">
            Upload
          </v-btn>
          <v-alert
            v-if="message"
            type="success"
            class="mt-4"
            transition="scale-transition"
          >
            {{ message }}
          </v-alert>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        file: null,
        message: "",
      };
    },
    methods: {
      async uploadFile() {
        if (!this.file) return;
        const formData = new FormData();
        formData.append("file", this.file);
  
        try {
          const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
          this.message = response.data.message;
          this.file = null; 
        } catch (error) {
          this.message = "Upload failed. Please try again.";
          console.error(error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  v-container {
    margin-top: 50px;
  }
  </style>