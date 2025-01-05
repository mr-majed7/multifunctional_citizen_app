<template>
    <div class="container">
      <div>
        <h1 class="title">TIN Registration</h1>
        <p class="subtitle">Apply for your Taxpayer Identification Number (TIN).</p>
        <form v-if="!applicationSubmitted" @submit.prevent="handleTINRegistration" class="form">
  
          <div class="form-group">
            <label for="name">Full Name*</label>
            <input
              v-model="tinData.name"
              id="name"
              class="form-control"
              type="text"
              placeholder="Enter your full name"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="nationalID">National ID*</label>
            <input
              v-model="tinData.nationalID"
              id="nationalID"
              class="form-control"
              type="text"
              placeholder="Enter your National ID"
              required
            />
          </div>
           <div class="form-group">
            <label for="address">Address*</label>
            <textarea
              v-model="tinData.address"
              id="address"
              class="form-control"
              rows="3"
              placeholder="Enter your address"
              required
            ></textarea>
          </div>
  
          <div class="form-group">
            <label for="phone">Phone Number*</label>
            <input
              v-model="tinData.phone"
              id="phone"
              class="form-control"
              type="text"
              placeholder="Enter your phone number"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="documents">Upload Supporting Documents</label>
            <input
              ref="tinFileInput"
              id="documents"
              class="form-control"
              type="file"
              @change="handleTINFileUpload"
            />
          </div>
  
          <button class="btn submit-btn" type="submit">Apply for TIN</button>
        </form>
  
  
        <div v-else class="confirmation-message">
          <h2>Your Application is Done</h2>
          
          <p>Your TIN number is: <strong>{{ tinNumber }}</strong></p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        tinData: {
          name: "",
          nationalID: "",
          address: "",
          phone: "",
        },
        tinFile: null,
        applicationSubmitted: false,
        tinNumber: "", 
      };
    },
    methods: {
      async handleTINRegistration() {
    const formData = new FormData();
    formData.append("name", this.tinData.name);
    formData.append("nationalID", this.tinData.nationalID);
    formData.append("address", this.tinData.address);
    formData.append("phone", this.tinData.phone);
  
    if (this.tinFile) {
      formData.append("documents", this.tinFile);
    } else {
      alert("Please upload a valid document.");
      return;
    }
  
    try {
      const response = await fetch("http://localhost:5000/api/tin/register", {
        method: "POST",
        body: formData,
      });
  
      const data = await response.json();
      if (response.ok) {
        this.tinNumber = data.tinNumber; 
        this.applicationSubmitted = true;
      } else {
        alert(data.error || "Failed to submit TIN application. Please try again.");
      }
    } catch (error) {
      console.error("Error submitting TIN application:", error);
      alert("An error occurred while submitting the application.");
    }
  },
      handleTINFileUpload(event) {
        this.tinFile = event.target.files[0];
      },
    },
  };
  
  
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: 50px auto;
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  }
  
  .title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
    color: #ffffff;
  }
  
  .subtitle {
    font-size: 14px;
    text-align: center;
    color: #e0e0e0;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-control {
    width: 100%;
    padding: 10px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 4px;
    margin-top: 5px;
    background-color: rgba(255, 255, 255, 0.1);
    color: #e0e0e0;
  }
  
  .btn {
    display: inline-block;
    width: 100%;
    padding: 10px;
    font-size: 16px;
    font-weight: bold;
    text-align: center;
    color: #fff;
    background-color: #4CAF50;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
    transition: background-color 0.3s ease;
  }
  
  .btn:hover {
    background-color: #45a049;
  }
  
  .status-section {
    margin-top: 20px;
    padding: 10px;
    background-color: rgba(212, 237, 218, 0.1);
    border: 1px solid rgba(195, 230, 203, 0.3);
    border-radius: 4px;
  }
  
  .status-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
    color: #4caf50;
  }
  
  /* Vuetify-specific styles */
  .v-card {
    background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
    border-radius: 16px;
    overflow: hidden;
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
  
  /* Responsive adjustments */
  @media (max-width: 600px) {
    .container {
      margin: 0;
      border-radius: 0;
    }
  }
  </style>
  
  