<script setup lang="ts">
import { defineProps } from "vue";
import { ref } from "vue";

// 接受路径参数作为输入，默认值为根目录
let props = defineProps({
  path: {
    type: String,
    default: "/",
  },
});
let path = ref(props.path);
</script>
<template>
  <div class="text-white text-center">
    <h1 class="text-2xl text-center">文件浏览器（移植中）</h1>
    {{ path }}
  </div>
</template>
