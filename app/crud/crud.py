from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.auth.auth import get_current_user

router = APIRouter(
    prefix="/diaries",
    tags=["diaries"]
)

# CREATE
@router.post("/", response_model=DiaryResponse)
def create_diary(
    diary: DiaryCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    new_diary = models.Diary(**diary.dict(), user_id=current_user)
    db.add(new_diary)
    db.commit()
    db.refresh(new_diary)
    return new_diary

# READ (단일)
@router.get("/{diary_id}", response_model=DiaryResponse)
def read_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    diary = db.query(models.Diary).filter(models.Diary.id == diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary

# READ (전체)
@router.get("/", response_model=list[DiaryResponse])
def read_all_diaries(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return db.query(models.Diary).filter(models.Diary.user_id == current_user).all()

# UPDATE
@router.put("/{diary_id}", response_model=DiaryResponse)
def update_diary(
    diary_id: int,
    diary_update: DiaryUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    diary = db.query(models.Diary).filter(models.Diary.id == diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    # ✅ 작성자 본인 확인
    if diary.user_id != current_user:
        raise HTTPException(status_code=403, detail="Permission denied")

    update_data = diary_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(diary, key, value)

    db.commit()
    db.refresh(diary)
    return diary


# DELETE
@router.delete("/{diary_id}")
def delete_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    diary = db.query(models.Diary).filter(models.Diary.id == diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    # ✅ 작성자 본인 확인
    if diary.user_id != current_user:
        raise HTTPException(status_code=403, detail="Permission denied")

    db.delete(diary)
    db.commit()
    return {"message": "Diary deleted"}


