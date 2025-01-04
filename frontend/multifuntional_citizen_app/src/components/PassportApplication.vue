
<template>
    <div class="container">
      <h1>Passport Application Form</h1>
      
      
      <div v-if="currentStep === 1">
        <h2 style="color: blue;">Step 1: Passport Type</h2>
        <form @submit.prevent="submitStep1">
          <label for="passport_type">Passport Type:</label>
          <select v-model="form.passport_type" id="passport_type" required>
            <option value="Ordinary"> Ordinary</option>
            <option value="Official"> Official</option>
          </select>
  
          <label for="passport_pages">Passport Pages:</label>
          <select v-model="form.passport_pages" id="passport_pages" required>
            <option value="48"> 48</option>
            <option value="64"> 64</option>
          </select>
  
          <label for="years_validity">Years of validity:</label>
          <select v-model="form.years_validity" id="years_validity" required>
            <option value="5"> 5</option>
            <option value="10"> 10</option>
          </select>
  
          <label for="nid">NID/Birth certificate number:</label>
          <input v-model="form.nid" type="tel" id="nid" required />
  
          <label for="mobile_number">Mobile Phone Number:</label>
          <div>
            <select v-model="form.country_code" id="country_code">
              <option value="+880">BANGLADESH +880</option>
            </select>
            <input v-model="form.mobile_number" type="tel" id="mobile_number" required />
          </div>
  
          
          <button type="submit">Save and Continue</button>
        </form>
      </div>
  
      
      <div v-if="currentStep === 2">
        <h2 style="color: blue;">Step 2: Personal Information</h2>
        <form @submit.prevent="submitStep2">
          <label for="full_name">Full Name (as per NID/BRC):</label>
          <input v-model="form.full_name" type="text" id="full_name" required />
  
          <label for="given_name">Given Name (optional):</label>
          <input v-model="form.given_name" type="text" id="given_name" />
  
          <label for="surname">Surname:</label>
          <input v-model="form.surname" type="text" id="surname" required />
  
          
          <label for="gender">Gender:</label>
          <select v-model="form.gender" id="gender" required>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Others">Others</option>
          </select>
  
          <label for="marital_status">Marital Status:</label>
          <select v-model="form.marital_status" id="marital_status" required>
            <option value="Married">Married</option>
            <option value="Unmarried">Unmarried</option>
            <option value="Divorced">Divorced</option>
          </select>
  
          <label for="profession">Profession:</label>
          <input v-model="form.profession" type="text" id="profession" required />
  
          <label for="religion">Religion:</label>
          <input v-model="form.religion" type="text" id="religion" required />
  
          <label for="email">Email:</label>
          <input v-model="form.email" type="email" id="email" required />
  
          <label for="password">Password:</label>
          <input v-model="form.password" type="password" id="password" required />
  
          <button type="submit">Save and Continue</button>
        </form>
      </div>
  
      
      <div v-if="currentStep === 3">
        <h2 style="color: blue;">Step 3: Address Information</h2>
        <form @submit.prevent="submitStep3">
          <h3>Permanent Address</h3>
          <label for="permanent_country">Country:</label>
          <input v-model="form.permanent_country" type="text" id="permanent_country" required />
  
          <label for="permanent_district">District:</label>
          <input v-model="form.permanent_district" type="text" id="permanent_district" required />
  
          <label for="permanent_city">City:</label>
          <input v-model="form.permanent_city" type="text" id="permanent_city" required />
  
          <label for="permanent_post_office">Post Office:</label>
          <input v-model="form.permanent_post_office" type="text" id="permanent_post_office" required />
  
          <label>
            <input type="checkbox" v-model="sameAddress" @change="autoFillAddress" />
            Present address is the same as permanent address
          </label>
  
          <h3>Present Address (Optional)</h3>
          <label for="present_country">Country:</label>
          <input v-model="form.present_country" type="text" id="present_country" />
  
          <label for="present_district">District:</label>
          <input v-model="form.present_district" type="text" id="present_district" />
  
          <label for="present_city">City:</label>
          <input v-model="form.present_city" type="text" id="present_city" />
  
          <label for="present_post_office">Post Office:</label>
          <input v-model="form.present_post_office" type="text" id="present_post_office" />
  
          <button type="submit">Save and Continue</button>
        </form>
      </div>
  
      
      <div v-if="currentStep === 4">
        <h2 style="color: blue;">Step 4: Family Information</h2>
        <form @submit.prevent="submitStep4">
          <h3>Father's Information</h3>
          <label for="father_name">Father's Name:</label>
          <input v-model="form.father_name" type="text" id="father_name" required />
  
          <label for="father_profession">Father's Profession:</label>
          <input v-model="form.father_profession" type="text" id="father_profession" required />
  
          <label for="father_nid">Father's NID:</label>
          <input v-model="form.father_nid" type="text" id="father_nid" required />
  
          <h3>Mother's Information</h3>
          <label for="mother_name">Mother's Name:</label>
          <input v-model="form.mother_name" type="text" id="mother_name" required />
  
          <label for="mother_profession">Mother's Profession:</label>
          <input v-model="form.mother_profession" type="text" id="mother_profession" required />
  
          <label for="mother_nid">Mother's NID:</label>
          <input v-model="form.mother_nid" type="text" id="mother_nid" required />
  
          <button type="submit">Submit Application</button>
        </form>
      </div>
  
      <div v-if="currentStep === 5">
        <h2 style="color: green;">Thank You!</h2>
        <p>You are done with your Passport Application.</p>
        <button @click="downloadReceipt">Download Receipt</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        currentStep: 1,
        applicationId: null,
        sameAddress: false,
        form: {
          passport_type: "",
          passport_pages: "",
          years_validity: "",
          nid: "",
          mobile_number: "",
          country_code: "+880",
          gender: "",
          marital_status: "",
          full_name: "",
          given_name: "",
          surname: "",
          profession: "",
          religion: "",
          email: "",
          password: "",
          permanent_country: "",
          permanent_district: "",
          permanent_city: "",
          permanent_post_office: "",
          present_country: "",
          present_district: "",
          present_city: "",
          present_post_office: "",
          father_name: "",
          father_profession: "",
          father_nid: "",
          mother_name: "",
          mother_profession: "",
          mother_nid: "",
        },
      };
    },
    methods: {
    autoFillAddress() {
      if (this.sameAddress) {
        this.form.present_country = this.form.permanent_country;
        this.form.present_district = this.form.permanent_district;
        this.form.present_city = this.form.permanent_city;
        this.form.present_post_office = this.form.permanent_post_office;
      } else {
        this.form.present_country = "";
        this.form.present_district = "";
        this.form.present_city = "";
        this.form.present_post_office = "";
      }
    },
    async submitStep1() {
      try {
        console.log("Submitting Step 1 data:", this.form);
        this.currentStep = 2;
      } catch (error) {
        console.error("Error submitting Step 1:", error.message);
      }
    },
    async submitStep2() {
      try {
        console.log("Submitting Step 2 data:", this.form);
        this.currentStep = 3;
      } catch (error) {
        console.error("Error submitting Step 2:", error.message);
      }
    },
    async submitStep3() {
      try {
        console.log("Submitting Step 3 data:", this.form);
        this.currentStep = 4;
      } catch (error) {
        console.error("Error submitting Step 3:", error.message);
      }
    },
    async submitStep4() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/submit_application", this.form);
        this.applicationId = response.data.id;
        this.receiptPath = response.data.receipt_path;
        this.currentStep = 5;
      } catch (error) {
        console.error("Error submitting application:", error.message);
      }
    },
    async downloadReceipt() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/download-receipt", {
          params: { path: this.receiptPath },
          responseType: "blob",
        });
  
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `receipt_${this.applicationId}.txt`);
        document.body.appendChild(link);
        link.click();
      } catch (error) {
        console.error("Error downloading receipt:", error.message);
      }
    },
  },
  
  };
  </script>
  
  
  <style scoped>
  .container {
    background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    padding: 20px;
    color: #e0e0e0;
    max-width: 600px;
    margin: 0 auto;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  }
  
  h1, h2, h3 {
    color: #ffffff;
    text-align: center;
    margin-bottom: 20px;
  }
  
  form {
    display: flex;
    flex-direction: column;
  }
  
  label {
    margin-bottom: 5px;
    font-weight: bold;
    color: #e0e0e0;
  }
  
  input,
  select,
  textarea {
    margin-bottom: 15px;
    padding: 10px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 4px;
    font-size: 16px;
    background-color: rgba(255, 255, 255, 0.1);
    color: #e0e0e0;
  }
  
  button {
    padding: 10px;
    border-radius: 4px;
    font-size: 16px;
    background-color: #007bff;
    color: #fff;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
    text-transform: none;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  button:active {
    background-color: #003f7f;
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
  
  /* Add some spacing between form sections */
  h2 {
    margin-top: 30px;
  }
  
  /* Style for the checkbox */
  input[type="checkbox"] {
    margin-right: 10px;
  }
  
  /* Style for the success message */
  .v-card__text {
    color: #4caf50;
    font-weight: bold;
  }
  
  /* Responsive adjustments */
  @media (max-width: 600px) {
    .container {
      width: 100%;
      border-radius: 0;
    }
  }
  </style>
  
  