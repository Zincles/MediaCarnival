<template>
  <q-page padding>
    <div class="text-h5 text-center q-my-md">文件浏览器</div>
    <div>当前路径： {{ currentPath }}</div>
    <div>访问API地址：{{ apiUrls.getFolder }}</div>

    <!-- 切换显示方式的下拉按钮 -->
    <q-select
      rounded
      filled
      outlined
      v-model="displayMode"
      :options="displayModeOptions"
      label="显示方式"
      class="text-white bg-grey-6"
      option-value="value"
      emit-value
      map-options
    />

    <!-- 切换按钮. 非瀑布流才会显示 -->
    <div v-if="displayMode != 'waterfall'">
      <div class="flex flex-center">{{ curPage }}/{{ totalPages }}页</div>
      <div class="flex flex-center">
        <q-btn label="上一页" @click="loadPrevPage" :disable="curPage <= 1" class="q-mt-md" />
        <q-btn label="下一页" @click="loadNextPage" :disable="reachedEnd" class="q-mt-md" />
      </div>
    </div>

    <q-list bordered separator>
      <q-item v-for="dir in displayedDirs" :key="dir.path" clickable @click="clickDir(dir)">
        <q-item-section>
          <q-item-label class="text-body1">
            <!-- 显示图标，根据类型 -->
            <q-icon size="md" name="folder" v-if="dir.type === 'folder'" />
            <q-icon size="md" name="image" v-else-if="dir.type === 'image'" />
            <q-icon size="md" name="arrow_back" v-else-if="dir.type === '..'" />
            <q-icon size="md" name="insert_drive_file" v-else />
            {{ dir.basename }}
          </q-item-label>
        </q-item-section>
      </q-item>
    </q-list>

    <!-- 切换按钮. 非瀑布流才会显示 -->
    <div v-if="displayMode != 'waterfall'">
      <div class="flex flex-center">{{ curPage }}/{{ totalPages }}页</div>
      <div class="flex flex-center">
        <q-btn label="上一页" @click="loadPrevPage" :disable="curPage <= 1" class="q-mt-md" />
        <q-btn label="下一页" @click="loadNextPage" :disable="reachedEnd" class="q-mt-md" />
      </div>
    </div>
  </q-page>

  <!-- 瀑布流 继续加载 按钮. 按下后会加载下一页. 如果到底了则不会显示. -->
  <div class="flex flex-center">
    <q-btn v-if="displayMode === 'waterfall' && !reachedEnd" label="继续加载" @click="loadNextPage" class="q-mt-md" />
  </div>

  <!-- 用于预览媒体文件 -->
  <!-- <q-btn label="Maximized" color="primary" @click="previewDialog = true" /> -->
  <q-dialog
    v-model="previewDialog"
    :maximized="maximizedToggle"
    transition-show="slide-up"
    transition-hide="slide-down"
  >
    <q-card class="bg-dark text-white">
      <!-- 顶部工具栏 -->
      <q-bar>
        {{ currentPreviewPath }}
        <q-space />
        <!-- 调整显示模式."fit-screen==true为适配屏幕,false为保持原样. 样式为toggle"  -->
        <q-toggle v-model="previewDialogFitScreen" label="适配屏幕" class="text-white" />

        <q-space />

        <q-btn dense flat icon="minimize" @click="maximizedToggle = false" :disable="!maximizedToggle">
          <q-tooltip v-if="maximizedToggle" class="bg-white text-primary">Minimize</q-tooltip>
        </q-btn>
        <q-btn dense flat icon="crop_square" @click="maximizedToggle = true" :disable="maximizedToggle">
          <q-tooltip v-if="!maximizedToggle" class="bg-white text-primary">Maximize</q-tooltip>
        </q-btn>
        <q-btn dense flat icon="close" v-close-popup>
          <q-tooltip class="bg-white text-primary">Close</q-tooltip>
        </q-btn>
      </q-bar>
      {{ apiUrls.getFilePreview + currentPreviewPath.path }}

      <!-- 预览图像.可调整图像显示方法: -->
      <q-card-section v-if="currentPreviewPath.type === 'image'" class="text-center flex justify-center">
        <img v-if="!previewDialogFitScreen" :src="apiUrls.getFilePreview + currentPreviewPath.path" alt="file" />
        <img v-else :src="getPreviewUrl()" alt="file" style="max-height: 95vh; object-fit: contain" />
      </q-card-section>

      <!-- 预览视频: -->
      <q-card-section v-else-if="currentPreviewPath.type === 'video'" class="text-center flex justify-center">
        <video v-if="!previewDialogFitScreen" :src="apiUrls.getFilePreview + currentPreviewPath.path" controls></video>
        <video v-else :src="getPreviewUrl()" controls style="max-height: 95vh; object-fit: contain"></video>
      </q-card-section>

      <!-- 预览音频: -->
      <q-card-section v-else-if="currentPreviewPath.type === 'audio'" class="text-center flex justify-center">
        <audio :src="apiUrls.getFilePreview + currentPreviewPath.path" controls></audio>
      </q-card-section>

      <!-- 预览其他文件,直接显示文件名 -->
      <q-card-section v-else class="text-center flex justify-center">
        {{ currentPreviewPath.basename }}
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { defineProps, watch } from 'vue';
import { ref } from 'vue';
import apiUrls from '../apiUrls';
import axios from 'axios';
import { dirname } from 'path-browserify';
import { SubPath } from 'components/models';

