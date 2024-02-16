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


export interface GetMediaLibraryResponse {
  libraries: MediaLibrary[];
}

// 一个媒体库的信息
export interface MediaLibrary {
  id: number;
  library_name: string;
}
