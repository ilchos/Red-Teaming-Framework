from fastapi import APIRouter
from garak_utils import run_garak_command
from schemas import GarakListProbesResponse

router = APIRouter()


@router.get("/garak_list_probes", response_model=GarakListProbesResponse)
async def get_garak_list_probes():
    command = "garak --list_probes"
    result = run_garak_command(command)
    list_probes_text = result.stdout.split("\n")[1:-1]
    list_probes = [probe_text[21:] for probe_text in list_probes_text]
    return GarakListProbesResponse(result=list_probes)
