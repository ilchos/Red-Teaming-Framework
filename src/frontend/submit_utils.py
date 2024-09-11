import requests


def send_file_to_backend(file):
    # URL бекенда, куда будет отправлен файл
    backend_url = "http://backend:8000/upload"

    # Отправка файла на бекенд
    files = {"file": (file.name, file.read())}
    response = requests.post(backend_url, files=files)

    # Возвращаем ответ от бекенда
    return response.json().get("message", "Неизвестная ошибка")
