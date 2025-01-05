<template>
    <div class="container">
      <h1>Property Tax Filing and Payment</h1>
      
      <form v-if="!formSubmitted" @submit.prevent="handleSubmit">
      <p>Please provide the necessary details to file your property tax.</p>
        
        <div class="form-group">
          <label for="propertyType">Property Type (O, P, F)*</label>
          <select
            v-model="formData.propertyType"
            id="propertyType"
            class="form-control"
            required
          >
            <option value="">-- Select Property Type --</option>
            <option value="O">O</option>
            <option value="P">P</option>
            <option value="F">F</option>
          </select>
        </div>
  
        
        <div class="form-group">
          <label for="sectionId">Section ID*</label>
          <input
            type="text"
            v-model="formData.sectionId"
            id="sectionId"
            class="form-control"
            maxlength="1"
            required
          />
        </div>
  
        
        <div class="form-group">
          <label for="pethId">Peth ID*</label>
          <input
            type="text"
            v-model="formData.pethId"
            id="pethId"
            class="form-control"
            maxlength="2"
            required
          />
        </div>
  
        
        <div class="form-group">
          <label for="accountNo">Account Number*</label>
          <input
            type="text"
            v-model="formData.accountNo"
            id="accountNo"
            class="form-control"
            maxlength="8"
            required
          />
        </div>
  
        
        <div class="form-group">
          <label for="name">Name*</label>
          <input
            type="text"
            v-model="formData.name"
            id="name"
            class="form-control"
            required
          />
        </div>
  
        
        <div class="form-group">
          <label for="address">Address*</label>
          <textarea
            v-model="formData.address"
            id="address"
            class="form-control"
            rows="3"
            required
          ></textarea>
        </div>
  
        
        <div class="form-group">
          <label for="propertyDescription">Property Description*</label>
          <textarea
            v-model="formData.propertyDescription"
            id="propertyDescription"
            class="form-control"
            rows="3"
            required
          ></textarea>
        </div>
  
        
        <div class="form-group">
          <label for="mobile">Mobile No*</label>
          <input
            type="text"
            v-model="formData.mobile"
            id="mobile"
            class="form-control"
            maxlength="11"
            required
          />
        </div>
  
        <div class="form-group">
          <label for="email">Email*:</label>
          <input
            type="email"
            v-model="formData.email"
            id="email"
            class="form-control"
            
            required
          />
        </div>
  
            
  
        <div class="form-group">
          <label for="year">Year*</label>
          <select v-model="formData.year" id="year" class="form-control" required>
            <option value="">-- Select Year --</option>
            <option v-for="year in years" :key="year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>
  
        
        <div class="form-group">
          <label for="amount">Amount (Taka)*</label>
          <input
            type="number"
            v-model="formData.amount"
            id="amount"
            class="form-control"
            required
          />
        </div>
  
        
        <div class="form-group">
          <label for="documents">Upload Documents</label>
          <input
            type="file"
            @change="handleFileChange"
            id="documents"
            class="form-control"
          />
        </div>
  
        
        <div class="buttons">
          <button type="submit" class="btn submit-btn">Submit</button>
        </div>
      </form>
  
      
      <div v-else class="message">
        <h2>Thank You</h2>
        <p>Your form has been successfully submitted.</p>
        <button @click="downloadReceipt" class="btn submit-btn">
          Download Receipt
        </button>
      </div>
  
      
      <div v-if="error" class="error-message">
        <h2>Error</h2>
        <p>{{ error }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        formSubmitted: false,
        formData: {
          propertyType: "",
          sectionId: "",
          pethId: "",
          accountNo: "",
          name: "",
          address: "",
          propertyDescription: "",
          mobile: "",
          email: "",
          year: "",
          amount: "",
          documents: null,
        },
        years: Array.from(
          { length: 20 },
          (_, i) => new Date().getFullYear() - i
        ),
        error: null,
      };
    },
    methods: {
      handleFileChange(event) {
        this.formData.documents = event.target.files[0];
      },
      async handleSubmit() {
           try {
              const formData = new FormData();
              Object.keys(this.formData).forEach((key) => {
                if (key !== 'documents') {
                  formData.append(key, this.formData[key]);
                } else if (this.formData.documents) {
                  formData.append(key, this.formData.documents);
                }
              });
  
                 const response = await fetch('https://multifunctional-citizen-app-api.onrender.com/api/property-tax', {
                   method: 'POST',
                   body: formData,
                 });
  
                  if (!response.ok) {
                    throw new Error('Failed to submit the form');
                  }
  
                  const result = await response.json();
                  if (result.error) {
                    throw new Error(result.error);
                  }
  
                  this.formSubmitted = true;
                } catch (err) {
                  this.error = err.message;
                }
       },
       async fetchRecords() {
        try {
          const response = await fetch('https://multifunctional-citizen-app-api.onrender.com/api/records');
          if (!response.ok) {
            throw new Error('Failed to fetch records');
          }
  
          this.records = await response.json();
        } catch (err) {
          this.error = err.message;
        }
      },
  
      downloadReceipt() {
        const receiptData = `
          Property Type: ${this.formData.propertyType}
          Section ID: ${this.formData.sectionId}
          Peth ID: ${this.formData.pethId}
          Account No: ${this.formData.accountNo}
          Name: ${this.formData.name}
          Address: ${this.formData.address}
          Property Description: ${this.formData.propertyDescription}
          Mobile No: ${this.formData.mobile}
          Email: ${this.formData.email}
          Year: ${this.formData.year}
          Amount: ${this.formData.amount} Taka
        `;
        const blob = new Blob([receiptData], { type: "text/plain" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "PropertyTaxReceipt.txt";
        link.click();
      },
    },
  };
  </script>
  
  <style scoped>
  body {
    font-family: Arial, sans-serif;
    background-color: #121212;
    color: #e0e0e0;
  }
  
  .container {
    max-width: 600px;
    margin: 50px auto;
    padding: 40px;
    border-radius: 16px;
    background: linear-gradient(135deg, #12100e 0%, #2b4162 100%);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  }
  
  h1 {
    text-align: center;
    color: #ffffff;
    margin-bottom: 20px;
  }
  
  label {
    font-weight: bold;
    color: #e0e0e0;
    margin-bottom: 5px;
    display: block;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-control {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 4px;
    background-color: rgba(255, 255, 255, 0.1);
    color: #e0e0e0;
    font-size: 16px;
  }
  
  .btn {
    display: block;
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    text-align: center;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    text-transform: none;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  
  .btn:hover {
    background-color: #0056b3;
  }
  
  .btn:active {
    background-color: #003f7f;
  }
  
  .message {
    margin-top: 20px;
    padding: 10px;
    background-color: rgba(212, 237, 218, 0.1);
    color: #4caf50;
    border: 1px solid rgba(195, 230, 203, 0.3);
    border-radius: 4px;
    text-align: center;
  }
  
  /* Vuetify-specific styles */
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
      padding: 20px;
    }
  }
  </style>
  
  