import requests
import json
import os


class BaseAPI:
    def __init__(self, config_file=None):
        # If no config path is passed, find config.json at project root
        if config_file is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))  # go up from controller → project root
            config_file = os.path.join(base_dir, "config.json")

        self.base_url = self._load_config(config_file)

    def _load_config(self, config_file):
        """Load base_url from JSON config"""
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file {config_file} not found")

        with open(config_file, "r") as f:
            config = json.load(f)

        return config.get("base_url", "http://localhost:5094/api")


class IssueAPI(BaseAPI):
    def get_issues(self):
        """Fetch issues from API"""
        try:
            response = requests.get(f"{self.base_url}/issues")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print("API Error:", e)
            return []

    def create_issue(self, data: dict):
        url = f"{self.base_url}/issues"
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                return response.json()
            else:
                print("Error creating issue:", response.text)
                return None
        except Exception as e:
            print("Exception in create_issue:", e)
            return None

