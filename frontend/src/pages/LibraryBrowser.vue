<template>
    <div class="bg-green q-pa-md">
        <div>Libraries: {{ librariesResponse }}</div>
        <div>Content: {{ libraryContentResponses }}</div>
        <div>Units: {{ mediaUnitResponses }}</div>
        <div>Mode: {{ mode }}</div>
        <div>CurUnit: {{ curUnit }}</div>
        <q-btn @click="switchMode" label="切换模式" />
        <q-btn @click="updateLibraries" label="刷新" />
    </div>

    <!-- Browser模式，展示媒体库列表 -->
    <div v-if="mode === 'browser'" class="text-white">
        <q-list bordered separator v-for="library in librariesResponse?.libraries" :key="library.id">
            <div class="text-h6 text-white">ID:{{ library.id }}, NAME:{{ library.library_name }}</div>

            <!-- 将属于某个库的媒体，展示到库里 -->
            <div v-for="unit_response in mediaUnitResponses" :key="unit_response.id">
                <div v-if="unit_response.library === library.id">
                    {{ unit_response }}
                    <q-btn @click="enterUnit(unit_response.id)" label="进入" />
                </div>
            </div>
        </q-list>
    </div>

    <!-- Inspector模式，展示单元的详细信息 -->
    <div v-if="mode === 'inspector'" class="text-white">
        你正在试图访问 [Unit={{ curUnit?.id }}] 的详细信息。

        {{ curUnit?.id }}
        {{ curUnit?.media_file_refs }}
        <div v-for="media_file_ref in curUnit?.media_file_refs" :key="media_file_ref.id">
            <div>
                ID:{{ media_file_ref.id }}<br />
                DESC:{{ media_file_ref.description }}<br />
                UNIT:{{ media_file_ref.unit }}<br />
            </div>
        </div>

        <q-btn @click="exitUnit" label="返回" />
    </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import apiUrls from 'src/apiUrls';
import { GetLibraryContentResponse, GetMediaLibraryResponse, MediaUnit } from 'src/components/models';

import { ref } from 'vue';

const mode = ref<string>('browser'); // 模式，可以是browser或者inspector
const curUnit = ref<MediaUnit | null>(); // 当前单元的ID

const librariesResponse = ref<GetMediaLibraryResponse | null>();
const libraryContentResponses = ref<GetLibraryContentResponse[] | null>();
const mediaUnitResponses = ref<MediaUnit[] | null>();

function switchMode() {
    if (mode.value === 'browser') {
        mode.value = 'inspector';
    } else {
        mode.value = 'browser';
    }
}

// 当点击了某个媒体Unit, 就切换模式并进入它的详细信息。
function enterUnit(unit_id: number) {
    mode.value = 'inspector';
    curUnit.value = mediaUnitResponses.value?.find((unit) => unit.id === unit_id) || null;
}

// 退出单元模式
function exitUnit() {
    mode.value = 'browser';
}

//
//
//
// ========================================
//
//
//

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
        let unit: MediaUnit | null = await getMediaUnit(unit_id);

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
async function getMediaUnit(unit_id: number): Promise<MediaUnit | null> {
    try {
        const response = await axios.get(apiUrls.getMediaUnit, { params: { unit_id: unit_id } });
        return response.data;
    } catch (error) {
        console.error('getMediaUnitDetail::错误::', error);
        return null;
    }
}
</script>
