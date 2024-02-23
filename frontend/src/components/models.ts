export interface Todo {
    id: number;
    content: string;
}

export interface Meta {
    totalCount: number;
}

// 一个文件/文件夹的信息
export interface SubPath {
    path: string;
    basename: string;
    type: string;
    index: number;
}

// 获取所有媒体库。通过直接访问 http://0.0.0.0:8000/api/get_media_libraries 获取
export interface GetMediaLibraryResponse {
    libraries: MediaLibrary[];
}

// 一个媒体库的信息
export interface MediaLibrary {
    id: number;
    library_name: string;
}

// 函数响应。
// {"id": 2, "library_name": "\u52a8\u6f2b\u5a92\u4f53\u5e93", "units": [{"id": 5, "library": 2, "fsnode": 24, "tmdb_id": 217512, "unit_type": "TV", "nickname": "16Bit\u7684\u611f\u52a8", "query_name": "16bit Sensation"}]}
export interface GetLibraryContentResponse {
    id: number;
    library_name: string;
    units_id: number[];
}

// 一个媒体单元的信息
export interface MediaUnit {
    id: number;
    library: number;
    fsnode: number;
    tmdb_id: number;
    unit_type: string;
    nickname: string;
    query_name: string;
    media_file_refs: MediaFileRef[];
}

export interface MediaFileRef {
    id: number;
    fsnode: number;
    unit: number;
    media_type: string;
    description: string;
    episode: number | null;
    season: number | null;
}

// TmdbTvSeriesMetadata 是从 TMDB API 获取到的数据
export interface TmdbTvEpisodeMetadata {
    air_date: string;
    crew: unknown[];
    episode_number: number;
    guest_stars: unknown[];
    name: string;
    overview: string;
    id: number;
    production_code: string;
    runtime: number;
    season_number: number;
    still_path: string;
    vote_average: number;
    vote_count: number;
}

export interface TmdbTvSeriesMetadata {
    adult: boolean;
    backdrop_path: string;
    created_by: unknown[];
    episode_run_time: number[];
    first_air_date: string;
    genres: { id: number; name: string }[];
    homepage: string;
    id: number;
    in_production: boolean;
    languages: string[];
    last_air_date: string;
    last_episode_to_air: {
        id: number;
        name: string;
        overview: string;
        vote_average: number;
        vote_count: number;
        air_date: string;
        episode_number: number;
        episode_type: string;
        production_code: string;
        runtime: number;
        season_number: number;
        show_id: number;
        still_path: string;
    };
    name: string;
    next_episode_to_air: null;
    networks: {
        id: number;
        logo_path: string;
        name: string;
        origin_country: string;
    }[];
    number_of_episodes: number;
    number_of_seasons: number;
    origin_country: string[];
    original_language: string;
    original_name: string;
    overview: string;
    popularity: number;
    poster_path: string;
    production_companies: {
        id: number;
        logo_path: string | null;
        name: string;
        origin_country: string;
    }[];
    production_countries: {
        iso_3166_1: string;
        name: string;
    }[];
    seasons: {
        air_date: string;
        episode_count: number;
        id: number;
        name: string;
        overview: string;
        poster_path: string;
        season_number: number;
        vote_average: number;
    }[];
    spoken_languages: {
        english_name: string;
        iso_639_1: string;
        name: string;
    }[];
    status: string;
    tagline: string;
    type: string;
    vote_average: number;
    vote_count: number;
}
