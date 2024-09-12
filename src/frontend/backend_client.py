import json
from typing import Any, Dict, List, Optional, Union

import requests
from loguru import logger
from settings import settings


class BackendClient:
    """
    Класс для взаимодействия с бэкендом через HTTP-запросы.

    Attributes:
        base_url (str): Базовый URL бэкенда.
        headers (Optional[Dict[str, str]]): Заголовки HTTP-запросов.
    """

    def __init__(self, base_url: str):
        """
        Инициализация класса BackendClient.

        Args:
            base_url (str): Базовый URL бэкенда.
        """
        self.base_url = base_url
        self.headers: Optional[Dict[str, str]] = None
        self.update_jwt_token()

    def update_jwt_token(self) -> None:
        """
        Обновляет JWT-токен для авторизации запросов.
        """
        token = self.post_data("token", settings.backend_settings.model_dump())[
            "access_token"
        ]
        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def fetch_data(self, endpoint: str) -> List[Dict[str, Any]]:
        """
        Выполняет GET-запрос к указанному эндпоинту и возвращает данные.

        Args:
            endpoint (str): Эндпоинт для запроса.

        Returns:
            List[Dict[str, Any]]: Список словарей с данными.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("result", [])
        else:
            logger.error(f"Error fetching data from {url}: {response.status_code}")
            return []

    def post_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполняет POST-запрос к указанному эндпоинту с переданными данными.

        Args:
            endpoint (str): Эндпоинт для запроса.
            data (Dict[str, Any]): Данные для отправки.

        Returns:
            Dict[str, Any]: Ответ от сервера в виде словаря.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error posting data to {url}: {response.status_code}")
            return {}

    def fetch_leaderboard_competitors(self) -> List[Dict[str, Any]]:
        """
        Получает список участников лидерборда.

        Returns:
            List[Dict[str, Any]]: Список словарей с данными участников.
        """
        return self.fetch_data("leaderboard_competitors")

    def fetch_leaderboard_categories_tree(self) -> Dict[str, Any]:
        """
        Получает дерево категорий лидерборда.

        Returns:
            Dict[str, Any]: Словарь с данными категорий.
        """
        response = requests.get(
            f"{self.base_url}/leaderboard_categories", headers=self.headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(
                f"Error fetching leaderboard categories: {response.status_code}"
            )
            return {}

    def send_file_to_backend(self, file: bytes) -> Union[str, Dict[str, Any]]:
        """
        Отправляет файл на бэкенд.

        Args:
            file (bytes): Байты файла для отправки.

        Returns:
            Union[str, Dict[str, Any]]: Ответ от бэкенда или сообщение об ошибке.
        """
        if not file:
            return "Ошибка!"

        json_str = file.decode("utf-8")
        json_dict = json.loads(json_str)

        response = self.post_data("upload", data=json_dict)

        logger.info(f"FRONTEND RESPONSE UPLOAD: {response}")

        # Возвращаем ответ от бекенда
        return response.get("message", "Ошибка!")
