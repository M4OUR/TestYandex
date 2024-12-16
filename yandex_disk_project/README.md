# Yandex Disk Web App

### Описание
Веб-приложение, разработанное с использованием Django, позволяет взаимодействовать с API Яндекс.Диска для просмотра файлов по публичной ссылке и их загрузки на локальный компьютер.

---

## Функционал
1. **Просмотр файлов по публичной ссылке**: Пользователь может ввести ссылку и получить список всех доступных файлов и папок.
2. **Скачивание файлов**: Возможность выбрать файлы и скачать их на локальный компьютер.
3. **Фильтрация файлов по типу**: Можно отобразить только документы или изображения.
4. **Поддержка публичных ссылок на Яндекс.Диск**: Используется REST API.

---

## Требования

Перед началом убедитесь, что у вас установлено:
- **Python 3.8 или выше**
- **pip** (Python Package Installer)
- **Git**

Также необходимо зарегистрироваться на Яндекс.Диске и получить доступ к публичным ссылкам.

---

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/M4OUR/TestYandex
   cd yandex-disk-web-app
   ```

2. **Создайте виртуальное окружение и активируйте его:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Примените миграции базы данных Django:**
   ```bash
   python manage.py migrate
   ```

5. **Запустите сервер разработки:**
   ```bash
   python manage.py runserver
   ```

6. **Откройте приложение в браузере:**
   Перейдите по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Использование

1. На главной странице введите публичную ссылку Яндекс.Диска в соответствующее поле.
2. Выберите тип файлов для фильтрации:
   - **Все файлы**
   - **Документы** (PDF, DOCX, TXT и т. д.)
   - **Изображения** (JPG, PNG и т. д.)
3. Нажмите кнопку **Показать файлы**.
4. Для загрузки файлов:
   - Отметьте галочкой нужные файлы.
   - Нажмите кнопку **Скачать выбранные файлы**.

---

## Структура проекта

- **yandex_disk/**: Корневая папка проекта.
  - **settings.py**: Основные настройки Django.
  - **urls.py**: Маршрутизация приложения.
  - **views.py**: Логика обработки запросов.
- **templates/**: HTML-шаблоны для веб-интерфейса.
- **static/**: CSS и другие статические файлы.

