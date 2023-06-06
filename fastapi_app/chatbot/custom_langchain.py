import openai
import re
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

from fastapi_app.chatbot.translation import translate_ru, translate_en

BUSINESS_INDEX_PATH = "./../../indexes/faiss-b/" if __name__ == "__main__" else "./indexes/faiss-b/"
TK_INDEX_PATH = "./../../indexes/faiss-tk/" if __name__ == "__main__" else "./indexes/faiss-tk/"
HR_INDEX_PATH = "./../../indexes/faiss-hr/" if __name__ == "__main__" else "./indexes/faiss-hr/"
YT_INDEX_PATH = "./../../indexes/faiss-yt/" if __name__ == "__main__" else "./indexes/faiss-yt/"


# print(__name__, __file__, BUSINESS_INDEX_PATH, TK_INDEX_PATH, HR_INDEX_PATH)


def get_faiss_index(faiss_index=None, api_key=None):
    index_path = TK_INDEX_PATH if faiss_index == 'tk' \
        else HR_INDEX_PATH if faiss_index == 'hr' \
        else YT_INDEX_PATH if faiss_index == 'yt' \
        else BUSINESS_INDEX_PATH
    return FAISS.load_local(folder_path=index_path, embeddings=OpenAIEmbeddings(openai_api_key=api_key))


def get_merged_faiss_index(faiss_indexes='business+hr', api_key=None):
    indexes = faiss_indexes.split('+')
    indexes = [get_faiss_index(f, api_key) for f in indexes]
    for idx, index in enumerate(indexes[:-1]):
        index.merge_from(indexes[idx + 1])
    return index


def remove_weird_tags(text):
    cleaned_text = re.sub(r'[\xa0]', ' ', text)
    return cleaned_text


def extract_sources(context):
    metadata = [s.metadata['source'] for s in context]
    sources = []
    for s in metadata:
        if type(s) is list:
            for ss in s:
                if ss not in sources:
                    sources.append(ss)
        elif type(s) is str:
            if s not in sources:
                sources.append(s)
    return sources


def get_embedding(text, model="text-embedding-ada-002", api_key=None):
    text = text.replace("\n", " ")
    openai.api_key = api_key
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def get_context(question, faiss_index='business', api_key=None, use_embedding=True):
    if "+" in faiss_index:
        search_index = get_merged_faiss_index(faiss_index, api_key)
    else:
        search_index = get_faiss_index(faiss_index, api_key)
    if use_embedding:
        q_embedding = get_embedding(question, api_key=api_key)
        context = search_index.similarity_search_by_vector(q_embedding, k=4)
    else:
        context = search_index.similarity_search(question, k=4)
    sources = extract_sources(context)
    context = [remove_weird_tags(d.page_content) for d in context if len(d.page_content) > 20]
    context = '\n\n###\n\n'.join(context)
    return context, sources


def get_context_with_score(question, faiss_index='business', api_key=None, threshold=0.33, use_embedding=True,
                           verbose=False):
    if "+" in faiss_index:
        search_index = get_merged_faiss_index(faiss_index, api_key)
    else:
        search_index = get_faiss_index(faiss_index, api_key)
    if use_embedding:
        q_embedding = get_embedding(question, api_key=api_key)
        context = search_index.similarity_search_with_score_by_vector(q_embedding, k=4)
    else:
        context = search_index.similarity_search_with_score(question, k=4)

    ##############################################
    if verbose:
        for d, s in context:
            print("\033[093SCORE:", s, "\033[0m")
            print("CONTENT:", d.page_content)
            print("SOURCE:", d.metadata['source'])
            print("---")
    ##############################################

    docs = [d for d, s in context if s < threshold]
    sources = extract_sources(docs)
    content = [d.page_content for d in docs]
    context = '\n\n###\n\n'.join(content)
    return context, sources


def answer_with_openai(question, faiss_index='default', api_key=None, verbose=False,
                       temperature=0.02, language='ru', context_threshold=0.33):
    # context, sources = get_context(question, faiss_index=faiss_index, api_key=api_key)
    context, sources = get_context_with_score(question, faiss_index=faiss_index, api_key=api_key,
                                              threshold=context_threshold)
    print(context) if verbose else None
    if context != "":
        answer = answer_with_context(question, context, api_key=api_key, temperature=temperature, language=language)
    else:
        answer = answer_without_context(question, api_key=api_key)
        sources = {"OpenAI": {"href": "https://chat.openai.com/", "name": "OpenAI GPT-3.5 Turbo w/o context"}}
    print(answer) if verbose else None
    print(sources) if verbose else None
    return answer, sources


