import requests
import json
import logging
from functions import find_max_size
from functions import time_convert

logging.basicConfig(level=logging.INFO, filename="logging.log",
                    encoding='utf-8', filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


class Vk_api:
    api_base_url = 'https://api.vk.com/method/'

    # Метод для получения token и id VK
    def __init__(self, token_id_list):
        self.vk_token = token_id_list[0]
        self.vk_user_id = token_id_list[1]

    # Метод для получения общих параметров VK
    def get_params(self):
        return {
            'access_token': self.vk_token,
            'v': '5.131',
            'extended': 1,
            'photo_sizes': 1
        }

    # Метод для получения нужного url VK
    def _build_url(self, api_method):
        return f'{self.api_base_url}/{api_method}'

    # Метод для получение списка альбомов из VK
    def get_albums(self):
        params = self.get_params()
        params.update({'owner_id': self.vk_user_id})
        response = requests.get(self._build_url('photos.getAlbums'), params=params)
        if 200 <= response.status_code < 300:
            response = response.json()
            response = response['response']
            albums_count = len(response['items'])
            albums_items = response['items']
            dict_albums = {}
            for i in range(albums_count):
                albums_id = albums_items[i]['id']
                albums_name = albums_items[i]['title']
                dict_albums[f'id альбома {albums_name}'] = albums_id
            with open('albums.json', 'w', encoding='utf-8') as f:
                json.dump(dict_albums, f, ensure_ascii=False, indent=2)
            print(f'Данные об альбомах записаны в файл "albums.json"\n')
            logging.info(f'Данные об альбомах записаны в файл albums.json')
            return dict_albums
        else:
            logging.warning(f"Ошибка {response.status_code}. Информация о альбомах не получена")

    # Метод для получения словаря со ссылками фото из нужного альбома в VK
    def get_photos(self, album_id):
        params = self.get_params()
        params.update({'owner_id': self.vk_user_id, 'album_id': f'{album_id}'})
        response = requests.get(self._build_url('photos.get'), params=params)
        if 200 <= response.status_code < 300:
            response = response.json()
            photo_info = response['response']
            photo_count = len(photo_info['items'])
            photo_items = photo_info['items']
            sort_dict = {}
            for i in range(photo_count):
                likes_count = str(photo_items[i]['likes']['count']).zfill(3)
                url_download, picture_size = find_max_size(photo_items[i]['sizes'])
                time_warp = time_convert(photo_items[i]['date'])
                file_id = photo_items[i]['id']
                file_name = f'{likes_count}likes {time_warp} id{file_id}.jpeg'
                sort_dict[file_name] = [url_download, picture_size]
            sorted_dict = dict(sorted(sort_dict.items(), reverse=True))
            print(f'\nСловарь со ссылками фото из альбома в VK сформирован')
            logging.info(f'Словарь со ссылками фото из альбома в VK сформирован')
            with open('save_photo.json', 'w') as f:
                json.dump(sorted_dict, f, ensure_ascii=False, indent=2)
            print(f'\nДанные в json-файл "save_photo.json" записаны\n')
            logging.info(f'Данные в json-файл "save_photo.json" записаны')
            return sorted_dict
        else:
            logging.warning(f"Ошибка {response.status_code}. Информация о фотографиях не получена")