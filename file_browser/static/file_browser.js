var json = JSON.parse(document.getElementById("path_files_folders_json").textContent)

var path = json[0];    // 当前所在路径。 STR
var files = json[1];   // 当前路径下文件。 ARR STR
var folders = json[2]; // 文件夹 ARR STR

var displayer = document.getElementById("file_displayer") // 显示用工具



alert((path))
alert((files))
alert((folders))