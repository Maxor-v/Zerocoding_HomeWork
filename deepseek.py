import requests
import json

API_KEY = "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"  # внутри скобок свой апи ключ отсюда https://openrouter.ai/settings/keys
MODEL = "egoogle/gemini-2.0-flash-exp:free"


def process_content(content):
    return content.replace('<think>', '').replace('</think>', '')


def chat_stream(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system",
            #  "content": f"Отвечай как клоун и используй только следующие ответы:\n{allowed_answers_str}"},
            "content": f"Отвечай как собака"},
            {"role": "assistant", "content": f"тебя зовут - шарик" },
            {"role": "user", "content": prompt}],
        "stream": True
    }

    with requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            stream=True
    ) as response:
        if response.status_code != 200:
            print("Ошибка API:", response.status_code)
            return ""

        full_response = []

        for chunk in response.iter_lines():
            if chunk:
                chunk_str = chunk.decode('utf-8').replace('data: ', '')

                try:
                    chunk_json = json.loads(chunk_str)
                    if "choices" in chunk_json:
                        content = chunk_json["choices"][0]["delta"].get("content", "")
                        if content:
                            cleaned = process_content(content)
                            print(cleaned, end='', flush=True)
                            full_response.append(cleaned)
                except:
                    pass

        print()  # Перенос строки после завершения потока
        return ''.join(full_response)


def main():
    print("Чат с DeepSeek-R1 (by Antric)\nДля выхода введите 'exit'\n")

    while True:
        user_input = input("Вы: ")

        if user_input.lower() == 'exit':
            print("Завершение работы...")
            break

        print("DeepSeek-R1:", end=' ', flush=True)
        chat_stream(user_input)


if __name__ == "__main__":
    main()