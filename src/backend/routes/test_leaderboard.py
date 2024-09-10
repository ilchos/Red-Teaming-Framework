import os

from fastapi import APIRouter
from garak_utils import (
    create_rest_settings_file,
    process_garak_report,
    run_garak_command,
)
from loguru import logger
from schemas import TestLeaderboardResponse, TestRequest2

router = APIRouter()


@router.post("/test_leaderboard", response_model=TestLeaderboardResponse)
async def test_leaderboard_endpoint(request: TestRequest2):
    create_rest_settings_file(request.model_name, "rest_settings_simple.json")
    current_path = os.getcwd()
    file_names = []
    probes = [
        "dan.ChatGPT_Developer_Mode_RANTI",
        "dan.DAN_Jailbreak",
        "dan.DUDE",
        "lmrc.SlurUsage",
    ]
    for probe in probes:
        report_prefix = f"{current_path}/garak_\
            {'_'.join(request.model_name.split('/'))}_\
            {'_'.join(probe.split('.'))}"
        command = (
            f"garak "
            f"--model_type rest "
            f"--generator_option_file rest_settings_simple.json "
            f"--probes {probe} "
            f"--report_prefix {report_prefix} "
            f"--verbose "
            f"--generations 2"
        )
        try:
            result = run_garak_command(command)
            file_names.append(report_prefix)
        except Exception as exc:
            logger.error(f"Exception: {exc}")
            logger.info(f"SKIP probe: {probe}")

        logger.info(f"result.stdout: {result.stdout}")
        logger.info(f"result.stderr: {result.stderr}")

    evals = []
    for fname in file_names:
        evals.extend(
            process_garak_report(fname, ["probe", "detector", "passed", "total"])
        )

    logger.info(f"BACKEND EVALS: {evals}")
    return TestLeaderboardResponse(evals=evals)
