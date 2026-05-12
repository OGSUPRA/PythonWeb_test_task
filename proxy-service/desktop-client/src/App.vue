<template>
  <div class="desktop-shell">
    <section class="hero-card">
      <div class="hero-copy">
        <p class="eyebrow">Proxy Desktop</p>
        <h1>Connect to a free proxy with your activation key</h1>
        <p class="hero-text">
          The desktop client talks directly to your FastAPI backend, requests a free
          virtual machine, and keeps the connection status fresh through WebSocket
          updates.
        </p>
      </div>

      <div class="hero-status">
        <span class="status-label">Current state</span>
        <span class="status-pill" :data-state="status">
          {{ statusTitle }}
        </span>
        <p>{{ state.message }}</p>
      </div>
    </section>

    <section class="content-grid">
      <article class="panel input-panel">
        <div class="panel-header">
          <div>
            <p class="panel-kicker">Connection Settings</p>
            <h2>Desktop Session</h2>
          </div>
          <button class="ghost-button" type="button" @click="resetForm">
            Reset
          </button>
        </div>

        <label class="field">
          <span>Backend URL</span>
          <input
            v-model.trim="backendUrl"
            type="text"
            placeholder="http://localhost:8000"
            autocomplete="off"
          />
        </label>

        <label class="field">
          <span>Activation Key</span>
          <input
            v-model.trim="activationKey"
            type="text"
            placeholder="Paste the one-time activation key from your profile"
            autocomplete="off"
          />
        </label>

        <div class="button-row">
          <button
            class="primary-button"
            type="button"
            :disabled="isConnecting || !backendUrl || !activationKey"
            @click="connect"
          >
            {{ isConnecting ? 'Connecting...' : 'Connect' }}
          </button>

          <button
            class="secondary-button"
            type="button"
            :disabled="isDisconnecting"
            @click="disconnect"
          >
            {{ isDisconnecting ? 'Disconnecting...' : 'Disconnect' }}
          </button>
        </div>

        <dl class="session-grid">
          <div>
            <dt>Desktop token</dt>
            <dd>{{ desktopToken ? 'Issued' : 'Not issued yet' }}</dd>
          </div>
          <div>
            <dt>WebSocket</dt>
            <dd>{{ websocketState }}</dd>
          </div>
          <div>
            <dt>Platform</dt>
            <dd>{{ appInfo.platform || 'browser' }}</dd>
          </div>
          <div>
            <dt>Electron</dt>
            <dd>{{ appInfo.versions?.electron || 'n/a' }}</dd>
          </div>
        </dl>
      </article>

      <article class="panel details-panel">
        <div class="panel-header">
          <div>
            <p class="panel-kicker">Assigned Proxy</p>
            <h2>Virtual Machine</h2>
          </div>
        </div>

        <div v-if="state.vm" class="vm-card">
          <div class="vm-name">
            {{ state.vm.name }}
          </div>
          <div class="vm-address">
            {{ state.vm.protocol }}://{{ state.vm.host }}:{{ state.vm.port }}
          </div>
        </div>
        <div v-else class="empty-card">
          No virtual machine assigned yet. Connect with a valid activation key to
          reserve one.
        </div>

        <div class="status-stack">
          <div class="status-row">
            <span class="status-key">Status message</span>
            <span class="status-value">{{ state.message }}</span>
          </div>
          <div class="status-row">
            <span class="status-key">Updated at</span>
            <span class="status-value">{{ lastUpdated }}</span>
          </div>
        </div>
      </article>
    </section>

    <section class="panel log-panel">
      <div class="panel-header">
        <div>
          <p class="panel-kicker">Live Feed</p>
          <h2>Activity Log</h2>
        </div>
      </div>

      <ul class="log-list">
        <li v-for="entry in activityLog" :key="entry.id" class="log-item">
          <span class="log-time">{{ entry.time }}</span>
          <span class="log-message">{{ entry.message }}</span>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import axios from 'axios'
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'

