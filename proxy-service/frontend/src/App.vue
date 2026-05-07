<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Proxy Service</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="isLoggedIn" @click="logout" text>Logout</v-btn>
    </v-app-bar>
    
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false
    }
  },
  mounted() {
    this.syncAuthState()
  },
  watch: {
    $route() {
      this.syncAuthState()
    }
  },
  methods: {
    syncAuthState() {
      this.isLoggedIn = !!localStorage.getItem('token')
    },
    logout() {
      localStorage.removeItem('token')
      this.syncAuthState()
      this.$router.push('/login')
    }
  }
}
</script>
