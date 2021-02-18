import json
import os
import re
import zipfile
from io import BytesIO
from pathlib import Path
import requests
from tenacity import retry, stop_after_attempt
from loguru import logger
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning
from typing import Literal, List

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

URL_DETAIL = "https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web"
URL_IMAGE_INDEX = "https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web"
URL_MANGA_HOST = "https://manga.hdslb.com"
URL_IMAGE_TOKEN = "https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web"

cookies = {}

# TODO: 支持连续下载
# TODO: 支持文件设置 session_data
# TODO: session 过期支持
# TODO: 下载的照片格式命名


@retry(stop=stop_after_attempt(3))
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
    return data['pics']


def get_token(url: str):
    data = requests.post(URL_IMAGE_TOKEN, data={"urls": f'["{url}"]'}, cookies=cookies).json()["data"][0]
    return f'{data["url"]}?token={data["token"]}'


def filter_str(name):
    return re.sub(r'[\\/:*?"<>|]', '', name).strip().rstrip('.')


def download(comic_id: int, mode: Literal["ep", "ord"], ids: List[int], sessdata: str):
    cookies['SESSDATA'] = sessdata

    if not (Path.exists(Path("downloads"))):
        os.mkdir('downloads')

    title, ep_list = get_manga_info(comic_id)
    print('[INFO]', title)

    if mode == "ep":
        ep_data_list = [data for data in ep_list if data["id"] in ids]
    else:
        ep_data_list = [data for data in ep_list if data["ord"] in ids]

    for ep_data in ep_data_list:
        image_list = get_images(comic_id, ep_data["id"])
        print(f'[INFO] 第 {ep_data["short_title"]} 话开始下载')
        dir_path = Path(f'downloads/{title}/{ep_data["short_title"] + ep_data["title"]}')
        dir_path.mkdir(parents=True, exist_ok=True)

        for index, image_url in enumerate(tqdm(image_list), 1):
            full_url = get_token(image_url)
            path = dir_path / f'{index}.jpg'
            download_image(full_url, path)

    print("下载完毕")
