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

export interface GetMediaUnitResponse {
    id: number;
    library: number;
    fsnode: number;
    tmdb_id: number;
    unit_type: string;
    nickname: string;
    query_name: string;
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
}
