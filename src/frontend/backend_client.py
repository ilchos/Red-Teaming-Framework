import requests


class BackendClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_data(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("result", [])
        else:
            print(f"Error fetching data from {url}: {response.status_code}")
            return []

    def post_data(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error posting data to {url}: {response.status_code}")
            return {}

    def fetch_options(self):
        return self.fetch_data("garak_list_probes")

    def fetch_models(self):
        return self.fetch_data("models_list")

    def fetch_leaderboard_competitors(self):
        return self.fetch_data("leaderboard_competitors")

    def fetch_leaderboard_categories_tree(self):
        response = requests.get(f"{self.base_url}/leaderboard_categories")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching leaderboard categories: {response.status_code}")
            return {}
