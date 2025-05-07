#   Docker контейнеры и CI/CD для Kittygram

Проект для обмена фотографиями котиков.

[![Kittygram Workflow](https://github.com/Frenky19/kittygram/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/Frenky19/kittygram/actions/workflows/main.yml)

## Стек технологий

![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)

## Требования

- Python 3.9
- Node.js 18+
- Docker
- Аккаунт на Docker Hub
- SSH-доступ к серверу
- Telegram-бот (для уведомлений)

## Настройка секретов

Добавьте в Secrets репозитория:

```
DOCKER_USERNAME - Логин Docker Hub
DOCKER_PASSWORD - Пароль Docker Hub
HOST - IP сервера
USER - Логин пользователя сервера
SSH_KEY - Приватный ключ SSH
SSH_PASSPHRASE - Код для ключа
TELEGRAM_TO - ID чата Telegram
TELEGRAM_TOKEN - Токен бота Telegram
```

## Устанавливаем Docker Compose на сервер

Поочерёдно выполните на сервере команды для установки Docker и Docker Compose для Linux.

```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin
```

Скопируйте на сервер в директорию проекта файл docker-compose.production.yml. Сделать это можно, например, при помощи утилиты SCP (secure copy) — она предназначена для копирования файлов между компьютерами или создайте копию файла вручную. Зайдите на своём компьютере в директорию проекта и выполните команду копирования:

```
scp -i path_to_SSH/SSH_name docker-compose.production.yml \
    username@server_ip:/home/username/<директория проекта>/docker-compose.production.yml 
```

- path_to_SSH — путь к файлу с SSH-ключом;
- SSH_name — имя файла с SSH-ключом (без расширения);
- username — ваш логин на сервере;
- server_ip — IP вашего сервера.


Скопируйте файл .env на сервер, в директорию проекта:

```
scp -i path_to_SSH/SSH_name .env \
    username@server_ip:/home/username/<директория проекта>/.env 
```

На сервере в редакторе nano откройте конфиг Nginx: sudo nano /etc/nginx/sites-enabled/default. Измените все настройки location на одну в секции server.

```
location / {
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:9000;
    }
```

Перезагрузите конфиг Nginx:

```
sudo service nginx reload 
```

## Деплой

После пуша в ветку main:

- Автоматически запускаются тесты

- Собираются и публикуются Docker-образы

- Разворачивается на сервере через docker-compose

- При успехе - отправляется уведомление в Telegram

## Структура проекта

```
.
├── backend/    # Backend приложение Django
├── frontend/   # Frontend приложение React
├── nginx/      # Конфигурация шлюза nginx
└── docker-compose.production.yml
```

## Автор  
[Андрей Головушкин / Andrey Golovushkin](https://github.com/Frenky19)