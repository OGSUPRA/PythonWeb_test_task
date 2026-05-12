<template>
  <article class="panel input-panel">
    <div class="panel-header">
      <div>
        <p class="panel-kicker">{{ props.tr('panel.connectionSettings') }}</p>
        <h2>{{ props.tr('panel.desktopSession') }}</h2>
      </div>
      <button class="ghost-button" type="button" @click="emit('reset')">
        {{ props.tr('buttons.reset') }}
      </button>
    </div>

    <label class="field">
      <span>{{ props.tr('fields.backendUrl') }}</span>
      <input
        :value="props.backendUrl"
        type="text"
        :placeholder="props.tr('placeholders.backendUrl')"
        autocomplete="off"
        @input="emit('update:backendUrl', $event.target.value.trim())"
      />
    </label>

    <label class="field">
      <span>{{ props.tr('fields.activationKey') }}</span>
      <input
        :value="props.activationKey"
        type="text"
        :placeholder="props.tr('placeholders.activationKey')"
        autocomplete="off"
        @input="emit('update:activationKey', $event.target.value.trim())"
      />
    </label>

    <p class="field-hint">
      {{ props.tr('panel.backendHint') }}
    </p>

    <div class="button-row">
      <button
        class="primary-button"
        type="button"
        :disabled="props.isConnecting || !props.backendUrl || !props.activationKey"
        @click="emit('connect')"
      >
        {{ props.isConnecting ? props.tr('buttons.connecting') : props.tr('buttons.connect') }}
      </button>

      <button
        class="secondary-button"
        type="button"
        :disabled="props.isDisconnecting"
        @click="emit('disconnect')"
      >
        {{
          props.isDisconnecting ? props.tr('buttons.disconnecting') : props.tr('buttons.disconnect')
        }}
      </button>
    </div>

    <dl class="session-grid">
      <div>
        <dt>{{ props.tr('session.desktopToken') }}</dt>
        <dd>{{ props.desktopToken ? props.tr('session.issued') : props.tr('session.notIssued') }}</dd>
      </div>
      <div>
        <dt>{{ props.tr('session.websocket') }}</dt>
        <dd>{{ props.websocketStateLabel }}</dd>
      </div>
      <div>
        <dt>{{ props.tr('session.platform') }}</dt>
        <dd>{{ props.appInfo?.platform || props.tr('session.browser') }}</dd>
      </div>
      <div>
        <dt>{{ props.tr('session.electron') }}</dt>
        <dd>{{ props.appInfo?.versions?.electron || props.tr('session.notAvailable') }}</dd>
      </div>
    </dl>
  </article>
</template>

<script setup>
const props = defineProps({
  activationKey: {
    type: String,
    required: true
  },
  appInfo: {
    type: Object,
    required: true
  },
  backendUrl: {
    type: String,
    required: true
  },
  desktopToken: {
    type: String,
    required: true
  },
  isConnecting: {
    type: Boolean,
    required: true
  },
  isDisconnecting: {
    type: Boolean,
    required: true
  },
  tr: {
    type: Function,
    required: true
  },
  websocketStateLabel: {
    type: String,
    required: true
  }
})

const emit = defineEmits([
  'connect',
  'disconnect',
  'reset',
  'update:activationKey',
  'update:backendUrl'
])
</script>
