<template>
  <q-layout view="hHh lpR fFf">
    <!-- 顶部导航栏 -->
    <q-header class="bg-grey-9 text-white text-xl shadow-4">
      <q-toolbar class="full-width">
        <!-- 左侧菜单按钮 -->
        <q-btn flat round dense icon="menu" class="q-mr-sm" @click="leftDrawerOpen = !leftDrawerOpen" />

        <!-- 中央导航按钮 -->
        <q-tabs v-model="tab" inline-label class="full-width">
          <q-route-tab name="home" label="主页" icon="home" stacked to="/home" />
          <q-route-tab name="library" label="媒体" icon="video_library" stacked to="/library_browser" />
          <q-route-tab name="file" label="文件" icon="folder" stacked to="/file_browser" />
          <q-route-tab name="about" label="关于" icon="info" stacked to="/about" />
        </q-tabs>

        <!-- 右侧设置按钮与设置面板 -->
        <q-btn flat round dense icon="settings" class="q-ml-sm" @click="rightDrawerOpen = !rightDrawerOpen" />
      </q-toolbar>
    </q-header>

    <!-- 左侧边栏内容 -->
    <q-drawer v-model="leftDrawerOpen" side="left" class="bg-grey-7" overlay> </q-drawer>

    <!-- 右侧边栏内容 -->
    <q-drawer v-model="rightDrawerOpen" side="right" class="bg-grey-7" overlay> </q-drawer>

    <!-- 主要内容区域 -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const tab = ref('home');
const leftDrawerOpen = ref(false);
const rightDrawerOpen = ref(false);

</script>