const STORAGE_KEY = 'proxy-desktop-backend-url'
const DEFAULT_API_URL = import.meta.env.VITE_DEFAULT_API_URL || 'http://localhost:8000'

const backendUrl = ref(localStorage.getItem(STORAGE_KEY) || DEFAULT_API_URL)
const activationKey = ref('')
const desktopToken = ref('')
const websocketState = ref('Disconnected')
const isConnecting = ref(false)
const isDisconnecting = ref(false)

const state = reactive({
  status: 'waiting',
  message: 'Paste the activation key from the web profile and start a desktop session.',
  vm: null,
  updatedAt: null
})

const activityLog = ref([])
const appInfo = ref({
  platform: '',
  versions: {}
})

let websocket = null
let logId = 0

const status = computed(() => state.status || 'waiting')
const statusTitle = computed(() => {
  const labels = {
    waiting: 'Waiting',
    connected: 'Connected',
    disconnected: 'Disconnected',
    no_free_vms: 'All Busy',
    error: 'Error'
  }
  return labels[status.value] || status.value
})

const lastUpdated = computed(() => {
  if (!state.updatedAt) {
    return 'Not updated yet'
  }

  const parsed = new Date(state.updatedAt)
  return Number.isNaN(parsed.getTime())
    ? state.updatedAt
    : parsed.toLocaleString()
})

watch(backendUrl, (value) => {
  localStorage.setItem(STORAGE_KEY, value)
})

onMounted(() => {
  if (window.proxyDesktop?.getAppInfo) {
    appInfo.value = window.proxyDesktop.getAppInfo()
  }
  addLog('Desktop client is ready.')
})

onBeforeUnmount(() => {
  closeWebSocket()
})

function addLog(message) {
  logId += 1
  activityLog.value.unshift({
    id: logId,
    time: new Date().toLocaleTimeString(),
    message
  })
  activityLog.value = activityLog.value.slice(0, 12)
}

function resetForm() {
  activationKey.value = ''
  if (!desktopToken.value) {
    updateState({
      status: 'waiting',
      message: 'Paste the activation key from the web profile and start a desktop session.',
      vm: null
    })
  }
  addLog('Input form was reset.')
}

function normalizeUrl(url) {
  return url.trim().replace(/\/$/, '')
}

function buildWebSocketUrl(apiUrl) {
  if (apiUrl.startsWith('https://')) {
    return `wss://${apiUrl.slice('https://'.length)}/ws/status?token=${encodeURIComponent(desktopToken.value)}`
  }

  if (apiUrl.startsWith('http://')) {
    return `ws://${apiUrl.slice('http://'.length)}/ws/status?token=${encodeURIComponent(desktopToken.value)}`
  }

  return `${apiUrl}/ws/status?token=${encodeURIComponent(desktopToken.value)}`
}

function updateState(payload) {
  state.status = payload.status || 'waiting'
  state.message = payload.message || 'Status updated.'
  state.vm = payload.vm || null
  state.updatedAt = payload.updated_at || payload.updatedAt || new Date().toISOString()
}

async function connect() {
  if (!backendUrl.value || !activationKey.value) {
    return
  }

  isConnecting.value = true
  closeWebSocket()
  updateState({
    status: 'waiting',
    message: 'Requesting a virtual machine from the backend...',
    vm: null
  })
  addLog('Connection request started.')

  try {
    const url = normalizeUrl(backendUrl.value)
    const response = await axios.post(`${url}/api/activate-key`, {
      key: activationKey.value
    })

    const payload = response.data
    desktopToken.value = payload.access_token
    updateState({
      status: payload.status,
      message: payload.message,
      vm: {
        name: 'Reserved proxy',
        host: payload.host,
        port: payload.port,
        protocol: payload.protocol
      }
    })
    addLog(`Proxy assigned: ${payload.protocol}://${payload.host}:${payload.port}`)

    openWebSocket(payload.ws_url || buildWebSocketUrl(url))
  } catch (error) {
    const detail = extractErrorMessage(error)
    desktopToken.value = ''
    updateState({
      status: 'error',
      message: detail,
      vm: null
    })
    addLog(`Connection failed: ${detail}`)
  } finally {
    isConnecting.value = false
  }
}

