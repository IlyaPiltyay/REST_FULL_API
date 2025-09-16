# README

## Платформа для Онлайн-Обучения (LMS-система)

### Описание

Эта платформа предназначена для создания системы управления обучением (LMS), где каждый желающий может размещать свои
полезные материалы и курсы в удобной и доступной форме.

### Основные функции

- Регистрация и аутентификация пользователей: Пользователи могут создавать аккаунты и входить в систему с использованием
  электронной почты в качестве основного идентификатора.
- Создание и публикация курсов: Пользователи могут создавать собственные курсы, добавлять материалы (тексты, видео,
  документы) и управлять ими.
- Интеграция с платежными сервисами https://api.stripe.com
- Сервисные функции в модуле users\service.py (на создание сессии, продукта, цены)

### Технологии

- Backend: Django (Python) с использованием Django REST Framework для создания API.
- База данных: PostgreSQL для хранения данных пользователей, курсов и другой информации.
- Документирование: swagger, redoc доступно по адресу http://127.0.0.1:8000/swagger/ или http://127.0.0.1:8000/redoc/
- Docker. В данном документе вы найдете инструкции по запуску и управлению контейнерами с помощью Docker.

### Установка и запуск

1. Клонируйте репозиторий:
   git clone https://github.com/IlyaPiltyay/REST_FULL_API.git
   cd repository
2. Установите зависимости с помощью Poetry:
3. Создайте и примените миграции:
   poetry run python manage.py makemigrations
   poetry run python manage.py migrate
4. Запустите сервер разработки:
   poetry run python manage.py runserver

## Основные команды Docker и Docker Compose

- **Остановить запущенный контейнер**:
    ```bash
    docker stop d5030b766bcc
    ```
- **Остановить и удалить все контейнеры, сети и тома**:
    ```bash
    docker-compose down
    ```
- **Удалить конкретный контейнер**:
    ```bash
    docker rm django-app
    ```
- **Просмотреть логи конкретного контейнера**:
    ```bash
    docker logs django-app
    ```
- **Построить образ Docker из `Dockerfile`**:
    ```bash
    docker build -t django-app .
    ```
- **Показать все запущенные контейнеры**:
    ```bash
    docker ps
    ```
- **Запустить контейнеры с пересборкой**:
    ```bash
    docker compose up --build
    ```
- **Получить доступ к контейнеру через оболочку**:
    ```bash
    docker exec -it <container_id> /bin/bash
    ```
- **Перейти в установленный рабочий каталог и просмотреть файлы**:
    ```bash
    ls -l
    ```

### 1. Настройка удаленного сервера

1. Подключитесь к вашему удаленному серверу:
   Используйте SSH для доступа к вашему серверу:
   ssh <user>@<server-ip>
2. Обновите пакеты системы:
   sudo apt update && sudo apt upgrade -y
3. Установите Docker:
   Для установки Docker выполните следующие команды:
   sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   sudo apt update
   sudo apt install docker-ce -y
4. Проверьте, что Docker установлен:
   sudo systemctl status docker
