from app.yandex_assistant.client import ask_assistant


question = "Какие есть лимиты REST API?"
answer = ask_assistant(question)

print(answer)
