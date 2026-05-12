<template>
  <section class="panel log-panel">
    <div class="panel-header">
      <div>
        <p class="panel-kicker">{{ props.tr('log.liveFeed') }}</p>
        <h2>{{ props.tr('log.activityLog') }}</h2>
      </div>
    </div>

    <ul class="log-list">
      <li v-for="entry in props.activityLog" :key="entry.id" class="log-item">
        <span class="log-time">{{ props.formatTime(entry.timestamp) }}</span>
        <span class="log-message">{{ props.renderLogMessage(entry) }}</span>
      </li>
    </ul>
  </section>
</template>

<script setup>
const props = defineProps({
  activityLog: {
    type: Array,
    required: true
  },
  formatTime: {
    type: Function,
    required: true
  },
  renderLogMessage: {
    type: Function,
    required: true
  },
  tr: {
    type: Function,
    required: true
  }
})
</script>
