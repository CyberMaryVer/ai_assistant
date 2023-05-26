import openai
import re
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

BUSINESS_INDEX_PATH = "./../../indexes/faiss-b/" if __name__ == "__main__" else "./indexes/faiss-b/"
TK_INDEX_PATH = "./../../indexes/faiss-tk/" if __name__ == "__main__" else "./indexes/faiss-tk/"

print(__name__, __file__, BUSINESS_INDEX_PATH, TK_INDEX_PATH)


def get_faiss_index(faiss_index=None, api_key=None):
    index_path = TK_INDEX_PATH if faiss_index == 'tk' else BUSINESS_INDEX_PATH
    return FAISS.load_local(folder_path=index_path, embeddings=OpenAIEmbeddings(openai_api_key=api_key))


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


def get_context(question, faiss_index='default', api_key=None):
    search_index = get_faiss_index(faiss_index, api_key)
    context = search_index.similarity_search(question, k=4)
    sources = extract_sources(context)
    context = [remove_weird_tags(d.page_content) for d in context if len(d.page_content) > 20]
    context = '\n\n###\n\n'.join(context)
    return context, sources


def answer_with_openai(question, verbose=False, faiss_index='default', api_key=None, update_sources=False):
    context, sources = get_context(question, faiss_index=faiss_index, api_key=api_key)
    print(context) if verbose else None
    answer = answer_with_context(question, context, api_key=api_key)
    print(answer) if verbose else None
    print(sources) if verbose else None
    return answer, sources


def print_openai_answer(question, faiss_index='default', verbose=False, api_key=None):
    answer, sources = answer_with_openai(question,
                                         verbose=verbose,
                                         faiss_index=faiss_index,
                                         api_key=api_key)
    print("\033[095mОТВЕТ: \033[0m", answer)
    print("\n\033[095mИСТОЧНИКИ: \033[0m")
    for s in sources:
        print(s)


def answer_with_context(
        question,
        context,
        api_key,
        model="gpt-3.5-turbo",
        max_tokens=2400,
):
    openai.api_key = api_key
    task = "Answer the question based on the context below, you can think on English but return answer in Russian\n\n"
    info = f"Context: {context}\n\n---\n\nQuestion: {question}\nAnswer:"
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
    # print_openai_answer("Какова средняя стоимость часа работы дизайнера?", verbose=True)
    # print_openai_answer("Как рассчитывается EBITDA?", verbose=False)
    # print_openai_answer("Как рассчитать НДФЛ?", verbose=False)
    print_openai_answer("Можно ли уволить самозанятого?", faiss_index='tk', verbose=False, api_key=OPENAI_API_KEY)
    print_openai_answer("Сколько зарабатывает ML инженер?", faiss_index='business', verbose=False, api_key=OPENAI_API_KEY)