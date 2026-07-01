# 웹 퀴즈 (GitHub Pages)

브라우저에서 **클릭으로 푸는** KMLE 퀴즈입니다. 설치·터미널이 필요 없습니다.

## 배포/접속 방법 (둘 중 하나)

### 방법 1 — 브랜치의 /docs 폴더로 배포 (가장 간단)
1. PR을 `main`에 병합합니다.
2. 저장소 **Settings ▸ Pages ▸ Build and deployment**
   - Source: **Deploy from a branch**
   - Branch: **main** / 폴더: **/docs** 선택 후 Save
3. 잠시 후 `https://<사용자명>.github.io/my-github-test/` 로 접속합니다.

### 방법 2 — GitHub Actions로 자동 배포
1. **Settings ▸ Pages ▸ Source = GitHub Actions** 로 설정합니다.
2. `main`에 `docs/` 변경이 push되면 [`.github/workflows/pages.yml`](../.github/workflows/pages.yml)이 자동 배포합니다.

> 로컬에서 미리 보려면(파일 열기만으로 동작): `docs/index.html`을 브라우저로 열면 됩니다.
> (`questions.js`를 함께 로드하므로 별도 서버 없이도 열립니다.)

## 구성
- `index.html` / `style.css` / `app.js` — 웹 퀴즈 UI·로직 (순수 JS, 의존성 없음)
- `questions.js` — 문항 데이터 번들 (**자동 생성**, 수정 금지)

## 문항을 고치려면
문항 원본은 `kmle/quiz/questions/*.json` 입니다. 수정 후 재생성하세요:
```bash
cd kmle/quiz && python3 quiz.py --export   # docs/questions.js 및 kmle/문항/*.md 갱신
```

## 오답 저장 방식 (중요)
- 웹 퀴즈의 오답은 **브라우저 저장소(localStorage)** 에 기록됩니다(이 기기·브라우저 한정).
- **오답노트 .md / .csv 내보내기** 버튼으로 파일을 받아 저장하거나 repo에 커밋할 수 있습니다.
- repo의 `kmle/오답노트/*.md`에 **파일로 자동 기록**하고 싶으면, 웹 대신 **Codespaces/로컬**에서
  `python3 kmle/quiz/quiz.py`를 사용하세요(정적 웹페이지는 보안상 repo 파일에 직접 쓸 수 없습니다).
