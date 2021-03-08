# 介绍
bilibili 漫画批量下载，付费内容可在购买登录后下载

# 安装
## cli
从 [release](https://github.com/renmu123/bilibili-manga-downloader/releases) 下载最新版cli
```
bili-comic-download.exe --help

# 下载漫画 id 为 27923 的 ep438701 话
bili-comic-download.exe bili-comic-download 27923 --mode=ep --ids=438701

# 下载漫画 id 为 25514 的第1-5和7话
bili-comic-download.exe bili-comic-download 25514 --mode=ord --ids=1-5,7
```

## 源码
```
git clone https://github.com/renmu123/bilibili-manga-downloader
cd bilibili-manga-downloader
pip install -r requirements.txt
python cli.py bili-comic-download --help
```

# 使用
```
bili-comic-download.exe bili-comic-download 35514
# 35514 是某个 comic 的 id
# 然后根据提示处理就可以了
# 
```

# 概念解释
ep模式是指后面输入的 id 为漫画的章节号  
ord模式是指后面输入的 id 为漫画的序号

# 获取 comic_id & ep
运行后根据提示操作 例如漫画章节页url https://manga.bilibili.com/mc26742/334263 中

mc号（漫画id）为26742 章节号为334263

## 啥是 ord？
ord 理论上就是漫画的序号，比如第一话就是1，但有时候还会有作者的节日插画，我测试过《高木同学》的漫画，基本都是对应的，如果有不对应，欢迎提 issue

# 获取 sessdata

如要下载的内容中包含付费章节，则需输入SESSDATA，请按以下方式获取SESSDATA

1.在浏览器中登录biliibli漫画，并购买好相应的章节

2.找到Cookie中的SESSDATA，复制其内容。

![image.png](https://i.loli.net/2020/10/26/RBhmXZdl9jJC7pw.png)

**也可以在该 exe 文件夹下新建 sessdata.txt，将上述的 sessdata 复制到其中，可以避免每次都要复制**

图片解析部分来自 https://github.com/flaribbit/bilibili-manga-spider

# TODOS
- [x] 支持同时下载多个
- [x] 支持文件设置 session_data
- [ ] session 过期支持
- [x] 下载的照片格式自动补位
- [x] 未解锁的漫画下载提醒
- [ ] 不进行重复下载