// 调用api,通过路径，获取图片
var path = "{{path}}";

var image_api_url = "/file_browser/api/get_image" + path;
var video_api_url = "/file_browser/api/get_video" + path;



// 判断文件是否为图片
function isImage(filename) {
  var extension = filename.split(".").pop().toLowerCase();
  return ["jpg", "jpeg", "png", "gif", "webp", "svg"].includes(extension);
}

function isVideo(filename) {
  var extension = filename.split(".").pop().toLowerCase();
  return ["mp4", "avi", "mov", "wmv", "flv", "mkv"].includes(extension);
}

function getExtensionWithoutDot(filename) {
  var parts = filename.split(".");
  return parts.pop().toLowerCase();
}

if (isImage(path)) {
  $.ajax({
    url: image_api_url,
    type: "GET",
    processData: false,
    xhrFields: {
      responseType: "blob",
    },
    success: function (blob) {
      let img = $("#image")[0];
      img.src = URL.createObjectURL(blob);
      img.class = "object-contain max-w-full, max-h-full, h-auto";
    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.error("Error:", textStatus, errorThrown);
    },
  });
} else {
  // if (isVideo(path)) {
  video_displayer = $("#video")[0];
  video_displayer.src = video_api_url;
  console.log(video_displayer.src);
}
