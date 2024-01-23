var library_displayer = $("#library-displayer");

function async_display_libraries() {
  $.ajax({
    url: "/media_library/api/get_media_libraries",
    type: "GET",
    success: function (data) {
      library_displayer.html(data);
      data = JSON.parse(data);
      data.libraries.forEach((library) => {
        // 媒体库预览用容器。展示前几个节目的缩略图
        let library_title = $(`<div class="text-md">${library.library_name}</div>`);
        let container = $(`<div class="flex flex-row bg-neutral-800 m-1 p-1 rounded-lg"></div>`);
        let placeholder = $(
          `<div class="flex flex-col items-center justify-center m-4"><div class="bg-gray-300 h-48 w-32"></div><label class="text-sm text-center">SHOW1</label></div>`
        );
        let placeholder2 = $(
          `<div class="flex flex-col items-center justify-center m-4"><div class="bg-gray-300 h-48 w-32"></div><label class="text-sm text-center">SHOW1</label></div>`
        );
        container.append(placeholder);
        container.append(placeholder2);
        library_displayer.append(library_title);
        library_displayer.append(container);
      });
    },
    error: function (data) {
      alert("ERROR");
      console.log(data);
    },
  });
}

async_display_libraries();
