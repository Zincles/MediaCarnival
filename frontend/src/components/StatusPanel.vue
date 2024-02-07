<!--
位于网页上端的状态栏。可用于切换界面。
接受title与param两个参数，分别用于显示标题与参数。
-->
<script setup lang="ts">
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
const SETTING_BUTTON_STYLE = " w-12 h-12 shadow rounded-lg p-3 bg-neutral-700 hover:bg-blue-500"; // 设置按钮的样式
const MENU_BUTTON_STYLE = " w-12 h-12 shadow rounded-lg p-3 bg-neutral-700 hover:bg-blue-500";
</script>

<template>
  <div class="bg-neutral-800 text-white text-xl p-4 flex flex-col shadow mx-auto">
    <!-- 顶部状态栏，容纳两个按钮与位于左侧的标题。 -->
    <div class="flex">
      <div class="w-full flex">
        <button :class="MENU_BUTTON_STYLE">
          <font-awesome-icon icon="bars" size="lg" class="text-white" />
        </button>
        <h1 class="text-2xl m-2">{{ props.title }}</h1>
      </div>
      <button :class="SETTING_BUTTON_STYLE">
        <font-awesome-icon icon="gear" size="lg" class="text-white" />
      </button>
    </div>

    <!-- 下方导航按钮 -->

    <div class="flex-wrap">
      <div class="p-2 overflow-hidden whitespace-normal">{{ props.param }}</div>
      <nav class="flex space-x-1 justify-center">
        <router-link :class="NAV_BUTTON_STYLE" to="/">主页</router-link>
        <router-link :class="NAV_BUTTON_STYLE" to="/about">关于</router-link>
        <router-link :class="NAV_BUTTON_STYLE" to="/file_browser">文件管理器</router-link>
      </nav>
    </div>

    <!-- -->
  </div>
</template>