// 一个路径下的文件/文件夹信息。
interface DirInfo {
  page: number; // 当前页码
  pageSize: number; // 每页的数量
  totalPages: number; // 总页数
  totalDirs: number; // 总文件数(非单页)
  isEnd: boolean; // 是否到达最后一页
  subPaths: SubPath[]; // 当前目录下的子目录（文件/文件夹）
}

// 接受路径参数作为输入，默认值为根目录
let props = defineProps({
  path: {
    type: String,
    default: '/home/zincles/Pictures',
  },
});

const displayMode = ref<string>('list'); // 显示列数

const displayModeOptions = ref([
  { label: '列表', value: 'list' },
  { label: '网格', value: 'grid' },
  { label: '瀑布流', value: 'waterfall' },
]);

watch(displayMode, () => {
  console.log('displayMode changed' + displayMode.value.toString());
});

const currentPath = ref(props.path); // 当前路径
const currentPreviewPath = ref<SubPath>({
  path: '',
  basename: '',
  type: '',
}); // 当前预览的文件路径

// const display_column = ref(3); // 显示列数

const curPage = ref(1); // 当前页码
const totalPages = ref(1); // 总页数
const pageSize = ref(30); // 每页显示的文件数

const displayedDirs = ref<SubPath[]>([]); // 当前页显示的文件/文件夹
const reachedEnd = ref(false); // 是否到达最后一页

const previewDialog = ref(false); // 是否显示预览Dialog
const maximizedToggle = ref(true); // 是否最大化预览Dialog

const previewDialogFitScreen = ref(false); // 是否适配屏幕

watch(currentPath, () => {
  // 确保路径改变时，页码重置为1
  curPage.value = 1;
});

const isLoading = ref(false); // 是否正在加载文件夹内容

// 从后端获取文件夹内容.仅会将文件夹内容附加到原来的文件夹内容上.
// 同时只能有一个请求在进行
function updateDirs() {
  if (isLoading.value) {
    return;
  }

  // 如果是流式加载,则不清空原来的文件夹内容
  // 否则清空原来的文件夹内容,在每一次加载新页时会添加“..”路径
  // 流式加载只会在page=1时清空原来的文件夹内容并添加“..”路径
  if (displayMode.value != 'waterfall') {
    displayedDirs.value = []; // 清空原来的文件夹内容

    // 添加“..”路径
    displayedDirs.value.push({
      path: dirname(currentPath.value), // 所在目录的路径，调用path-browserify的dirname方法
      basename: '..',
      type: '..',
    });
  } else {
    // 如果是瀑布流,则不清空原来的文件夹内容,除非page==1
    if (curPage.value == 1) {
      displayedDirs.value = []; // 清空原来的文件夹内容

      // 添加“..”路径
      displayedDirs.value.push({
        path: dirname(currentPath.value), // 所在目录的路径，调用path-browserify的dirname方法
        basename: '..',
        type: '..',
      });
    }
  }

  isLoading.value = true;
  axios
    .get<DirInfo>(apiUrls.getFolder, {
      params: {
        path: currentPath.value, // 路径
        page: curPage.value, // 当前页码
        pageSize: pageSize.value, // 每页显示的文件数
      },
    })
    .then((response) => {
      console.log(response.data);
      totalPages.value = response.data.totalPages; // 更新总页数
      displayedDirs.value = displayedDirs.value.concat(response.data.subPaths); // 将文件夹内容附加到原来的文件夹内容上
      reachedEnd.value = response.data.isEnd; // 是否到达最后一页
      isLoading.value = false;
    })
    .catch((error) => {
      console.error('获取文件夹内容失败', error);
      isLoading.value = false;
    });
}

function loadNextPage() {
  if (reachedEnd.value) {
    return;
  }
  curPage.value += 1;
  updateDirs();
}

function loadPrevPage() {
  if (curPage.value <= 1) {
    return;
  }
  curPage.value -= 1;
  updateDirs();
}

// 点击了一个文件夹
function clickDir(dir: SubPath) {
  if (dir.type === '..') {
    // 点击了“..”路径
    currentPath.value = dirname(currentPath.value); // 返回上一级目录
    curPage.value = 1; // 重置页码
    updateDirs();
    return;
  } else if (dir.type === 'folder') {
    // 点击了文件夹
    currentPath.value = dir.path; // 进入文件夹
    curPage.value = 1; // 重置页码
    updateDirs();
    return;
  } else {
    // 点击了文件
    console.log('点击了文件', dir);
    currentPreviewPath.value = dir;
    previewDialog.value = true;
    // TODO 弹出文件查看对话框
  }
}

function getPreviewUrl() {
  return apiUrls.getFilePreview + currentPreviewPath.value.path;
}

updateDirs();
</script>