async function disconnect() {
  closeWebSocket()

  if (!desktopToken.value) {
    updateState({
      status: 'disconnected',
      message: 'No active desktop session.',
      vm: null
    })
    addLog('Disconnect requested without an active token.')
    return
  }

  isDisconnecting.value = true
  addLog('Disconnect request started.')

  try {
    const url = normalizeUrl(backendUrl.value)
    const response = await axios.post(
      `${url}/api/disconnect`,
      {},
      {
        headers: {
          Authorization: `Bearer ${desktopToken.value}`
        }
      }
    )

    updateState({
      status: response.data.status,
      message: response.data.message,
      vm: null
    })
    addLog(response.data.message)
  } catch (error) {
    const detail = extractErrorMessage(error)
    updateState({
      status: 'error',
      message: detail,
      vm: null
    })
    addLog(`Disconnect failed: ${detail}`)
  } finally {
    desktopToken.value = ''
    websocketState.value = 'Disconnected'
    isDisconnecting.value = false
  }
}

function openWebSocket(url) {
  closeWebSocket()
  websocketState.value = 'Connecting'
  addLog('Opening WebSocket channel.')

  websocket = new WebSocket(url)

  websocket.onopen = () => {
    websocketState.value = 'Connected'
    addLog('WebSocket connected.')
  }

  websocket.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data)
      updateState(payload)
      addLog(`Status update: ${payload.status} — ${payload.message}`)
    } catch (error) {
      addLog('Received a non-JSON WebSocket message.')
    }
  }

  websocket.onerror = () => {
    websocketState.value = 'Error'
    addLog('WebSocket reported an error.')
  }

  websocket.onclose = () => {
    websocketState.value = 'Disconnected'
    addLog('WebSocket closed.')
  }
}

function closeWebSocket() {
  if (websocket) {
    websocket.close()
    websocket = null
  }
}

function extractErrorMessage(error) {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.detail || error.message || 'Request failed'
  }
  return error instanceof Error ? error.message : 'Unknown error'
}
</script>

<style scoped>
.desktop-shell {
  min-height: 100vh;
  padding: 28px;
  background:
    linear-gradient(160deg, rgba(8, 14, 32, 0.92), rgba(11, 16, 32, 0.98)),
    radial-gradient(circle at top left, rgba(28, 100, 242, 0.28), transparent 34%),
    radial-gradient(circle at right, rgba(56, 189, 248, 0.18), transparent 30%);
}

.hero-card,
.panel {
  border: 1px solid rgba(190, 220, 255, 0.14);
  background: rgba(12, 18, 38, 0.82);
  backdrop-filter: blur(16px);
  box-shadow: 0 28px 70px rgba(3, 7, 18, 0.4);
}

.hero-card {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(260px, 1fr);
  gap: 24px;
  padding: 28px;
  border-radius: 28px;
}

