import requests
from pprint import pprint
import collections
from pathlib import Path


def get_photo(id_vk):
    photo_list = []
    url_list = []
    url = "https://api.vk.com/method/photos.get"
    params = {
        'owner_id': id_vk,
        'album_id': 'profile',
        'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
        'extended': '1',
        'v': '5.118',
        'photo_sizes': '1'
                            }
    response = requests.get(url=url, params=params).json()
    response1 = response['response']['items']
    count = collections.Counter()
    for photo in response1:
        name_keys = (photo['likes']['count'])
        count[name_keys] += 1
        if count[name_keys] >= 2:
            name_keys = photo['likes']['count'], photo['date']
        url_values = photo['sizes'][-1]['url']
        photo_dict = {name_keys: url_values}
        photo_list.append(photo_dict)
        url_list.append(url_values)
    pprint(photo_list)
    return url_list


def new_folder():
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    params = {"path": album, "overwrite": "true"}
    headers = {'Content-Type': 'application/json',
               'Authorization': token
               }
    response = requests.put(url=url,  headers=headers, params=params)
    response = response.json()
    response = response.get('href')
    # pprint(response)
    return response


def get_url():
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    p = {"path": urls, "overwrite": "true", "fields": "Link"}
    h = {'Content-Type': 'application/json',
         'Authorization': token
         }  
    response = requests.get(url=url,  headers=h, params=p)
    r1 = response.json()
    pprint(r1)
    r2 = r1.get('href')
    pprint(r2)
    return r2


def upload_photo():
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {'Content-Type': 'application/json',
               'Authorization': token}
    params = {"path": 'VK_photo/',
              'url': urls,
              "disable_redirects": "false"}
    response = requests.post(url=url,  headers=headers, params=params)
    pprint(response.json())


if __name__ == '__main__':
    # id_vk = input('введите id: ')
    id_vk = '552934290'

    urls = get_photo(id_vk)

    # pprint(urls)

    # token = input('Введите токен')
    token = '...'
    album = Path("VK_photo")

    new_folder()
    upload_photo()
#
# # from alive_progress import alive_bar
# # import time
# #
# # mylist = [1,2,3,4,5,6,7,8]
# #
# # with alive_bar(len(mylist)) as bar:
# #     for i in mylist:
# #         bar()
# #         time.sleep(1)