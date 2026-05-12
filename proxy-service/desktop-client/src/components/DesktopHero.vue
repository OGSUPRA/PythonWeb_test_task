<template>
  <section class="hero-card">
    <div class="hero-copy">
      <div class="hero-topbar">
        <p class="eyebrow">{{ props.tr('hero.eyebrow') }}</p>

        <div class="language-toggle">
          <span class="language-label">{{ props.tr('language.label') }}</span>
          <div class="language-buttons">
            <button
              class="lang-button"
              :class="{ active: props.locale === 'en' }"
              type="button"
              @click="emit('switch-language', 'en')"
            >
              {{ props.tr('language.english') }}
            </button>
            <button
              class="lang-button"
              :class="{ active: props.locale === 'ru' }"
              type="button"
              @click="emit('switch-language', 'ru')"
            >
              {{ props.tr('language.russian') }}
            </button>
          </div>
        </div>
      </div>

      <h1>{{ props.tr('hero.title') }}</h1>
      <p class="hero-text">
        {{ props.tr('hero.text') }}
      </p>
    </div>

    <div class="hero-status">
      <span class="status-label">{{ props.tr('hero.currentState') }}</span>
      <span class="status-pill" :data-state="props.status">
        {{ props.statusTitle }}
      </span>
      <p>{{ props.stateMessage }}</p>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  locale: {
    type: String,
    required: true
  },
  stateMessage: {
    type: String,
    required: true
  },
  status: {
    type: String,
    required: true
  },
  statusTitle: {
    type: String,
    required: true
  },
  tr: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['switch-language'])
</script>
