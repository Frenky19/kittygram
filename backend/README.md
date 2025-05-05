#   Контейнеры и CI/CD для Kittygram

## Стек технологий

![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)

## Устанавливаем Docker Compose на сервер

Поочерёдно выполните на сервере команды для установки Docker и Docker Compose для Linux.

```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin
```

Скопируйте на сервер в директорию проекта файл docker-compose.yml. Сделать это можно, например, при помощи утилиты SCP (secure copy) — она предназначена для копирования файлов между компьютерами, либо создав копию файла вручную. Зайдите на своём компьютере в директорию проекта и выполните команду копирования:

```
scp -i path_to_SSH/SSH_name docker-compose.yml \
    username@server_ip:/home/username/<директория проекта>/docker-compose.yml 
```

- path_to_SSH — путь к файлу с SSH-ключом;
- SSH_name — имя файла с SSH-ключом (без расширения);
- username — ваше имя пользователя на сервере;
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

## Workflow для обновления проекта на сервере

Чтобы обновить проект на продакшене, нужно:

- выполнить на команду docker compose pull, чтобы скачать с Docker Hub на сервер обновлённые образы для контейнеров;
- перезапустить контейнеры из обновлённых образов.

При выполнении этих задач «вручную» разработчик соединяется по SSH с сервером и отправляет на сервер команды docker compose pull, docker compose down и docker compose up. После этого — выполняет команды для миграций и сборки статики. При работе с GitHub Actions эти действия должен выполнить раннер, читая инструкции из workflow.


Перейдите в настройки репозитория GitHub — Settings, выберите на панели слева Secrets and Variables → Actions, нажмите New repository secret:

Сохраните переменные:

DOCKER_USERNAME - Логин Docker Hub
DOCKER_PASSWORD - Пароль Docker Hub
HOST - IP сервера
USER - SSH пользователь
SSH_KEY - Приватный ключ SSH
SSH_PASSPHRASE - Пасфраза для ключа
TELEGRAM_TO - ID чата Telegram
TELEGRAM_TOKEN - Токен бота Telegram


Ваш продакшен-сервер будет получать команды не с вашего компьютера, а от сервера GitHub Actions. 

Сделайте коммит и пуш в репозиторий и проверьте, что все шаги выполнились.