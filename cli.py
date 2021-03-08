from cleo import Application, Command
from BilibiliMangaDownload import download
from pathlib import Path
from loguru import logger


class Download(Command):
    """
    bilibili 漫画下载命令行工具

    bili-comic-download
        {comicId : 想要下载的漫画mc号?}
        {--m|mode= : 下载模式，ep: 根据ep_id来进行下载, ord: 根据顺序来进行下载?}
        {--e|ids= : ep_id 或者 ord_id}
        {--s|sessdata= : 如果要下载已购买的漫画，这个参数是必要的}
    """

    def handle(self):
        try:
            comic_id = int(self.argument('comicId'))
        except ValueError as e:
            self.line("comicId只能为数字")
            raise e
        if mode := self.option('mode'):
            if mode not in {"ep", "ord"}:
                mode = self.choice("1选择下载模式", ["ep", "ord"])
        else:
            mode = self.choice("选择下载模式", ["ep", "ord"])

        ids = self.option('ids')
        id_array = []
        if not ids:
            # TODO: ask 增加验证
            ids = self.ask('请输入需要下载的漫画章节，支持用“,”分隔：\n > ')
        try:
            for split_ids in ids.split(","):
                split_id_array = split_ids.split("-")
                if len(split_id_array) == 2:
                    start, end = int(split_id_array[0]), int(split_id_array[1])
                    id_array += [i for i in range(start, end + 1)]
                else:
                    id_array.append(int(split_id_array[0]))
        except Exception as e:
            logger.error(str(e), ids, mode)
            self.line("输入的ids格式有误，请重新输入")
            raise e

        sessdata = self.option("sessdata")
        if not sessdata:
            sessdata_path = Path("sessdata.txt")
            if Path.exists(Path(sessdata_path)):
                with open(sessdata_path, "r") as f:
                    sessdata = f.read()
            else:
                sessdata = self.ask('请输入sessdata（如果下载的漫画无需登录即可下载，可以留空），获取方式请查询文档：\n > ')

        download(comic_id, mode, id_array, sessdata)


application = Application("bili-comic-download", "0.91")
application.add(Download())

if __name__ == '__main__':
    application.run()
