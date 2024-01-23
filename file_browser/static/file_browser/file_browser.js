// 用于处理文件浏览器的前端逻辑。path在django html中定义。
console.log(path);

var page = 1;
var page_size = 50;

var isLoading = false;

var macyInstances = [];

// 判断文件是否为图片
function isImage(filename) {
  var extension = filename.split(".").pop().toLowerCase();
  return ["jpg", "jpeg", "png", "gif", "webp", "svg"].includes(extension);
}

function recalcAllMacy() {
  console.log("尝试重新排列所有Macy:", macyInstances.length, macyInstances);

  macyInstances.forEach((macyInstance) => {
    console.log("Recalc: ", macyInstance.recalculate(true));
  });
}

function getIcon(filename, is_folder = false) {
  //console.log(filename, is_folder)
  var extension = filename.split(".").pop().toLowerCase();
  var result = "";

  if (is_folder) {
    result = "fas fa-folder";
  } else if (["jpg", "png", "gif"].includes(extension)) {
    result = "fas fa-file-image";
  } else if (["mp4", "avi", "mkv"].includes(extension)) {
    result = "fas fa-file-video";
  } else if (["mp3", "wav", "flac"].includes(extension)) {
    result = "fas fa-file-audio";
  } else if (["doc", "docx"].includes(extension)) {
    result = "fas fa-file-word";
  } else if (["xls", "xlsx"].includes(extension)) {
    result = "fas fa-file-excel";
  } else if (["ppt", "pptx"].includes(extension)) {
    result = "fas fa-file-powerpoint";
  } else if (["pdf"].includes(extension)) {
    result = "fas fa-file-pdf";
  } else if (["zip", "rar", "7z"].includes(extension)) {
    result = "fas fa-file-archive";
  } else if (["txt"].includes(extension)) {
    result = "fas fa-file-alt";
  } else {
    result = "fas fa-file";
  }
  return `<i class="${result} text-5xl text-neutral-200"></i>`;
}

// 判断文件是否可以预览
function isPreviewable(filename) {
  return isImage(filename);
}

// 读取文件。可设置为网格或流式样式。（grid, flow）
// 流式样式高度不固定，网格样式各元素大小完全固定。

function asyncLoadFiles(style = "flow", column = 2) {
  return new Promise((resolve, reject) => {
    if (isLoading) {
      resolve();
      return;
    }

    isLoading = true;

    $.ajax({
      url: "/file_browser/api/get_folder" + path + "/",
      data: {
        page: page,
        page_size: page_size,
      },
      success: function (data) {
        data = JSON.parse(data);

        // 如果没有数据了，就不再加载
        if (data.paths.length == 0) {
          isLoading = true;
          resolve();
          return;
        }
        page += 1;

        const data_paths = data.paths;
        const data_names = data.names;

        // 添加分隔符，用于分隔两个不同批次的文件集合
        const total_pages = data.total_pages;
        let splitter = $(`<div class='text-center text-white text-sm m-2'>
                <div class="text-sm round-lg bg-neutral-800 rounded-lg p-1">第${page - 1}页  /  共${total_pages}页</div>
              </div>`);
        $("#macy-containers").append(splitter);

        // 创建容器，创建Macy实例，将容器添加到DOM中
        let macyContainer = $('<div class="macy-container"></div>');
        let macyInstance = Macy({
          container: macyContainer[0],
          margin: 16,
          columns: column,
        });
        macyInstances.push(macyInstance);
        macyContainer[0].macyinstance = macyInstance;
        $("#macy-containers").append(macyContainer[0]);
        macyInstance.runOnImageLoad(() => {
          macyInstance.recalculate();
        }, true);

        // 遍历元素，向容器添加元素
        data_paths.forEach((path, index) => {
          const name = data_names[index];
          const path_url = "/file_browser/browser" + path;
          const type = data.types[index];

          let card = $(
            `<a href="${path_url}" class="card hover:bg-blue-500 shadow bg-neutral-700 rounded-lg  overflow-hidden p-2 "></a>`
          );
          macyContainer.append(card);
          let icon = isPreviewable(name) && style == "flow" ? "" : getIcon(name, type == "folder");

          card.append(`<div class="flex justify-center items-center">${icon}</div>`); // 设置卡片的图标
          card.append(`<p class=" text-white text-center whitespace-nowrap overflow-ellipsis">${name}</p>`); // 设置文本

          // 是文本且为FLOW,则考虑显示图像
          if (isImage(name) && style == "flow") {
            card[0].setAttribute("target", "_blank");
            card[0].setAttribute("rel", "noreferrer noopener");
            let api_url = "/file_browser/api/get_file_preview" + path;

            // 创建一个占位符
            let placeholder = $('<div class="w-full h-full bg-gray-200"></div>');
            card.append(placeholder);

            // 创建图像元素，但不立即添加到 DOM 中. 当图像加载完成后，替换占位符
            let preview = $(`<img src="${api_url}" class="w-full h-full object-cover">`);
            preview.on("load", function () {
              placeholder.replaceWith(preview);
              macyInstance.recalculate(true);
            });
          }
        });
        isLoading = false;
        recalcAllMacy();
        resolve();
        return;
      },

      error: function (data) {
        isLoading = false;

        data = data.response;
        alert(data);
        reject();
        return;
      },
    });
  });
}

// 处理滚动事件，当滚动到底部时，加载更多文件。
$(window).scroll(function () {
  if ($(document).height() - $(window).scrollTop() - $(window).height() <= 10) {
    console.log("Reached bottom!");
    asyncLoadFiles().then(recalcAllMacy);
  }
});

$(document).ready(function () {
  asyncLoadFiles().then(function () {
    setTimeout(() => {
      recalcAllMacy();
    }, 1);
  });
});
