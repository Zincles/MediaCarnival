## 当前状况？

正在试图使用 Vue 重构原本那令人作呕的前端，Django 将仅作为服务，提供后端 API<br>
这需要一段时间，但是能让整个项目变得更加可读<br>
<br>
目前尚不可用。请勿试图部署。包括本 README 也处于施工状态。<br>

## 功能？

一个基于 python django 编写的媒体库。名称源于 Emby 的某个第三方修改版本。<br>
它仍缺少基本的作为媒体库的功能，离完成还需要不少功夫。<br>
Media Carnival 是作为 Emby 的仿制品开发的，所以功能大概和它相似。<br>
我大概不会尝试去实现“不太有用”的部分，比如“系列”之类的东西。<br>
开发会优先考虑补足其不足之处，例如对更多媒体格式的支持，等。<br>

## 部署？

你需要同时运行 Django 后端与 vite 前端，才可以完整使用这个项目： <br>

初始化迁并移数据库， 然后运行: <br>

> python manage.py makemigrations <br>
> python manage.py migrate <br>
> python manage.py run <br>
> 这将会在 8080 端口处暴露 API。<br>

运行 Vite 前端<br>

> ./run.sh

## 仍在施工中

WORKING ON PROGRESS..
