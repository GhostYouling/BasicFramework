from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class EducationDetail(BaseModel):
    school: str
    period: str
    degree: str

class WorkExperience(BaseModel):
    company: str
    period: str
    position: str
    industry: str
    subordinates: str
    salary: str
    job_category: str
    responsibility: str

class CandidateBase(BaseModel):
    uuid: str
    name: str
    gender: str
    age: str
    education: str
    education_detail: List[EducationDetail]
    location: str
    expectation: str
    skills: List[str]
    work_experiences: List[WorkExperience]
    detail_link: str
    detail_extracted: bool = True
    extract_time: datetime

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int

    class Config:
        from_attributes = True 