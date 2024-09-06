import subprocess
import os
import json

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI()

class TestRequest(BaseModel):
    model_type: str
    model_name: str
    probes: str

@app.post("/test")
async def test_endpoint(request: TestRequest):
    current_path = os.getcwd()

    report_prefix = current_path + "/garak"
    print(f"report_prefix={report_prefix}")
    command = (
        f"garak \
            --model_type rest \
            --generator_option_file rest_settings_simple.json \
            --probes promptinject.HijackHateHumansMini \
            --report_prefix {report_prefix} \
            --verbose \
            --generations 1"
    )
    # result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # print(f"result.stdout: {result.stdout}")
    # print(f"result.stderr: {result.stderr}")
    results = []
    with open(report_prefix + ".report.jsonl", "r") as f:
        data = f.readlines()
        for line in data:
            loaded_json_line = json.loads(line)
            try:
                prompt = loaded_json_line["prompt"]
                model_output = loaded_json_line["outputs"][0]

                results.append({"prompt": prompt, "model_output": model_output})
            except Exception as exc:
                print(f"Exception! {exc}")
                print(f"loaded_json_line={loaded_json_line}")

    # TODO: insert data to database

    return {"result": results}

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()