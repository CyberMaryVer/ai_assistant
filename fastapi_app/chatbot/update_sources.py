import requests


def update_sources(list_of_sources):
    list_of_texts = []
    for s in list_of_sources:
        print(f"Updating {s}...")
        try:
            r = requests.get(s)
            if r.status_code == 200:
                text_from_source = r.text
                list_of_texts.append(text_from_source)
                print(f"Updated {s}: {len(text_from_source)} symbols")
                print("First 1000 symbols:", text_from_source[:1000])
            else:
                print(f"Error {r.status_code}")
        except Exception as e:
            print(f"Error {e}")


if __name__ == "__main__":
    from fastapi_app.chatbot.custom_langchain import answer_with_openai
    from fastapi_app.chatbot.secret import OPENAI_API_KEY
    TEST_QUESTION = "Какая стоимость доставки в Москве и Московской области?"

    answers, sources = answer_with_openai(TEST_QUESTION, verbose=True, api_key=OPENAI_API_KEY)
    print(answers)
    print(sources)

    update_sources(sources)
