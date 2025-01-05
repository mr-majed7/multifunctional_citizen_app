<template>
  <v-container fluid class="nid-upload-container">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" md="10" lg="8">
        <v-card class="nid-card" elevation="10">
          <v-card-title class="text-h4 font-weight-bold text-center py-4 primary white--text">
            Upload Your NID Card
          </v-card-title>
          <v-card-text class="pa-6">
            <v-row>
              <v-col cols="12">
                <v-file-input
                  v-model="uploadedFile"
                  label="Choose an Image"
                  accept="image/*"
                  outlined
                  dense
                  prepend-icon="mdi-file-image"
                  @change="handleFileUpload"
                  :clearable="true"
                  @click:clear="resetImagePreview"
                  :error-messages="fileError"
                  class="mb-4"
                ></v-file-input>
              </v-col>
              <v-col cols="12">
                <v-img
                  v-if="imagePreview"
                  :src="imagePreview"
                  max-width="100%"
                  max-height="600"
                  contain
                  class="mt-4 rounded-lg"
                >
                  <template v-slot:placeholder>
                    <v-row class="fill-height ma-0" align="center" justify="center">
                      <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    </v-row>
                  </template>
                </v-img>
              </v-col>
              <v-col cols="12" class="text-center">
                <v-btn
                  :disabled="!uploadedFile || isProcessing"
                  color="primary"
                  @click="processImage"
                  class="px-6 mt-4"
                  elevation="2"
                >
                  <v-icon left>mdi-shield-account</v-icon>
                  {{ isProcessing ? "Verifying NID..." : "Verify NID" }}
                  <v-progress-circular
                    v-if="isProcessing"
                    indeterminate
                    color="white"
                    size="20"
                    width="2"
                    class="ml-2"
                  ></v-progress-circular>
                </v-btn>

            </v-col>

            </v-row>
          </v-card-text>
        </v-card>

        <v-expand-transition>
          <v-card v-if="extractedData" class="mt-8 nid-card" elevation="10">
            <v-card-title class="text-h5 font-weight-bold text-center py-4 secondary white--text">
              Confirm Extracted Information
            </v-card-title>
            <v-card-text class="pa-6">
              <v-list>
                <v-list-item v-for="(value, key) in extractedData" :key="key">
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-medium">{{ key }}:</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">{{ value }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-card-actions class="pb-6 px-6">
              <v-spacer></v-spacer>
              <v-btn color="error" text @click="reset" class="mr-2">
                <v-icon left>mdi-refresh</v-icon>
                Retry
              </v-btn>
              <v-btn color="success" @click="confirmData" elevation="2">
                <v-icon left>mdi-check-circle</v-icon>
                Confirm
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-expand-transition>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar" :color="snackbarColor" top>
      {{ snackbarText }}
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from "axios";
import userData from "../data";

export default {
  data() {
    return {
      uploadedFile: null,
      imagePreview: null,
      isProcessing: false,
      extractedData: null,
      fileError: "",
      snackbar: false,
      snackbarText: "",
      snackbarColor: "success",
    };
  },
  methods: {
    handleFileUpload() {
      if (this.uploadedFile) {
        this.imagePreview = URL.createObjectURL(this.uploadedFile);
        this.fileError = "";
      }
    },
    resetImagePreview() {
      this.imagePreview = null;
    },
    async processImage() {
      if (!this.uploadedFile) {
        this.fileError = "Please select an image file";
        return;
      }

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
          Name: response.data.Name || "N/A",
          "Date of Birth": response.data["Date of Birth"] || "N/A",
          "NID Number": response.data["ID NO"] || "N/A",
        };
        this.showSnackbar("NID information extracted successfully", "success");
      } catch (error) {
        console.log("Error processing image:", error);
        this.showSnackbar("Failed to process the image. Please try again.", "error");
      } finally {
        this.isProcessing = false;
      }
    },
    confirmData() {
      const latestUserInput = userData[userData.length - 1];

      if (!latestUserInput) {
        this.showSnackbar("No user data found for comparison.", "error");
        return;
      }

      const normalizeDate = (date) => {
        try {
          const parsedDate = new Date(date);
          const year = parsedDate.getFullYear();
          const month = String(parsedDate.getMonth() + 1).padStart(2, "0"); // Months are 0-indexed
          const day = String(parsedDate.getDate()).padStart(2, "0");
          return `${year}-${month}-${day}`;
        } catch {
          return null; 
        }
      };

      const extractedDob = normalizeDate(this.extractedData["Date of Birth"]);
      const userDob = latestUserInput.dob.trim();

      const mismatches = [];

      if (
        latestUserInput.name.trim().toLowerCase() !==
        (this.extractedData.Name || "").trim().toLowerCase()
      ) {
        mismatches.push(
          `Name mismatch: Expected "${latestUserInput.name}", found "${this.extractedData.Name}"`
        );
      }

      if (userDob !== extractedDob) {
        mismatches.push(
          `Date of Birth mismatch: Expected "${userDob}", found "${this.extractedData["Date of Birth"]}"`
        );
      }

      if (latestUserInput.nid.trim() !== (this.extractedData["NID Number"] || "").trim()) {
        mismatches.push(
          `NID Number mismatch: Expected "${latestUserInput.nid}", found "${this.extractedData["NID Number"]}"`
        );
      }

      if (mismatches.length === 0) {
        this.showSnackbar("NID information matches successfully!", "success");
        this.handleSignup(); 
      } else {
        this.showSnackbar(mismatches.join("\n"), "error");
      }
    },
    async handleSignup() {
      try {
        const payload = userData[userData.length - 1];
        const response = await fetch('http://localhost:5000/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await response.json();

        if (response.status === 201) {
          alert('Sign-up successful!');
          this.$router.push('/');
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error('Sign-up error:', error);
        alert('An error occurred during sign-up.');
      }
    },
    reset() {
      this.uploadedFile = null;
      this.imagePreview = null;
      this.extractedData = null;
      this.fileError = "";
    },
    showSnackbar(text, color) {
      this.snackbarText = text;
      this.snackbarColor = color;
      this.snackbar = true;
    },
  },
};
</script>

<style scoped>
.nid-card {
  background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.nid-card:hover {
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

.v-list-item-subtitle {
  line-height: 1.5;
}


.v-img {
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.v-img:hover {
  border-color: #1976d2;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
