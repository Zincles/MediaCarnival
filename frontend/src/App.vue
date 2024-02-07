<script setup lang="ts">
import StatusPanel from './components/StatusPanel.vue'
</script>

<template>

  <div class="bg-neutral-500 text-4xl">This is an vue app.</div>
  <StatusPanel  />
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/about">About</router-link>

  </nav>

  <router-view />
</template>
