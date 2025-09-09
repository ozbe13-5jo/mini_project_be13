#!/bin/bash
# GitHub PR 준비용 스크립트 (Windows Git Bash)

# 설정
REMOTE_URL="https://github.com/ozbe13-5jo/mini_project_be13"
MAIN_BRANCH="main"

# 1️⃣ 현재 브랜치 확인
BRANCH=$(git branch --show-current)
echo "현재 브랜치: $BRANCH"

# 2️⃣ feature 브랜치가 아닌 경우 브랜치 생성 안내
if [[ "$BRANCH" == "$MAIN_BRANCH" ]]; then
  echo "⚠️ 메인 브랜치에 있습니다. 새 feature 브랜치를 만드세요:"
  echo "   git checkout -b feature/브랜치이름"
  exit 1
fi

# 3️⃣ 커밋 없는 경우 임시 커밋
if [ -z "$(git log --oneline)" ] || [ -n "$(git status --porcelain)" ]; then
  echo "커밋 없음 또는 변경 사항 있음 → 임시 커밋 생성"
  git add .
  git commit --allow-empty -m "초기 커밋"
fi

# 4️⃣ 원격 URL 설정
git remote set-url origin $REMOTE_URL
echo "원격 저장소 URL 확인:"
git remote -v

# 5️⃣ 브랜치 원격 푸시
git push --set-upstream origin $BRANCH

# 6️⃣ PR URL 출력
echo "PR 생성 URL:"
echo "https://github.com/ozbe13-5jo/mini_project_be13/compare/$MAIN_BRANCH...$BRANCH?expand=1"
