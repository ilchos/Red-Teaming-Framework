from enum import Enum
from pathlib import Path
from datetime import datetime

PROJECT_PATH = Path(__file__).parents[1]
DATA_PATH = PROJECT_PATH / "data"

class ProjectRouter(Enum):
    PROJECT = Path(__file__).parent
    DATA = DATA_PATH
    PROMPTS = DATA_PATH / "prompts"

    def get_timestamp_path(self):
        base = self.value
        dt = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
        folder_path = base / dt
        folder_path.mkdir(parents=True, exist_ok=True)
        return folder_path
