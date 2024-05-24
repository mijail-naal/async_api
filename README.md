# Проектная работа 5 спринта

### [Async_API_sprint_2](https://github.com/mijail-naal/Async_API_sprint_2)

Команда: [Михаил](https://github.com/mijail-naal) [Артём](https://github.com/Benrise)

[Приглашение](https://github.com/mijail-naal/Async_API_sprint_2/invitations)


### Тестирование

**1. Локальный запуск сервиса API и тестов.**

![image](https://github.com/mijail-naal/Async_API_sprint_2/assets/55480132/e0ba686b-b86d-40a6-a902-efd95e3528a2)

Инструкция:

1. Запустить используемые базы данных в изолированной среде Docker :
   ```shell
   docker-compose -f docker-compose.db.yaml up -d
   ```
2. Сервис API запускать в корневной папки проекта FastAPI (`fastapi/src`) -> `python3.11 main.py`
3. Запуск тестов запускать в корневной папки функциональных тестов (`tests/functional`) -> `python3.11 -m pytest src`

**2. Локальный запусков тестов.**

![image](https://github.com/mijail-naal/Async_API_sprint_2/assets/55480132/537ac3b3-54b1-4f98-bb44-cfa503811b72)

Инструкция:

1. Запустить используемые базы данных с сервисом API в изолированной среде Docker`:
   ```shell
   docker-compose \
      -f docker-compose.db.yaml \
      -f docker-compose.api.yaml \
      up -d --build
   ```
2. Запуск тестов запускать в корневной папки функциональных тестов (`tests/functional`) -> `python3.11 -m pytest src`

**3. Изолированный запуск тестов, бд и севриса API.**

![image](https://github.com/mijail-naal/Async_API_sprint_2/assets/55480132/407590e4-ec46-4338-8e5e-102a0dece50f)

Инструкция:

1. Для запуска полной сборки ввести команду:
   ```shell
   docker-compose -f docker-compose.db.yaml \
      -f docker-compose.api.yaml \
      -f docker-compose.tests.yaml \
      up -d --build
   ```
