<template>
  <VApp>
    <header class="app-header">
      <div class="header-title">Citizen App</div>
      <nav class="header-nav">
        <VBtn flat>Home</VBtn>
        <VBtn flat>About Us</VBtn>
      </nav>
    </header>

    <VMain>
      <VContainer>
        <div class="voting-container">
          <h2 class="voting-title">Voting Window</h2>
          <div class="candidates-row">
            <div
              v-for="candidate in candidates"
              :key="candidate.id"
              class="candidate-logo"
              :style="{ backgroundImage: 'url(' + candidate.logoUrl + ')' }"
              @click="submitVote(candidate.id)"
            ></div>
          </div>
        </div>

        <VSnackbar v-model="snackbar" color="success" top>
          Your vote has been submitted!
          <template v-slot:action>
            <VBtn color="white" @click="snackbar = false">Close</VBtn>
          </template>
        </VSnackbar>
      </VContainer>
    </VMain>
  </VApp>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      snackbar: false,
      candidates: []
    };
  },
  methods: {
    async getCandidates() {
      try {
        const response = await axios.get('https://multifunctional-citizen-app-api.onrender.com/candidates');
        this.candidates = response.data; 
      } catch (error) {
        console.error('Error fetching candidates:', error);
      }
    },
    async submitVote(candidateId) {
      try {
        const response = await axios.post('https://multifunctional-citizen-app-api.onrender.com/vote', {
          candidate_id: candidateId
        });
        this.snackbar = true; 
      } catch (error) {
        console.error('Error submitting vote:', error);
        alert(error.response?.data?.message || 'Error submitting vote');
      }
    }
  },
  mounted() {
    this.getCandidates();
  }
};
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f5f5f5;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.header-nav {
  display: flex;
  gap: 10px;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}

.login-card {
  width: 400px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}


.voting-container {
  text-align: center;
  padding: 20px;
}

.voting-title {
  font-size: 1.8rem;
  color: red;
  margin-bottom: 20px;
}

.candidates-row {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.candidate-logo {
  width: 150px;
  height: 150px;
  background-size: cover;
  background-position: center;
  border: 2px solid #ccc;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}

.candidate-logo:hover {
  border-color: #000;
  transform: scale(1.1);
}


</style>
