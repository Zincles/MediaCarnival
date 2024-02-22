<template>
    <div class="text-white">
        <div>Libraries: {{ librariesResponse }}</div>
        <div>Content: {{ libraryContentResponses }}</div>
        <div>Units: {{ mediaUnitResponses }}</div>
        <q-list bordered separator v-for="library in librariesResponse?.libraries" :key="library.id">
            <div class="text-h6 text-white">{{ library }}</div>
            <div></div>
        </q-list>
    </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import apiUrls from 'src/apiUrls';
import { GetLibraryContentResponse, GetMediaLibraryResponse, GetMediaUnitResponse } from 'src/components/models';

import { ref } from 'vue';

const librariesResponse = ref<GetMediaLibraryResponse | null>();
const libraryContentResponses = ref<GetLibraryContentResponse[] | null>();
const mediaUnitResponses = ref<GetMediaUnitResponse[] | null>();

async function updateLibraries() {
    // 获取媒体库列表
    librariesResponse.value = await getMediaLibraries();
    libraryContentResponses.value = [];
    mediaUnitResponses.value = [];

    let libraryIds: number[] = []; // 媒体库ID列表

    let mediaUnitIds: number[] = []; // 所有显示在浏览器里的库的单元的ID构成的列表

    // 遍历每个媒体库，把它的ID全部添加到上面的数组里。
    librariesResponse.value?.libraries.forEach((library) => {
        libraryIds.push(library.id);
    });

    // 遍历每个媒体库，获取其详细信息，并把它的所有存在的unit_id全部添加到上面的数组里。
    await Promise.all(
        libraryIds.map(async (libraryId) => {
            // 获取媒体库的媒体文件列表，追加到列表中
            let library: GetLibraryContentResponse | null = await getMediaLibraryContent(libraryId);
            if (library === null) {
                console.log('获取媒体库内容失败');
                return;
            }
            libraryContentResponses.value?.push(library);

            console.log('获取媒体库内容成功！媒体库信息:', library);
            library.units_id.forEach((unit_id) => {
                mediaUnitIds.push(unit_id);
            });
        }),
    );

    // 获取每个单元的详细信息
    mediaUnitIds.forEach(async (unit_id) => {
        let unit: GetMediaUnitResponse | null = await getMediaUnit(unit_id);

        if (unit !== null) {
            mediaUnitResponses.value?.push(unit);
            console.log('媒体单元信息:', unit);
        }
    });
}

// 页面加载时，获取媒体库列表
async function update() {
    await updateLibraries();
}

update();

//
//
//
// ========================================
//
//
//

//调用API，获取媒体库列表
async function getMediaLibraries(): Promise<GetMediaLibraryResponse | null> {
    try {
        const response = await axios.get<GetMediaLibraryResponse>(apiUrls.getMediaLibraries, {});
        return response.data;
    } catch (error) {
        console.error(error);
        return null;
    }
}

// 调用API，获取具体的媒体库的媒体文件列表
async function getMediaLibraryContent(library_id: number): Promise<GetLibraryContentResponse | null> {
    console.log('访问Library ID: ', library_id);
    try {
        const response = await axios.get<GetLibraryContentResponse>(apiUrls.getMediaLibraryContent, {
            params: { library_id: library_id },
        });
        return response.data;
    } catch (error) {
        console.error('getMediaLibraryContent::错误::', error);
        return null;
    }
}

// 调用API,获取MediaUnit的详细信息
async function getMediaUnit(unit_id: number): Promise<GetMediaUnitResponse | null> {
    try {
        const response = await axios.get(apiUrls.getMediaUnit, { params: { unit_id: unit_id } });
        return response.data;
    } catch (error) {
        console.error('getMediaUnitDetail::错误::', error);
        return null;
    }
}
</script>
