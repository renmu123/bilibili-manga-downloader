# 介绍
bilibili 漫画批量下载，付费内容可在购买登录后下载

# 安装
## cli
从 [release](https://github.com/renmu123/bilibili-manga-downloader/releases) 下载最新版cli
```
bili-comic-download.exe --help
```

## 源码
```
git clone https://github.com/renmu123/bilibili-manga-downloader
cd bilibili-manga-downloader
pip install -r requirements.txt
python cli.py bili-comic-download --help
```

# 使用

# 获取 sessdata
运行后根据提示操作 例如漫画章节页url https://manga.bilibili.com/mc26742/334263 中

mc号为26742 章节号为334263

如要下载的内容中包含付费章节，则需输入SESSDATA，请按以下方式获取SESSDATA

1.在浏览器中登录biliibli漫画，并购买好相应的章节

2.找到Cookie中的SESSDATA，复制其内容。

![image.png](https://i.loli.net/2020/10/26/RBhmXZdl9jJC7pw.png)

图片解析部分来自 https://github.com/flaribbit/bilibili-manga-spider

# TODOS
- [x] 支持同时下载多个
- [x] 支持文件设置 session_data
- [ ] session 过期支持
- [x] 下载的照片格式自动补位
- [x] 未解锁的漫画下载提醒
- [ ] 不进行重复下载