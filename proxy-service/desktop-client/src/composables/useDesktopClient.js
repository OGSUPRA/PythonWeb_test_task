import axios from 'axios'
import { onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'

import { DEFAULT_API_URL, RESERVED_PROXY_NAME, STORAGE_KEY } from '../constants/desktopClient'

export function useDesktopClient({ trEn }) {
  const backendUrl = ref(localStorage.getItem(STORAGE_KEY) || DEFAULT_API_URL)
  const activationKey = ref('')
  const desktopToken = ref('')
  const websocketState = ref('disconnected')
  const isConnecting = ref(false)
  const isDisconnecting = ref(false)

  const state = reactive({
    status: 'waiting',
    message: trEn('messages.initial'),
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

  watch(backendUrl, (value) => {
    localStorage.setItem(STORAGE_KEY, value)
  })

  onMounted(() => {
    if (window.proxyDesktop?.getAppInfo) {
      appInfo.value = window.proxyDesktop.getAppInfo()
    }
    addLog('messages.desktopReady')
  })

  onBeforeUnmount(() => {
    closeWebSocket()
  })

  function addLog(key, params = {}, rawMessage = null) {
    logId += 1
    activityLog.value.unshift({
      id: logId,
      timestamp: Date.now(),
      key,
      params,
      rawMessage
    })
    activityLog.value = activityLog.value.slice(0, 12)
  }

  function resetForm() {
    activationKey.value = ''
    if (!desktopToken.value) {
      updateState({
        status: 'waiting',
        message: trEn('messages.initial'),
        vm: null
      })
    }
    addLog('messages.formReset')
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
    state.message = payload.message || trEn('messages.statusUpdated')
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
      message: trEn('messages.requestVm'),
      vm: null
    })
    addLog('messages.connectionRequestStarted')

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
          name: RESERVED_PROXY_NAME,
          host: payload.host,
          port: payload.port,
          protocol: payload.protocol
        }
      })
      addLog('messages.proxyAssigned', {
        protocol: payload.protocol,
        host: payload.host,
        port: payload.port
      })

      openWebSocket(payload.ws_url || buildWebSocketUrl(url))
    } catch (error) {
      const detail = extractErrorMessage(error)
      desktopToken.value = ''
      updateState({
        status: 'error',
        message: detail,
        vm: null
      })
      addLog('messages.connectionFailed', { detail })
    } finally {
      isConnecting.value = false
    }
  }

  async function disconnect() {
    closeWebSocket()

    if (!desktopToken.value) {
      updateState({
        status: 'disconnected',
        message: trEn('messages.noActiveDesktopSession'),
        vm: null
      })
      addLog('messages.disconnectWithoutToken')
      return
    }

    isDisconnecting.value = true
    addLog('messages.disconnectRequestStarted')

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
      addLog(null, {}, response.data.message)
    } catch (error) {
      const detail = extractErrorMessage(error)
      updateState({
        status: 'error',
        message: detail,
        vm: null
      })
      addLog('messages.disconnectFailed', { detail })
    } finally {
      desktopToken.value = ''
      websocketState.value = 'disconnected'
      isDisconnecting.value = false
    }
  }

  function openWebSocket(url) {
    closeWebSocket()
    websocketState.value = 'connecting'
    addLog('messages.websocketOpening')

    websocket = new WebSocket(url)

    websocket.onopen = () => {
      websocketState.value = 'connected'
      addLog('messages.websocketConnected')
    }

    websocket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data)
        updateState(payload)
        addLog('messages.statusUpdate', {
          status: payload.status,
          message: payload.message
        })
      } catch (error) {
        addLog('messages.nonJsonSocket')
      }
    }

    websocket.onerror = () => {
      websocketState.value = 'error'
      addLog('messages.websocketError')
    }

    websocket.onclose = () => {
      websocketState.value = 'disconnected'
      addLog('messages.websocketClosed')
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
      return error.response?.data?.detail || error.message || trEn('messages.requestFailed')
    }
    return error instanceof Error ? error.message : trEn('messages.requestFailed')
  }

  return {
    activationKey,
    activityLog,
    appInfo,
    backendUrl,
    connect,
    desktopToken,
    disconnect,
    isConnecting,
    isDisconnecting,
    resetForm,
    state,
    websocketState
  }
}
