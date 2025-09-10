# 🤝 협업 가이드

## 📋 브랜치 전략

### 브랜치 규칙
- **main**: 프로덕션 브랜치 (절대 직접 수정 금지)
- **develop**: 개발 브랜치 (기능 통합용)
- **feature/기능명**: 새로운 기능 개발용
- **hotfix/수정내용**: 긴급 수정용

### 🚀 작업 시작하기

1. **최신 main 브랜치 가져오기**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **새로운 기능 브랜치 생성**
   ```bash
   git checkout -b feature/새로운기능명
   ```

3. **작업 진행**
   - 브랜치에서만 작업
   - main 브랜치 건드리지 않기

### 🔄 작업 완료 후

1. **변경사항 커밋**
   ```bash
   git add .
   git commit -m "feat: 새로운 기능 추가"
   ```

2. **브랜치 푸시**
   ```bash
   git push origin feature/새로운기능명
   ```

3. **Pull Request 생성**
   - GitHub에서 PR 생성
   - 코드 리뷰 요청

### ⚠️ 충돌 방지 규칙

1. **main 브랜치 보호**
   - main 브랜치에 직접 push 금지
   - 반드시 PR을 통해서만 병합

2. **정기적인 동기화**
   ```bash
   # 작업 중 주기적으로 main과 동기화
   git checkout main
   git pull origin main
   git checkout feature/내브랜치
   git merge main
   ```

3. **작업 전 확인**
   - 작업 시작 전 main 브랜치 최신화
   - 다른 팀원의 작업과 겹치지 않는지 확인

### 📝 커밋 메시지 규칙

```
type: 간단한 설명

- 상세 설명 1
- 상세 설명 2
```

**Type 종류:**
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 스타일 변경
- `refactor`: 코드 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드, 설정 등

### 🔧 충돌 해결

1. **충돌 발생 시**
   ```bash
   git status  # 충돌 파일 확인
   # 충돌 파일 수동 해결
   git add .
   git commit -m "resolve: 충돌 해결"
   ```

2. **복잡한 충돌 시**
   - 팀원과 상의
   - 필요시 브랜치 재생성

### 📞 소통 방법

- 작업 시작 전 팀원에게 알림
- 같은 파일 수정 시 사전 협의
- PR 생성 시 상세한 설명 작성
