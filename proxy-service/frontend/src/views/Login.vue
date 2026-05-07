<template>
  <v-row justify="center">
    <v-col cols="12" sm="8" md="6">
      <v-card>
        <v-card-title class="text-h5">Login</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="login">
            <v-text-field
              v-model="form.email"
              label="Email"
              type="email"
              required
            ></v-text-field>
            
            <v-text-field
              v-model="form.password"
              label="Password"
              type="password"
              required
            ></v-text-field>
            
            <v-btn type="submit" color="primary" block :loading="loading">
              Login
            </v-btn>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <router-link to="/register">Don't have an account? Register</router-link>
        </v-card-actions>
      </v-card>
      
      <v-snackbar v-model="snackbar.show" :color="snackbar.color">
        {{ snackbar.text }}
      </v-snackbar>
    </v-col>
  </v-row>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      loading: false,
      snackbar: {
        show: false,
        text: '',
        color: 'error'
      }
    }
  },
  methods: {
    async login() {
      this.loading = true
      try {
        const response = await axios.post('/api/login', this.form)
        localStorage.setItem('token', response.data.access_token)
        this.$emit('login')
      } catch (error) {
        this.snackbar = {
          show: true,
          text: error.response?.data?.detail || 'Login failed',
          color: 'error'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>