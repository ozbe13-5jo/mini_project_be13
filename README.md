# 미니 프로젝트 BE13

<img width="1197" height="595" alt="스크린샷 2025-09-08 오후 5 52 31" src="https://github.com/user-attachments/assets/c0a66091-c6ca-44cb-a825-b653f6b792f1" />

## 랜덤 질문 API

자기성찰을 위한 랜덤 질문을 제공하는 기능이 추가되었습니다.

### 구현된 기능

- 랜덤 질문 조회: 매번 다른 자기성찰 질문을 받아볼 수 있습니다
- 모든 질문 조회: 데이터베이스에 저장된 모든 질문을 확인할 수 있습니다
- 질문 개수 확인: 현재 저장된 질문의 총 개수를 확인할 수 있습니다

### API 엔드포인트

- `GET /api/questions/random` - 랜덤 질문 조회
- `GET /api/questions/all` - 모든 질문 조회  
- `GET /api/questions/count` - 질문 개수 조회
- `GET /docs` - Swagger UI 문서 (http://localhost:8000/docs)

### 실행 방법

```bash
# 의존성 설치
pip3 install -r requirements.txt

# 애플리케이션 실행
python3 main.py
```

### API 테스트

```bash
# 랜덤 질문 조회
curl http://localhost:8000/api/questions/random

# 질문 개수 확인
curl http://localhost:8000/api/questions/count
```
