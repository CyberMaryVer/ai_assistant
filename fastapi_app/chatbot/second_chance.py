from fastapi_app.chatbot.assistant import get_answer_simple

NOT_OK_ANSWERS = ["нет информации",
                  "в данном контексте",
                  "данной информации в контексте не приведено",
                  "невозможно дать точный ответ",
                  "невозможно дать ответ",
                  "контекст не содержит информации",
                  "из текста не ясно",
                  "контекст не содержит ответ"]

SECOND_CHANCE_PROMPT = "Назови пару источников, где можно найти информацию о том, "
SECOND_CHANCE_PREFIX = " Могу порекомендовать поискать тут:\n"
SECOND_CHANCE_SOURCE = "https://www.google.com/"


def second_chance(answer, sources, user_input, api_key):
    print("\033[095msecond chance:\033[0m", answer)

    is_answer_not_ok = [x in answer.lower() for x in NOT_OK_ANSWERS]

    if any(is_answer_not_ok):
        try:
            prompt = SECOND_CHANCE_PROMPT
            second_answer = get_answer_simple(question=user_input, prompt=prompt, api_key=api_key)
            second_answer = answer + SECOND_CHANCE_PREFIX + second_answer["answer"]
            sources = sources + [SECOND_CHANCE_SOURCE, ]
            return second_answer, sources

        except Exception as e:
            print(f"[{__name__}] Error decoding: {e}")
            return answer, sources

    else:
        return answer, sources
