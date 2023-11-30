import datetime
import configparser


# Функция для чтения token и id пользователя из файла 'token_id_test.ini'
def get_token_id(file_name):
    data = configparser.ConfigParser()
    data.read(file_name)
    token_vk = data["VK"]["token_vk"]
    user_id_vk = data["VK"]["user_id_vk"]
    token_ya = data["YANDEX"]["token_ya"]

    return [token_vk, user_id_vk, token_ya]


# Функция возвращает 'url' фото максимального размера и соответствующее буквенное обозначение размера 'type'
def find_max_size(dict_sizes):
    max_photo = 0
    photo_number = 0
    for i in range(len(dict_sizes)):
        photo_sizes = dict_sizes[i].get('width') * dict_sizes[i].get('height')
        if photo_sizes > max_photo:
            max_photo = photo_sizes
            photo_number = i
    return dict_sizes[photo_number].get('url'), dict_sizes[photo_number].get('type')


# Функция преобразует дату загрузки фото 'date' в формат 'гггг-мм-дд(чч-мм-сс)'
def time_convert(time_unix):
    time_bc = datetime.datetime.fromtimestamp(time_unix)
    str_time = time_bc.strftime('%Y-%m-%d(%H-%M-%S)')
    return str_time
