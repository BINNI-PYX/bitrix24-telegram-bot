from app.yandex_assistant.client import ask_assistant


question = "Лимиты REST API"
answer = ask_assistant(question)

print(answer)
