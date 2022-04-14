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
        'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
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

        size_list = {photo['sizes'][0]['height']: photo['sizes'][0]['width']}
        info = {name_keys: size_list}
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

    # id_vk = input('Введите id страницы VK:')
    id_vk = '552934290'
    path = '/VK_photo/'

    # TOKEN = input('Введите token yandex.disk:')
    TOKEN = 'AQAAAAAb702VAADLW8tCNia9yU5JlUg_5YVBPtI'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}

    count_photos_user = int(input('Введите количество фотографий, которые необходимо загрузить:'))
    if 0 < count_photos_user <= 5:
        count_photos = count_photos_user

    urls = get_photo(id_vk)

    for_upload_photo(urls)
    create_folder(path)


