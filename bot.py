import telebot
from openai import OpenAI
from gtts import gTTS
import os
import tempfile

# Инициализация клиента OpenAI
client = OpenAI(
    api_key="",
    base_url="https://api.proxyapi.ru/openai/v1",
)

# Инициализация Telegram бота
bot = telebot.TeleBot("")

# Словарь для хранения формата ответа пользователей
user_preference = {}


@bot.message_handler(commands=['set_format'])
def set_format(message):
    # Установка формата ответа от пользователя
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Текст', 'Голос')
    bot.send_message(message.chat.id, "Выберите формат ответа:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Текст', 'Голос'])
def choose_format(message):
    # Сохраняем предпочтение пользователя
    user_preference[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"Формат ответа установлен на: {message.text}")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    # Проверяем, установил ли пользователь формат ответа
    format_choice = user_preference.get(message.chat.id, 'Текст')  # По умолчанию - текст

    # Список допустимых ответов
    allowed_answers = [
        "Седан – это тип кузова автомобиля с четырьмя дверями.",
        "Кроссоверы обычно имеют высокий клиренс и просторный салон.",
        "Электромобили работают на электричестве и имеют нулевой уровень выбросов.",
        "Спорткары созданы для высокой скорости и производительности.",
        "режим работы - со вторника по пятницу"
    ]

    # Создаем строку из допустимых ответов
    allowed_answers_str = "\n".join(allowed_answers)

    # Отправляем запрос к нейросети
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system",
            #  "content": f"Отвечай как клоун и используй только следующие ответы:\n{allowed_answers_str}"},
            "content": f"Отвечай как веселый парень"},
            {"role": "user", "content": user_input}
        ]
    )

    # Получаем ответ от нейросети
    response_content = chat_completion.choices[0].message.content

    if format_choice == 'Текст':
        # Отправляем текстовое сообщение
        bot.send_message(message.chat.id, response_content)
    elif format_choice == 'Голос':
        # Преобразуем текст в голосовое сообщение
        tts = gTTS(text=response_content, lang='ru')

        # Создаем временный файл для аудио
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            tmp_file.close()

            # Отправляем голосовое сообщение пользователю
            with open(tmp_file.name, 'rb') as audio:
                bot.send_voice(message.chat.id, audio)

        # Удаляем временный файл
        os.remove(tmp_file.name)


# Запуск бота
print("Бот запущен. Нажмите Ctrl+C для остановки.")
bot.polling()
