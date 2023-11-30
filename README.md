# Курсовая работа «Резервное копирование»

## Состав проекта
1. В файле [main.py](main.py) реализовано выполнение основного задания.
2. В файл [token_id_test.ini](token_id_test.ini) необходимо записать token VK, id VK и token Яндекса.
Формат файла
```
[VK]
token_vk = вставить token ВК
user_id_vk = вставить id ВК
[YANDEX]
token_ya = вставить token Яндекса
```
3. В файле [Vk_api.py](Vk_api.py) реализован класс Vk_api для работы с папками в Vk, содержащими фото.
4. В файле [Yandex.py](Yandex.py) реализован класс Yandex для загрузки фото на Яндекс-диск.
5. В файле [functions.py](functions.py) находятся вспомогательные функции.
6. В файл [albums.json](albums.json) записывается словарь, ключами в котором являются названия альбомов фото в Vk, значениями их id.
7. В файл [save_photo.json](save_photo.json) записывается словарь для всех файлов из выбранного альбома в качестве значений ссылка для загрузки и размер файла.
8. В файл [copied_photo.json](copied_photo.json) записывается список скопированных файлов на Яндекс-диск в виде:
```
[{
"file_name": "likes Data id.jpg",
"size": "w"
}]
```
Где likes - количество лайков, Data - дата и время создания файла, id - id фото из VK, w - размер фото.

## Общая информация

1. Проект реализован в виде двух классов Vk_api, Yandex и трех вспомогательных функций.
2. Функционал программы реализован при помощи создания объектов этих классов, вызова методов этих классов и функций.
4. Во время работы программы ведется перезаписываемый лог хода выполнения программы.

### Класс Vk_api

В нем определяются аргументы и методы для работы с альбомами фотографий пользователя VK.  
При инициализации требуются токен и id владельца.

Методы:
- get_params - Метод для получения общих параметров VK.
- _build_url - Метод для получения нужного url VK.
- get_albums - Метод для получение списка альбомов из VK.
- get_photos - Метод для получения словаря со ссылками фото из нужного альбома в VK.

### Класс Yandex

В нем определяются аргументы и методы для работы с файлами на Яндекс-диске.
При инициализации требуются токен, имя каталога для резервного копирования и количество файлов.  

Методы:
- _create_folder - Метод создания папки на Ядиске.
- _in_folder - Метод для получения  ссылки для загрузки фото на Ядиск
- create_copy - Метод загрузки фотографий на Я-диск и формирования списка скопированных файлов.

### Вспомогательные функции

- get_token_id - Функция для чтения token и id пользователя из файла 'token_id_test.ini'.
- find_max_size - Функция возвращает 'url' фото максимального размера и соответствующее буквенное обозначение размера 'type'.
- time_convert - Функция преобразует дату загрузки фото 'date' в формат 'гггг-мм-дд(чч-мм-сс)'.

## Порядок работы программы

1. Файл [token_id_test.ini](token_id_test.ini) должен содержать токен VK, id владельца, и токен Яндекса.
2. После запуска программы необходимо выбрать id альбома из файла [albums.json](albums.json).
4. Сформируется словарь со ссылками фото из альбома в VK и запишутся в json-файл "save_photo.json" 
5. Ввести количество файлов для резервирования.
7. После этого начнется копирование файлов.
8. После завершения копирования появится сообщение, в котором будет указано сколько файлов скопировано из общего количества в альбоме.
9. При совпадении имени папки с существующим на Я-диске, будет выведено предупреждение.
10. При совпадении имени файла с существующим в указанной папке, копирование этого файла произведено не будет и будет выведено сообщение об этом.

