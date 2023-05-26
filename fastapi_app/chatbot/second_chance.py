from fastapi_app.chatbot.assistant import get_answer_simple


def second_chance(answer, sources, user_input, api_key):
    print("\033[095msecond chance:\033[0m", answer)
    if "нет информации" in answer.lower() or "в данном контексте" in answer.lower():
        try:
            prompt = f"Назови один-два сайта с информацией о том, "
            answer = get_answer_simple(question=user_input, prompt=prompt, api_key=api_key)
            answer = "В данной тематике нет такой информации. Могу порекомендовать поискать тут:\n" \
                     + answer["answer"]
            sources = ["https://www.google.com/", ]
            return answer, sources
        except Exception as e:
            print(f"[{__name__}] Error decoding: {e}")
            return answer, sources
    else:
        return answer, sources
