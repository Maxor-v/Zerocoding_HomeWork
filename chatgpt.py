from openai import OpenAI

# Инициализация клиента OpenAI
client = OpenAI(
    api_key=" ",
    base_url="https://api.proxyapi.ru/openai/v1",
)

# Начинаем бесконечный цикл для общения
print("Введите 'exit' для выхода из программы.")
while True:
    # Получаем ввод от пользователя
    user_input = input("Вы: ")

    # Проверяем, не хочет ли пользователь выйти
    if user_input.lower() == 'exit':
        print("Выход из программы.")
        break

    # Отправляем запрос к нейросети
    chat_completion = client.chat.completions.create(
       model="gpt-3.5-turbo-1106",
       messages=[{"role": "user", "content": user_input}]
    )

    # Получаем ответ от нейросети

    response_content = chat_completion.choices[0].message.content

    # Выводим ответ
    print("Нейросеть:", response_content)
