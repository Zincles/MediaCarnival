<!--
位于网页上端的状态栏。可用于切换界面。
接受title与param两个参数，分别用于显示标题与参数。
-->
<script setup lang="ts">
import { defineProps, ref } from "vue";

// 接受参数title与param输入，有默认值：
const props = defineProps({
  title: {
    type: String,
    default: "默认标题",
  },
  param: {
    type: String,
    default: "默认参数",
  },
});

const NAV_BUTTON_STYLE = "shadow rounded-lg p-1 bg-neutral-700 hover:bg-blue-500"; // URL按钮的样式
const SETTING_BUTTON_STYLE = "shadow rounded-lg p-3 bg-neutral-700 hover:bg-blue-500"; // 设置按钮的样式

const setting_button_showing = ref(false); // 设置按钮是否显示
function on_setting_button_pressed() {
  setting_button_showing.value = !setting_button_showing.value;
}
</script>

<template>
  <div class="status-panel bg-neutral-800 text-white text-sm p-4 flex shadow mx-auto justify-between items-center">
    <div class="flex-wrap">
      <h1 class="text-2xl">{{ props.title }}</h1>
      <div class="p-2 overflow-hidden whitespace-normal">{{ props.param }}</div>
      <nav id="nav-buttons-div" class="flex space-x-1">
        <router-link :class="NAV_BUTTON_STYLE" to="/">主页</router-link>
        <router-link :class="NAV_BUTTON_STYLE" to="/about">关于</router-link>
      </nav>
    </div>

    <!-- 设置按钮 -->
    <div id="setting-button-div" class="relative">
      <button @click="on_setting_button_pressed" :class="SETTING_BUTTON_STYLE">
        <font-awesome-icon icon="gear" size="2x" />
      </button>

      <div
        v-if="setting_button_showing"
        class="settings-dropdown absolute z-50 right-0 mt-2 w-48 bg-neutral-700 text-white shadow-2xl rounded-lg p-2">
        <a to="/user_config" class="block px-2 py-1 hover:bg-blue-500 rounded-lg hover:text-white">用户</a>
        <a to="/server_config" class="block px-2 py-1 hover:bg-blue-500 rounded-lg hover:text-white">设置</a>
        <a
          href="/admin"
          target="_blank"
          rel="noopener noreferrer"
          class="block px-2 py-1 hover:bg-blue-500 rounded-lg hover:text-white"
          >Django站点管理器</a
        >

        <!-- 添加更多的设置选项 -->
      </div>
    </div>
  </div>
</template>
