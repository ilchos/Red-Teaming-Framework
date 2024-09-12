import json

import requests
from settings import settings


class BackendClient:
    def __init__(self, base_url):
        self.base_url = base_url

        self.headers = None
        self.update_jwt_token()

    def update_jwt_token(self):
        token = self.post_data("/token", settings.backend_settings.model_dump())[
            "access_token"
        ]
        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def fetch_data(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("result", [])
        else:
            print(f"Error fetching data from {url}: {response.status_code}")
            return []

    def post_data(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error posting data to {url}: {response.status_code}")
            return {}

    def fetch_leaderboard_competitors(self):
        return self.fetch_data("leaderboard_competitors")

    def fetch_leaderboard_categories_tree(self):
        response = requests.get(
            f"{self.base_url}/leaderboard_categories", headers=self.headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching leaderboard categories: {response.status_code}")
            return {}

    def send_file_to_backend(self, file: bytes):

        if not file:
            return "Ошибка!"

        json_str = file.decode("utf-8")
        json_dict = json.loads(json_str)

        response = self.post_data("/upload", data=json_dict)

        print(f"FRONTEND RESPONSE UPLOAD: {response}")

        # Возвращаем ответ от бекенда
        return response.get("message", "Ошибка!")