def answer_with_openai_translated(question, faiss_index='default', api_key=None, verbose=False, temperature=0.01):
    question_en = translate_ru(question+"?")
    answer_en, sources = answer_with_openai(question_en, verbose=verbose, faiss_index=faiss_index, api_key=api_key,
                                            temperature=temperature, language='en', context_threshold=0.40)
    answer_ru = translate_en(answer_en.split('\n'))
    return answer_ru, sources


def print_openai_answer(question, faiss_index='default', verbose=False, api_key=None, temperature=0.02):
    answer, sources = answer_with_openai(question,
                                         verbose=verbose,
                                         faiss_index=faiss_index,
                                         api_key=api_key,
                                         temperature=temperature)
    print("\033[095mОТВЕТ: \033[0m", answer)
    print("\n\033[095mИСТОЧНИКИ: \033[0m")
    for s in sources:
        print(s)


def print_openai_answer_translated(question_ru, faiss_index='default', verbose=False, api_key=None, temperature=0.01):
    answer, sources = answer_with_openai_translated(question_ru,
                                                    verbose=verbose,
                                                    faiss_index=faiss_index,
                                                    api_key=api_key,
                                                    temperature=temperature)
    print(f"\033[095mОТВЕТ: \033[0m\n{answer}")
    print("\n\033[095mИСТОЧНИКИ: \033[0m")
    for s in sources:
        print(s)


def answer_with_context(
        question,
        context,
        api_key,
        model="gpt-3.5-turbo",
        max_tokens=2400,
        temperature=0.02,
        language="ru",
):
    openai.api_key = api_key

    pretext = "You an expert in the field of business, finance, law, and HR. You are answering questions from a client."
    addition = "IN CASE THERE IS NO ANSWER: If context does not contain enough information for answer, " \
               "write 'Not enough information in the context'"
    task = "TASK: Answer the question based on the context below. Be specific and use bullet points"
    lang = ", return answer in Russian. " if language == "ru" else ". "
    info = f"{pretext}\n\n{addition}\n\n{task}{lang}\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:"
    # print(f"\033[093m{info}\033[0m")
    messages = [{"role": "system", "content": info}]

    # task = "You are an expert. Answer the question based on the context below. " \
    #        "Be specific and use bullet points, return answer in Russian.\n\n"
    # info = f"Context: {context}\n\n---\n\nQuestion: {question}\nAnswer:"
    # messages = [{"role": "system", "content": f"{task}{info}"}]
    try:
        # Create a completions using the question and context
        completion = openai.ChatCompletion.create(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model=model,
        )
        return completion['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("[ERROR]", e)
        return ""


def answer_without_context(
        question,
        api_key,
        model="gpt-3.5-turbo",
        max_tokens=2800,
):
    openai.api_key = api_key
    pretext = "You an expert in the field of business, finance, law, and HR. You are answering questions from a client."
    task = "Answer the question. Be specific and use bullet points, return answer in Russian\n\n"
    info = f"Context: {pretext}\n\n---\n\nQuestion: {question}\nAnswer:"
    messages = [{"role": "system", "content": f"{task}{info}"}]
    try:
        # Create a completions using the question and context
        completion = openai.ChatCompletion.create(
            messages=messages,
            temperature=0.02,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model=model,
        )
        return completion['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("[ERROR]", e)
        return ""


if __name__ == '__main__':
    from fastapi_app.chatbot.secret import OPENAI_API_KEY
    import time
    print(OPENAI_API_KEY)

    # print_openai_answer("Какова средняя стоимость часа работы дизайнера?", verbose=True, api_key=OPENAI_API_KEY)
    # print_openai_answer("Как рассчитывается EBITDA?", verbose=False)
    # print_openai_answer("Как рассчитать НДФЛ?", verbose=False)
    # print_openai_answer("Можно ли уволить самозанятого?", faiss_index='tk', verbose=False, api_key=OPENAI_API_KEY)
    # print_openai_answer("Сколько зарабатывает ML инженер?", faiss_index='business', verbose=False, api_key=OPENAI_API_KEY)
    # print_openai_answer("Какие выплаты может получить работник при увольнении?", faiss_index='hr', verbose=False, api_key=OPENAI_API_KEY)

    get_context_with_score("Как перейти на УСН?",
                           faiss_index='business+hr',
                           api_key=OPENAI_API_KEY,
                           verbose=True)
    # start = time.time()
    # print_openai_answer("Какие выплаты может получить работник при увольнении?", faiss_index='tk', verbose=False,
    #                     api_key=OPENAI_API_KEY)
    # print("\033[093m", time.time() - start, "\033[0m")

    # start = time.time()
    # print_openai_answer_translated("Что будет с иммигрантами из России", faiss_index='yt', api_key=OPENAI_API_KEY,
    #                                verbose=False)
    # print("\033[093m", time.time() - start, "\033[0m")