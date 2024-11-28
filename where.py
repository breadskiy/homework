from transformers import pipeline


classifier = pipeline("sentiment-analysis", model="blanchefort/rubert-base-cased-sentiment")


texts = [
    "Отличный товар",
    "Мне не понравилось",
    "Прекрасно выглядит, ничего не меняйте!",
    "Ничего не понял",
    "У меня не работала розетка, в остальном всё отлично"
]


results = classifier(texts)


for text, result in zip(texts, results):
    print(f"Текст: {text} | Результат: {result}")