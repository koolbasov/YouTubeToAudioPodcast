# YouTubeToAudioPodcast
Конвертирует публичный или unlisted YouTube плейлист в аудиоподкаст и предоставляет возможность подписаться по RSS в приложениях для прослушивания подкастов, например iTunes.

Проект создан в рамках учебного курса [Learn Python](https://learn.python.ru/) совместно 
с [DavydovPa](https://github.com/DavydovPa)

## Сборка репозитория и локальный запуск

В проекте используется база данных SQLite
1. Клонируйте репозиторий с github:
    git clone https://github.com/koolbasov/YouTubeToAudioPodcast.git
2. Создайте виртуальное окружение и активируйте его
3. Установите зависимости
```
pip install -r requirements.txt
```
4. В файле webapp/config.py замените значение
```
SECRET_KEY = "ВПИШИТЕ СЮДА ДРУГОЕ ЗНАЧЕНИЕ"
```
5. Установите FFmpeg и настройте переменные окружения:
* [Mac](https://phoenixnap.com/kb/ffmpeg-mac) - (проще всего устанавливать через homebrew)
* [Windows](https://phoenixnap.com/kb/ffmpeg-windows)
6. Находясь в корневой папке проекта создайте базу данных с помощью команды:
```
python create_db.py
```
7. Запустите проект с помощью команды:
```
./run.sh  # Macos, Linux: 
```
```
run.bat  # Windows: 
```
8. Для регулярного обновления всех загруженных плейлистов используется файл
update_all_podcasts.py, его можно обновлять по crontab в MacOs и Linux или при
помощи планировщика задач в Windows.

### Дополнительно
Если проект запущен локально, то при добавлении RSS ссылки в iTunes подкаст 
отображается, но обновляется только вручную, для того чтобы подкаст обновлялся 
автоматически проект нужно выкладывать на публичный сервер, либо предоставлять 
к нему публичный доступ с помощью таких сервисов как ngrok или xtunnel.

![2024-07-26_11-33-16](https://github.com/user-attachments/assets/f6d85e27-410f-4613-b43c-9b02c463c090)

![2024-07-26_11-40-00](https://github.com/user-attachments/assets/c8f964a1-f956-41e7-aaf5-95470b9057f6)

![2024-07-26_11-40-36](https://github.com/user-attachments/assets/cb5dc176-3c4a-4af7-99c6-834770222700)
