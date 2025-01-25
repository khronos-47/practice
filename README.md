# Описание проекта:



utils - хранит вспомогательные функции 
	search_contacts_with_inn - поиск данных из excell файлов 
		имеет метод get_contact(int: INN) вощвращает словарь с данными 
		-> default = {"Номер телефона":None, "Электронная почта": None}


database - хранит настройки базы данных, метод подключение и схему 

parcer - главный запускаемы файл .

kal.json один из видов возвращаемых данных из dadata
### Требования

Необходимо, чтобы были установлены следующие компоненты:

- `Docker` и `docker-compose`
- `Python 3.12`
- `Poetry`

создать .env файл как минимум с дефолтными параметрами

Пример:
POSTGRES_DB=database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=6432


### Установка

1. Создание виртуального окружения и установка зависимостей
```commandline
poetry install
```

2. Активация виртуального окружения

```commandline
poetry shell
```


### Запуск

0. Создать `.env` файл с этими переменными (можно командой `make env`)
```dotenv
POSTGRES_DB=database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

2. Создание базы в docker-контейнере (чтобы не работать с локальной базой):
```commandline
make db
```
3. Выполнение миграций:
```commandline
make migrate head
```
4. Запуск приложения:
```commandline
make run
```
5. Запуск приложения в docker-контейнере:
```commandline
make docker_run
```