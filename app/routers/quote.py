from fastapi import APIRouter, Depends
from app.models import User, Quote
from app.crud.bookmark import is_bookmarked, add_bookmark, remove_bookmark
from app.dependencies import get_current_user
import random

from app.schemas.schemas import QuestionResponse

router = APIRouter(tags=["quotes"])

# 전체 명언 조회
@router.get("/")
async def get_quotes():
    return await Quote.all()

# 랜덤 명언 제공
@router.get("/random", response_model=QuestionResponse)
async def random_quote():
    quotes = await Quote.all()
    if not quotes:
        return {"message": "No quotes available."}
    quote = random.choice(quotes)  # DB에서 가져온 리스트 중 랜덤 선택
    return {"id": quote.id, "content": quote.quote_content, "author": quote.author}

# 북마크 조회
@router.get("/{quote_id}/bookmark")
async def check_bookmark(quote_id: int, user: User = Depends(get_current_user)):
    bookmarked = await is_bookmarked(user, quote_id)
    return {"quote_id": quote_id, "is_bookmarked": bookmarked}

# 북마크 추가
@router.post("/{quote_id}/bookmark")
async def create_bookmark(quote_id: int, user: User = Depends(get_current_user)):
    bookmark = await add_bookmark(user, quote_id)
    return {"message": "Bookmark added", "bookmark_id": bookmark.id}

# 북마크 삭제
@router.delete("/{quote_id}/bookmark")
async def delete_bookmark(quote_id: int, user: User = Depends(get_current_user)):
    await remove_bookmark(user, quote_id)
    return {"message": "Bookmark deleted"}
