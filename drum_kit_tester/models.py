from pydantic import BaseModel
from typing import List


class TestResult(BaseModel):
    test_name : str
    passed : bool
    error : str | None = None
    selector: str | None = None 

class TestReport(BaseModel):
    total_tests: int
    passed : int
    failed : int
    results : List[TestResult]
    ai_diagnosis : str | None = None
