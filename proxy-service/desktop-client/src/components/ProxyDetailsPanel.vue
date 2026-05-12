<template>
  <article class="panel details-panel">
    <div class="panel-header">
      <div>
        <p class="panel-kicker">{{ props.tr('proxy.assignedProxy') }}</p>
        <h2>{{ props.tr('proxy.virtualMachine') }}</h2>
      </div>
    </div>

    <div v-if="props.vm" class="vm-card">
      <div class="vm-name">
        {{ props.vmDisplayName }}
      </div>
      <div class="vm-address">
        {{ props.vm.protocol }}://{{ props.vm.host }}:{{ props.vm.port }}
      </div>
    </div>
    <div v-else class="empty-card">
      {{ props.tr('proxy.noVm') }}
    </div>

    <div class="status-stack">
      <div class="status-row">
        <span class="status-key">{{ props.tr('details.statusMessage') }}</span>
        <span class="status-value">{{ props.stateMessage }}</span>
      </div>
      <div class="status-row">
        <span class="status-key">{{ props.tr('details.updatedAt') }}</span>
        <span class="status-value">{{ props.lastUpdated }}</span>
      </div>
    </div>
  </article>
</template>

<script setup>
const props = defineProps({
  lastUpdated: {
    type: String,
    required: true
  },
  stateMessage: {
    type: String,
    required: true
  },
  tr: {
    type: Function,
    required: true
  },
  vm: {
    type: Object,
    default: null
  },
  vmDisplayName: {
    type: String,
    required: true
  }
})
</script>
