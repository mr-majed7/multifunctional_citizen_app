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
                <v-autocomplete
                  ref="country"
                  v-model="country"
                  :items="countries"
                  :rules="[() => !!country || 'This field is required']"
                  label="Country"
                  placeholder="Select..."
                  required
                ></v-autocomplete>
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
                <v-btn color="primary" variant="text" @click="submit">Submit</v-btn>
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
      country: '',
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
          country: this.country,
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
  }
  
  
  .fill-height {
    height: 100vh;
  }
  </style>
  