<template>
  <v-row justify="center">
    <v-col cols="12" md="8">
      <v-card>
        <v-card-title>Profile</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item>
              <v-list-item-title>Email</v-list-item-title>
              <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
            </v-list-item>
            
            <v-list-item>
              <v-list-item-title>Activation Key</v-list-item-title>
              <v-list-item-subtitle>
                {{ user.activation_key || 'No active key' }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <v-alert
            type="info"
            variant="tonal"
            class="my-4"
            text="Use this key in the desktop client to get a proxy server and receive real-time connection status."
          ></v-alert>

          <v-btn
            v-if="user.activation_key"
            class="mb-4"
            color="secondary"
            variant="outlined"
            @click="copyActivationKey"
          >
            Copy Activation Key
          </v-btn>
          
          <v-divider class="my-4"></v-divider>
          
          <v-btn @click="refreshKey" color="warning" :loading="refreshing">
            Refresh Key (send to email)
          </v-btn>
          
          <v-divider class="my-4"></v-divider>
          
          <v-form @submit.prevent="changePassword">
            <v-text-field
              v-model="passwordForm.old_password"
              label="Old Password"
              type="password"
              required
            ></v-text-field>
            
            <v-text-field
              v-model="passwordForm.new_password"
              label="New Password"
              type="password"
              required
            ></v-text-field>
            
            <v-btn type="submit" color="primary" :loading="changingPassword">
              Change Password
            </v-btn>
          </v-form>
        </v-card-text>
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
      user: {
        email: '',
        activation_key: null
      },
      passwordForm: {
        old_password: '',
        new_password: ''
      },
      refreshing: false,
      changingPassword: false,
      snackbar: {
        show: false,
        text: '',
        color: 'success'
      }
    }
  },
  mounted() {
    this.loadProfile()
  },
  methods: {
    getAuthHeader() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },
    async loadProfile() {
      try {
        const response = await axios.get('/api/profile', {
          headers: this.getAuthHeader()
        })
        this.user = response.data
      } catch (error) {
        if (error.response?.status === 401) {
          this.$router.push('/login')
        }
      }
    },
    async refreshKey() {
      this.refreshing = true
      try {
        const response = await axios.post('/api/refresh-key', {}, {
          headers: this.getAuthHeader()
        })
        this.user.activation_key = response.data.activation_key
        this.snackbar = {
          show: true,
          text: 'New activation key sent to your email!',
          color: 'success'
        }
      } catch (error) {
        this.snackbar = {
          show: true,
          text: error.response?.data?.detail || 'Failed to refresh key',
          color: 'error'
        }
      } finally {
        this.refreshing = false
      }
    },
    async copyActivationKey() {
      if (!this.user.activation_key) {
        return
      }

      try {
        await navigator.clipboard.writeText(this.user.activation_key)
        this.snackbar = {
          show: true,
          text: 'Activation key copied to clipboard!',
          color: 'success'
        }
      } catch (error) {
        this.snackbar = {
          show: true,
          text: 'Failed to copy activation key',
          color: 'error'
        }
      }
    },
    async changePassword() {
      this.changingPassword = true
      try {
        await axios.post('/api/change-password', this.passwordForm, {
          headers: this.getAuthHeader()
        })
        this.snackbar = {
          show: true,
          text: 'Password changed successfully!',
          color: 'success'
        }
        this.passwordForm = { old_password: '', new_password: '' }
      } catch (error) {
        this.snackbar = {
          show: true,
          text: error.response?.data?.detail || 'Failed to change password',
          color: 'error'
        }
      } finally {
        this.changingPassword = false
      }
    }
  }
}
</script>
