import { computed, ref, watch } from 'vue'

import { LANGUAGE_STORAGE_KEY } from '../constants/desktopClient'
import { translations } from '../i18n/translations'

export function useDesktopTranslations() {
  const locale = ref(localStorage.getItem(LANGUAGE_STORAGE_KEY) === 'ru' ? 'ru' : 'en')

  const localeCode = computed(() => (locale.value === 'ru' ? 'ru-RU' : 'en-US'))

  watch(
    locale,
    (value) => {
      localStorage.setItem(LANGUAGE_STORAGE_KEY, value)
      document.documentElement.lang = value
    },
    { immediate: true }
  )

  function getTranslation(localeName, path, params = {}) {
    const value = path.split('.').reduce((acc, part) => acc?.[part], translations[localeName])
    if (typeof value === 'function') {
      return value(params)
    }
    return value ?? path
  }

  function tr(path, params = {}) {
    return getTranslation(locale.value, path, params)
  }

  function trEn(path, params = {}) {
    return getTranslation('en', path, params)
  }

  function switchLanguage(nextLocale) {
    if (nextLocale === 'en' || nextLocale === 'ru') {
      locale.value = nextLocale
    }
  }

  function formatTime(timestamp) {
    return new Date(timestamp).toLocaleTimeString(localeCode.value, {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }

  function localizeServerMessage(message) {
    if (!message) {
      return tr('messages.statusUpdated')
    }

    const directMap = {
      [trEn('messages.initial')]: 'messages.initial',
      [trEn('messages.requestVm')]: 'messages.requestVm',
      [trEn('messages.noActiveDesktopSession')]: 'messages.noActiveDesktopSession',
      [trEn('messages.noActiveProxyConnection')]: 'messages.noActiveProxyConnection',
      [trEn('messages.statusUpdated')]: 'messages.statusUpdated',
      [trEn('messages.allBusy')]: 'messages.allBusy',
      [trEn('messages.invalidActivationKey')]: 'messages.invalidActivationKey',
      [trEn('messages.activationKeyExpired')]: 'messages.activationKeyExpired',
      [trEn('messages.requestFailed')]: 'messages.requestFailed',
      'Network Error': 'messages.networkError',
      'Failed to fetch': 'messages.networkError'
    }

    if (directMap[message]) {
      return tr(directMap[message])
    }

    const connectedMatch = message.match(/^Connected to (.+)$/)
    if (connectedMatch) {
      return tr('messages.connectedTo', { name: connectedMatch[1] })
    }

    const reconnectedMatch = message.match(/^Reconnected to (.+)$/)
    if (reconnectedMatch) {
      return tr('messages.reconnectedTo', { name: reconnectedMatch[1] })
    }

    const disconnectedMatch = message.match(/^Disconnected from (.+)$/)
    if (disconnectedMatch) {
      return tr('messages.disconnectedFrom', { name: disconnectedMatch[1] })
    }

    return message
  }

  function renderLogMessage(entry) {
    if (entry.rawMessage) {
      return localizeServerMessage(entry.rawMessage)
    }

    if (entry.key === 'messages.statusUpdate') {
      return tr(entry.key, {
        status: tr(`status.${entry.params.status}`),
        message: localizeServerMessage(entry.params.message)
      })
    }

    if (entry.key === 'messages.connectionFailed' || entry.key === 'messages.disconnectFailed') {
      return tr(entry.key, {
        detail: localizeServerMessage(entry.params.detail)
      })
    }

    if (!entry.key) {
      return tr('messages.statusUpdated')
    }

    return tr(entry.key, entry.params)
  }

  return {
    formatTime,
    locale,
    localeCode,
    localizeServerMessage,
    renderLogMessage,
    switchLanguage,
    tr,
    trEn
  }
}
