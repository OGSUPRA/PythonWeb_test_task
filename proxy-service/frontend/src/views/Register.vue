<template>
  <v-row justify="center">
    <v-col cols="12" sm="8" md="6">
      <v-card>
        <v-card-title class="text-h5">Register</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="register">
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
            
            <v-text-field
              v-model="form.confirm_password"
              label="Confirm Password"
              type="password"
              required
            ></v-text-field>
            
            <v-btn type="submit" color="primary" block :loading="loading">
              Register
            </v-btn>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <router-link to="/login">Already have an account? Login</router-link>
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
        password: '',
        confirm_password: ''
      },
      loading: false,
      snackbar: {
        show: false,
        text: '',
        color: 'success'
      }
    }
  },
  methods: {
    async register() {
      this.loading = true
      try {
        await axios.post('/api/register', this.form)
        this.snackbar = {
          show: true,
          text: 'Registration successful! Check your email for activation key.',
          color: 'success'
        }
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
      } catch (error) {
        this.snackbar = {
          show: true,
          text: error.response?.data?.detail || 'Registration failed',
          color: 'error'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>