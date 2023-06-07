import os

HOST = os.getenv("EXTERNAL_HOST") or "localhost:8000"
LOGO = "https://static.vecteezy.com/system/resources/thumbnails/005/381/497/small/cute-robot-illustration-with-happy-expression-free-vector.jpg"

LOGO_HTML = f"""
<img src="{LOGO}" width="210" height="240">
"""

DESCRIPTION = f"""
{LOGO_HTML}

АПИ для работы с AI-ассистентом. Позволяет выполнять следующие операции:

**Для пользователей**
* Получение списка тематик
* Получение ответа от AI-ассистента в обычном режиме
* Получение ответа от AI-ассистента в расширенном режиме (с контекстом)
* Получение списка источников по тематике

<details>
  <summary>**Для администраторов**</summary>
    <p>Для администраторов доступны все операции, описанные выше.</p>
    <p>Кроме того, администратор может:</p>
    <ul>
        <li>Добавлять новые тематики</li>
        <li>Добавлять новые ответы на вопросы</li>
        <li>Добавлять новые источники</li>
        <li>Добавлять новые теги</li>
        <li>Добавлять новых пользователей</li>
        <li>Получать список пользователей</li>
        <li>Получать список тематик</li>
        <li>Получать список вопросов</li>
        <li>Получать список источников</li>
        <li>Получать список тегов</li>
    </ul>
</details>

"""

TAGS_METADATA = [
    {
        "name": "assistant",
        "description": "Documentation for AI assistant API is available here.",
        "externalDocs": {
            "description": "External docs",
            "url": f"http://{HOST}/redoc",
        },
    },
    # {
    #     "name": "files",
    #     "description": "Operations with files. For demo only. Not available in production.",
    # },
    # {
    #     "name": "tables",
    #     "description": "Database queries. For demo only. Not available in production.",
    # },
    # {
    #     "name": "users",
    #     "description": "Operations with users. For developers. These endpoints are not available in production."
    # },
    {
        "name": "healthcheck",
        "description": "Healthcheck endpoint. Returns 200 if the service is up and running.",
    },
]
CONTACT = {
    "name": "AI ENGINEERS",
    "url": f"http://{HOST}",
    "email": "mary-ver@yandex.ru",
}
LICENSE = {
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
}
