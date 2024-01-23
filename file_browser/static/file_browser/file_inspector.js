// 接受来自Python的参数
console.log(path);
console.log(type);

// 默认隐藏
image = $("#image")[0];
video = $("#video")[0];
audio = $("#audio")[0];

image.style.display = "none";
video.style.display = "none";
audio.style.display = "none";

// 预览API
var preview_api_url = "/file_browser/api/get_file_preview" + path;
var subtitle_api_url = "/file_browser/api/get_subtitle" + path;

switch (type) {
  case "image":
    image.style.display = "block";
    image.src = preview_api_url;
    break;
  case "video":
    video.style.display = "block";
    video.src = preview_api_url;

    // 获取字幕数据
    var subtitle_api_url = "/file_browser/api/get_subtitle" + path;
    fetch(subtitle_api_url)
      .then((response) => response.text())
      .then((data) => {
        // 创建一个 Blob 来存储字幕数据
        var blob = new Blob([data], { type: "text/vtt" });

        // 创建一个 URL 来引用这个 Blob
        var url = URL.createObjectURL(blob);

        // 创建一个新的 <track> 元素
        var track = document.createElement("track");
        track.kind = "captions";
        track.label = "字幕";
        track.src = url;
        track.default = true;

        // 将 <track> 元素添加到视频元素中
        video.appendChild(track);

        // 更新 Plyr 播放器的字幕
        video_player = new Plyr("#video", {
          tracks: [{ kind: "captions", label: "字幕", src: url, default: true }],
        });
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    break;
  case "audio":
    audio_player = new Plyr("#audio");
    audio.style.display = "block";
    audio.src = preview_api_url;
    break;
  default:
    break;
}
