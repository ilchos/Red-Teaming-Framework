# schemas.py

from typing import Dict, List, Optional

from pydantic import BaseModel


class TestRequest(BaseModel):
    model_name: str
    probes: List[str]


class TestRequest2(BaseModel):
    model_name: str


class GarakListProbesResponse(BaseModel):
    result: List[str]


class LeaderboardCompetitorsResponse(BaseModel):
    result: List[Dict]
    error: Optional[str] = None


class ModelsListResponse(BaseModel):
    result: List[str]


class TestResponse(BaseModel):
    hitlog: List[Dict]
    evals: List[Dict]


class TestLeaderboardResponse(BaseModel):
    evals: List[Dict]


class UploadFileRequest(BaseModel):
    model_name: str
    score: float
    low_level_category: str
    high_level_category: str
    lang: str
    manually_tested: bool
    benchmark_version: str
