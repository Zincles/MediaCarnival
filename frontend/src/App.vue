<script setup lang="ts">
import StatusPanel from "./components/StatusPanel.vue";
import { ref } from "vue";

const curPos = ref("Hello, World!"); // 当前app位置
</script>

<template>
  <StatusPanel :title="curPos" />
  <router-view />
</template>
