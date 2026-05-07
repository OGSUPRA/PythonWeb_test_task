import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const apiTarget = process.env.VITE_API_PROXY_TARGET || 'http://localhost:8000'
const wsTarget = process.env.VITE_WS_PROXY_TARGET || 'ws://localhost:8000'
const usePolling = process.env.CHOKIDAR_USEPOLLING === 'true'
const pollingInterval = Number(process.env.CHOKIDAR_INTERVAL || 300)

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    watch: usePolling
      ? {
          usePolling: true,
          interval: pollingInterval
        }
      : undefined,
    proxy: {
      '/api': {
        target: apiTarget,
        changeOrigin: true
      },
      '/ws': {
        target: wsTarget,
        ws: true
      }
    }
  }
})
