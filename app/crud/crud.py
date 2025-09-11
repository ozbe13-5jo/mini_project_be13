from fastapi import APIRouter, HTTPException, Depends
from app.models import Diary
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.auth.auth import get_current_user

router = APIRouter(
    prefix="/diaries",
    tags=["diaries"]
)

# CREATE
@router.post("/", response_model=DiaryResponse)
async def create_diary(diary: DiaryCreate, current_user=Depends(get_current_user)):
    new_diary = await Diary.create(**diary.model_dump(), user=current_user)
    return DiaryResponse.model_validate(new_diary)

# READ (단일)
@router.get("/{diary_id}", response_model=DiaryResponse)
async def read_diary(diary_id: int, current_user=Depends(get_current_user)):
    diary = await Diary.filter(id=diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    if diary.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    return DiaryResponse.model_validate(diary)

# READ (전체)
@router.get("/", response_model=list[DiaryResponse])
async def read_all_diaries(current_user=Depends(get_current_user)):
    diaries = await Diary.filter(user_id=current_user.id)
    return [DiaryResponse.model_validate(d) for d in diaries]

# UPDATE
@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary(diary_id: int, diary_update: DiaryUpdate, current_user=Depends(get_current_user)):
    diary = await Diary.filter(id=diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    if diary.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    update_data = diary_update.model_dump(exclude_unset=True)
    await diary.update_from_dict(update_data).save()
    return DiaryResponse.model_validate(diary)

# DELETE
@router.delete("/{diary_id}")
async def delete_diary(diary_id: int, current_user=Depends(get_current_user)):
    diary = await Diary.filter(id=diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    if diary.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    await diary.delete()
    return {"message": "Diary deleted"}
