import datetime

from pymystem3 import Mystem

from fastapi_app.routes.content_filter.schemas import Filter


async def check_filters_mystem_lex(phrase_check, filter_lex):
    for check_word in phrase_check:
        if "analysis" in check_word:
            for analysis in check_word["analysis"]:
                if analysis.get("lex") and analysis["lex"] == filter_lex:
                    return filter_lex

    return False


async def check_filters_mystem_text(analysis, filter_text):
    for check_word in analysis:
        if check_word.get("text") and check_word["text"] == filter_text:
            return filter_text

    return False


async def filter_message(message: str, filter_rules: list[Filter]):
    mystem = Mystem()
    analysis = mystem.analyze(message)

    for filter_rule in filter_rules:
        filter = mystem.analyze(filter_rule.word)[0]
        if filter.get("text"):
            if await check_filters_mystem_text(analysis, filter["text"]):
                return filter_rule

        #Проверка по ликсеме
        if "analysis" in filter:
            for f_analysis in filter["analysis"]:
                if f_analysis["lex"] and await check_filters_mystem_lex(analysis, f_analysis["lex"]):
                    return filter_rule

    return None


if __name__ == "__main__":
    import asyncio

    sentence = "Я вижу большую кошку на дереве. string."

    filters = [
        Filter(id=1, word="string", created_at=datetime.datetime.utcnow(), company_id=1, is_archive=True),
        Filter(id=5, word="кошка", created_at=datetime.datetime.utcnow(), company_id=1, is_archive=True),
        Filter(id=6, word="дерево", created_at=datetime.datetime.utcnow(), company_id=1, is_archive=True),
    ]

    filter = asyncio.run(filter_message(sentence, filters))
    print(f"Сработал фильр: {filter}")
