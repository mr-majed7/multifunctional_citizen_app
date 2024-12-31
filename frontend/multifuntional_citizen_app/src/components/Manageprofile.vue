<template>
  <v-app>
    <v-container>
      <v-card>
        <v-card-title>Edit Profile</v-card-title>
        <v-card-text>
        
          <div class="text-center profile-photo-container">
            <v-avatar
              v-if="profile.profile_photo"
              :size="150"
              class="mx-auto"
            >
              <v-img
                :src="'http://127.0.0.1:5000/uploads/' + profile.profile_photo"
                alt="Profile Photo"
              ></v-img>
            </v-avatar>
            <v-file-input
              label="Change Profile Photo"
              accept="image/*"
              class="mt-3"
              @change="uploadPhoto"
            ></v-file-input>
          </div>

        
          <v-form ref="form">
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="profile.first_name"
                  label="First Name"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="profile.last_name"
                  label="Last Name"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="profile.email"
                  label="Email"
                  type="email"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="profile.contact_number"
                  label="Contact Number"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="profile.address"
                  label="Address"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="profile.city"
                  label="City"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="profile.state"
                  label="State"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="profile.zip_code"
                  label="Zip Code"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="profile.country"
                  label="Country"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="saveChanges">Save Changes</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      profile: {},
    };
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/profile");
        console.log(response)
        this.profile = response.data;
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    },
    async saveChanges() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/profile"
        );
        alert(response.data.message);
      } catch (error) {
        console.error("Error saving profile:", error);
        alert("Failed to save profile changes. Please try again.");
      }
    },
    async uploadPhoto(event) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/profile/photo",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        alert(response.data.message);
        this.profile.profile_photo = response.data.photo;
      } catch (error) {
        console.error("Error uploading photo:", error);
        alert("Failed to upload photo. Please try again.");
      }
    },
  },
  watch: {
   
    "profile.profile_photo"(newValue) {
      if (newValue) {
        console.log("Profile photo updated to:", newValue);
        
      }
    },
  },
  mounted() {
    this.fetchProfile();
  },
};
</script>

<style scoped>
.text-center {
  text-align: center;
}

.profile-photo-container {
  margin-top: 20px; 
  margin-bottom: 20px; 
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
  display: block;
}

.mt-3 {
  margin-top: 20px;
}
</style>
