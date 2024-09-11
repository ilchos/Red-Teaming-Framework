import os

from authorization.jwt_bearer import JWTBearer
from fastapi import APIRouter, Depends
from garak_utils import (
    create_rest_settings_file,
    process_garak_hitlog,
    process_garak_report,
    run_garak_command,
)
from loguru import logger
from schemas import TestRequest, TestResponse

router = APIRouter()


@router.post("/test", response_model=TestResponse, dependencies=[Depends(JWTBearer())])
async def test_endpoint(request: TestRequest):
    create_rest_settings_file(request.model_name, "rest_settings_simple.json")
    current_path = os.getcwd()
    report_prefix = f"{current_path}/garak"
    probes = ",".join(request.probes)
    command = (
        f"garak "
        f"--model_type rest "
        f"--generator_option_file rest_settings_simple.json "
        f"--probes {probes} "
        f"--report_prefix {report_prefix} "
        f"--verbose "
        f"--generations 1"
    )
    result = run_garak_command(command)
    logger.info(f"result.stdout: {result.stdout}")
    logger.info(f"result.stderr: {result.stderr}")

    evals = process_garak_report(
        report_prefix, ["probe", "detector", "passed", "total"]
    )
    hitlog = process_garak_hitlog(
        report_prefix, ["prompt", "output", "probe", "detector", "score"]
    )

    return TestResponse(hitlog=hitlog, evals=evals)
