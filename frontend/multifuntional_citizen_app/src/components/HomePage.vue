<template>
    <v-app>
        <v-app-bar color="#0d1117" dark app>
            <v-toolbar-title>Citizen App</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn class="mx-2" color="primary" variant="tonal" ripple @click="logout">
                Logout
            </v-btn>
            <v-btn class="mx-2" color="primary" variant="tonal" ripple @click="goToHome">
                Home
            </v-btn>
            <v-btn class="mx-2" color="primary" variant="tonal" ripple @click="giveFeedback">
                Feedback
            </v-btn>
        </v-app-bar>
        <v-main>
            <v-container fluid class="background-container pa-0">
                <v-layout>
                    <v-navigation-drawer
                        v-model="drawer"
                        :rail="rail"
                        permanent
                        class="elevation-2 full-height no-gap"
                        @click="rail = false"
                    >
                        <v-list-item
                            prepend-avatar="/citizen_logo.png"
                            title="Welcome To Citizen App"
                        >
                            <template v-slot:append>
                                <v-btn icon variant="text" @click.stop="rail = !rail">
                                    <v-icon>{{ rail ? 'mdi-chevron-left' : 'mdi-chevron-right' }}</v-icon>
                                </v-btn>
                            </template>
                        </v-list-item>

                        <v-divider></v-divider>

                        <v-list dense nav>
                            <v-list-item prepend-icon="mdi-update" title="Edit Profile" ripple @click="goToHome"></v-list-item>
                            <v-list-item prepend-icon="mdi-file-document-edit" title="Update Document" ripple @click="this.$router.push('/doc_correction')"></v-list-item>
                            <v-list-item prepend-icon="mdi-numeric" title="Important Numbers" ripple @click="goToHome"></v-list-item>
                        </v-list>
                    </v-navigation-drawer>

                    <v-main>
                        <v-container fluid>
                            <v-row dense>
                                <v-col
                                    v-for="(image, index) in images.slice(0, 3)"
                                    :key="index"
                                    cols="4"
                                    class="d-flex flex-column align-center"
                                >
                                    <v-card class="pa-0 large-square-card" outlined>
                                        <v-img
                                            :src="require(`@/assets/${image.src}`)"
                                            class="m-0"
                                            cover
                                        ></v-img>
                                    </v-card>

                                    <v-btn
                                        color="primary"
                                        ripple
                                        @click="navigateToPage(image.path)"
                                        small
                                        class="mt-2"
                                    >
                                        {{ image.name }}
                                    </v-btn>
                                </v-col>
                            </v-row>



                            <v-divider class="my-4" :thickness="3" color="info"></v-divider>

                            <v-row dense>
                                <v-col
                                    v-for="(image, index) in images.slice(3, 6)"
                                    :key="index"
                                    cols="4"
                                    class="d-flex flex-column align-center"
                                    >
                                    <v-card class="pa-0 large-square-card" outlined>
                                        <v-img
                                        :src="require(`@/assets/${image.src}`)"
                                        class="m-0"
                                        cover
                                        ></v-img>
                                    </v-card>

                                    <v-btn
                                        color="primary"
                                        ripple
                                        @click="navigateToPage(image.path)"
                                        small
                                        class="mt-2"
                                    >
                                        {{ image.name }}
                                    </v-btn>
                                </v-col>
                            </v-row>
                            <!-- Divider After First Row -->
                            <v-divider class="my-4" :thickness="3" color="info"></v-divider>

                            <!-- Second Row: Next Three Images -->
                            <v-row dense>
                                <v-col
                                    v-for="(image, index) in images.slice(6, 9)"
                                    :key="index"
                                    cols="4"
                                    class="d-flex flex-column align-center"
                                >
                                    <!-- Large Square Card -->
                                    <v-card class="pa-0 large-square-card" outlined>
                                        <v-img
                                            :src="require(`@/assets/${image.src}`)"
                                            class="m-0"
                                            cover
                                        ></v-img>
                                    </v-card>

                                    <!-- Button Below Image -->
                                    <v-btn
                                        color="primary"
                                        ripple
                                        @click="navigateToPage(image.path)"
                                        small
                                        class="mt-2"
                                        >
                                        {{ image.name }}
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-main>
                </v-layout>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
export default  {
    data() {
        return {
            drawer: true,
            rail: true,
            images: [
                { src: "utbill.png", name: "Utility Payment",path:"/utbill" },
                { src: "votesystem.png", name: "Vote",path:"/votesystem" },
                { src: "Documents.png", name: "Documents",path: "/listfiles"},
                { src: "Income_tax.png", name: "Income Tax",path:"/income_tax" },
                { src: "Property_tax.png", name: "Property Tax",path: "/propertytax" },
                { src: "E_nomination.png", name: "E-Nomination",path: "/e-nomination" },
                { src: "Passport.jpg", name: "Passport Application", path: "/passportapplication" },
                { src: "traffic_fine.jpg", name: "Traffic Fine",path: "/trafficfine" },
                { src: "Complaint.jpg", name: "Complaint", path: "/complaints" } 
            ],
        };
    },
    methods: {
        logout() {
            alert("Logged out!");
            this.$router.push("/");
        },
        goToHome() {
            alert("Navigating to Home!");
            this.$router.push("/home");
            },
            giveFeedback() {
        
        this.$router.push('/feedback'); 
        },
        navigateToPage(path) {
        if (path) {
            this.$router.push(path);
        } else {
            console.error("Path not defined for this image.");
            alert("Path not defined for this image!");
        }
    },
    },
};
</script>

<style scoped>
.no-gap {
    margin: 0;
    padding: 0;
}


.background-container {
  background: url("../assets/background.jpg");
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background: linear-gradient(135deg, #344f36 0%, #701717 100%);
  min-height: 100vh;
}


.full-height {
  height: 100vh;
}
.v-app-bar{
    margin: 0;
    padding: 0;
    width: 100%
}
.large-square-card {
  width: 300px; 
  height: 300px; 
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.v-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.my-4 {
  margin: 16px 0;
}
</style>