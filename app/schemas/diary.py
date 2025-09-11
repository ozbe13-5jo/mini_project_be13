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
    title: str
    content: str
    user_id: int  # ORM 객체의 user.id에서 가져옴

    model_config = {
        "from_attributes": True
    }