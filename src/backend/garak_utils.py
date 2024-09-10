import json
import subprocess
from typing import Dict, List

from loguru import logger
from settings import settings


def create_rest_settings_file(model_name: str, file_path: str):
    rest_settings_simple = {
        "rest": {
            "RestGenerator": {
                "name": "ChatGPT",
                "uri": settings.vse_gpt_url,
                "method": "post",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.vse_gpt_api_key}",  # noqa: E501
                },
                "req_template_json_object": {
                    "model": model_name,
                    "messages": [{"role": "user", "content": "$INPUT"}],
                },
                "response_json": True,
                "response_json_field": "$.choices[0].message.content",
            }
        }
    }
    with open(file_path, "w+") as f:
        f.write(json.dumps(rest_settings_simple))


def run_garak_command(command: str) -> subprocess.CompletedProcess:
    logger.info(f"Running command: {command}")
    return subprocess.run(command, shell=True, capture_output=True, text=True)


def process_garak_report(report_prefix: str, keys: List[str]) -> List[Dict]:
    results = []
    try:
        with open(f"{report_prefix}.report.jsonl", "r") as f:
            for line in f.readlines():
                loaded_json_line = json.loads(line)
                if loaded_json_line["entry_type"] == "eval":
                    results.append({k: loaded_json_line[k] for k in keys})
    except Exception as exc:
        logger.error(f"Exception: {exc}")
    return results


def process_garak_hitlog(report_prefix: str, keys: List[str]) -> List[Dict]:
    results = []
    try:
        with open(f"{report_prefix}.hitlog.jsonl", "r") as f:
            for line in f.readlines():
                loaded_json_line = json.loads(line)
                results.append({k: loaded_json_line[k] for k in keys})
    except Exception as exc:
        logger.error(f"Exception: {exc}")
    return results
