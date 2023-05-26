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
                    "user_request": {
                        "user_input": "Как рассчитывается НДФЛ?",
                        "topic": "business",
                        "user_id": "1",
                        "user_key": "11111test"
                    },
                    "uses_left": 90,
                    "elapsed_time": 15.030277252197266
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
                    "user_request": {
                        "user_id": "1",
                        "user_input": "как начисляется ндфл сотруднику работающему из другой страны",
                        "user_key": "11111test"
                    },
                    "key_status": 89,
                    "elapsed_time": 11.23199200630188
                }
            }
        }
    }
}
