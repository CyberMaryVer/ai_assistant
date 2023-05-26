from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

enru_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
enru_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-ru")

ruen_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
ruen_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-en")


def translate_ruen(text):
    input_ids = ruen_tokenizer(text, return_tensors="pt", padding=True).input_ids
    outputs = ruen_model.generate(input_ids=input_ids, num_beams=5, num_return_sequences=1)
    res = ruen_tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return res


def translate_enru(text):
    input_ids = enru_tokenizer(text, return_tensors="pt", padding=True).input_ids
    outputs = enru_model.generate(input_ids=input_ids, num_beams=5, num_return_sequences=1)
    res = enru_tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return res
