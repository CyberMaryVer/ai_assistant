from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

enru_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
enru_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-ru")

ruen_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
ruen_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-en")


def translate_ru(ru_text):
    input_ids = ruen_tokenizer(ru_text, return_tensors="pt", padding=True).input_ids
    outputs = ruen_model.generate(input_ids=input_ids, max_length=512, num_beams=5, num_return_sequences=1)
    en_text = ruen_tokenizer.batch_decode(outputs, skip_special_tokens=True)
    en_text = "\n".join([s.capitalize() for s in en_text])
    return en_text


def translate_en(en_text):
    input_ids = enru_tokenizer(en_text, return_tensors="pt", padding=True).input_ids
    outputs = enru_model.generate(input_ids=input_ids, max_length=512, num_beams=5, num_return_sequences=1)
    ru_text = enru_tokenizer.batch_decode(outputs, skip_special_tokens=True)
    ru_text = "\n".join([s.capitalize() for s in ru_text])
    return ru_text

# def ask_in_english(question_ru, verbose=False):
#     question_en = translate_ru(question_ru+"?")
#     print(f"\033[092mTranslated question: {question_en}\033[0m") if verbose else None
#     answer_en, sources = answer_with_openai(question_en, verbose=verbose)
#     print(f"\033[092mTranslated answer: {answer_en}\033[0m") if verbose else None
#     answer_ru = translate_en(answer_en.split('\n'))
#
#     print(f"\033[095mОТВЕТ: \033[0m\n{answer_ru}")
#     print("\n\033[095mИСТОЧНИКИ: \033[0m")
#     for s in sources:
#         print(s)
