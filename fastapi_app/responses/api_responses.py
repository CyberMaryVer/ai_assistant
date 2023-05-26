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
                    "answer": "НДФЛ рассчитывается от прибыли или дохода, в зависимости от категории налогоплательщика и размера налоговой базы. Налоговая ставка может быть 13% или 15%, в зависимости от суммы налоговой базы за налоговый период.",
                    "sources": [
                        "https://www.kontur-extern.ru/info/3-ndfl-dlya-ip-za-god",
                        "https://www.irs.gov/ru/businesses/small-businesses-self-employed/operating-a-business",
                        "https://www.garant.ru/actual/nalog/ndfl/"
                    ],
                    "topic": "business",
                    "user_id": "test_user",
                    "user_input": "Как рассчитывается НДФЛ?",
                    "elapsed_time": 0.5
                }
            }
        }
    }
}
CHAT_RESPONSES_SIMPLE = {
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
                    "answer": "НДФЛ (Налог на доходы физических лиц) рассчитывается как 13% от дохода физического лица за налоговый период.",
                    "user_id": "test_user",
                    "user_input": "Как рассчитывается НДФЛ?",
                    "elapsed_time": 0.5
                }
            }
        }
    }
}
