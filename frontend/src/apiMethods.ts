import axios from 'axios';
import apiUrls from './apiUrls';

export async function getTmdbTvSeriesMetadata(unit_id: number | undefined) {
    const response = await axios.get(apiUrls.getTmdbTvSeriesMetadataByUnit, {
        params: {
            unit_id: unit_id,
        },
    });
    return response.data;
}

// 获取某个Episode的 TMDB 信息。需要提供 unit_id, season, episode
export async function getTmdbTvEpisodeMetadata(
    unit_id: number | undefined,
    season: number | undefined,
    episode: number | undefined,
) {
    const response = await axios.get(apiUrls.getTmdbTvEpisodeMetadataByUnit, {
        params: {
            unit_id: unit_id,
            season: season,
            episode: episode,
        },
    });
    return response.data;
}

export default {
    getTmdbTvSeriesMetadata,
    getTmdbTvEpisodeMetadata,
};
