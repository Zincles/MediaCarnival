<script setup lang="ts">
import { defineProps } from "vue";
import { ref } from "vue";
import apiUrls from "../apiUrls";
import axios from "axios";

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
    default: "/",
  },
});

const path = ref(props.path); // 当前路径
const curPage = ref(1); // 当前页码
const pageSize = ref(30); // 每页显示的文件数

const displayedDirs = ref<SubPath[]>([]); // 当前页显示的文件/文件夹
const reachedEnd = ref(false); // 是否到达最后一页

// 从后端获取文件夹内容.会将文件夹内容附加到原来的文件夹内容上
axios
  .get<DirInfo>(apiUrls.getFolder, {
    params: {
      path: props.path, // 路径
      page: curPage.value, // 当前页码
      pageSize: pageSize.value, // 每页显示的文件数
    },
  })
  .then((response) => {
    console.log(response.data);
    displayedDirs.value = displayedDirs.value.concat(response.data.subPaths);
    reachedEnd.value = response.data.isEnd;
  });
</script>

<template>
  <div class="text-white text-center">
    <h1 class="text-2xl text-center">文件浏览器（移植中）</h1>
    当前路径： {{ path }}<br />
    访问API地址：{{ apiUrls.getFolder }}<br />
    <br /><br />

    <div v-for="dir in displayedDirs" :key="dir.path">BASE={{ dir.basename }}<br /></div>
    
    
    是否到达最后一页：{{ reachedEnd }}
  </div>
</template>
