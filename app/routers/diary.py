from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import Diary
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.auth.auth import get_current_user

router = APIRouter(
    prefix="/diaries",
    tags=["diaries"]
)

# CREATE
@router.post("/", response_model=DiaryResponse)
async def create_diary(
    diary: DiaryCreate,
    current_user: int = Depends(get_current_user)
):
    new_diary = await Diary.create(**diary.model_dump(), author_id=current_user)
    return await DiaryResponse.from_tortoise_orm(new_diary)

# READ (단일)
@router.get("/{diary_id}", response_model=DiaryResponse)
async def read_diary(
    diary_id: int,
    current_user: int = Depends(get_current_user)
):
    diary = await Diary.filter(id=diary_id, author_id=current_user).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return await DiaryResponse.from_tortoise_orm(diary)

# READ (전체)
@router.get("/", response_model=List[DiaryResponse])
async def read_all_diaries(current_user: int = Depends(get_current_user)):
    diaries = await Diary.filter(author_id=current_user)
    return await DiaryResponse.from_queryset(diaries)

# UPDATE
@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary(
    diary_id: int,
    diary_update: DiaryUpdate,
    current_user: int = Depends(get_current_user)
):
    diary = await Diary.filter(id=diary_id, author_id=current_user).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    update_data = diary_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(diary, key, value)
    await diary.save()
    return await DiaryResponse.from_tortoise_orm(diary)

# DELETE
@router.delete("/{diary_id}")
async def delete_diary(
    diary_id: int,
    current_user: int = Depends(get_current_user)
):
    diary = await Diary.filter(id=diary_id, author_id=current_user).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    await diary.delete()
    return {"message": "Diary deleted"}
