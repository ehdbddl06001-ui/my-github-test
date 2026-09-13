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

## 핸드폰 앱(PWA)으로 쓰기 · Cloudflare Pages

- `docs/` 는 그대로 PWA 다. Android Chrome 에서 열고 메뉴 ▸ **홈 화면에 추가**(또는 화면의 「📲 앱으로 설치」).
  `manifest.webmanifest`·`sw.js`·`pwa.js`·`icons/` 가 그 역할을 한다. 한 번 연 문항·영상은 오프라인에서도 열린다.
- **나만 보기**: GitHub Pages 는 저장소를 비공개로 바꿔도 사이트가 공개로 남는다. 대신 **Cloudflare Pages** 에
  이 저장소를 연결하고(빌드 명령 없음, 출력 디렉터리 `docs`), **Cloudflare Access** 로 로그인을 걸면
  저장소를 비공개로 돌려도 본인만 들어갈 수 있다. 개인 사용 범위에서는 둘 다 무료 플랜이다.
- **오답 동기화**: Cloudflare Pages 에서는 `functions/api/wrong.js` 가 `/api/wrong` 으로 떠서 오답을
  `state/wrong_sync/<exam>.json` 에 커밋한다(환경변수 `GITHUB_TOKEN` 필요 — Contents 쓰기 권한의
  fine-grained PAT, Cloudflare 대시보드에 Secret 으로). 그러면 `wrong-sync.yml` 이 `kmle/오답노트/웹동기화*.md` 를
  자동 생성한다. GitHub Pages 주소에서는 함수가 없어 오답이 기기에만 남는다(내보내기 버튼은 그대로).
- **🩻 영상 덱**: 의대_시험지_제작 아침 루틴이 `opendata medkos-export` 로 옮긴 오픈데이터 영상 문항
  (`content/imaging/`, `docs/assets/imaging/`, 번들 `questions_imaging.js`). 홈 화면 바로가기
  `index.html?exam=imaging&mode=latest` 가 「오늘의 영상」으로 바로 연다.
