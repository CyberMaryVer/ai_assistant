from pymystem3 import Mystem

# Создание объекта анализатора
mystem = Mystem()

# Английское предложение для анализа
sentence = "I see a big cat on the tree string"
sentence = "Я вижу большую кошку на дереве."

# Разделение предложения на слова
words = sentence.split()

# Проверка наличия слов
for word in words:
    # Морфологический анализ слова
    analysis = mystem.analyze(word)
    print(analysis)

    # Проверка наличия слова
    if 'analysis' in analysis[0]:
        print(f"Найдено слово '{word}' в предложении.")
