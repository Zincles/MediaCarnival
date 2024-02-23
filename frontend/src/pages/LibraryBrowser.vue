<template>
    <div class="bg-green q-pa-md">
        <div v-if="mode === 'browser'">
            <div>Libraries: {{ librariesResponse }}</div>
            <div>Content: {{ libraryContentResponses }}</div>
            <div>Units: {{ mediaUnitResponses }}</div>
            <div>Mode: {{ mode }}</div>
            <div>CurUnit: {{ curUnit }}</div>
        </div>
        <div v-if="mode === 'inspector'">
            <div>metadata:{{ mediaUnitTmdbTvSeriesMetadata }}</div>
            <div>episodeTmdbMetadatas:{{ episodeTmdbMetadatas }}</div>
        </div>
        <q-btn @click="switchMode" label="切换模式" />
        <q-btn @click="updateLibraries" label="刷新" />
    </div>

    <!-- Browser模式，展示媒体库列表 -->
    <div v-if="mode === 'browser'" class="text-white">
        <q-list bordered separator v-for="library in librariesResponse?.libraries" :key="library.id">
            <div class="text-h6 text-white">ID:{{ library.id }}, NAME:{{ library.library_name }}</div>

            <!-- 将属于某个库的媒体，展示到库里 -->
            <div v-for="unit_response in mediaUnitResponses" :key="unit_response.id">
                <!-- 媒体Ref条目 -->
                <div v-if="unit_response.library === library.id">
                    {{ unit_response }}
                    <q-btn @click="enterUnit(unit_response.id)" label="进入" />
                </div>
            </div>
        </q-list>
    </div>

    <!-- Inspector模式，展示单元的详细信息 -->
    <div v-if="mode === 'inspector'" class="text-white q-ma-md">
        <q-card class="bg-grey-9 q-ma-lg q-pa-lg">
            <div class="text-h5">{{ mediaUnitTmdbTvSeriesMetadata?.name }}</div>
            {{ mediaUnitTmdbTvSeriesMetadata?.overview }}<br />
            发行日期：{{ mediaUnitTmdbTvSeriesMetadata?.first_air_date }}<br />
            语言：{{ mediaUnitTmdbTvSeriesMetadata?.original_language }}<br />
            评分：{{ mediaUnitTmdbTvSeriesMetadata?.vote_average }}<br />
            评分人数：{{ mediaUnitTmdbTvSeriesMetadata?.vote_count }}<br />
            总集数：{{ mediaUnitTmdbTvSeriesMetadata?.number_of_episodes }}<br />
            总季数：{{ mediaUnitTmdbTvSeriesMetadata?.number_of_seasons }}<br />
        </q-card>

        <q-list v-for="media_file_ref in curUnit?.media_file_refs" :key="media_file_ref.id">
            <q-item>
                <q-card class="row bg-grey-9" flat bordered>
                    <q-card-section horizontal>
                        <!-- 图像 -->
                        <q-card-section class="">
                            <q-img class="bg-white" style="height: 120px; width: 200px" />
                        </q-card-section>

                        <!-- 文字描述 -->
                        <q-card-section class="">
                            <!-- 标题 -->
                            <q-item-label class="text-lg">{{
                                getEpisodeDisplayTitle(media_file_ref.season, media_file_ref.episode)
                            }}</q-item-label>

                            <!-- 描述 -->
                            <q-item-label class="text-grey-6">{{
                                findEpisodeMetadata(media_file_ref.season, media_file_ref.episode)?.overview
                            }}</q-item-label>
                        </q-card-section>
                    </q-card-section>
                </q-card>
            </q-item>
        </q-list>

        <q-btn @click="exitUnit" label="返回" />
    </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import apiUrls from 'src/apiUrls';
import apiMethods from 'src/apiMethods';

import {
    GetLibraryContentResponse,
    GetMediaLibraryResponse,
    MediaUnit,
    TmdbTvEpisodeMetadata,
    TmdbTvSeriesMetadata,
} from 'src/components/models';

import { ref } from 'vue';

const mode = ref<string>('browser'); // 模式，可以是browser或者inspector
const curUnit = ref<MediaUnit | null>(); // 当前单元的ID

const librariesResponse = ref<GetMediaLibraryResponse | null>();
const libraryContentResponses = ref<GetLibraryContentResponse[] | null>();
const mediaUnitResponses = ref<MediaUnit[] | null>();

const mediaUnitTmdbTvSeriesMetadata = ref<TmdbTvSeriesMetadata | null>();
const episodeTmdbMetadatas = ref<TmdbTvEpisodeMetadata[] | null>(); // 用于存储每个episode的元数据

function switchMode() {
    if (mode.value === 'browser') {
        mode.value = 'inspector';
    } else {
        mode.value = 'browser';
    }
}

// GUI元件。根据season和episode，获取显示的标题
function getEpisodeDisplayTitle(season: number | null, episode: number | null): string {
    if (season === null || episode === null) return 'Unknown Episode';

    let episode_meta = findEpisodeMetadata(season, episode);
    if (episode_meta === null) return `S${season}E${episode}`;
    else return `S${season}E${episode}: ${episode_meta.name}`;
}

// 根据season和episode，获取episode的元数据
function findEpisodeMetadata(season: number | null, episode: number | null): TmdbTvEpisodeMetadata | null {
    // 如果season 或者 episode是null，就返回null
    if (season === null || episode === null) return null;

    let data = episodeTmdbMetadatas.value?.find(
        (metadata) => metadata.season_number === season && metadata.episode_number === episode,
    );
    if (data === undefined) return null;
    else return data;
}

// 根据已有curUnit以及media_file_refs，更新episodeTmdbMetadatas
function updateEpisodeTmdbMetadatas() {
    episodeTmdbMetadatas.value = [];

    if (curUnit.value === null) return;

    let media_file_refs = curUnit.value?.media_file_refs;
    if (media_file_refs === null) return;

    media_file_refs?.forEach(async (media_file_ref) => {
        let metadata = await apiMethods.getTmdbTvEpisodeMetadata(
            media_file_ref.unit,
            media_file_ref.season ?? undefined,
            media_file_ref.episode ?? undefined,
        );
        episodeTmdbMetadatas.value?.push(metadata);
    });
}

// 当点击了某个媒体Unit, 就切换模式并进入它的详细信息。
async function enterUnit(unit_id: number) {
    mode.value = 'inspector';
    curUnit.value = mediaUnitResponses.value?.find((unit) => unit.id === unit_id) || null;

    let metadata = await apiMethods.getTmdbTvSeriesMetadata(curUnit.value?.id);
    mediaUnitTmdbTvSeriesMetadata.value = metadata;
    updateEpisodeTmdbMetadatas();

    // 对episode metadatas排序
    episodeTmdbMetadatas.value?.sort((a, b) => {
        if (a.season_number === b.season_number) {
            return a.episode_number - b.episode_number;
        } else {
            return a.season_number - b.season_number;
        }
    });

    // 对curUnit内的media_file_refs排序
    curUnit.value?.media_file_refs.sort((a, b) => {
        if (a.season === b.season) {
            return (a.episode ?? 0) - (b.episode ?? 0);
        } else {
            return (a.season ?? 0) - (b.season ?? 0);
        }
    });
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
