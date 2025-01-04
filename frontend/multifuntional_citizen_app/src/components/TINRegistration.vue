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
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  .title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
  }
  .subtitle {
    font-size: 14px;
    text-align: center;
    color: #555;
    margin-bottom: 20px;
  }
  .form-group {
    margin-bottom: 15px;
  }
  .form-control {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-top: 5px;
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
  }
  .btn:hover {
    background-color: #45a049;
  }
  .status-section {
    margin-top: 20px;
    padding: 10px;
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 4px;
  }
  .status-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  </style>
  