<template>
    <v-container>
      <v-card class="mx-auto" max-width="600">
        <v-card-title>Uploaded Files</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item
              v-for="file in files"
              :key="file"
            >
              <v-list-item-content>
                <v-list-item-title>{{ file }}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn
                  icon
                  color="primary"
                  @click="downloadFile(file)"
                >
                  <v-icon>mdi-download</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
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
        files: [],
        message: "",
      };
    },
    mounted() {
      this.fetchFiles();
    },
    methods: {
      async fetchFiles() {
        try {
          const response = await axios.get("https://multifunctional-citizen-app-api.onrender.com/files");
          this.files = response.data;
        } catch (error) {
          console.error("Error fetching files:", error);
        }
      },
      async downloadFile(filename) {
        try {
          const response = await axios.get(
            `https://multifunctional-citizen-app-api.onrender.com/download/${filename}`,
            {
              responseType: "blob", 
            }
          );

          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", filename);
          document.body.appendChild(link);
          link.click();
          link.remove();
          this.message = `File '${filename}' downloaded successfully.`;
        } catch (error) {
          console.error("Error downloading file:", error);
          this.message = `Failed to download '${filename}'.`;
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