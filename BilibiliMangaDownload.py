import json
import os
import re
import zipfile
from io import BytesIO
from pathlib import Path
import requests

URL_DETAIL = "https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web"
URL_IMAGE_INDEX = "https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web"
URL_MANGA_HOST = "https://manga.hdslb.com"
URL_IMAGE_TOKEN = "https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web"

cookies = {}


def download_image(url: str, path: str):
    r = requests.get(url, cookies=cookies, verify=False)
    with open(path, 'wb') as f:
        f.write(r.content)


def get_manga_info(comic_id: int):
    data = requests.post(URL_DETAIL, data={'comic_id': comic_id}).json()['data']
    return data['title'], data['ep_list']


def get_images(comic_id: int, ep_id: int):
    data = requests.post(URL_IMAGE_INDEX, data={'ep_id': ep_id}, cookies=cookies).json()['data']
    data = bytearray(requests.get(data['host'] + data['path']).content[9:])
    key = [ep_id & 0xff, ep_id >> 8 & 0xff, ep_id >> 16 & 0xff, ep_id >> 24 & 0xff, comic_id & 0xff,
           comic_id >> 8 & 0xff,
           comic_id >> 16 & 0xff, comic_id >> 24 & 0xff]
    for i in range(len(data)):
        data[i] ^= key[i % 8]
    file = BytesIO(data)
    zf = zipfile.ZipFile(file)
    data = json.loads(zf.read('index.dat'))
    zf.close()
    file.close()
    print("aaa", data)
    return data['pics']


def get_token(url: str):
    # data = requests.post(URL_IMAGE_TOKEN, data={"urls": "[\"" + url + "\"]"}, cookies=cookies).json()["data"][0]
    data = requests.post(URL_IMAGE_TOKEN, data={"urls": "[\"" + url + "\"]"}, cookies=cookies).json()["data"][0]
    print(data)
    return f'{data["url"]}?token={data["token"]}'


# def download_manga(comic_id, ep_id, ch_name):
#     if not (os.path.exists(f'downloads/{title}/{ch_name}')):
#         os.mkdir(f'downloads/{title}/{ch_name}')
#     print(f'[INFO]{ch_name}开始下载')
#     image_list = get_images(comic_id, ep_id)
#     for idx, url in enumerate(image_list, 1):
#         full_url = get_token(url)
#         path = f'downloads/{title}/{ch_name}/{idx}.jpg'
#         download_image(full_url, path)
#     print('[INFO]%s下载完成' % ch_name)


def filter_str(name):
    return re.sub(r'[\\/:*?"<>|]', '', name).strip().rstrip('.')


def main():
    if not (Path.exists(Path("downloads"))):
        os.mkdir('downloads')
    # comic_id = int(input("请输入mc号："))
    comic_id = 25514
    title, ep_list = get_manga_info(comic_id)
    print(title, ep_list)
    print('[INFO]', title)

    # if not (os.path.exists(f'downloads/{title}')):
    #     os.mkdir(f'downloads/{title}')

    # sessdata = "10a5ce8f%2C1620394062%2C6d782*b1"
    sessdata_path = Path("sessdata.txt")

    if Path.exists(Path(sessdata_path)):
        with open(sessdata_path, "r") as f:
            cookies['SESSDATA'] = f.read()
    else:
        cookies['SESSDATA'] = input("请按说明粘贴SESSDATA：")

    ep_id_list = [512551]
    ep_data_list = [data for data in ep_list if data["id"] in ep_id_list]
    # ep_data = [data for data in ep_list if data["ord"] in [ord_list]]

    for ep_data in ep_data_list:
        image_list = get_images(comic_id, ep_data["id"])
        print(f'[INFO] 第 {ep_data["short_title"]} 话开始下载')
        dir_path = Path(f'downloads/{title}/{ep_data["short_title"] + ep_data["title"]}')
        dir_path.mkdir(parents=True, exist_ok=True)

        for index, image_url in enumerate(image_list, 1):
            full_url = get_token(image_url)
            path = dir_path / f'{index}.jpg'
            download_image(full_url, path)

    print("下载完毕")


if __name__ == "__main__":
    # TODO: 支持连续下载
    # TODO: 支持文件设置 session_data
    # TODO: session 过期支持
    # TODO: 下载的照片格式命名

    main()

