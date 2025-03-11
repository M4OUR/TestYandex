from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
from django.core.cache import cache

# Функция для получения списка файлов с кэшированием
def get_files(public_key, file_type):
    cache_key = f"files_{public_key}_{file_type}"
    files = cache.get(cache_key)

    if not files:
        # Если данных нет в кэше, запрашиваем их из базы данных
        files = File.objects.filter(public_key=public_key, file_type=file_type)
        cache.set(cache_key, files, timeout=60*15)

    return files


# Функция для скачивания файла с Яндекс.Диска
def download_file(public_key, file_path):
    url = f'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={public_key}&path={file_path}'
    response = requests.get(url)

    if response.status_code == 200:
        download_url = response.json().get('href')
        file_response = requests.get(download_url)

        if file_response.status_code == 200:
            return file_response.content
        else:
            raise Exception(f"Error downloading file: {file_response.status_code} - {file_response.text}")
    else:
        raise Exception(f"Error getting download URL: {response.status_code} - {response.text}")


# Функция для получения списка файлов по публичной ссылке
def get_public_files(public_key):
    url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}'
    headers = {
        'Authorization': 'OAuth YOUR_ACCESS_TOKEN'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching files: {response.status_code} - {response.text}")

#Класс для отображения главной страницы
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

#Класс для отображения списка файлов по публичной ссылке
class FileListView(View):
    def post(self, request):
        public_key = request.POST.get('public_key')
        file_type = request.POST.get('file_type', 'all')
        try:
            # Получаем список файлов с Яндекс.Диска
            files_data = get_public_files(public_key)
            items = files_data['_embedded']['items']  # Получаем список файлов

            # Фильтруем файлы по типу
            if file_type != 'all':
                items = [item for item in items if self.filter_files(item, file_type)]

            return render(request, 'files_list.html', {'items': items, 'public_key': public_key, 'file_type': file_type})
        except Exception as e:
            return HttpResponse(str(e), status=400)
    # Фильтрует файлы по типу
    def filter_files(self, item, file_type):
        if file_type == 'document':
            return item['name'].lower().endswith(('.pdf', '.doc', '.dt', '.docx', '.txt', '.csv', '.xls', '.xlsx'))
        elif file_type == 'image':
            # Добавить другие типы изображений
            return item['name'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'))
        elif file_type == 'audio':
            # Если нужно фильтровать по аудиофайлам
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
