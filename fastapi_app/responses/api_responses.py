CHAT_RESPONSES = {
    404: {
        "description": "Server is not responding",
        "content": {
            "application/json": {
                "example": {"error": "OpenAI server is not responding"},
            }
        }
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {"error": "Data validation error"},
            }
        }
    },
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "chatbot_answer": {
                        "text": "There are 14 applicable cases for your request: ...",
                        "sources": ["https://pravo.gov.ru/", "https://www.consultant.ru/"],
                    },
                    "info": {
                        "topic": "business",
                        "parameters": {"topic": "enable", "sources": "enable"}
                    }
                }
            }
        }
    }}
