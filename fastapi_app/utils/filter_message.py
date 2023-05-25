import datetime

from pymystem3 import Mystem

from fastapi_app.routes.content_filter.schemas import Filter


async def check_filters_mystem(analysis, filter_lex):
    for filter_mystem in analysis:
        if "analysis" in filter_mystem:
            for analysis in filter_mystem["analysis"]:
                print(f'{analysis["lex"]}')
                print(f'{filter_lex=}')
                if analysis.get("lex") and analysis["lex"] == filter_lex:
                    return filter_mystem


async def filter_message(message: str, filter_rules: list[Filter]):
    mystem = Mystem()

    analysis = mystem.analyze(message)

    print("filter_message!!!!!!!!!!!!!!!!")
    for filter_rule in filter_rules:
        filter = mystem.analyze(filter_rule.word)[0]
        print(f"{filter=}")
        if "analysis" in filter:
            for f_analysis in filter["analysis"]:
                if f_analysis["lex"] and await check_filters_mystem(analysis, f_analysis["lex"]):
                    return filter_rule

    return None


if __name__ == "__main__":
    sentence = "Я вижу большую кошку на дереве."

    filters = [Filter(id=1, word="кошка", created_at=datetime.datetime.utcnow(), company_id=1, is_archive=True),
               Filter(id=2, word="дерево", created_at=datetime.datetime.utcnow(), company_id=1, is_archive=True),
               ]

    print(filter_message(sentence, filters))
