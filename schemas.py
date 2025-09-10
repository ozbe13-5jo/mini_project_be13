from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class QuestionResponse(BaseModel):
    """질문 응답 스키마"""
    id: int
    question_text: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class RandomQuestionResponse(BaseModel):
    """랜덤 질문 응답 스키마"""
    question: QuestionResponse
    message: str = "오늘의 자기성찰 질문입니다."
    
    class Config:
        from_attributes = True
