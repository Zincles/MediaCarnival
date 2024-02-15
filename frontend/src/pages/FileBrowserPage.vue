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
    default: '/',
  },
});

const currentPath = ref(props.path); // 当前路径
// const display_column = ref(3); // 显示列数

const curPage = ref(1); // 当前页码
const totalPages = ref(1); // 总页数
const pageSize = ref(30); // 每页显示的文件数

const displayedDirs = ref<SubPath[]>([]); // 当前页显示的文件/文件夹
const reachedEnd = ref(false); // 是否到达最后一页

watch(currentPath, () => {
  // 确保路径改变时，页码重置为1
  curPage.value = 1;
});

// 从后端获取文件夹内容.会将文件夹内容附加到原来的文件夹内容上.
function updateDirs() {
  displayedDirs.value = []; // 清空原来的文件夹内容

  // 添加“..”路径
  displayedDirs.value.push({
    path: dirname(currentPath.value), // 所在目录的路径，调用path-browserify的dirname方法
    basename: '..',
    type: '..',
  });

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
      totalPages.value = response.data.totalPages;
      displayedDirs.value = displayedDirs.value.concat(response.data.subPaths); // 将文件夹内容附加到原来的文件夹内容上
      reachedEnd.value = response.data.isEnd;
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

    // TODO 弹出文件查看对话框
  }
}

updateDirs();
</script>

<template>
  <q-page padding>
    <div class="text-h5 text-center q-my-md">文件浏览器</div>
    <div>当前路径： {{ currentPath }}</div>
    <div>访问API地址：{{ apiUrls.getFolder }}</div>

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

    <!-- 分页器 -->
    <div>
      <div class="flex flex-center">{{ curPage }}/{{ totalPages }}页</div>
      <div class="flex flex-center">
        <q-btn label="上一页" @click="loadPrevPage" :disable="curPage <= 1" class="q-mt-md" />
        <q-btn label="下一页" @click="loadNextPage" :disable="reachedEnd" class="q-mt-md" />
      </div>
    </div>
  </q-page>

  <!-- <q-page z-index:1000 style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center;">
  <q-card style="width: 90%; height: 100%;">
    <q-card-section class="items-center justify-center row full-height">
      <div class="text-h6">这是一个全屏的对话框</div>
    </q-card-section>
  </q-card>
</q-page> -->
</template>
