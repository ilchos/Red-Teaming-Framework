import subprocess
import os
import json

from fastapi import FastAPI
import psycopg.rows
from pydantic import BaseModel
import uvicorn
import psycopg


app = FastAPI()

class TestRequest(BaseModel):
    model_name: str
    probes: list[str]

@app.get("/garak_list_probes")
async def get_garak_list_probes():
    command = "garak --list_probes"
    result = subprocess.run(command, shell=True, capture_output=True)

    list_probes_text = result.stdout.decode().split("\n")[1:-1]
    list_probes = [l[21:] for l in list_probes_text]

    return {"result": list_probes}

@app.get("/leaderboard_competitors")
async def get_leaderboard_competitors():
    result = []
    
    try:
        # Подключение к базе данных
        conn = psycopg.connect(
            host="postgres",
            dbname="postgres",
            user="postgres",
            password="postgres",
            row_factory=psycopg.rows.dict_row,
        )
        
        # Создание курсора для выполнения SQL-запросов
        cur = conn.cursor()

        # Выполнение SQL-запроса
        query = "SELECT \
                    model_name, \
                    total, \
                    passed, \
                    hit_rate, \
                    manually_tested, \
                    high_level_category, \
                    mid_level_category, \
                    low_level_category \
                FROM leaderboard_competitors"
        cur.execute(query)
        
        # Получение результатов запроса
        result = cur.fetchall()        
        
        # Закрытие курсора и соединения
        cur.close()
        conn.close()
    
    except Exception as e:
        return {"error": str(e)}
    
    return {"result": result}

@app.get("/models_list")
async def get_garak_list_probes():
    list_models = ["openai/gpt-3.5-turbo-0125", "openai/gpt-4o-mini", "google/gemini-pro"]
    return {"result": list_models}


@app.post("/test")
async def test_endpoint(request: TestRequest):
    rest_settings_simple = {
        "rest": {
            "RestGenerator": {
                "name": "ChatGPT",
                "uri": "https://api.vsegpt.ru/v1/chat/completions",
                "method": "post",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer sk-or-vv-272184de5415a787c23ee34c4b4c97fa47f9287fbe85030fc7f2721790a3fac2"
                }, 
                "req_template_json_object": {
                    "model": request.model_name,
                    "messages": [
                        {
                            "role": "user",
                            "content": "$INPUT"
                        }
                    ]
                }, 
                "response_json": True, 
                "response_json_field": "$.choices[0].message.content"
            }
        }
    }
    with open("rest_settings_simple.json", "w+") as f:
        f.write(json.dumps(rest_settings_simple))


    current_path = os.getcwd()

    report_prefix = current_path + "/garak"
    probes = ",".join(request.probes)
    command = (
        f"garak \
            --model_type rest \
            --generator_option_file rest_settings_simple.json \
            --probes {probes} \
            --report_prefix {report_prefix} \
            --verbose \
            --generations 1"
    )
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print(f"result.stdout: {result.stdout}")
    print(f"result.stderr: {result.stderr}")
    results = []

    # processing tables
    evals = []
    evals_keys = ["probe", "detector", "passed", "total"]
    try:
        with open(report_prefix + ".report.jsonl", "r") as f:
            data = f.readlines()
            for line in data:
                loaded_json_line = json.loads(line)

                if loaded_json_line["entry_type"] == "eval":
                    d = {k: loaded_json_line[k] for k in evals_keys}
                    evals.append(d)
    except Exception as exc:
        print(f"Exception: {exc}")
    # TODO: delete this file

    hitlog = []
    hitlog_keys = ["prompt", "output", "probe", "detector", "score"]
    try:
        with open(report_prefix + ".hitlog.jsonl", "r") as f:
            data = f.readlines()
            for line in data:
                loaded_json_line = json.loads(line)
                d = d = {k: loaded_json_line[k] for k in hitlog_keys}
                hitlog.append(d)
    except Exception as exc:
        print(f"Exception: {exc}")

     # TODO: delete this file

    # TODO: insert data to database

    return {"hitlog": hitlog, "evals": evals}


class TestRequest2(BaseModel):
    model_name: str

@app.post("/test_leaderboard")
async def test_leaderboard_endpoint(request: TestRequest2):
    rest_settings_simple = {
        "rest": {
            "RestGenerator": {
                "name": "ChatGPT",
                "uri": "https://api.vsegpt.ru/v1/chat/completions",
                "method": "post",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer sk-or-vv-272184de5415a787c23ee34c4b4c97fa47f9287fbe85030fc7f2721790a3fac2"
                }, 
                "req_template_json_object": {
                    "model": request.model_name,
                    "messages": [
                        {
                            "role": "user",
                            "content": "$INPUT"
                        }
                    ]
                }, 
                "response_json": True, 
                "response_json_field": "$.choices[0].message.content",
            }
        }
    }
    with open("rest_settings_simple.json", "w+") as f:
        f.write(json.dumps(rest_settings_simple))

    current_path = os.getcwd()

    file_names = []

    probes = [
        # "dan.AntiDAN",
        "dan.ChatGPT_Developer_Mode_RANTI",
        # "dan.ChatGPT_Developer_Mode_v2",
        "dan.DAN_Jailbreak",
        # "lmrc.Bullying",
        "dan.DUDE",
        # "dan.DanInTheWildMini",
        # "encoding.InjectBase64",
        # "promptinject.HijackHateHumansMini",
        "lmrc.SlurUsage",


    ]
    for probe in probes:
        report_prefix = current_path + f"/garak_{'_'.join(request.model_name.split('/'))}_{'_'.join(probe.split('.'))}"
        command = (
            f"garak \
                --model_type rest \
                --generator_option_file rest_settings_simple.json \
                --probes {probe} \
                --report_prefix {report_prefix} \
                --verbose \
                --generations 2"
        )
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            file_names.append(report_prefix)
        except Exception as exc:
            print(f"Exception: {exc}")
            print(f"SKIP probe: {probe}")

        print(f"result.stdout: {result.stdout}")
        print(f"result.stderr: {result.stderr}")

    evals = []
    evals_keys = ["probe", "detector", "passed", "total"]
    for fname in file_names:
        try:
            with open(fname + ".report.jsonl", "r") as f:
                data = f.readlines()
                for line in data:
                    loaded_json_line = json.loads(line)

                    if loaded_json_line["entry_type"] == "eval":
                        d = {k: loaded_json_line[k] for k in evals_keys}
                        d["model_name"] = request.model_name
                        evals.append(d)
        except Exception as exc:
            print(f"Exception: {exc}")
        # TODO: delete this file

    print(f"BACKEND EVALS: {evals}")

    return {"evals": evals}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
