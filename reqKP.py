import requests
from pprint import pprint
import time
from tqdm import tqdm
import json
import collections


def get_photo(id_vk):
    """"Получение url фотографий из VK и назачение им имени."""

    photo_list = []
    info_list = []
    url = "https://api.vk.com/method/photos.get"
    params = {
        'owner_id': id_vk,
        'album_id': 'profile',
        'access_token': 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd',
        'extended': '1',
        'v': '5.118',
        'photo_sizes': '1'
                            }
    response = requests.get(url=url, params=params).json()['response']['items']

    count = collections.Counter()

    for photo in tqdm(response):
        name_keys = (photo['likes']['count'])
        count[name_keys] += 1
        if count[name_keys] >= 2:
            name_keys = str(photo['likes']['count'])+str(photo['date'])
        url_values = photo['sizes'][-1]['url']
        photo_dict = {name_keys: url_values}
        photo_list.append(photo_dict)

        name_list = str(f"file_name: {name_keys} ")
        size_list = str(f"size: {photo['sizes'][-1]['type']} ")
        info = {name_list: size_list}
        info_list.append(info)
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(info_list[0: count_photos], file)

    return photo_list


def create_folder(path):
    """Создание папки."""
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    params = {"path": path, "overwrite": "true"}
    response = requests.put(url=url, headers=headers, params=params)
    response = response.json()
    return response


def for_upload_photo(urls):
    """Загрузка фоток."""
    photo_info_list = []

    for dict_photo in tqdm(urls[0:count_photos]):
        for name_photo, url_photo in dict_photo.items():
            url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            params = {"path": 'VK_photo/' + str(name_photo),
                      'url': url_photo,
                      "disable_redirects": "false"
                      }
            response = requests.post(url=url,  headers=headers, params=params).json()
            photo_info_list.append(response)

    return photo_info_list


if __name__ == '__main__':

    id_vk = input('Введите id страницы VK:')

    path = '/VK_photo/'

    TOKEN = input('Введите token yandex.disk:')

    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}

    count_photos_user = int(input('Введите количество фотографий, которые необходимо загрузить:'))
    if 0 < count_photos_user <= 5:
        count_photos = count_photos_user

    urls = get_photo(id_vk)
    create_folder(path)
    for_upload_photo(urls)

