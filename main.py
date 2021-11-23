import requests
from pprint import pprint
import collections
photo_list = []


def get_photo(id):
    url = "https://api.vk.com/method/photos.get"
    p = {'owner_id': id,
         "album_id": 'profile',
         'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
         'extended': '1',
         'v': '5.118',
         'photo_sizes': '1'}
    resp1 = requests.get(url=url, params=p).json()
    resp1 = resp1['response']['items']
    c = collections.Counter()
    for photo in resp1:
        name_keys = (photo['likes']['count'])
        c[name_keys] += 1
        if c[name_keys] >= 2:
            name_keys = photo['likes']['count'], photo['date']
        url_values = photo['sizes'][-1]['url']
        photo_dict = {name_keys: url_values}
        photo_list.append(photo_dict)
    return photo_list


def new_folder():
    YA_url = "https://cloud-api.yandex.net/v1/disk/resources"
    p = {"path": albom, "overwrite": "true"}
    h = {'Content-Type': 'application/json',
        'Authorization': token
        }
    response = requests.put(url=YA_url,  headers=h, params=p)
    r1 = response.json()
    r2 = r1.get('href')
    pprint(r2)


def get_url():
    YA_url = "https://cloud-api.yandex.net/v1/disk/resources/{albom}/upload"
    p = {"path": path, "overwrite": "true", "fields": "Link"}
    h = {'Content-Type': 'application/json',
         'Authorization': token
         }
    response = requests.get(url=YA_url,  headers=h, params=p)
    r1 = response.json()
    pprint(r1)
    r2 = r1.get('href')
    pprint(r2)
    return r2

#
# def upload_photo_YAdisk():
#     url = get_url()
#     h = {'Content-Type': 'application/json',
#          'Authorization': token
#          }
#     p = {"path": path,
#          "overwrite": "true",
#          'url': path}
#     response = requests.post(url=url,  headers=h, params=p)
#     pprint(response.status_code)


if __name__ == '__main__':
    id_vk = '552934290'
    get_photo(id_vk)

    path = photo_list
    token = ''

    albom = 'VK_photo'
    new_folder()

    get_url()

    # upload_photo_YAdisk()
