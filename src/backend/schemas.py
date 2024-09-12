from typing import Dict, List, Optional

from pydantic import BaseModel


class LeaderboardCompetitorsResponse(BaseModel):
    result: List[Dict]
    error: Optional[str] = None


class UploadFileRequest(BaseModel):
    model_name: str
    score: float
    low_level_category: str
    high_level_category: str
    lang: str
    manually_tested: bool
    benchmark_version: str
