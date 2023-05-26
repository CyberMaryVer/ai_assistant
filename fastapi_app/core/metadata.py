LOGO = "https://is5-ssl.mzstatic.com/image/thumb/Purple126/v4/83/25/7a/83257a4b-9d54-8af8-8e31-5c79e612dbd9/AppIcon-0-1x_U007emarketing-0-10-0-85-220.png/512x512bb.jpg"

LOGO_HTML = f"""
<img src="{LOGO}" width="250" height="250">
"""

DESCRIPTION = f"""
{LOGO_HTML}

АПИ для работы с AI-ассистентом. Позволяет выполнять следующие операции:

**ДЛЯ РАЗРАБОТЧИКОВ**
* Регистрация пользователей
* Аутентификация пользователей
* Генерация нового ключа доступа к АПИ (при этом ключ привязан к компании и к конкретной тематике)
* Получение списка ключей доступа к АПИ для конкретной компании
* Удаление ключа доступа к АПИ

**ДЛЯ ПОЛЬЗОВАТЕЛЕЙ**
* Получение списка тематик
* Получение списка тематик, доступных для конкретного пользователя
* Получение ответа от AI-ассистента по конкретной тематике
* Получение списка ответов от AI-ассистента по конкретной тематике

"""

TAGS_METADATA = [
    {
        "name": "assistant",
        "description": "Documentation for AI assistant API is available here.",
        "externalDocs": {
            "description": "External docs",
            "url": "http://localhost:9000/redoc",
        },
    },
    # {
    #     "name": "files",
    #     "description": "Operations with files. For developers. These endpoints are not available in production.",
    # },
    # {
    #     "name": "tables",
    #     "description": "Database queries. For developers. These endpoints are not available in production.",
    # },
    # {
    #     "name": "users",
    #     "description": "Operations with users. For developers. These endpoints are not available in production."
    # },
    # {
    #     "name": "healthcheck",
    #     "description": "Healthcheck endpoint. Returns 200 if the service is up and running.",
    # },
]
CONTACT = {
    "name": "AI ENGINEERS",
    "url": "https://gitlab.com/maria.startseva",
    "email": "mary-ver@yandex.ru",
}
LICENSE = {
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
}
SERVERS = [
        {"url": "localhost:8000"},
        {"url": "localhost:9000", "description": "Staging environment"},
    ]