.eyebrow,
.panel-kicker {
  margin: 0 0 10px;
  color: #7dd3fc;
  font-size: 0.8rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.hero-copy h1,
.panel-header h2 {
  margin: 0;
  font-size: clamp(1.8rem, 2vw, 2.6rem);
  line-height: 1.05;
}

.hero-text {
  max-width: 620px;
  margin: 16px 0 0;
  color: #c9d6ee;
  font-size: 1rem;
  line-height: 1.6;
}

.hero-status {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 10px;
  padding: 20px;
  border-radius: 22px;
  background: linear-gradient(180deg, rgba(18, 28, 58, 0.95), rgba(10, 15, 31, 0.85));
}

.status-label {
  color: #8ea5cf;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
}

.status-pill {
  width: fit-content;
  padding: 10px 16px;
  border-radius: 999px;
  background: rgba(56, 189, 248, 0.16);
  color: #dff6ff;
  font-weight: 700;
}

.status-pill[data-state='connected'] {
  background: rgba(34, 197, 94, 0.18);
  color: #c7ffd9;
}

.status-pill[data-state='error'],
.status-pill[data-state='no_free_vms'] {
  background: rgba(248, 113, 113, 0.18);
  color: #ffd7d7;
}

.status-pill[data-state='disconnected'] {
  background: rgba(148, 163, 184, 0.18);
  color: #dce8f4;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(320px, 0.95fr);
  gap: 18px;
  margin-top: 18px;
}

.panel {
  border-radius: 26px;
  padding: 24px;
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.ghost-button,
.primary-button,
.secondary-button {
  border: none;
  border-radius: 16px;
  cursor: pointer;
  transition: transform 160ms ease, opacity 160ms ease, background 160ms ease;
}

.ghost-button {
  padding: 10px 14px;
  background: rgba(129, 140, 248, 0.12);
  color: #dce6ff;
}

.primary-button,
.secondary-button {
  flex: 1;
  padding: 16px 18px;
  font-weight: 700;
  font-size: 1rem;
}

.primary-button {
  background: linear-gradient(135deg, #1d4ed8, #38bdf8);
  color: #f9fdff;
}

.secondary-button {
  background: rgba(148, 163, 184, 0.18);
  color: #ecf4ff;
}

.ghost-button:hover,
.primary-button:hover,
.secondary-button:hover {
  transform: translateY(-1px);
}

.ghost-button:disabled,
.primary-button:disabled,
.secondary-button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  transform: none;
}

.field {
  display: block;
  margin-bottom: 16px;
}

.field span {
  display: inline-block;
  margin-bottom: 8px;
  color: #9db0d0;
  font-size: 0.92rem;
}

.field input {
  width: 100%;
  padding: 16px 18px;
  border: 1px solid rgba(173, 192, 225, 0.14);
  border-radius: 18px;
  background: rgba(6, 11, 26, 0.82);
  color: #f8fbff;
  outline: none;
  transition: border-color 160ms ease, box-shadow 160ms ease, background 160ms ease;
}

.field input::placeholder {
  color: #627190;
}

.field input:focus {
  border-color: rgba(56, 189, 248, 0.54);
  box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.12);
}

.button-row {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.session-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin: 22px 0 0;
}

.session-grid div,
.status-stack,
.vm-card,
.empty-card {
  border-radius: 20px;
  background: rgba(8, 13, 28, 0.66);
  border: 1px solid rgba(184, 208, 242, 0.1);
}

.session-grid div {
  padding: 16px;
}

.session-grid dt {
  margin-bottom: 8px;
  color: #7d95bc;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.session-grid dd {
  margin: 0;
  color: #f5f9ff;
}

.vm-card,
.empty-card {
  padding: 22px;
}

.vm-name {
  font-size: 1.3rem;
  font-weight: 700;
}

.vm-address {
  margin-top: 10px;
  color: #86c9ff;
  word-break: break-word;
}

.empty-card {
  color: #b9c7df;
  line-height: 1.6;
}

.status-stack {
  margin-top: 16px;
  padding: 8px 18px;
}

.status-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0;
  border-bottom: 1px solid rgba(184, 208, 242, 0.08);
}

.status-row:last-child {
  border-bottom: none;
}

.status-key {
  color: #8ea5cf;
}

.status-value {
  text-align: right;
  color: #f5f9ff;
}

.log-panel {
  margin-top: 18px;
}

.log-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 12px;
}

.log-item {
  display: grid;
  grid-template-columns: 92px 1fr;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(9, 14, 30, 0.72);
  border: 1px solid rgba(184, 208, 242, 0.08);
}

.log-time {
  color: #7dd3fc;
  font-size: 0.86rem;
}

.log-message {
  color: #e8f2ff;
}

@media (max-width: 980px) {
  .desktop-shell {
    padding: 18px;
  }

  .hero-card,
  .content-grid {
    grid-template-columns: 1fr;
  }

  .button-row,
  .session-grid {
    grid-template-columns: 1fr;
    flex-direction: column;
  }

  .status-row,
  .log-item {
    grid-template-columns: 1fr;
  }

  .status-value {
    text-align: left;
  }
}
</style>
