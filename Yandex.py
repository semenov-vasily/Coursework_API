import requests
import logging
from pprint import pprint
import json

logging.basicConfig(level=logging.INFO, filename="logging.log",
                    encoding='utf-8', filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


class Yandex:
    # Метод для получения основных параметров
    def __init__(self, folder_name, token_id_list, number):
        self.token = token_id_list[2]
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': self.token}
        self.folder = self._create_folder(folder_name)
        self.add_files_number = number

    # Метод создания папки на Ядиске
    def _create_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'\nПапка {folder_name} успешно создана в корневом каталоге Яндекс диска\n')
            logging.info(f'\nПапка {folder_name} успешно создана в корневом каталоге Яндекс диска\n')
        else:
            print(f'\nПапка {folder_name} уже существует. Файлы с одинаковыми именами не будут скопированы\n')
            logging.warning(f'Папка {folder_name} уже существует. Файлы с одинаковыми именами не будут скопированы\n')
        return folder_name

    # Метод для получения  ссылки для загрузки фото на Ядиск
    def _in_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        response = requests.get(url, headers=self.headers, params=params)
        if 200 <= response.status_code < 300:
            response = response.json()['_embedded']['items']
            name_file_list = []
            for elem in response:
                name_file_list.append(elem['name'])
            print(f'\nСписок существующих файлов получен:\n')
            pprint(name_file_list, sort_dicts=False, width=100)
            logging.warning(f'Список существующих файлов получен {name_file_list}')
            return name_file_list
        else:
            print(f'\nСписок существующих файлов не получен. Ошибка {response.status_code}\n')
            logging.warning(f'Список существующих файлов не получен. Ошибка {response.status_code}')

    # Метод загрузки фотографий на Ядиск и формирования списка скопированных файлов
    def create_copy(self, dict_files):
        name_file_list = self._in_folder(self.folder)
        copy_files = 0
        copied_photo = []
        for key, i in zip(dict_files.keys(), range(self.add_files_number)):
            if copy_files < self.add_files_number:
                if key not in name_file_list:
                    params = {'path': f'{self.folder}/{key}',
                              'url': dict_files[key][0],
                              'overwrite': 'false'}
                    response = requests.post(self.url, headers=self.headers, params=params)
                    if response.status_code == 202:
                        copy_files += 1
                        copied_photo.append({'file name': key, 'size': dict_files[key][1]})
                        print(f'\nФото {key} скопировано', end='')
                        logging.info(f'Фото {key} скопировано')
                    else:
                        logging.warning(f"Файл {key} НЕ скопирован. Ошибка {response.status_code}")
                else:
                    print(f'\nВнимание:Файл {key} уже существует', end='')
                    logging.warning(f'Внимание:Файл {key} уже существует')
            else:
                break
        with open('copied_photo.json', 'w') as f:
            json.dump(copied_photo, f, ensure_ascii=False, indent=2)
        print(f'\n\nСписок скопированных файлов записан в файл "copied_photo.json"\n')
        logging.info(f'Список скопированных файлов записан в файл "copied_photo.json"')
        print(f'Копирование завершено, новых фото скопировано: {copy_files}\n'
              f'\nВсего фото в альбоме в VK: {len(dict_files)}')
        logging.info(f'Копирование завершено, новых фото скопировано: {copy_files}'
                     f'\nВсего фото в альбоме в VK: {len(dict_files)}')
