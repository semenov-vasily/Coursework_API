from Vk_api import Vk_api
from Yandex import Yandex
from functions import get_token_id

if __name__ == '__main__':
    token_vk = 'token_id.ini'  # Берем token и id из файла 'token_id.ini'

    # Создаем словарь со ссылками фото из конкретного альбома в VK
    vk_albums_json = Vk_api(get_token_id(token_vk)).get_albums()
    vk_photo_json = Vk_api(get_token_id(token_vk)).get_photos(input('Введите id альбома из файла "albums.json": '))

    token_ya = 'token_id.ini'  # Берем token из файла 'token_id.ini'

    # Создаем экземпляр класса Yandex с параметрами "Имя папки"и "Токен"
    yandex_photo = Yandex('Vk_photo', get_token_id(token_ya),
                          int(input('Введите количество фото для загрузки на Ядиск: ')))
    # Записываем фото из VK на Ядиск
    yandex_photo.create_copy(vk_photo_json)
