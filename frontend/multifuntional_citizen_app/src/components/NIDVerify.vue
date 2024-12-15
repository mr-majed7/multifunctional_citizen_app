<template>
    <v-container class="mt-5">
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card outlined>
            <v-card-title class="text-h5">Upload Your NID Card</v-card-title>
            <v-card-text>
              <v-file-input
                v-model="uploadedFile"
                label="Choose an Image"
                accept="image/*"
                outlined
                @change="handleFileUpload"
              ></v-file-input>
              <v-img
                v-if="imagePreview"
                :src="imagePreview"
                max-width="100%"
                class="mt-4"
              ></v-img>
            </v-card-text>
            <v-card-actions>
              <v-btn
                :disabled="!uploadedFile || isProcessing"
                color="primary"
                @click="processImage"
              >
                <v-progress-circular
                  v-if="isProcessing"
                  indeterminate
                  color="primary"
                  size="20"
                  class="mr-2"
                ></v-progress-circular>
                {{ isProcessing ? "Verifying NID..." : "Verify NID" }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
  
      <v-row v-if="extractedData" justify="center" class="mt-5">
        <v-col cols="12" md="8">
          <v-card outlined>
            <v-card-title class="text-h5">Confirm Extracted Information</v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>Name:</v-list-item-title>
                    <v-list-item-subtitle>{{ extractedData.name }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>Date of Birth:</v-list-item-title>
                    <v-list-item-subtitle>{{ extractedData.dob }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>NID Number:</v-list-item-title>
                    <v-list-item-subtitle>{{ extractedData.nidNumber }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-card-actions>
              <v-btn color="success" @click="confirmData">Confirm</v-btn>
              <v-btn color="error" @click="reset">Retry</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
import axios from "axios";
  
  export default {
    data() {
      return {
        uploadedFile: null,
        imagePreview: null,
        isProcessing: false,
        extractedData: null,
      };
    },
    methods: {
      handleFileUpload() {
        if (this.uploadedFile) {
          this.imagePreview = URL.createObjectURL(this.uploadedFile);
        }
      },
      async processImage() {
        if (!this.uploadedFile) return;
  
        this.isProcessing = true;
  
        const formData = new FormData();
        formData.append("image", this.uploadedFile);
  
        try {
          const response = await axios.post("http://127.0.0.1:5000/detect-text", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
          console.log("Response data:", response.data);
          this.extractedData = {
            name: response.data.Name || "N/A",
            dob: response.data["Date of Birth"] || "N/A",
            nidNumber: response.data["ID NO"] || "N/A",
          };
        } catch (error) {
          console.log("Error processing image:", error);
          alert("Failed to process the image. Please try again.");
        } finally {
          this.isProcessing = false;
        }
      },
      confirmData() {
        this.$router.push("/home"); 
      },
      reset() {
        this.uploadedFile = null;
        this.imagePreview = null;
        this.extractedData = null;
      },
    },
  };
  </script>
  
  <style>
  .v-card {
    transition: box-shadow 0.3s ease-in-out;
  }
  .v-card:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }
  </style>
  