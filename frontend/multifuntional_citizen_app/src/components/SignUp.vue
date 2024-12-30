<template>
    <v-app>
      <v-container fluid class="fill-height gradient-background">
        <v-row justify="center" align="center">
          <v-col cols="12" sm="10" md="8" lg="6">
            <v-card ref="form" class="mx-auto pa-12 pb-8" elevation="8" width="448" rounded="lg">
              <v-card-text>
                <v-text-field
                  ref="name"
                  v-model="name"
                  :rules="[() => !!name || 'This field is required']"
                  label="Full Name"
                  placeholder="John Doe"
                  required
                ></v-text-field>
                <v-text-field
                  ref="address"
                  v-model="address"
                  :rules="[() => !!address || 'This field is required', () => !!address && address.length <= 25 || 'Address must be less than 25 characters']"
                  counter="25"
                  label="Address Line"
                  placeholder="Snowy Rock Pl"
                  required
                ></v-text-field>
                <v-text-field
                  ref="city"
                  v-model="city"
                  :rules="[() => !!city || 'This field is required']"
                  label="City"
                  placeholder="El Paso"
                  required
                ></v-text-field>
                <v-text-field
                  ref="nid"
                  v-model="nid"
                  :rules="[() => !!nid || 'This field is required', value => value.length === 10 || 'NID must be exactly 10 digits']"
                  label="National ID Number"
                  placeholder="1234567890"
                  type="text"
                  maxlength="10"
                  required
                ></v-text-field>
                <v-text-field
                  ref="dob"
                  v-model="dob"
                  :rules="[() => !!dob || 'This field is required']"
                  label="Date of Birth"
                  type="date"
                  required
                ></v-text-field>
                <v-text-field
                  ref="phone"
                  v-model="phone"
                  :rules="[() => !!phone || 'This field is required']"
                  label="Phone Number"
                  placeholder="123-456-7890"
                  required
                ></v-text-field>
                <v-text-field
                  ref="religion"
                  v-model="religion"
                  :rules="[() => !!religion || 'This field is required']"
                  label="Religion"
                  placeholder="e.g., Christianity"
                  required
                ></v-text-field>
                <v-radio-group
                  ref="gender"
                  v-model="gender"
                  :rules="[() => !!gender || 'This field is required']"
                  label="Gender"
                  required
                >
                  <v-radio label="Male" value="male"></v-radio>
                  <v-radio label="Female" value="female"></v-radio>
                </v-radio-group>
                <v-text-field
                  ref="email"
                  v-model="email"
                  :rules="[() => !!email || 'This field is required', value => /.+@.+\..+/.test(value) || 'E-mail must be valid']"
                  label="Email Address"
                  placeholder="example@domain.com"
                  required
                ></v-text-field>
              </v-card-text>
              <v-divider class="mt-12"></v-divider>
              <v-card-actions>
                <v-btn variant="text" @click="goToSignin">Cancel</v-btn>
                <v-spacer></v-spacer>
                <v-btn color="primary" variant="text" @click="continue">Continue</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-app>
  </template>
  
  <script>
  export default {
    data: () => ({
      countries: ['Afghanistan', 'Albania', 'Algeria', 'Bangladesh', 'United States', 'India', 'Canada'],
      name: '',
      address: '',
      city: '',
      nid: '',
      dob: '',
      phone: '',
      religion: '',
      gender: '',
      email: '',
      password: '',
    }),
  
    methods: {
      goToSignin() {
        this.$router.push({ name: 'signin' });
      },
      async submit() {
        const form = {
          name: this.name,
          address: this.address,
          city: this.city,
          nid: this.nid,
          dob: this.dob,
          phone: this.phone,
          religion: this.religion,
          gender: this.gender,
          email: this.email,
          password: this.password,
        };
        try {
          const response = await fetch('http://localhost:5000/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(form),
          });
          const data = await response.json();
          if (response.status === 201) {
            alert('Sign-up successful!');
            this.goToSignin();
          } else {
            alert(data.message);
          }
        } catch (error) {
          console.error(error);
          alert('An error occurred during sign-up.');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .gradient-background {
    background: url('@/assets/flag.png') no-repeat center center fixed;
    background-size: cover;
    height: 100vh;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
  }
  
  
  .fill-height {
    height: 100vh;
    overflow-y: auto;
    position: relative;
    z-index: 1;
  }
  </style>
  