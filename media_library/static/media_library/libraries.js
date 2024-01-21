var library_displayer = $("#library-displayer");

function async_display_libraries() {
  $.ajax({
    url: "/media_library/api/get_media_libraries",
    type: "GET",
    success: function (data) {
      library_displayer.html(data);
      data = JSON.parse(data);
      data.libraries.forEach((library) => {
        
        // TODO: 用卡片样式显示媒体库
        let card = $(`<div class="bg-neutral-600 m-4">
                ${library.library_name}
                </div>`);
        library_displayer.append(card);
        
      });
    },
    error: function (data) {
      alert("ERROR");
      console.log(data);
    },
  });
}

async_display_libraries();
