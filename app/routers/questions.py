from fastapi import APIRouter, HTTPException
from app.models.models import Question
from app.schemas.schemas import RandomQuestionResponse, QuestionResponse
import random

router = APIRouter()

@router.get("/random", response_model=RandomQuestionResponse)
async def get_random_question():
    """
    랜덤 자기성찰 질문을 제공합니다.
    
    - **question**: 랜덤으로 선택된 질문 정보
    - **message**: 응답 메시지
    """
    try:
        # 모든 질문 조회
        questions = await Question.all()
        
        if not questions:
            raise HTTPException(
                status_code=404, 
                detail="질문이 데이터베이스에 없습니다."
            )
        
        # 랜덤 질문 선택
        random_question = random.choice(questions)
        
        return RandomQuestionResponse(
            question=QuestionResponse(
                id=random_question.id,
                content=random_question.content,
                category=random_question.category,
                created_at=random_question.created_at
            ),
            message="오늘의 자기성찰 질문입니다."
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"질문을 가져오는 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/all", response_model=list[QuestionResponse])
async def get_all_questions():
    """
    모든 자기성찰 질문을 조회합니다.
    
    - **questions**: 모든 질문 목록
    """
    try:
        questions = await Question.all().order_by('id')
        
        return [
            QuestionResponse(
                id=question.id,
                content=question.content,
                category=question.category,
                created_at=question.created_at
            )
            for question in questions
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"질문 목록을 가져오는 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/count")
async def get_questions_count():
    """
    데이터베이스에 저장된 질문의 총 개수를 반환합니다.
    
    - **count**: 질문 개수
    """
    try:
        count = await Question.all().count()
        
        return {
            "count": count,
            "message": f"총 {count}개의 질문이 있습니다."
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"질문 개수를 가져오는 중 오류가 발생했습니다: {str(e)}"
        )
