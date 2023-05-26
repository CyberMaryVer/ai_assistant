[![License][license-shield]][license-url]
[![Github][github-shield]][github-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


# Описание проекта

![img][product-screenshot1]

Умный корпоративный ассистент, который помогает быстро находить специализированную информацию по заранее определенным тематикам.

Пример интерфейса пользователя:
[![Product Name Screen Shot][product-screenshot4]](https://example.com)

## Основные возможности
АПИ чат-бота для корпоративного чата, который позволяет:
* Получать ответы на определенную тематику
* Добавлять источники информации
* Добавлять ответы на часто задаваемые вопросы
* Управлять доступом к боту и базой знаний

## Структура проекта

![img][product-schema]

Проект состоит из 3-х частей:

<details>
  <summary><b><strong>АПИ</strong></b></summary>
  
  FastAPI приложение, которое предоставляет доступ к боту и базе знаний. 
    Приложение состоит из 3-х частей:

* АПИ чат-бота (простой и расширенный)
* АПИ базы знаний (добавление индексов)
* АПИ для администрирования проекта

</details>
<details>
  <summary><b><strong>База данных</strong></b></summary>
  
PostgreSQL база данных, которая хранит:
  * Информацию о компаниях
  * Информацию о ключах к АПИ
  * Информацию о запросах пользователей
  * Правила фильтрации запросов

</details>

<details>
  <summary><b><strong>База знаний</strong></b></summary>
  
  В базе знаний хранятся индексы:
  * Индекс для поиска ответов на вопросы, связанные с ТК
  * Индекс для поиска ответов на общие вопросы по бизнесу
  * Индекс для поиска ответов на вопросы, связанные с уплатой налогов
  * Индекс для поиска ответов на вопросы, связанные с бухучетом

</details>

Сборка проекта осуществляется с помощью `docker-compose`.

## Используемые технологии

В проекте используются следующие технологии:

* [![Python][python]][python-url]
* [![Fastapi][Fastapi]][Fastapi-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![Docker][Docker]][Docker-url]

## Схема работы


## Работа с API

<details>
  <summary>Интерфейс</summary>
  
  ![img][product-screenshot2]
</details>

<details>
  <summary>Документация</summary>
  
  ![img][product-screenshot3]
</details>

<details>
  <summary>Примеры запросов</summary>

1. HTTP запрос

    ```bash
    http://localhost:8000/api/chatbot_simple/1
    ```
   Параметры:
    * `user_input` - вопрос пользователя
    * `params` - параметры запроса
    * `api_key` - ключ для доступа к АПИ

    ```json
    {
      "user_input": "Что такое НДФЛ?",
      "question": {
        "api_key": "API_KEY"
      }
    }
2. CURL запрос

    ```bash
        curl -X 'POST' \
          'http://localhost:8000/api/chatbot_simple/1' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
          "user_input": "Что такое НДФЛ?",
          "question": {
            "api_key": "API_KEY"
          }
        }'
    ```

</details>

## Веб-интерфейс пользователя

<details>
  <summary>Интерфейс</summary>
  
  ![img][product-screenshot4]
</details>

## Запуск проекта

Для запуска проекта необходимо:
1. Склонировать репозиторий
2. Перейти в папку проекта
3. Запустить проект с помощью команды `docker-compose up --build`
4. Перейти на `localhost:8000` для входа в веб-интерфейс

## Запуск АПИ без базы знаний и базы данных
```bash
docker run -d -p 8000:8000 -e OPENAI_API_KEY={your_key} --name smart_assistant smart_assistant
```

## Запуск без докера
1. Установить зависимости
```bash
pip install -r requirements.txt
```
2. Запустить проект
```bash
cd fastapi_app
uvicorn fastapi_app.fastapp:app --reload --port 9000 --env-file config.env
```
где `config.env` - файл с переменными окружения:
```bash
OPENAI_API_KEY={your_key}
DEBUG=True
```

## Лицензия

Распространяется под лицензией [APACHE][license-url].

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/badge/License-APACHE-yellow.svg?style=for-the-badge
[license-url]: https://github.com/CyberMaryVer/ai_assistant/blob/main/LICENSE
[product-logo]: images/logo.jpg
[product-screenshot1]: images/landing.jpg
[product-screenshot2]: images/api.jpg
[product-screenshot3]: images/docs.jpg
[product-screenshot4]: images/front.jpg
[product-schema]: images/architecture.png
[Fastapi]: https://img.shields.io/badge/Fastapi-0.68.1-blue?style=for-the-badge
[Fastapi-url]: https://fastapi.tiangolo.com/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-13.3-blue?style=for-the-badge
[PostgreSQL-url]: https://www.postgresql.org/
[Docker]: https://img.shields.io/badge/Docker-20.10.7-blue?style=for-the-badge
[Docker-url]: https://www.docker.com/
[python]: https://img.shields.io/badge/Python-3.9.6-blue?style=for-the-badge
[python-url]: https://www.python.org/
[github-shield]: https://img.shields.io/badge/Github-000000?style=for-the-badge&logo=github&logoColor=white
[github-url]: https://github.com/CyberMaryVer/ai_assistant
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://www.linkedin.com/in/maria-startseva/


