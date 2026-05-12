<template>
  <div class="desktop-shell">
    <DesktopHero
      :locale="locale"
      :state-message="localizedStateMessage"
      :status="status"
      :status-title="statusTitle"
      :tr="tr"
      @switch-language="switchLanguage"
    />

    <section class="content-grid">
      <ConnectionPanel
        v-model:activation-key="activationKey"
        v-model:backend-url="backendUrl"
        :app-info="appInfo"
        :desktop-token="desktopToken"
        :is-connecting="isConnecting"
        :is-disconnecting="isDisconnecting"
        :tr="tr"
        :websocket-state-label="websocketStateLabel"
        @connect="connect"
        @disconnect="disconnect"
        @reset="resetForm"
      />

      <ProxyDetailsPanel
        :last-updated="lastUpdated"
        :state-message="localizedStateMessage"
        :tr="tr"
        :vm="state.vm"
        :vm-display-name="vmDisplayName"
      />
    </section>

    <ActivityLogPanel
      :activity-log="activityLog"
      :format-time="formatTime"
      :render-log-message="renderLogMessage"
      :tr="tr"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'

import ActivityLogPanel from './components/ActivityLogPanel.vue'
import ConnectionPanel from './components/ConnectionPanel.vue'
import DesktopHero from './components/DesktopHero.vue'
import ProxyDetailsPanel from './components/ProxyDetailsPanel.vue'
import { RESERVED_PROXY_NAME } from './constants/desktopClient'
import { useDesktopClient } from './composables/useDesktopClient'
import { useDesktopTranslations } from './composables/useDesktopTranslations'

const { formatTime, locale, localeCode, localizeServerMessage, renderLogMessage, switchLanguage, tr, trEn } =
  useDesktopTranslations()

const {
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
} = useDesktopClient({ trEn })

const status = computed(() => state.status || 'waiting')
const statusTitle = computed(() => tr(`status.${status.value}`))
const websocketStateLabel = computed(() => tr(`status.${websocketState.value}`))
const localizedStateMessage = computed(() => localizeServerMessage(state.message))
const vmDisplayName = computed(() => {
  if (!state.vm) {
    return ''
  }
  return state.vm.name === RESERVED_PROXY_NAME ? tr('proxy.reservedName') : state.vm.name
})
const lastUpdated = computed(() => {
  if (!state.updatedAt) {
    return tr('details.notUpdatedYet')
  }

  const parsed = new Date(state.updatedAt)
  return Number.isNaN(parsed.getTime())
    ? state.updatedAt
    : parsed.toLocaleString(localeCode.value)
})
</script>
