import json
from pathlib import Path
import requests
import uuid

from langchain_openai import ChatOpenAI
from yandex_chain import YandexLLM, YandexGPTModel
from langchain_community.chat_models import GigaChat



class LLMLoader():
    def __init__(self, keys_path: Path = None):
        default_keys_path = Path(__file__).parents[1] / "config" / "api_keys.json"
        self.keys_path = default_keys_path if keys_path is None else keys_path
        self.api_keys = json.loads(self.keys_path.read_text())

    def load_vsegpt(self, model="openai/gpt-4o", temperature = 0):
        keys = self.api_keys["vsegpt"]
        llm = ChatOpenAI(
                base_url=keys["base_url"],
                api_key=keys["key"],
                model=model,
                temperature=temperature
        )
        return llm

    def load_openai(self, model="gpt-4o", temperature=0, mode="vsegpt"):
        if mode == "openai":
            key = self.api_keys["openai"]["key"]
            llm = ChatOpenAI(openai_api_key=key, model=model, temperature=temperature)
            return llm
        if mode == "vsegpt":
            model_full_title = f"openai/{model}" if not model.startswith("openai/") else model
            return self.load_vsegpt(model_full_title, temperature)


    def load_yandexgpt(self, model=YandexGPTModel.Pro, temperature=0):
        keys = self.api_keys["yandex"]
        llm = YandexLLM(folder_id=keys["folder_id"],
                        api_key=keys["key"],
                        model=model,
                        temperature=temperature
        )
        return llm


    def load_gigachat(self, model="GigaChat-Pro", temperature=0.001): # должна быть > 0 согласно документации
        def get_access_token(auth_token, scope='GIGACHAT_API_PERS'):
            # Создадим идентификатор UUID (36 знаков)
            rq_uid = str(uuid.uuid4())

            # API URL
            url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

            # Заголовки
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': rq_uid,
                'Authorization': f'Basic {auth_token}'
            }

            # Тело запроса
            payload = {
                'scope': scope
            }

            try:
                # Делаем POST запрос с отключенной SSL верификацией
                # (можно скачать сертификаты Минцифры, тогда отключать проверку не надо)
                response = requests.post(url, headers=headers, data=payload, verify=False)
                return response
            except requests.RequestException as e:
                print(f"Ошибка: {str(e)}")
                return -1

        keys = self.api_keys["gigachat"]
        response = get_access_token(keys["auth"])
        if response != 1:
            print(response.text)
            giga_token = response.json()['access_token']

        llm = GigaChat(verify_ssl_certs=False,
                scope="GIGACHAT_API_PERS",
                model=model,
                access_token=giga_token,
                temperature=temperature)
        return llm


    def load_anthropic(self, model="anthropic/claude-3.5-sonnet", temperature=0):
        keys = self.api_keys["vsegpt"]
        llm = ChatOpenAI(
            base_url=keys["base_url"],
            api_key=keys["key"],
            model=model,
            temperature=temperature
        )
        return llm
