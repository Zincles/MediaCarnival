<script setup lang="ts">
import { defineProps } from 'vue';
import { ref } from 'vue';
import apiUrls from '../apiUrls';
import axios from 'axios';
import { dirname } from 'path-browserify';

// 一个路径下的文件/文件夹信息。
interface DirInfo {
  page: number; // 当前页码
  pageSize: number; // 每页的数量
  totalPages: number; // 总页数
  totalDirs: number; // 总文件数(非单页)
  isEnd: boolean; // 是否到达最后一页
  subPaths: SubPath[]; // 当前目录下的子目录（文件/文件夹）
}

// 一个文件/文件夹的信息
interface SubPath {
  path: string;
  basename: string;
  type: string;
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

// 从后端获取文件夹内容.会将文件夹内容附加到原来的文件夹内容上.
function updateDirs() {
  displayedDirs.value = []; // 清空原来的文件夹内容

  // 添加“..”路径
  displayedDirs.value.push({
    path: dirname(currentPath.value), // 所在目录的路径，调用path-browserify的dirname方法
    basename: '..',
    type: 'dir',
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
  // alert("点击了文件夹：" + dir.basename);
  currentPath.value = dir.path;
  updateDirs();
  // alert(displayedDirs.value.toString());
}

updateDirs();
</script>

<template>
  <div class="text-white text-center bg-neutral-800 rounded-2xl m-2 p-2">
    <h1 class="text-2xl text-center">文件浏览器（移植中）</h1>
    当前路径： {{ path }}<br />
    访问API地址：{{ apiUrls.getFolder }}<br />
    <br /><br />

    <div v-for="dir in displayedDirs" :key="dir.path">
      <div
        class="rounded-lg text-xl bg-neutral-700 m-2 hover:bg-blue-500"
        @click="clickDir(dir)"
      >
        {{ dir.basename }}
      </div>
    </div>

    {{ curPage }}/{{ totalPages }}页
    <div>
      <button
        class="rounded-2xl bg-neutral-600 m-1 p-1"
        v-if="curPage >= 2"
        @click="loadPrevPage"
      >
        上一页
      </button>
      <button
        class="rounded-2xl bg-neutral-600 m-1 p-1"
        v-if="!reachedEnd"
        @click="loadNextPage"
      >
        下一页
      </button>
    </div>
  </div>
</template>
