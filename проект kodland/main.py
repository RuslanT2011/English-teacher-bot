import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import time

sample_rate = 44100
duration = 4  # секунд записи
max_errors = 3
score = 0
errors = 0
print("🎮 Добро пожаловать в игру «Говори правильно»!")
print("Выбери уровень сложности: easy / medium / hard")
level = input(">>> ").strip().lower()
while errors<max_errors:
    words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
    }
    word=random.choice(words_by_level[level])
    print(f"\n🟢 Уровень сложности: {level.capitalize()}")
    print("🧠 Ты увидишь слово по-русски. Произнеси его перевод на английском.")
    time.sleep(2)
    print("Ваше слово:", word)

    translator = Translator()
    translated = translator.translate(word, src='ru', dest='en').text.lower()  # здесь 'en' — это английский

    print("Говори...")
    recording = sd.rec(
    int(duration * sample_rate), # длительность записи в сэмплах
    samplerate=sample_rate,      # частота дискретизации
    channels=1,                  # 1 — это моно
    dtype="int16")               # формат аудиоданных
    sd.wait()  # ждём завершения записи

    wav.write("output.wav", sample_rate, recording)
    print("Запись завершена, теперь распознаём...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        text=text.lower()
        print("Ты сказал:", text)
    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("Не удалось распознать речь.")
    except sr.RequestError as e:             # - если нет интернета или API недоступен
        print(f"Ошибка сервиса: {e}")
    if text==translated:
        print("Вы молодец! Это правильный ответ!🤗")
        score += 1
    else:
        print("К сожалению, это неправильный ответ😭, правильный ответ -", translated)
        errors += 1
if score<3:
    print("Игра окончена! Ваш результат -", score, "Это довольно плохой результат, но не расстраивайтесь, в следующий раз у вас точно получится!")
elif score>2 and score<7:
    print("Игра окончена! Ваш результат -", score, "Это неплохой результат, но можно и лучше, но вот вам цветочек за старания🌷")
else:
    print("Игра окончена! Ваш результат -", score, "Это отличный результат, вот вам подарок за работу🎁")