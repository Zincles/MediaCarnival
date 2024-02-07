# 当前状况？
正在试图使用Vue重构原本那令人作呕的前端，Django将仅作为服务，提供后端API
这需要一段时间，但是能让整个项目变得更加可读

# Media Carnival

一个基于 python django 编写的媒体库。名称源于 Emby 的某个第三方修改版本。<br>
它仍缺少基本的作为媒体库的功能，离完成还需要不少功夫。<br>

## 功能？

Media Carnival 是作为 Emby 的仿制品开发的，所以功能大概和它相似。<br>
我大概不会尝试去实现“不太有用”的部分，比如“系列”之类的东西。<br>
开发会优先考虑补足其不足之处，例如对更多媒体格式的支持，等。<br>

## 进度？

代码质量取决于编写时作者的精神状态。<br>
离完成还遥遥无期。<br>
也请不要吐槽中文注释和中文 readme.md,正式版本再考虑别的。<br>

## 部署？

和一般的 Django 应用程序一样，在安装了`requirements.txt`里的 python 依赖后，使用: <br>

初始化迁并移数据库: <br>

> python manage.py makemigrations <br>
> python manage.py migrate <br>

运行工程 <br>

> python manage.py run <br>

请不要对奇怪的 requirements 产生疑惑，我会正式版本会尝试精简的。 <br>

## 外部库？

感谢这些很棒的第三方库，它们为我省下了不少时间。（还有其他的库，暂未列出）<br>
<a href="https://github.com/jquery/jquery" >JQuery</a>
<a href="https://github.com/tailwindlabs/tailwindcss" >Tailwind CSS</a>
<a href="https://github.com/shiyiya/oplayer" >OPlayer</a>
<a href="https://github.com/sampotts/plyr" >plyr</a>
<a href="https://github.com/bigbite/macy.js" >Macy.js</a>
<a href="https://github.com/juliangarnier/anime/" >anime.js</a>
<a href="https://fontawesome.com/start" >font-awesome-free-v5</a>
