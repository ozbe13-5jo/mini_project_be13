from fastapi import APIRouter, Depends
from app.models import User
from app.crud.bookmark import is_bookmarked, add_bookmark, remove_bookmark
from app.dependencies import get_current_user

router = APIRouter(prefix="/quote", tags=["quote"])

# 랜덤 명언 제공
@router.get("/random")
async def random_quote(user: User = Depends(get_current_user)):
    quote = await user.get_random_quote()
    if not quote:
        return {"message": "No quotes available."}
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


# 도야머야ㅏ
