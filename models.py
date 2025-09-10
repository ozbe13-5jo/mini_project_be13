from tortoise.models import Model
from tortoise import fields

class Question(Model):
    """자기성찰 질문 모델"""
    id = fields.IntField(pk=True)
    question_text = fields.TextField(description="질문 내용")
    created_at = fields.DatetimeField(auto_now_add=True, description="생성일시")
    updated_at = fields.DatetimeField(auto_now=True, description="수정일시")
    
    class Meta:
        table = "questions"
        table_description = "자기성찰 질문 테이블"
