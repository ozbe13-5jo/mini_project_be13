from app.models import Bookmark, Quote, User
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

async def is_bookmarked(user: User, quote_id: int) -> bool:
    try:
        quote = await Quote.get(id=quote_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Quote not found")
    return await quote.is_bookmarked_by(user)

async def add_bookmark(user: User, quote_id: int):
    try:
        quote = await Quote.get(id=quote_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Quote not found")

    if await quote.is_bookmarked_by(user):
        raise HTTPException(status_code=409, detail="Already bookmarked")

    return await Bookmark.create(user=user, quote=quote)

async def remove_bookmark(user: User, quote_id: int):
    bookmark = await Bookmark.filter(user=user, quote_id=quote_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    await bookmark.delete()
    return True
