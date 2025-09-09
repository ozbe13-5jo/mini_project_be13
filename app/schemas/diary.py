from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 공통 속성
class DiaryBase(BaseModel):
    title: str
    content: str

# 작성 요청
class DiaryCreate(DiaryBase):
    pass

# 수정 요청
class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# 응답
class DiaryResponse(DiaryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
