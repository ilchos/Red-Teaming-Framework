from typing import Dict, List, Optional

from pydantic import BaseModel


class LeaderboardCompetitorsResponse(BaseModel):
    result: List[Dict]
    error: Optional[str] = None


class UploadFileRequest(BaseModel):
    id: float
    agent_name: str
    score: float
    vul_deepeval: str
    type_general: str
    lang: str
    manually_tested: bool = True
    benchmark_version: str = "1.0"
    reason: str
