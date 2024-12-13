from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
from django.core.cache import cache

# Функция для получения списка файлов с кэшированием
def get_files(public_key, file_type):
    cache_key = f"files_{public_key}_{file_type}"  # Ключ кэша, зависящий от публичного ключа и типа файлов
    files = cache.get(cache_key)  # Попытка получить данные из кэша

    if not files:
        # Если данных нет в кэше, запрашиваем их из базы данных
        files = File.objects.filter(public_key=public_key, file_type=file_type)
        cache.set(cache_key, files, timeout=60*15)  # Кэшируем данные на 15 минут

    return files


# Функция для скачивания файла с Яндекс.Диска
def download_file(public_key, file_path):
    url = f'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={public_key}&path={file_path}'
    response = requests.get(url)  # Отправка запроса на получение URL для скачивания

    if response.status_code == 200:
        download_url = response.json().get('href')  # Получаем ссылку для скачивания файла
        file_response = requests.get(download_url)  # Запрос для скачивания файла

        if file_response.status_code == 200:
            return file_response.content  # Возвращаем содержимое файла
        else:
            raise Exception(f"Error downloading file: {file_response.status_code} - {file_response.text}")
    else:
        raise Exception(f"Error getting download URL: {response.status_code} - {response.text}")


# Функция для получения списка файлов по публичной ссылке
def get_public_files(public_key):
    url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}'
    headers = {
        'Authorization': 'OAuth YOUR_ACCESS_TOKEN'  # Если нужно авторизоваться, используйте токен OAuth
    }
    response = requests.get(url, headers=headers)  # Отправляем запрос на получение файлов

    if response.status_code == 200:
        return response.json()  # Возвращаем данные в формате JSON
    else:
        raise Exception(f"Error fetching files: {response.status_code} - {response.text}")

#Класс для отображения главной страницы
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')  # Отправка главной страницы с шаблоном

#Класс для отображения списка файлов по публичной ссылке
class FileListView(View):
    def post(self, request):
        public_key = request.POST.get('public_key')  # Получаем публичный ключ
        file_type = request.POST.get('file_type', 'all')  # Получаем тип файла, по умолчанию все файлы
        try:
            # Получаем список файлов с Яндекс.Диска
            files_data = get_public_files(public_key)
            items = files_data['_embedded']['items']  # Получаем список файлов

            # Фильтруем файлы по типу
            if file_type != 'all':
                items = [item for item in items if self.filter_files(item, file_type)]

            return render(request, 'files_list.html', {'items': items, 'public_key': public_key, 'file_type': file_type})
        except Exception as e:
            return HttpResponse(str(e), status=400)  # Возвращаем ошибку, если что-то пошло не так
    # Фильтрует файлы по типу
    def filter_files(self, item, file_type):
        if file_type == 'document':
            # Можно добавить другие расширения, такие как .csv, .xls
            return item['name'].lower().endswith(('.pdf', '.doc', '.dt', '.docx', '.txt', '.csv', '.xls', '.xlsx'))
        elif file_type == 'image':
            # Добавить другие типы изображений
            return item['name'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'))
        elif file_type == 'audio':
            # Если нужно фильтровать по аудиофайлам, можно добавить такие расширения
            return item['name'].lower().endswith(('.mp3', '.wav', '.flac', '.ogg'))
        elif file_type == 'archive':
            # Если нужно фильтровать архивы
            return item['name'].lower().endswith(('.zip', '.tar', '.gz', '.rar'))
        return True  # Для типа 'all' показываем все файлы


#Класс для скачивания файла
class DownloadFileView(View):
    def post(self, request):
        public_key = request.POST.get('public_key')  # Получаем публичный ключ
        file_path = request.POST.get('file_path')  # Получаем путь к файлу
        try:
            # Скачиваем файл с Яндекс.Диска
            file_content = download_file(public_key, file_path)
            # Возвращаем файл в ответе
            response = HttpResponse(file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Exception as e:
            return HttpResponse(f"Ошибка скачивания файла {file_path}: {str(e)}", status=400)  # Обработка ошибок скачивания
