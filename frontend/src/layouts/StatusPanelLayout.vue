<template>
  {{ props.title }}
  <q-toolbar class="bg-grey-9 text-white text-xl shadow-4">
    <q-btn
      flat
      round
      dense
      icon="menu"
      class="q-mr-sm"
      @click="toggleMenu"
      :color="menuOpen ? 'blue-4' : 'grey-4'"
    />
    <q-toolbar-title>{{ title }}</q-toolbar-title>
    <q-space />
    <q-btn
      flat
      round
      dense
      icon="settings"
      class="q-mr-sm"
      @click="toggleSettings"
      :color="settingsOpen ? 'blue-4' : 'grey-4'"
    />
  </q-toolbar>
  <div class="row q-gutter-sm justify-center">
    <q-btn
      v-for="link in links"
      :key="link.name"
      :to="link.path"
      label="link.name"
      class="shadow-2 rounded-borders"
    />
  </div>
  <q-card class="q-ma-md">
    <q-card-section>
      {{ param }}
    </q-card-section>
  </q-card>

  <router-view class="bg-dark" />
</template>

<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: '默认标题',
  },
  param: {
    type: String,
    default: '默认参数',
  },
});

const links = [
  { name: '主页', path: '/' },
  { name: '关于', path: '/about' },
  { name: '文件', path: '/file_browser' },
];

const menuOpen = ref(false);
const settingsOpen = ref(false);

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};

const toggleSettings = () => {
  settingsOpen.value = !settingsOpen.value;
};
</script>
