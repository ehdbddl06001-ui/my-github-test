// 자동 생성 파일 — 수정하지 마세요.
// 원본: content/anatomy/**/*.md → `python pipelines/export_anatomy_web.py`
window.MEDKOS_ANATOMY = {
 "generated": "2026-08-14",
 "deadlines": {
  "tagging1": "2026-09-10",
  "tagging2": "2026-10-19",
  "end": "2026-10-19"
 },
 "schedule": [
  {
   "date": "2026-08-18",
   "topics": [
    "orientation",
    "위령전례",
    "등·다리 피부벗기기"
   ],
   "regions": [
    "back",
    "lower-limb"
   ],
   "exam": null
  },
  {
   "date": "2026-08-20",
   "topics": [
    "등 얕은층·중간층·깊은층 근육",
    "볼기부위·넓적다리 뒤부분"
   ],
   "regions": [
    "back",
    "lower-limb"
   ],
   "exam": null
  },
  {
   "date": "2026-08-24",
   "topics": [
    "뒤통수밑삼각",
    "어깨뼈부위",
    "다리오금·종아리 뒤부위"
   ],
   "regions": [
    "back",
    "lower-limb"
   ],
   "exam": null
  },
  {
   "date": "2026-08-27",
   "topics": [
    "큰가슴근부위",
    "가슴벽",
    "얼굴·표정근육·귀밑샘·얼굴 신경/혈관·씹기근육·입술·바깥코·바깥귀"
   ],
   "regions": [
    "thorax",
    "head"
   ],
   "exam": null
  },
  {
   "date": "2026-08-31",
   "topics": [
    "가슴벽·가슴안·가슴막·위세로칸·심장막·심장",
    "관자부위·관자아래부위"
   ],
   "regions": [
    "thorax",
    "head"
   ],
   "exam": null
  },
  {
   "date": "2026-09-03",
   "topics": [
    "목의 삼각·목의 내장",
    "다리 얕은층·넓적다리 앞/안쪽칸·종아리 앞·발등"
   ],
   "regions": [
    "neck",
    "lower-limb"
   ],
   "exam": null
  },
  {
   "date": "2026-09-07",
   "topics": [
    "목의 뿌리·인두",
    "종아리 가쪽·발목 안쪽면·발바닥"
   ],
   "regions": [
    "neck",
    "lower-limb"
   ],
   "exam": null
  },
  {
   "date": "2026-09-10",
   "topics": [
    "Tagging 1"
   ],
   "regions": [],
   "exam": "tagging-1"
  },
  {
   "date": "2026-09-14",
   "topics": [
    "피드백",
    "팔 얕은근막·겨드랑",
    "기관·기관지·허파·뒤세로칸"
   ],
   "regions": [
    "upper-limb",
    "thorax"
   ],
   "exam": null
  },
  {
   "date": "2026-09-17",
   "topics": [
    "위팔 앞칸·팔오금·아래팔 앞칸·손바닥",
    "배벽·얕은근막·배근육·고샅관·정삭·음낭·고환"
   ],
   "regions": [
    "upper-limb",
    "abdomen"
   ],
   "exam": null
  },
  {
   "date": "2026-09-21",
   "topics": [
    "위팔 뒤칸·아래팔 뒤칸·손등",
    "복막·위·지라·간·작은창자·큰창자·샘창자·이자"
   ],
   "regions": [
    "upper-limb",
    "abdomen"
   ],
   "exam": null
  },
  {
   "date": "2026-09-28",
   "topics": [
    "척주·척수막",
    "샅·항문삼각·비뇨생식삼각·남녀 바깥생식기관"
   ],
   "regions": [
    "back",
    "pelvis-perineum"
   ],
   "exam": null
  },
  {
   "date": "2026-10-01",
   "topics": [
    "머리덮개·머리뼈 속구조·뇌 적출·눈확",
    "부신·콩팥·배대동맥·복막·가로막·뒤배벽"
   ],
   "regions": [
    "head",
    "abdomen"
   ],
   "exam": null
  },
  {
   "date": "2026-10-06",
   "topics": [
    "팔의 관절",
    "골반 복막·골반 절단·남녀 내부생식기관·골반가로막"
   ],
   "regions": [
    "upper-limb",
    "pelvis-perineum"
   ],
   "exam": null
  },
  {
   "date": "2026-10-08",
   "topics": [
    "머리 시상절단·입안·후두",
    "인두·후두",
    "다리의 관절"
   ],
   "regions": [
    "head",
    "neck",
    "lower-limb"
   ],
   "exam": null
  },
  {
   "date": "2026-10-19",
   "topics": [
    "Tagging 2"
   ],
   "regions": [],
   "exam": "tagging-2"
  }
 ],
 "concepts": [
  {
   "id": "anatomy-2026-0029",
   "title": "등 근육 3층과 지배신경 규칙",
   "region": "back",
   "subregion": "superficial-back",
   "layer": "superficial",
   "conceptStyle": "layer-order",
   "relations": [
    "covers",
    "adjacent-to"
   ],
   "structureClasses": [
    "muscle",
    "nerve"
   ],
   "examPhase": "tagging-1",
   "confidence": "high",
   "classificationConfidence": null,
   "tree": null,
   "image": "assets/anatomy/diag-back-layers-labeled.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "얕은층 근육 — 등세모근·넓은등근·마름근"
    }
   ],
   "body": "## 층 순서 — 얕은층 → 중간층 → 깊은층\n\n도해: `docs/assets/anatomy/diag-back-layers-labeled.svg` (퀴즈판 `…-quiz.svg`, 문항 `anatomy-2026-0027`)\n\n| 층 | 근육 | 지배신경 | 기능 축 |\n|---|---|---|---|\n| 얕은층 ① | 등세모근 trapezius | **더부신경(XI)** (+C3·4 고유감각) | 팔이음뼈 운동 |\n| 얕은층 ① | 넓은등근 latissimus dorsi | 가슴등신경 C6–8 | 어깨 폄·모음·안쪽돌림 |\n| 얕은층 ② | 어깨올림근·작은/큰마름근 | 등쪽어깨신경 C5 | 어깨뼈 올림·뒤당김 |\n| 중간층 | 위뒤톱니근 serratus post. superior | 갈비사이신경 | 갈비뼈 올림(들숨) |\n| 중간층 | 아래뒤톱니근 serratus post. inferior | 갈비사이신경 | 갈비뼈 내림(날숨) |\n| 깊은층 | 척주세움근(엉덩갈비-가장긴-가시) | **척수신경 뒤가지** | 척주 폄 |\n| 깊은층 | 가로돌기가시근육(반가시-뭇갈래-돌림) | **뒤가지** | 분절 돌림·안정화 |\n\n## 왜 이런 규칙인가 (외우지 말고 이해)\n\n얕은·중간층은 배아기에 **팔이음뼈·갈비 쪽에서 등으로 이주해 온** 근육이라 원래 살던\n동네의 신경(척수신경 **앞가지**)을 그대로 데리고 왔다. 깊은층만 처음부터 등에서\n만들어진 **고유등근육**이라 **뒤가지** 지배를 받는다. 그래서 태깅에서 신경을 물으면\n\"이 근육이 몇 층이냐\"를 먼저 판단하면 된다.\n\n예외는 **등세모근** 하나 — 얕은층이지만 운동지배가 더부신경(XI)이다(목빗근과 한 짝으로\n인두굽이 유래). C3·4는 고유감각만 보낸다.\n\n## 척주세움근 3기둥 — 가쪽에서 안쪽으로\n\n```\n가쪽 ──────────────────────────── 안쪽\n엉덩갈비근      가장긴근        가시근\niliocostalis    longissimus     spinalis\n(갈비뼈각)      (가로돌기·꼭지)  (가시돌기)\n```\n\n그 아래 더 깊은 층이 가로돌기가시근육: **반가시근**(4–6분절 건너뜀) → **뭇갈래근**\n(2–4분절, 허리에서 최대) → **돌림근**(1–2분절, 가슴에서 발달). 건너뛰는 분절 수가\n줄수록 깊다.\n\n## 임상 삼각 (도해에 노란 점선)\n\n- **청진삼각** triangle of auscultation — 등세모근 가쪽모서리 · 넓은등근 위모서리 ·\n  큰마름근(또는 어깨뼈 안쪽모서리). 근육이 얇아 허파 청진이 잘 된다.\n- **허리삼각(Petit)** lumbar triangle — 엉덩뼈능선 · 넓은등근 앞모서리 · 배바깥빗근\n  뒤모서리. 허리탈장 호발 부위."
  },
  {
   "id": "anatomy-2026-0030",
   "title": "큰궁둥구멍 통과 구조물과 볼기부위 혈관·신경 분지",
   "region": "lower-limb",
   "subregion": "gluteal",
   "layer": "",
   "conceptStyle": "branch-tree",
   "relations": [
    "passes-through",
    "branches-from",
    "adjacent-to"
   ],
   "structureClasses": [
    "muscle",
    "nerve",
    "artery"
   ],
   "examPhase": "tagging-1",
   "confidence": "high",
   "classificationConfidence": null,
   "tree": null,
   "image": "assets/anatomy/diag-gluteal-foramina-labeled.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "볼기부위 — 궁둥구멍근과 통과 구조물"
    }
   ],
   "body": "## 기준은 궁둥구멍근 하나\n\n도해: `docs/assets/anatomy/diag-gluteal-foramina-labeled.svg` (퀴즈판 `…-quiz.svg`, 문항 `anatomy-2026-0028`)\n\n궁둥구멍근 piriformis 이 큰궁둥구멍을 가로지르며 위·아래로 나눈다. 볼기부위 문제는\n거의 전부 \"이 구조가 궁둥구멍근 위냐 아래냐\"로 환원된다.\n\n```\n큰궁둥구멍 greater sciatic foramen\n├─ 위구멍 suprapiriform  : 위볼기동맥 · 위볼기정맥 · 위볼기신경 ← 이 셋뿐\n└─ 아래구멍 infrapiriform : 아래볼기 동맥·정맥·신경\n                            궁둥신경 (가장 가쪽, 가장 굵다)\n                            뒤넙다리피부신경\n                            음부신경 + 속음부동맥\n                              └→ 궁둥뼈가시 뒤를 감아 작은궁둥구멍으로 재진입\n```\n\n## 혈관 분지 — 어디서 갈라지나\n\n```\n속엉덩동맥 internal iliac a.\n├─ 뒤갈래 posterior division ─→ 위볼기동맥 superior gluteal a.\n└─ 앞갈래 anterior division  ─┬→ 아래볼기동맥 inferior gluteal a.\n                              └→ 속음부동맥 internal pudendal a.\n```\n\n외우는 법: **위는 뒤갈래, 아래·음부는 앞갈래.**\n\n## 신경 — 무엇을 지배하나\n\n| 신경 | 나오는 곳 | 지배 |\n|---|---|---|\n| 위볼기신경 superior gluteal n. | 위구멍 | 중간볼기근·작은볼기근·넙다리근막긴장근 |\n| 아래볼기신경 inferior gluteal n. | 아래구멍 | 큰볼기근 **단독** |\n| 궁둥신경 sciatic n. (L4–S3) | 아래구멍 | 햄스트링 → 다리오금에서 정강/온종아리신경 분지 |\n| 뒤넙다리피부신경 | 아래구멍 | 넓적다리 뒤 피부(감각) |\n| 음부신경 pudendal n. (S2–4) | 아래구멍 → 재진입 | 회음 |\n\n## 임상 — 태깅·구술 단골\n\n- **Trendelenburg 징후**: 위볼기신경 손상 → 중간·작은볼기근 마비 → 한발 서기에서\n  **반대쪽** 골반이 처진다(보상 = 몸통을 환측으로 기울임).\n- **근육주사 안전구역**: 볼기 **위가쪽 1/4**(또는 von Hochstetter 부위) — 궁둥신경과\n  볼기신경을 피한다.\n- **궁둥신경 표면 표지**: 궁둥뼈결절과 큰돌기의 **중간점** 심부.\n- **변이**: 궁둥신경이 궁둥구멍근을 뚫고 지나는 변이가 흔하며, 궁둥구멍근증후군의\n  해부학적 근거가 된다."
  },
  {
   "id": "anatomy-2026-0001",
   "title": "속엉덩동맥 분지 트리",
   "region": "pelvis-perineum",
   "subregion": "pelvic-cavity",
   "layer": "",
   "conceptStyle": "branch-tree",
   "relations": [
    "branches-from",
    "ends-at"
   ],
   "structureClasses": [
    "artery"
   ],
   "examPhase": "tagging-2",
   "confidence": "medium",
   "classificationConfidence": null,
   "tree": {
    "name": "속엉덩동맥 (internal iliac artery)",
    "children": [
     {
      "name": "배꼽동맥 (umbilical artery)",
      "children": [
       {
        "name": "위방광동맥 (superior vesical artery) — 방광 위부분"
       }
      ]
     },
     {
      "name": "아래방광동맥 (inferior vesical artery) — 방광 아랫부분·전립샘 (중간곧창자동맥과 한 줄기로 나오기도)"
     },
     {
      "name": "중간곧창자동맥 (middle rectal artery) — 위·아래곧창자동맥과 연결"
     },
     {
      "name": "엉덩허리동맥 (iliolumbar artery) — 벽가지, 위골반문 가로질러 위가쪽",
      "children": [
       {
        "name": "엉덩근가지 (iliacus branch)"
       },
       {
        "name": "허리가지 (lumbar branch) — 큰허리근·허리네모근"
       }
      ]
     },
     {
      "name": "가쪽엉치동맥 (lateral sacral artery) — 엉치뼈 앞면, 보통 2개 ★tagging 답 후보"
     },
     {
      "name": "위볼기동맥 (superior gluteal artery) — 큰궁둥구멍 윗부분으로 나감"
     },
     {
      "name": "아래볼기동맥 (inferior gluteal artery) — 큰궁둥구멍 아랫부분으로 나감"
     },
     {
      "name": "속음부동맥 (internal pudendal artery) — 궁둥뼈가시 바로 위, 큰궁둥구멍 아랫부분"
     },
     {
      "name": "폐쇄동맥 (obturator artery) — 폐쇄신경과 함께 폐쇄관으로 ★tagging 답 후보"
     }
    ]
   },
   "image": "assets/anatomy/diag-internal-iliac-labeled.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "속엉덩동맥"
    },
    {
     "file": "tagging 2차.pdf",
     "page": null,
     "section": "골반 Pelvis [동맥]"
    }
   ],
   "body": "## 속엉덩동맥 분지 — 트리로 외우기\n\n온엉덩동맥에서 일어나 아래로 달려 골반안으로 들어간다(강의 14차시 실측 확인).\n낱말이 아니라 **어디로 빠져나가는가**로 묶는 것이 태깅 대비 핵심이다.\n\n- **앞쪽(내장 방향)**: 배꼽동맥→위방광동맥 · 아래방광동맥 · 중간곧창자동맥\n- **뒤·벽쪽**: 엉덩허리동맥(엉덩근/허리 가지) · 가쪽엉치동맥\n- **큰궁둥구멍으로 나가는 셋**: 위볼기동맥(윗부분) / 아래볼기동맥·속음부동맥(아랫부분)\n- **폐쇄관으로**: 폐쇄동맥(폐쇄신경 아래쪽 동행)\n\n혼동 주의: **위곧창자동맥은 속엉덩동맥의 가지가 아니라 아래창자간막동맥의\n가지**다(강의 항문관 절에서 명시) — 중간곧창자동맥과 문합한다.\n\n## 관계 문장(말로 설명하기)\n\n1. 폐쇄신경·동맥·정맥은 함께 폐쇄관으로 들어간다(신경이 위).\n2. 속음부동맥은 궁둥뼈가시 바로 위에서 큰궁둥구멍 아랫부분으로 골반을 빠져나간다.\n3. 요관은 속엉덩동맥 **앞**에서 아래앞쪽으로 달린다(수술·태깅 표지 관계)."
  },
  {
   "id": "anatomy-2026-0003",
   "title": "골반가로막의 구성 — 안에서 가쪽으로",
   "region": "pelvis-perineum",
   "subregion": "pelvic-diaphragm",
   "layer": "",
   "conceptStyle": "layer-order",
   "relations": [
    "adjacent-to",
    "covers"
   ],
   "structureClasses": [
    "muscle",
    "fascia"
   ],
   "examPhase": "tagging-2",
   "confidence": "medium",
   "classificationConfidence": null,
   "tree": null,
   "image": "assets/anatomy/diag-pelvic-diaphragm-labeled.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "골반가로막"
    },
    {
     "file": "tagging 2차.pdf",
     "page": null,
     "section": "골반 [골반가로막]"
    }
   ],
   "body": "## 골반가로막 = 항문올림근 + 꼬리근 (+ 근막)\n\n**항문올림근(levator ani) ★tagging 답 후보** 를 앞안쪽→가쪽 순서로:\n\n1. **두덩곧창자근 (puborectalis)** — 가장 앞·안쪽. 두덩뼈몸통에서 일어나 항문관을\n   감싸고 뒤에서 양쪽이 연결. 양쪽 사이 틈새 = **비뇨생식구멍**(요도·질 통과)\n2. **두덩꼬리근 (pubococcygeus)** — 두덩곧창자근 바로 가쪽. 두덩뼈몸통 → 꼬리뼈\n3. **엉덩꼬리근 (iliococcygeus)** — 가장 가쪽. **항문올림근힘줄활**에서 일어나 꼬리뼈로\n4. **꼬리근 (coccygeus)** — 항문올림근보다 가쪽. 궁둥뼈가시 → 꼬리뼈·엉치뼈\n\n기준 구조물:\n\n- **항문올림근힘줄활** — 속폐쇄근막이 선 모양으로 두꺼워진 것. 궁둥뼈가시 →\n  폐쇄관까지 거의 수평\n- 전체 배열은 수평이 아니라 **가쪽벽에서 아래안쪽으로**(움푹한 그릇 모양) —\n  그 아래면이 **궁둥항문오목의 안쪽벽**이 된다\n\n## 관계 문장(말로 설명하기)\n\n1. 곧창자는 골반가로막을 뚫으며 항문곧창자연결이 그 높이에 있다.\n2. 속폐쇄근(가쪽벽) → 속폐쇄근막 → 힘줄활 → 항문올림근 기시의 층 순서.\n3. 궁둥구멍근은 골반가로막이 아니라 엉치뼈 앞면에서 일어나 볼기로 나간다(혼동 주의)."
  },
  {
   "id": "anatomy-2026-0002",
   "title": "돌림근띠와 어깨관절 안정화 구조물",
   "region": "upper-limb",
   "subregion": "shoulder",
   "layer": "",
   "conceptStyle": "relation",
   "relations": [
    "covers",
    "adjacent-to"
   ],
   "structureClasses": [
    "muscle",
    "ligament",
    "joint"
   ],
   "examPhase": "tagging-2",
   "confidence": "medium",
   "classificationConfidence": null,
   "tree": null,
   "image": null,
   "imageOrigin": null,
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "어깨관절"
    }
   ],
   "body": "## 어깨관절을 안정화하는 구조물 (실습 응용과제 1번 그대로)\n\n**돌림근띠(rotator cuff)** — 힘줄이 관절주머니에 단단히 붙어 안정성을 만든다:\n\n| 근육 | 관절주머니에서의 위치 |\n|---|---|\n| 어깨밑근 (subscapularis) | **앞** |\n| 가시위근 (supraspinatus) | 위 |\n| 가시아래근 (infraspinatus) | 뒤위 |\n| 작은원근 (teres minor) | 뒤아래 |\n\n보조 구조물:\n\n- **접시테두리(glenoid labrum)** — 접시오목의 깊이를 깊게 함\n- **접시위팔인대(glenohumeral ligament)** — 관절주머니 앞부분이 두꺼워진 띠.\n  겉보다 **관절주머니 속에서** 더 잘 보인다(위·중간·아래 구분)\n- **부리위팔인대(coracohumeral ligament)** — 부리돌기 가쪽모서리 → 위팔뼈 큰결절\n- **위팔두갈래근 긴갈래** — 위팔가로인대 깊은쪽 결절사이고랑을 지난다\n\n## 관계 문장(말로 설명하기)\n\n1. 어깨밑근은 관절주머니 **앞**을 덮고, 어깨밑근힘줄밑주머니는 관절주머니\n   섬유막구멍과 연결된다.\n2. 관절주머니 섬유막은 안쪽으로 접시오목 모서리, 가쪽으로 위팔뼈 **해부목**에 붙는다.\n3. 부리빗장인대(마름인대 가쪽 + 원뿔인대 안쪽)는 봉우리빗장관절을 간접 지지한다."
  },
  {
   "id": "anatomy-2026-0032",
   "title": "어깨뼈부위 3공간 — 경계·내용물·어깨동맥그물",
   "region": "upper-limb",
   "subregion": "scapular-region",
   "layer": "",
   "conceptStyle": "relation",
   "relations": [
    "passes-through",
    "adjacent-to",
    "branches-from"
   ],
   "structureClasses": [
    "muscle",
    "nerve",
    "artery"
   ],
   "examPhase": "tagging-1",
   "confidence": "high",
   "classificationConfidence": null,
   "tree": null,
   "image": "assets/anatomy/diag-scapular-spaces-labeled.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "어깨뼈부위 — 3공간과 통과 구조물"
    }
   ],
   "body": "## 기준은 위팔세갈래근 긴갈래 하나\n\n도해: `docs/assets/anatomy/diag-scapular-spaces-labeled.svg` (퀴즈판 `…-quiz.svg`, 문항 `anatomy-2026-0031`)\n\n위·아래 경계는 세 공간이 사실상 공유한다(위 작은원근 / 아래 큰원근). 실제로 공간을\n가르는 것은 **위팔세갈래근 긴갈래**라는 세로 기둥이다.\n\n```\n            작은원근 teres minor\n   ┌──────────────┬──────────────┐\n   │   세모공간    │   네모공간    │\n   │ (긴갈래 안쪽) │ (긴갈래 가쪽) │\n   └──────────────┴──────────────┘\n            큰원근 teres major\n        ┌──────────────┐\n        │   세모간격    │\n        └──────────────┘\n      ↑ 세로 기둥 = 위팔세갈래근 긴갈래\n```\n\n## 경계와 내용물\n\n| 공간 | 경계 | 내용물 |\n|---|---|---|\n| **네모공간** quadrangular space | 위 작은원근 · 아래 큰원근 · 안쪽 긴갈래 · 가쪽 **위팔뼈 외과목** | **겨드랑신경** + 뒤위팔휘돌이동맥 |\n| **세모공간** triangular space | 위 작은원근 · 아래 큰원근 · 가쪽 긴갈래 | **어깨휘돌이동맥** |\n| **세모간격** triangular interval | 위 큰원근 · 안쪽 긴갈래 · 가쪽 위팔뼈 | **노신경** + 깊은위팔동맥 |\n\n외우는 법: 긴갈래 **가쪽 = 네모(신경)**, **안쪽 = 세모(동맥)**, 큰원근 **아래 = 세모간격**.\n\n## 어깨동맥그물 (scapular anastomosis)\n\n```\n빗장밑동맥 subclavian a.\n├─ 갑상목동맥 → 어깨위동맥 suprascapular a.\n└─ 등쪽어깨동맥 dorsal scapular a.\n        ↕  (문합)\n겨드랑동맥 → 어깨밑동맥 → 어깨휘돌이동맥 circumflex scapular a.  ← 세모공간 통과\n```\n\n겨드랑동맥 근위를 결찰해도 팔이 사는 이유. 어깨위신경·동맥과 위가로어깨인대의 관계는\n**\"Army over the bridge, Navy under\"** — 동맥은 인대 위, 신경은 어깨패임 속(인대 아래).\n\n## 임상\n\n- **위팔뼈 외과목 골절** → 네모공간의 **겨드랑신경** 손상 → 어깨세모근 마비 +\n  어깨 가쪽(견장 부위) 감각소실. 어깨 벌림 15–90°가 안 된다.\n- **노신경**은 세모간격을 지나 위팔뼈 뒤면의 노신경고랑으로 들어간다 → 위팔뼈 몸통\n  중간 골절에서 손목처짐(wrist drop).\n- 돌림근띠(SITS)는 가시위근·가시아래근·작은원근·어깨밑근 — **큰원근은 돌림근띠가 아니다**."
  }
 ],
 "questions": [
  {
   "id": "anatomy-2026-0015",
   "style": "spotter",
   "region": "back",
   "subregion": "gluteal-region",
   "examPhase": "tagging-1",
   "stem": "큰볼기근을 젖힌 볼기 부위 해부 사진에서, 포셉이 잡고 있으며 번호핀 ①이 가리키는 혈관의 이름을 말하시오.",
   "choices": null,
   "answer": "위볼기동맥 (superior gluteal artery)",
   "explanation": "위볼기동맥은 속엉덩동맥 뒤갈래의 가지로, 큰궁둥구멍 윗부분(궁둥구멍근 위)으로 골반을 빠져나와 볼기 부위에 분포한다. 원본 영상 라벨에서 답이 실측 확인됨. 이미지는 학생 필기(빨간 별표·지시선·'큰볼기근'·YYY)를 주변 배경 기반 inpainting으로 제거하고 영상 라벨만 자연 패치로 가린 복원본이다.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "볼기부위 큰볼기근 (업로드 스캔 pf2 p1)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0016",
   "style": "spotter",
   "region": "back",
   "subregion": "superficial-back",
   "examPhase": "tagging-1",
   "stem": "등 얕은층 해부 사진에서 ▲ 포인터가 가리키며 번호핀 ①이 지시하는, 뒤통수뼈융기·목덜미인대·C7–T12 가시돌기에서 일어나는 얕은층 근육의 이름을 말하시오.",
   "choices": null,
   "answer": "등세모근 (trapezius muscle)",
   "explanation": "등세모근은 등 얕은층의 가장 표면 근육으로 위·중간·아래섬유로 나뉘며 빗장뼈 가쪽 1/3·봉우리(acromion)·어깨뼈가시에 닿는다. 원본 영상 라벨에서 답이 실측 확인됨. 이미지는 학생 필기(위/중간/아래, 목덜미인대, C1–T12, acromion, 세로 측정선, 파란 형광 윤곽 트레이스, 빨간 지시선, YYY)를 색 검출 + 주변 기반 inpainting으로 제거하고, 정답을 노출하는 영상 타이틀·라벨은 자연 패치로 가린 복원본이다.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "얕은층 근육 등세모근 (업로드 스캔 pf1 p1)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0017",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "popliteal-fossa",
   "examPhase": "tagging-1",
   "stem": "넓적다리 뒤쪽에서 종아리로 이어지는 해부 사진에서, 번호핀 ①(▲)이 가리키는 — 넙다리동맥이 다리오금으로 들어오면서 이름이 바뀐 — 혈관의 이름을 말하시오.",
   "choices": null,
   "answer": "오금동맥 (popliteal artery)",
   "explanation": "넙다리동맥은 모음근구멍(adductor hiatus)을 지나 다리오금으로 들어오면서 오금동맥이 된다. 오금동맥은 무릎동맥 5가지(위가쪽·위안쪽·아래가쪽·아래안쪽·중간무릎동맥)를 낸다. 원본 영상 라벨에서 답 실측 확인. 이미지는 필기 제거 후 donor/점진 인페인팅 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "다리오금의 혈관 (업로드 스캔 5183 p1)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0018",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "popliteal-fossa",
   "examPhase": "tagging-1",
   "stem": "다리오금 해부 사진에서, 궁둥신경이 갈라진 두 가지 중 번호핀 ①(▲)이 가리키는 — 넙다리두갈래근 안쪽 모서리를 따라 가쪽으로 달리는 — 신경의 이름을 말하시오.",
   "choices": null,
   "answer": "온종아리신경 (common fibular nerve)",
   "explanation": "궁둥신경은 다리오금 위에서 정강신경과 온종아리신경으로 갈라진다. 온종아리신경은 넙다리두갈래근 힘줄 안쪽을 따라 가쪽으로 내려가 종아리뼈머리를 감아돈다. 깊이 관계(가장 얕음: 정강신경 → 오금정맥 → 가장 깊음: 오금동맥)도 함께 기억. 원본 영상 라벨 실측 확인. 이미지는 필기 제거 후 donor/점진 인페인팅 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "다리오금의 신경 (업로드 스캔 5183 p8)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0019",
   "style": "spotter",
   "region": "back",
   "subregion": "suboccipital",
   "examPhase": "tagging-1",
   "stem": "뒤통수 부위 피부벗기기 사진에서, 번호핀 ①(▲)이 가리키는 — 뒤통수를 향해 올라가는 구불구불한 동맥과 동행하는 — 피부신경의 이름을 말하시오.",
   "choices": null,
   "answer": "큰뒤통수신경 (greater occipital nerve)",
   "explanation": "큰뒤통수신경은 둘째목신경(C2) 뒤가지의 안쪽가지로, 뒤통수동맥과 동행하며 뒤통수 피부에 분포한다. 원본 영상 라벨 실측 확인. 이미지는 필기 제거 후 donor/점진 인페인팅 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "표면해부와 피부벗기기 — 피부신경 (업로드 스캔 0150 p3)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0020",
   "style": "spotter",
   "region": "back",
   "subregion": "suboccipital-triangle",
   "examPhase": "tagging-1",
   "stem": "뒤통수밑삼각 해부 사진에서, 번호핀 ①(▲)이 가리키는 — 뒤통수밑삼각의 위안쪽 경계를 이루는 — 근육의 이름을 말하시오.",
   "choices": null,
   "answer": "큰뒤머리곧은근 (rectus capitis posterior major muscle)",
   "explanation": "뒤통수밑삼각의 경계: 위안쪽 큰뒤머리곧은근, 위가쪽 위머리빗근, 아래가쪽 아래머리빗근. 삼각 안에 척추동맥과 뒤통수밑신경(C1 뒤가지)이 지난다. 원본 영상 라벨 실측 확인. 이미지는 필기 제거 후 donor/점진 인페인팅 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "뒤통수밑삼각 (업로드 스캔 0150 p9)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0023",
   "style": "spotter",
   "region": "back",
   "subregion": "superficial-back",
   "examPhase": "tagging-1",
   "stem": "등 얕은층 해부 사진에서, 등세모근을 젖힌 뒤 그 아래로 드러난 — 번호핀 ①(▲)이 가리키는 — 근육의 이름을 말하시오.",
   "choices": null,
   "answer": "마름근 (rhomboid muscle)",
   "explanation": "등세모근을 젖히면 어깨뼈 안쪽모서리로 비스듬히 달리는 마름근(작은마름근: 목덜미인대·C7–T1 가시돌기 → 어깨뼈가시 안쪽 끝 높이 / 큰마름근: T2–5 가시돌기 → 어깨뼈 안쪽모서리)이 나온다. 지배신경은 둘 다 등쪽어깨신경(C5)이며 작용은 어깨뼈 뒤당김·아래쪽돌림. 위쪽에 이어지는 어깨올림근과 헷갈리지 말 것(어깨올림근은 C1–4 가로돌기에서 어깨뼈 위각). 원본 영상 라벨 실측 확인. 이미지는 필기(빨간 펜 주석)를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "얕은층 근육 — 등세모근 젖힌 뒤 마름근 (업로드 스캔 pf1 p2)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0024",
   "style": "spotter",
   "region": "back",
   "subregion": "superficial-back",
   "examPhase": "tagging-1",
   "stem": "넓은등근을 젖히고 그 속면(deep surface)을 관찰하는 사진에서, 번호핀 ①(▲)이 가리키는 — 같은 이름의 신경과 나란히 이 근육으로 들어가는 — 동맥의 이름을 말하시오.",
   "choices": null,
   "answer": "가슴등동맥 (thoracodorsal artery)",
   "explanation": "가슴등동맥은 어깨밑동맥(subscapular a.)의 종말가지로, 같은 이름의 가슴등신경(C6–8, 뒤신경다발)과 함께 넓은등근 속면으로 들어가 이 근육을 먹여살린다. 어깨밑동맥은 겨드랑동맥 3부의 가지이며 어깨휘돌이동맥(circumflex scapular a.)과 가슴등동맥으로 갈린다. 임상: 넓은등근 피판(latissimus dorsi flap) 이식의 혈관줄기가 바로 이 가슴등동맥이라, 유방재건·수부재건에서 반드시 보존한다. 원본 영상 라벨 실측 확인. 이미지는 필기(여백 빨간 펜·조직 위 파란 펜)를 제거하고 영상 프레임만 남긴 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "얕은층 근육 — 넓은등근의 혈관·신경 (업로드 스캔 pf1 p8)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0025",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "popliteal-fossa",
   "examPhase": "tagging-1",
   "stem": "다리오금 해부 사진에서, 오금동맥이 무릎관절 둘레로 내는 5개의 가지 중 번호핀 ①(▲)이 가리키는 — 넙다리뼈 가쪽관절융기 위를 돌아 나가는 — 동맥의 이름을 말하시오.",
   "choices": null,
   "answer": "위가쪽무릎동맥 (lateral superior genicular artery)",
   "explanation": "오금동맥은 무릎동맥그물(genicular anastomosis)을 이루는 5가지를 낸다: 위가쪽·위안쪽·중간·아래가쪽·아래안쪽무릎동맥. 위가쪽무릎동맥은 넙다리뼈 가쪽관절융기 바로 위를 감아 앞쪽으로 돌아간다. 중간무릎동맥만 관절주머니를 뚫고 들어가 십자인대에 분포한다는 점이 구분 포인트. 이 그물은 넙다리동맥이 모음근구멍 부위에서 막혔을 때 측부순환이 된다. 원본 영상 라벨 실측 확인. 이미지는 필기(흰 펜 주석)를 제거하고 영상 프레임만 남긴 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "다리오금의 혈관 — 무릎동맥 5가지 (업로드 스캔 5183 p2)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0027",
   "style": "spotter",
   "region": "back",
   "subregion": "superficial-back",
   "examPhase": "tagging-1",
   "stem": "등 근육 3층 도해에서 번호핀 ①~⑦이 가리키는 근육의 이름(한·영)과 각각의 지배신경을 말하시오. 왼쪽 패널부터 얕은층 → 중간층 → 깊은층이다.",
   "choices": null,
   "answer": "① 등세모근 trapezius — 더부신경(XI) / ② 넓은등근 latissimus dorsi — 가슴등신경(C6–8) / ③ 위뒤톱니근 serratus posterior superior — 갈비사이신경 / ④ 아래뒤톱니근 serratus posterior inferior — 갈비사이신경 / ⑤ 엉덩갈비근 iliocostalis — 척수신경 뒤가지 / ⑥ 가장긴근 longissimus — 뒤가지 / ⑦ 가시근 spinalis — 뒤가지",
   "explanation": "층을 먼저 판단하면 신경이 따라온다. 얕은·중간층은 배아기에 팔이음뼈·갈비 쪽에서 등으로 이주해 온 근육이라 척수신경 **앞가지**를 데리고 왔고(등세모근만 예외적으로 더부신경 XI 운동지배, C3·4는 고유감각), 깊은층 고유등근육만 처음부터 등에서 만들어져 **뒤가지** 지배를 받는다. ⑤⑥⑦은 척주세움근 3기둥으로 가쪽→안쪽 순서가 엉덩갈비-가장긴-가시다(엉·가·가로 외우기). 중간층 두 근육은 호흡 보조 — 위뒤톱니근이 갈비뼈를 올려 들숨, 아래뒤톱니근이 내려 날숨. 도해는 자체 제작(claude-drawn-svg)이라 공개 가능하며, 라벨판은 diag-back-layers-labeled.svg.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": "assets/anatomy/diag-back-layers-quiz.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "얕은층 근육 — 등세모근·넓은등근·마름근"
    }
   ]
  },
  {
   "id": "anatomy-2026-0028",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "gluteal",
   "examPhase": "tagging-1",
   "stem": "오른쪽 볼기를 뒤에서 본 도해에서 번호핀 ①~⑦의 이름(한·영)을 말하고, 각각 궁둥구멍근의 위구멍(suprapiriform)과 아래구멍(infrapiriform) 중 어디로 나오는지 답하시오.",
   "choices": null,
   "answer": "① 궁둥구멍근 piriformis (구멍을 위·아래로 나누는 기준) / ② 위볼기동맥 superior gluteal a. — 위구멍 / ③ 위볼기신경 superior gluteal n. — 위구멍 / ④ 아래볼기동맥 inferior gluteal a. — 아래구멍 / ⑤ 궁둥신경 sciatic n. — 아래구멍(가장 가쪽·가장 굵다) / ⑥ 뒤넙다리피부신경 posterior femoral cutaneous n. — 아래구멍 / ⑦ 음부신경 pudendal n. + 속음부동맥 internal pudendal a. — 아래구멍으로 나왔다가 궁둥뼈가시 뒤를 감아 작은궁둥구멍으로 재진입",
   "explanation": "외우는 핵심은 '위구멍으로는 위볼기 동맥·정맥·신경 셋만 나오고 나머지는 전부 아래구멍'이다. 혈관 계보는 둘 다 속엉덩동맥 가지지만 위볼기동맥은 **뒤갈래**, 아래볼기동맥·속음부동맥은 **앞갈래**에서 나온다. 임상: 위볼기신경 손상 → 중간·작은볼기근 마비 → 한발 서기에서 **반대쪽** 골반이 처지는 Trendelenburg 징후, 그래서 근육주사는 볼기 위가쪽 1/4에 놓아 궁둥신경을 피한다. 궁둥신경 표면 표지는 궁둥뼈결절과 큰돌기의 중간점이며, 궁둥구멍근을 뚫고 지나는 변이가 흔해 궁둥구멍근증후군의 해부 근거가 된다. 도해는 자체 제작(claude-drawn-svg), 라벨판은 diag-gluteal-foramina-labeled.svg.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": "assets/anatomy/diag-gluteal-foramina-quiz.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "볼기부위 — 궁둥구멍근과 통과 구조물"
    }
   ]
  },
  {
   "id": "anatomy-2026-0031",
   "style": "spotter",
   "region": "upper-limb",
   "subregion": "scapular-region",
   "examPhase": "tagging-1",
   "stem": "오른쪽 어깨를 뒤에서 본 도해에서 ①~③은 공간의 경계를 이루는 근육, ④·⑥·⑦은 공간의 이름과 그 통과 구조물, ⑤는 지나가는 신경이다. 각각을 한·영으로 답하시오.",
   "choices": null,
   "answer": "① 작은원근 teres minor (세 공간의 공통 위 경계) / ② 큰원근 teres major (공통 아래 경계) / ③ 위팔세갈래근 긴갈래 long head of triceps (공간을 가르는 세로 기둥) / ④ 네모공간 quadrangular space — 겨드랑신경 + 뒤위팔휘돌이동맥 / ⑤ 겨드랑신경 axillary n. / ⑥ 세모공간 triangular space — 어깨휘돌이동맥 / ⑦ 세모간격 triangular interval — 노신경 + 깊은위팔동맥",
   "explanation": "세 공간은 '위팔세갈래근 긴갈래를 어디서 만나느냐'로 갈린다. 긴갈래 **가쪽**이 네모공간(가쪽 경계는 위팔뼈 외과목), **안쪽**이 세모공간, 큰원근 **아래**가 세모간격이다. 내용물은 네모=신경(겨드랑신경)+뒤위팔휘돌이동맥, 세모=동맥 하나(어깨휘돌이동맥), 세모간격=노신경+깊은위팔동맥으로 외운다. 임상 연결: 위팔뼈 **외과목 골절**은 네모공간을 지나는 겨드랑신경을 다치게 해 어깨세모근 마비 + 어깨 가쪽 감각소실을 만든다. 어깨휘돌이동맥은 어깨동맥그물(빗장밑동맥 ↔ 겨드랑동맥 우회로)의 연결고리라 겨드랑동맥 근위 결찰 시 측부순환이 된다. 라벨판은 diag-scapular-spaces-labeled.svg.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": "assets/anatomy/diag-scapular-spaces-quiz.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "어깨뼈부위 — 3공간과 통과 구조물"
    }
   ]
  },
  {
   "id": "anatomy-2026-0035",
   "style": "spotter",
   "region": "upper-limb",
   "subregion": "scapular-region",
   "examPhase": "tagging-1",
   "stem": "어깨뼈부위 해부 사진에서 번호핀 ①이 지시하는 — 위 작은원근, 아래 큰원근, 안쪽 위팔세갈래근 긴갈래, 가쪽 위팔뼈 외과목으로 둘러싸인 — 공간의 이름과 그 통과 구조물 2가지를 말하시오.",
   "choices": null,
   "answer": "네모공간 (quadrangular space) — 겨드랑신경(axillary n.) + 뒤위팔휘돌이동맥(posterior circumflex humeral a.)",
   "explanation": "어깨뼈부위 3공간 중 태깅 최다 빈출. 위팔세갈래근 긴갈래를 기준으로 **가쪽**이 네모공간, **안쪽**이 세모공간이며, 큰원근 아래가 세모간격(노신경+깊은위팔동맥)이다. 네 경계 중 가쪽이 **위팔뼈 외과목**이라는 점이 임상과 직결된다 — 외과목 골절에서 겨드랑신경이 손상되어 어깨세모근 마비와 어깨 가쪽 감각소실이 생긴다. 영상 라벨과 자막('이곳은 네모공간(quadrangular space)으로')에서 답이 실측 확인됨. 이미지는 학생 필기(검정 펜 주석·지시선)를 획 단위로 제거하고 정답 라벨·자막·타이틀을 가린 복원본.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "어깨뼈부위 — 네모공간 (업로드 스캔 0150 p35)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0036",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "leg-posterior",
   "examPhase": "tagging-1",
   "stem": "종아리 뒤칸 해부 사진에서 ▲와 번호핀 ①이 가리키는 — 무릎 뒤에서 정강뼈 뒤면 위쪽에 붙는 깊은층 근육의 이름을 말하시오.",
   "choices": null,
   "answer": "오금근 (popliteus muscle)",
   "explanation": "종아리 뒤칸 **깊은층**의 가장 위쪽 근육으로, 넙다리뼈 가쪽관절융기에서 정강뼈 뒤면 위쪽(가자미근선 위)으로 달린다. 기능은 **무릎 잠금 해제(unlocking)** — 완전히 편 무릎에서 정강뼈를 안쪽으로 돌려 굽힘을 시작하게 한다. 지배는 정강신경. 오금동맥은 이 근육의 아래모서리에서 앞·뒤정강동맥으로 종말분지한다는 점이 함께 나온다. 영상 라벨과 자막에서 실측 확인됨.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "종아리 뒤칸 — 깊은층 오금근 (업로드 스캔 5183 p25)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0037",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "leg-posterior",
   "examPhase": "tagging-1",
   "stem": "종아리 뒤칸 깊은층 해부 사진에서 ▲와 번호핀 ①이 가리키는 — 긴발가락굽힘근과 긴엄지굽힘근 사이 가장 깊은 곳에 있는 근육의 이름을 말하시오.",
   "choices": null,
   "answer": "뒤정강근 (tibialis posterior muscle)",
   "explanation": "종아리 뒤칸 깊은층 4근육(오금근·긴발가락굽힘근·긴엄지굽힘근·뒤정강근) 중 **가장 깊다**. 정강뼈·종아리뼈·뼈사이막 뒤면에서 일어나 안쪽복사 뒤를 돌아 발배뼈·안쪽쐐기뼈에 닿으며, **발바닥활(arch) 유지**의 핵심이다. 안쪽복사 뒤 통과 순서 'Tom, Dick ANd Harry'에서 가장 앞(T)이 이 근육의 힘줄이다. 지배는 정강신경. 영상 라벨과 자막에서 실측 확인됨.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "종아리 뒤칸 — 깊은층 뒤정강근 (업로드 스캔 5183 p32)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0038",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "popliteal-fossa",
   "examPhase": "tagging-1",
   "stem": "다리오금의 경계를 관찰하는 사진에서 번호핀 ①이 지시하는 — 다리오금의 아래안쪽모서리를 이루는 — 구조의 이름을 말하시오.",
   "choices": null,
   "answer": "장딴지근 안쪽갈래 (medial head of gastrocnemius muscle)",
   "explanation": "다리오금은 마름모꼴이며 경계는 위가쪽 넙다리두갈래근, 위안쪽 반힘줄근·반막근, **아래가쪽·아래안쪽이 장딴지근의 두 갈래**다. 장딴지근은 무릎 **위**(넙다리뼈 관절융기)에서 일어나므로 무릎 굽힘에도 관여하는 반면, 가자미근은 무릎 아래에서 일어나 발바닥굽힘만 한다 — 이 차이가 구분 문항 단골. 오금 바닥은 넙다리뼈 오금면·빗오금인대·오금근이다. 영상 라벨과 자막에서 실측 확인됨.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "다리오금 — 경계(아래안쪽모서리) (업로드 스캔 0150 p47)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0039",
   "style": "spotter",
   "region": "back",
   "subregion": "superficial-back",
   "examPhase": "tagging-1",
   "stem": "등 얕은층 해부 사진에서, 어깨뼈 아래각 아래·가쪽 가슴우리 벽에서 톱니 모양으로 드러난 — 번호핀 ①(▲)이 가리키는 — 근육의 이름을 말하시오.",
   "choices": null,
   "answer": "앞톱니근 (serratus anterior muscle)",
   "explanation": "넓은등근·등세모근을 젖히면 가쪽 가슴우리 벽에 톱니 모양(digitation)으로 붙는 앞톱니근이 드러난다. 1–8(9)째 갈비뼈 가쪽면에서 일어나 어깨뼈 안쪽모서리 앞면(특히 아래각)에 닿고, 긴가슴신경(long thoracic n., C5–7)의 지배를 받아 어깨뼈를 앞당김(protraction)·위쪽돌림 시킨다. 마비되면 날개어깨뼈(winged scapula). 등 쪽에서 보이는 것은 어깨뼈 아래각 주변으로 삐져나온 부분이라, '등 근육'이 아니라 팔이음뼈–가슴우리 근육임에 주의. 원본 영상 라벨 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "얕은층 근육 — 넓은등근 젖힌 뒤 어깨뼈각 아래 (업로드 스캔 pf1 p7)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0040",
   "style": "spotter",
   "region": "back",
   "subregion": "superficial-back",
   "examPhase": "tagging-1",
   "stem": "등세모근을 젖혀 그 깊은면을 노출한 해부 사진에서, 번호핀 ①(▲)이 가리키는 — 목빗근 뒤모서리를 지나 등세모근 깊은면을 따라 내려오는 — 신경의 이름을 말하시오.",
   "choices": null,
   "answer": "더부신경 (accessory nerve, CN XI)",
   "explanation": "등세모근의 운동지배는 얕은층 중 유일하게 뇌신경인 더부신경(XI)이 맡는다. 목정맥구멍으로 두개를 나와 목빗근을 지배한 뒤 뒤목삼각을 가로질러 등세모근 깊은면으로 들어가며, 이 부위에서 셋째·넷째 목신경(C3–4)의 가지와 합쳐진다(C3·4는 고유감각·통각 담당). 뒤목삼각 수술·림프절 생검에서 손상되면 등세모근 위쪽이 위축되어 어깨처짐·팔 외전 제한이 생긴다. 같은 시야에서 등쪽어깨신경(C5, 마름근)·가로목동맥과 헷갈리지 말 것. 원본 영상 라벨 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "얕은층 근육 — 등세모근 깊은면의 신경 (업로드 스캔 pf1 p11)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0041",
   "style": "spotter",
   "region": "back",
   "subregion": "superficial-back",
   "examPhase": "tagging-1",
   "stem": "마름근과 어깨올림근을 젖힌 해부 사진에서, 포셉이 들어올리고 있으며 번호핀 ①(◁)이 가리키는 — 어깨뼈 안쪽모서리를 따라 아래로 달리는 — 혈관의 이름을 말하시오.",
   "choices": null,
   "answer": "등쪽어깨동맥 (dorsal scapular artery)",
   "explanation": "등쪽어깨동맥은 대개 빗장밑동맥 셋째부분(또는 가로목동맥의 깊은가지)에서 나와 어깨뼈 안쪽모서리를 따라 내려가며 마름근·어깨올림근에 분포하고, 어깨뼈 주위 동맥고리(어깨위동맥·어깨휘돌이동맥과의 문합)에 참여한다. 같은 이름의 등쪽어깨신경(C5)이 나란히 내려오므로 실습에서는 '동맥과 신경이 같이 있는 층'으로 기억한다. 두 구조 모두 큰마름근·작은마름근의 깊은면(속면)으로 들어간다. 원본 영상 라벨 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "얕은층 근육 — 마름근·어깨올림근 깊은면의 혈관 (업로드 스캔 pf1 p16)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0042",
   "style": "spotter",
   "region": "back",
   "subregion": "deep-back",
   "examPhase": "tagging-1",
   "stem": "등 깊은층을 노출한 해부 사진에서, 프로브가 들어올리고 있으며 번호핀 ①이 가리키는 — 목덜미인대와 위쪽 등뼈 가시돌기에서 일어나 목빗근 깊은면으로 비스듬히 올라가는 — 근육의 이름을 말하시오.",
   "choices": null,
   "answer": "머리널판근 (splenius capitis muscle)",
   "explanation": "널판근은 등 고유근육의 가장 얕은 층으로 목덜미인대와 C7–T3(머리널판근)·T3–T6(목널판근) 가시돌기에서 일어난다. 머리널판근은 꼭지돌기와 위목덜미선 가쪽 1/3에 닿고, 목널판근은 C1–3 가로돌기에 닿는다. 둘 다 척수신경 뒤가지(등 고유근육의 공통 규칙) 지배이며, 한쪽만 작용하면 같은쪽 돌림·가쪽굽힘, 양쪽이 함께 작용하면 목·머리 폄. 겉에서 보이는 방향이 목빗근과 반대(아래안쪽 → 위가쪽)라 실습에서 목빗근·어깨올림근과 가르는 기준이 된다. 원본 영상 라벨 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "등의 깊은층 근육 — 널판근 (업로드 스캔 pf1 p23)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0043",
   "style": "spotter",
   "region": "back",
   "subregion": "deep-back",
   "examPhase": "tagging-1",
   "stem": "척주세움근을 노출한 해부 사진에서, 가슴 높이에서 가장 가쪽 기둥을 이루며 번호핀 ①(▲)이 가리키는 근육의 이름을 말하시오.",
   "choices": null,
   "answer": "엉덩갈비근 (iliocostalis muscle)",
   "explanation": "척주세움근은 엉치뼈·엉덩뼈능선·허리등뼈 가시돌기의 공통힘줄에서 일어나 가쪽부터 엉덩갈비근–가장긴근–가시근의 세 기둥으로 갈라진다('엉–가–가'). 가장 가쪽인 엉덩갈비근은 갈비뼈각에 닿고(허리·등·목 부분), 중간의 가장긴근은 가로돌기와 꼭지돌기에, 가장 안쪽의 가시근은 가시돌기에 닿는다. 모두 척수신경 뒤가지 지배이며 양쪽이 작용하면 척주 폄, 한쪽이면 같은쪽 가쪽굽힘. 더 깊은 층의 가로돌기가시근육(반가시근–뭇갈래근–돌림근)과 층을 구분해야 한다. 원본 영상 라벨 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "등의 깊은층 근육 — 척주세움근 3기둥 (업로드 스캔 pf1 p27)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0044",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "gluteal",
   "examPhase": "tagging-1",
   "stem": "큰볼기근을 젖힌 볼기 부위 해부 사진에서, 궁둥구멍근 아래모서리에서 나와 번호핀 ①(▲)이 가리키는 — 몸에서 가장 굵은 말초신경 — 의 이름을 말하시오.",
   "choices": null,
   "answer": "궁둥신경 (sciatic nerve)",
   "explanation": "궁둥신경은 엉치신경얼기(L4–S3)에서 나와 큰궁둥구멍의 궁둥구멍근 아래(infrapiriform foramen)로 볼기부위에 들어오는, 몸에서 가장 굵고 긴 말초신경이다. 큰돌기와 궁둥뼈결절 사이 중간을 지나 넓적다리 뒤칸으로 내려가며 정강신경(tibial)과 온종아리신경(common fibular) 두 성분을 함께 싸고 있다(대개 오금 위쪽에서 갈라지나 궁둥구멍근을 관통하며 미리 갈라지는 변이가 흔하다). 볼기 근육주사를 위가쪽 1/4 사분면에 놓는 이유가 바로 이 신경 손상 회피. 원본 영상 라벨·자막 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "볼기부위 — 궁둥구멍근 주위 (업로드 스캔 pf2 p10)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0045",
   "style": "spotter",
   "region": "pelvis-perineum",
   "subregion": "gluteal",
   "examPhase": "tagging-1",
   "stem": "볼기 부위 깊은 해부 사진에서, 엉치가시인대(궁둥뼈가시) 뒤를 돌아 작은궁둥구멍으로 다시 들어가며 번호핀 ①(▲)이 가리키는 신경의 이름을 말하시오.",
   "choices": null,
   "answer": "음부신경 (pudendal nerve)",
   "explanation": "음부신경(S2–4)은 큰궁둥구멍의 궁둥구멍근 아래로 골반을 나온 뒤, 궁둥뼈가시·엉치가시인대 뒤를 감아 곧바로 작은궁둥구멍으로 되돌아 들어가 폐쇄근막이 만드는 음부신경관(Alcock canal)으로 들어간다. 속음부동·정맥과 동행하며(신경이 인대에서 가장 안쪽) 아래곧창자신경·회음신경·음경(음핵)등신경을 낸다. '골반을 나갔다가 다시 들어가는' 이 U자 주행이 태깅 단골이며, 음부신경 차단술은 궁둥뼈가시를 지표로 삼는다. 원본 영상 라벨 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "볼기부위 — 궁둥구멍근 아래·엉치가시인대 주변 (업로드 스캔 pf2 p13)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0046",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "posterior-thigh",
   "examPhase": "tagging-1",
   "stem": "넓적다리 뒤칸을 노출한 해부 사진에서, 프로브가 들어올리고 있으며 번호핀 ①(◁)이 가리키는 — 궁둥뼈결절에서 일어나 가쪽아래로 달리는 — 근육(갈래까지)의 이름을 말하시오.",
   "choices": null,
   "answer": "넙다리두갈래근 긴갈래 (long head of biceps femoris muscle)",
   "explanation": "넓적다리 뒤칸(햄스트링)은 궁둥뼈결절에서 일어나 무릎을 굽히고 엉덩관절을 펴며, 궁둥신경의 정강부분 지배를 받는다는 공통 규칙을 갖는다. 넙다리두갈래근은 예외적으로 두 갈래인데, 긴갈래만 궁둥뼈결절에서 일어나 정강부분 지배를 받고, 짧은갈래는 넙다리뼈 거친선 가쪽선에서 일어나 온종아리신경 지배를 받는다(그래서 짧은갈래는 엄밀히 햄스트링 정의에서 벗어난다). 두 갈래가 합쳐져 종아리뼈머리에 닿으며 무릎굽힘 + 굽힌 무릎의 가쪽돌림을 한다. 안쪽의 반힘줄근·반막근과 함께 오금의 위가쪽/위안쪽 경계를 만든다. 원본 영상 라벨 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "넓적다리 뒤칸의 근육 (업로드 스캔 pf2 p24)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0047",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "popliteal-fossa",
   "examPhase": "tagging-1",
   "stem": "오른쪽 다리를 뒤에서 본 도해(왼쪽이 가쪽)에서 ①~④는 다리오금 마름모의 네 경계 근육, ⑤~⑦은 얕은 것부터 깊은 것 순서의 내용물, ⑧은 마름모의 가쪽 변을 따라 빠져나가는 신경이다. 각각을 한·영으로 답하고, 이어서 (가) 마름모의 바닥을 이루는 것 두 가지 (나) 무릎동맥 5가지 중 관절주머니를 뚫는 것 (다) ⑧이 감아도는 뼈 부위와 손상 시의 보행 이상을 답하시오.",
   "choices": null,
   "answer": "① 넙다리두갈래근 biceps femoris (위가쪽 경계) / ② 반힘줄근·반막근 semitendinosus·semimembranosus (위안쪽 경계) / ③ 장딴지근 가쪽갈래 lateral head of gastrocnemius (아래가쪽) / ④ 장딴지근 안쪽갈래 medial head (아래안쪽) / ⑤ 정강신경 tibial n. (가장 얕다) / ⑥ 오금정맥 popliteal v. (중간) / ⑦ 오금동맥 popliteal a. (가장 깊다) / ⑧ 온종아리신경 common fibular n. — (가) 넙다리뼈 오금면 popliteal surface + 오금근 popliteus (아래쪽) / (나) 중간무릎동맥 middle genicular a. / (다) 종아리뼈목 neck of fibula — 발처짐 foot drop",
   "explanation": "다리오금은 마름모꼴 공간으로, 위 두 변은 햄스트링(가쪽 넙다리두갈래근 · 안쪽 반힘줄근·반막근), 아래 두 변은 장딴지근 두 갈래가 이룬다. 바닥은 위에서부터 넙다리뼈 오금면 → 무릎관절주머니 뒤 → 오금근이고, 지붕은 오금근막이다. 내용물의 깊이 순서는 **뒤(얕은)에서 앞(깊은)으로 정강신경 → 오금정맥 → 오금동맥**('신–정–동')이며, 오금동맥이 가장 깊기 때문에 맥박을 잡으려면 무릎을 살짝 굽혀 깊이 눌러야 한다. 오금동맥은 넙다리동맥이 모음근구멍을 지나면서 이름이 바뀐 것이고, 무릎동맥 5가지(위가쪽·위안쪽·중간·아래가쪽·아래안쪽)를 내어 무릎동맥그물을 만든 뒤 오금근 아래모서리에서 앞정강동맥·뒤정강동맥으로 갈린다. 이 중 **중간무릎동맥만 관절주머니를 뚫고** 들어가 십자인대에 분포한다. 궁둥신경의 두 종말가지 중 정강신경은 오금 한가운데를 수직으로 지나 종아리 뒤칸으로 가고, 온종아리신경은 넙다리두갈래근 힘줄 안쪽을 따라 가쪽아래로 내려가 종아리뼈목을 감아 앞칸·가쪽칸으로 들어간다 — 이 자리가 표면에 가까워 골절·석고붕대 압박으로 가장 흔히 다치며 발처짐과 발등 감각소실이 생긴다. 라벨판은 diag-popliteal-fossa-labeled.svg.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": "assets/anatomy/diag-popliteal-fossa-quiz.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "다리오금 — 경계·내용물·무릎동맥 / 종아리 뒤칸"
    }
   ]
  },
  {
   "id": "anatomy-2026-0048",
   "style": "spotter",
   "region": "back",
   "subregion": "suboccipital-triangle",
   "examPhase": "tagging-1",
   "stem": "뒤통수밑삼각을 노출한 해부 사진에서, 삼각의 바닥에서 포셉이 들어올리고 있으며 번호핀 ①(▲)이 가리키는 혈관의 이름을 말하시오.",
   "choices": null,
   "answer": "척추동맥 (vertebral artery)",
   "explanation": "뒤통수밑삼각의 바닥은 뒤통수뒤통수막(posterior atlanto-occipital membrane)과 고리뼈 뒤활이며, 그 위 고리뼈 가로돌기구멍을 나온 척추동맥이 뒤활 위면의 척추동맥고랑을 따라 안쪽으로 달리다가 큰구멍으로 들어간다. 삼각의 내용물은 이 척추동맥 3부분과 뒤통수밑신경(C1 뒤가지)이다. 척추동맥은 빗장밑동맥 첫부분에서 나와 C6–C1 가로돌기구멍을 올라온 뒤 여기서 급격히 꺾이는데, 이 굴곡부가 목 과신전·급격한 회전(도수치료·미용실 세면대)에서 박리를 일으켜 뒷순환 뇌졸중의 원인이 된다. 큰뒤통수신경(C2 뒤가지)은 삼각을 덮고 지나갈 뿐 내용물이 아니다. 원본 영상 라벨·자막 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "뒤통수밑삼각 — 삼각 바닥의 혈관 (업로드 스캔 0150 p12)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0049",
   "style": "spotter",
   "region": "upper-limb",
   "subregion": "scapular-region",
   "examPhase": "tagging-1",
   "stem": "가시위근을 젖혀 어깨뼈패임을 노출한 해부 사진에서, 패임을 가로질러 구멍으로 바꿔 놓으며 번호핀 ①(▲)이 가리키는 구조물의 이름을 말하시오.",
   "choices": null,
   "answer": "위가로어깨인대 (superior transverse scapular ligament)",
   "explanation": "어깨뼈패임(scapular notch)은 위가로어깨인대가 덮으면서 하나의 구멍이 되고, 이 지점이 태깅 단골이다. 통과 규칙은 ==신경은 인대 아래, 동맥은 인대 위==(army over, navy under — artery over, nerve under) — 즉 어깨위신경(C5–6)은 인대 밑 구멍으로, 어깨위동맥은 인대 위로 지나간다. 그래서 인대가 골화되거나 패임이 좁으면 어깨위신경만 눌려 가시위근·가시아래근 위축과 어깨 뒤 깊은 통증이 생긴다(suprascapular nerve entrapment). 신경은 이어서 가시오목패임(spinoglenoid notch)을 돌아 가시아래근으로 가므로, 그 지점이 막히면 가시아래근만 단독 위축된다(배구·야구 선수). 원본 영상 라벨 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "어깨뼈부위 — 가시위근을 젖힌 어깨뼈패임 (업로드 스캔 0150 p38)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0050",
   "style": "spotter",
   "region": "upper-limb",
   "subregion": "scapular-region",
   "examPhase": "tagging-1",
   "stem": "가시위근을 젖힌 어깨뼈패임 부위 해부 사진에서, 위가로어깨인대의 위쪽으로 지나가며 번호핀 ①(▲)이 가리키는 혈관의 이름을 말하시오.",
   "choices": null,
   "answer": "어깨위동맥 (suprascapular artery)",
   "explanation": "어깨위동맥은 빗장밑동맥의 갑상목동맥(thyrocervical trunk) 가지로, 어깨뼈패임에 이르면 ==위가로어깨인대의 위로== 넘어간다(같은 이름의 어깨위신경은 인대 아래 구멍으로 통과 — 동맥은 위, 신경은 아래). 이후 가시위오목·가시아래오목으로 이어져 어깨휘돌이동맥·등쪽어깨동맥과 문합해 어깨동맥그물(scapular anastomosis)을 이룬다. 이 그물 덕분에 겨드랑동맥 근위를 결찰해도 팔로 가는 곁순환이 유지된다. 동반 정맥은 대개 바깥목정맥으로 흘러 동맥과 경로가 갈린다. 원본 영상 라벨 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "어깨뼈부위 — 어깨뼈패임 위를 지나는 혈관 (업로드 스캔 0150 p41)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0051",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "posterior-leg",
   "examPhase": "tagging-1",
   "stem": "종아리 뒤칸의 피부신경을 노출한 해부 사진에서, 장딴지근 두 갈래 사이 고랑을 따라 내려오며 번호핀 ①(▲)이 가리키는 — 정강신경에서 갈라져 나온 — 피부신경의 이름을 말하시오.",
   "choices": null,
   "answer": "안쪽장딴지피부신경 (medial sural cutaneous nerve)",
   "explanation": "정강신경은 오금에서 안쪽장딴지피부신경을 내어 장딴지근 두 갈래 사이 고랑을 따라 내려온다. 종아리 중간쯤에서 온종아리신경이 낸 ==장딴지신경교통가지(가쪽장딴지피부신경 계열)==와 합쳐져 **장딴지신경(sural nerve)** 이 되고, 이것이 가쪽복사 뒤를 지나 발 가쪽모서리·새끼발가락 가쪽 피부를 담당한다(가쪽발등피부신경으로 이어짐). 표재성이고 운동섬유가 없어 **신경 생검·신경 이식의 표준 공여신경**이며, 발목 부위에서 sural nerve block의 표적이다. 정강신경(운동)·온종아리신경(운동+감각)과 달리 순수 감각신경임에 주의. 원본 영상 라벨 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "종아리 뒤칸 — 피부신경 (업로드 스캔 5183 p10)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0052",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "posterior-leg",
   "examPhase": "tagging-1",
   "stem": "종아리 뒤칸의 얕은층을 노출한 해부 사진에서, 손가락이 짚고 있으며 번호핀 ①이 가리키는 — 넙다리뼈 두 관절융기에서 두 갈래로 일어나 발꿈치힘줄로 이어지는 — 근육의 이름을 말하시오.",
   "choices": null,
   "answer": "장딴지근 (gastrocnemius muscle)",
   "explanation": "장딴지근은 종아리 뒤칸 얕은층의 가장 표면 근육으로, 안쪽갈래는 넙다리뼈 안쪽관절융기 위, 가쪽갈래는 가쪽관절융기에서 일어나 아래에서 합쳐지고 가자미근과 함께 발꿈치힘줄(아킬레스힘줄)을 만들어 발꿈치뼈융기에 닿는다. ==무릎관절 위에서 일어나므로 발바닥굽힘뿐 아니라 무릎굽힘에도 관여==하는 두관절근육이며, 그래서 무릎을 편 상태에서 발등굽힘이 제한된다(무릎을 굽히면 풀린다 — Silfverskiöld 검사의 원리). 무릎 아래에서 일어나는 가자미근은 무릎 자세와 무관하게 작용하고 '제2의 심장'이라 불리는 정맥펌프 역할을 한다. 두 근육 모두 정강신경 지배. 원본 영상 자막 실측 확인(자막: 현재 보이는 근육이 장딴지근입니다). 이미지는 필기를 제거한 복원본이며 정답 자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "3회차(0825) 허미선pf.pdf",
     "page": null,
     "section": "종아리 뒤칸 — 얕은층 근육 (업로드 스캔 5183 p13)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0053",
   "style": "spotter",
   "region": "back",
   "subregion": "gluteal",
   "examPhase": "tagging-1",
   "stem": "볼기 부위의 얕은근막을 벗겨 피부신경을 노출한 해부 사진에서, 엉덩뼈능선을 넘어 볼기 위쪽으로 내려오며 번호핀 ①(▲)이 가리키는 신경의 이름을 말하시오.",
   "choices": null,
   "answer": "위볼기피부신경 (superior cluneal nerves)",
   "explanation": "위볼기피부신경은 L1–L3 척수신경 **뒤가지의 가쪽가지**가 모여 만들어지며, 엉덩뼈능선을 타고 넘어 볼기 위쪽 피부를 담당한다. 뒤가지 유래이므로 얼기를 만들지 않고 분절 배열이 유지된다. 엉덩뼈능선에서 뼈를 채취(bone graft)하거나 그 부위를 절개할 때 이 신경이 잘려 만성 볼기 통증이 생기는 것이 임상 포인트. 같은 화면의 중간볼기피부신경(S1–S3 뒤가지)·아래볼기피부신경(뒤넙다리피부신경 가지 = 앞가지 계열)과 **유래가 다르다는 점**이 태깅의 핵심이다. 원본 영상 라벨·자막 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "다리 뒤쪽 피부신경 — 엉덩뼈능선을 넘는 가지 (업로드 스캔 pf1 p44 · 영상 12:18)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0054",
   "style": "spotter",
   "region": "back",
   "subregion": "gluteal",
   "examPhase": "tagging-1",
   "stem": "볼기 부위 피부신경 해부 사진에서, 엉치뼈 뒤면의 구멍에서 나와 가쪽으로 퍼지며 번호핀 ①(▲)이 가리키는 신경의 이름을 말하시오.",
   "choices": null,
   "answer": "중간볼기피부신경 (middle cluneal nerves)",
   "explanation": "중간볼기피부신경은 S1–S3 척수신경 **뒤가지**가 뒤엉치구멍(posterior sacral foramina)으로 나와 엉치엉덩관절 위쪽 볼기 피부를 담당한다. 세 볼기피부신경 중 가운데 높이에서 나오므로 '나오는 높이'로 구분한다 — 위(엉덩뼈능선) · 중간(엉치뼈 뒤면) · 아래(큰볼기근 아래모서리). 위·중간은 뒤가지 유래라 얼기를 만들지 않지만, 아래볼기피부신경만 뒤넙다리피부신경(앞가지·엉치신경얼기)의 가지다. 엉치엉덩관절 부위 통증의 감별에서 이 신경의 분포가 근거가 된다. 원본 영상 라벨·자막 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "다리 뒤쪽 피부신경 — 뒤엉치구멍에서 나오는 가지 (업로드 스캔 pf1 p45 · 영상 12:23)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0055",
   "style": "spotter",
   "region": "back",
   "subregion": "gluteal",
   "examPhase": "tagging-1",
   "stem": "볼기 부위 피부신경 해부 사진에서, 큰볼기근 아래모서리를 감아 볼기 아래쪽 피부로 올라가며 번호핀 ①(▲)이 가리키는 신경의 이름을 말하시오.",
   "choices": null,
   "answer": "아래볼기피부신경 (inferior cluneal nerves)",
   "explanation": "아래볼기피부신경은 이름만 볼기피부신경 3형제에 속할 뿐, 유래가 다르다 — **뒤넙다리피부신경(S1–S3 앞가지)의 가지**로, 큰볼기근 아래모서리를 감아 올라가 볼기 아래쪽 피부를 담당한다. 위·중간볼기피부신경이 척수신경 **뒤가지** 유래인 것과 대비되는 이 한 가지가 태깅·구술의 단골 함정이다. 뒤넙다리피부신경 자체는 궁둥구멍근 아래구멍으로 골반을 나오므로, 아래볼기피부신경도 결국 엉치신경얼기 계열이다. 앉을 때 닿는 볼기 아래 피부 감각이 이 신경의 영역이다. 원본 영상 라벨·자막 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "다리 뒤쪽 피부신경 — 큰볼기근 아래모서리를 감아 올라가는 가지 (업로드 스캔 pf1 p46 · 영상 12:27)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0056",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "posterior-thigh",
   "examPhase": "tagging-1",
   "stem": "넓적다리 뒤쪽의 얕은근막을 벗긴 해부 사진에서, 깊은근막을 뚫고 나와 넓적다리 뒤 피부로 퍼지며 번호핀 ①(▲)이 가리키는 신경 가지의 이름을 말하시오.",
   "choices": null,
   "answer": "뒤넙다리피부신경의 관통가지 (perforating branches of the posterior cutaneous nerve of thigh)",
   "explanation": "뒤넙다리피부신경(S1–S3 앞가지)은 궁둥구멍근 아래구멍으로 골반을 나와 큰볼기근 깊은면을 지난 뒤 넓적다리 뒤 정중선을 따라 내려가면서, 깊은근막을 뚫고 나오는 여러 **관통가지**로 넓적다리 뒤 피부를 담당한다. 위쪽으로는 아래볼기피부신경, 안쪽으로는 회음가지를 낸다. 순수 감각신경이라 손상되어도 근력 저하는 없고 넓적다리 뒤 감각소실만 생긴다. 같은 넓적다리 뒤칸을 지나는 궁둥신경(운동+감각, 깊은층)과는 층이 다르다 — 피부신경은 **얕은근막** 안에 있고 궁둥신경은 깊은근막 아래에 있다는 것이 피부벗기기 실습의 요점. 원본 영상 라벨·자막 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "다리 뒤쪽 피부신경 — 넓적다리 뒤 피부로 나오는 가지 (업로드 스캔 pf1 p47 · 영상 12:45)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0057",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "posterior-leg",
   "examPhase": "tagging-1",
   "stem": "종아리 뒤쪽의 얕은근막에서, 작은두렁정맥과 나란히 가쪽복사 쪽으로 내려가며 번호핀 ①(▲)이 가리키는 굵은 피부신경의 이름을 말하시오.",
   "choices": null,
   "answer": "장딴지신경 (sural nerve)",
   "explanation": "장딴지신경은 정강신경이 낸 **안쪽장딴지피부신경**과 온종아리신경이 낸 **장딴지신경교통가지**가 종아리 중간쯤에서 합쳐져 만들어진다. 작은두렁정맥과 나란히 내려가 가쪽복사 뒤를 지나 발 가쪽모서리·새끼발가락 가쪽 피부를 담당한다(가쪽발등피부신경으로 이어짐). 운동섬유가 없는 순수 감각신경이고 표재성이라 **신경 생검·신경 이식의 표준 공여신경**이며, 발목 부위 sural nerve block의 표적이다. 종아리 뒤쪽에서 얕은근막을 벗길 때 가장 먼저 눈에 띄는 굵은 흰 줄이 이것이다. 원본 영상 라벨·자막 실측 확인. 이미지는 필기를 제거한 복원본이며 정답 라벨·자막·타이틀은 가림.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": "restored-scan",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "다리 뒤쪽 피부신경 — 종아리 뒤의 굵은 피부신경 (업로드 스캔 pf1 p48 · 영상 13:03)"
    }
   ]
  },
  {
   "id": "anatomy-2026-0058",
   "style": "spotter",
   "region": "lower-limb",
   "subregion": "posterior-lower-limb",
   "examPhase": "tagging-1",
   "stem": "오른쪽 다리를 뒤에서 본 도해에서 ①~③은 볼기의 피부신경 3형제(위에서 아래로), ④⑤는 넓적다리 뒤, ⑥⑦⑧은 종아리 뒤의 피부신경이다. 각각을 한·영으로 답하고, 이어서 (가) ①~③ 중 앞가지에서 온 것 (나) ⑧을 이루는 두 신경 (다) ⑧이 공여신경으로 쓰이는 이유 (라) 넓적다리·종아리 안쪽 피부를 담당하는 신경을 답하시오.",
   "choices": null,
   "answer": "① 위볼기피부신경 superior cluneal nn. (L1–L3 뒤가지) / ② 중간볼기피부신경 middle cluneal nn. (S1–S3 뒤가지) / ③ 아래볼기피부신경 inferior cluneal nn. / ④ 뒤넙다리피부신경 posterior cutaneous n. of thigh (S1–S3 앞가지) / ⑤ 관통가지 perforating branches / ⑥ 안쪽장딴지피부신경 medial sural cutaneous n. / ⑦ 장딴지신경교통가지 sural communicating br. / ⑧ 장딴지신경 sural n. — (가) ③ 아래볼기피부신경(뒤넙다리피부신경의 가지), 나머지 둘은 척수신경 뒤가지 / (나) 안쪽장딴지피부신경(정강신경) + 장딴지신경교통가지(온종아리신경) / (다) 운동섬유가 없는 순수 감각신경이라 절제해도 근력 손실이 없고 표재성이라 채취가 쉽다 / (라) 두렁신경 saphenous n. (넙다리신경의 가지)",
   "explanation": "볼기피부신경 3형제는 **나오는 높이**로 가른다 — 위(엉덩뼈능선을 넘음) · 중간(뒤엉치구멍) · 아래(큰볼기근 아래모서리). 그런데 유래는 2:1로 갈린다: 위·중간은 척수신경 **뒤가지**(각각 L1–L3, S1–S3)라 얼기를 만들지 않고 분절 배열을 지키는 반면, 아래볼기피부신경만 뒤넙다리피부신경(S1–S3 **앞가지**·엉치신경얼기)의 가지다. 이 한 가지가 구술·태깅의 단골 함정이다. 뒤넙다리피부신경은 궁둥구멍근 아래구멍으로 골반을 나와 넓적다리 뒤 정중선을 따라 내려가며 관통가지로 피부에 분포하고, 위로는 아래볼기피부신경, 안쪽으로는 회음가지를 낸다. 종아리에서는 정강신경의 안쪽장딴지피부신경과 온종아리신경의 교통가지가 합쳐져 장딴지신경이 되고, 작은두렁정맥과 나란히 가쪽복사 뒤를 지나 발 가쪽으로 간다. 넓적다리·종아리 **안쪽** 피부는 뒤칸 신경이 아니라 넙다리신경의 두렁신경 담당임에 주의. 라벨판은 diag-posterior-cutaneous-nerves-labeled.svg.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": "assets/anatomy/diag-posterior-cutaneous-nerves-quiz.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "다리 뒤쪽 피부신경 실습영상(1회차 배정 구간) — 도해 근거"
    }
   ]
  },
  {
   "id": "anatomy-2026-0059",
   "style": "layer-order",
   "region": "back",
   "subregion": "back-general",
   "examPhase": "tagging-1",
   "stem": "등뼈 높이 가로단면 도해(등이 위쪽)에서 ①~⑤는 피부에서 안쪽으로 지나는 층, ⑥⑦은 척수신경이 갈라지는 두 가지, ⑧은 감각신경세포체가 모인 곳이다. 각각을 답하고, 이어서 (가) ⑥과 ⑦의 차이를 굵기·얼기·지배 영역 세 가지로 (나) ⑤의 지배 가지와 그 예외가 되는 근육 (다) 피부신경·피부정맥이 있는 층 (라) ⑧ 손상 시의 결손을 답하시오.",
   "choices": null,
   "answer": "① 피부 skin / ② 얕은근막(피부밑조직) superficial fascia / ③ 깊은근막 deep fascia / ④ 얕은층 근육(등세모근·넓은등근) / ⑤ 고유등근육 intrinsic back mm. / ⑥ 뒤가지 dorsal ramus / ⑦ 앞가지 ventral ramus / ⑧ 뒤뿌리신경절 dorsal root ganglion — (가) 뒤가지는 가늘고·얼기를 만들지 않고·고유등근육과 척주 옆 등 피부만 / 앞가지는 굵고·얼기(목·팔·허리·엉치)를 이루고·몸통 앞가쪽과 팔다리 전체 / (나) 고유등근육은 전부 뒤가지 지배이며, 등에 있어도 이주근육(등세모근·넓은등근·마름근·어깨올림근)은 앞가지 또는 더부신경 지배라 예외 / (다) ② 얕은근막 / (라) 감각신경세포체가 죽어 해당 분절의 감각만 소실되고 운동은 보존된다",
   "explanation": "척수신경은 척주사이구멍을 나오자마자 앞가지와 뒤가지로 갈리고, 그 뒤로는 영역이 겹치지 않는다. **뒤가지**는 가늘고 얼기를 만들지 않아 분절 배열이 그대로 유지되며, 고유등근육(척주세움근·가로돌기가시근육 등)과 척주 옆 등 피부만 담당한다. 뒤가지는 다시 안쪽가지·가쪽가지로 갈려 각각 피부가지를 낸다. **앞가지**는 굵고 목·팔·허리·엉치 얼기를 이뤄 팔다리와 몸통 앞가쪽을 담당하며, 갈비사이신경만 얼기 없이 분절을 지킨다. 시험의 함정은 '등에 있으니 뒤가지 지배'라는 추론이다 — 등세모근(더부신경 XI)·넓은등근(가슴등신경)·마름근(등쪽어깨신경)은 발생학적으로 다른 곳에서 이주해 온 근육이라 앞가지 계열의 지배를 받는다. 피부벗기기 실습에서는 피부 → 얕은근막 → 깊은근막 순으로 지나며, **피부신경과 피부정맥이 얕은근막 안에 있으므로** 여기서 너무 깊이 들어가면 분절 분포를 확인할 수 없게 된다. 라벨판은 diag-back-layers-rami-labeled.svg.",
   "confidence": "high",
   "answerOnlyBacked": false,
   "image": "assets/anatomy/diag-back-layers-rami-quiz.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "2회차(0818) 김홍태pf.pdf",
     "page": null,
     "section": "Back — Superficial layer 실습영상 + 1회차 과제(앞가지·뒤가지) — 도해 근거"
    }
   ]
  },
  {
   "id": "anatomy-2026-0004",
   "style": "branch-tree",
   "region": "pelvis-perineum",
   "subregion": "pelvic-cavity",
   "examPhase": "tagging-2",
   "stem": "골반안의 동맥 박리 중이다. 다음 중 속엉덩동맥의 가지가 아닌 것은?",
   "choices": [
    "A. 배꼽동맥 (umbilical artery)",
    "B. 위볼기동맥 (superior gluteal artery)",
    "C. 위곧창자동맥 (superior rectal artery)",
    "D. 폐쇄동맥 (obturator artery)",
    "E. 가쪽엉치동맥 (lateral sacral artery)"
   ],
   "answer": "C",
   "explanation": "위곧창자동맥은 아래창자간막동맥의 가지로, 곧창자 뒷면에서 속엉덩동맥의 가지인 중간곧창자동맥과 문합한다(강의 14차시 곧창자·속엉덩동맥 절). 나머지는 모두 속엉덩동맥의 가지다. 가쪽엉치동맥·폐쇄동맥은 tagging 2차 자료의 번호 항목(과거 태깅 답 후보).",
   "confidence": "medium",
   "answerOnlyBacked": true,
   "image": null,
   "imageOrigin": null,
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "속엉덩동맥·곧창자"
    },
    {
     "file": "tagging 2차.pdf",
     "page": null,
     "section": "골반 [동맥]"
    }
   ]
  },
  {
   "id": "anatomy-2026-0005",
   "style": "course-tracing",
   "region": "pelvis-perineum",
   "subregion": "pelvic-cavity",
   "examPhase": "tagging-2",
   "stem": "골반 가쪽벽에서 폐쇄관으로 들어가는 신경을 추적한다. 이 신경의 주행으로 옳은 순서는? ㉠ 허리신경얼기에서 기시 ㉡ 큰허리근 안쪽모서리로 나옴 ㉢ 바깥엉덩동맥 뒤·속엉덩동맥 가쪽을 지남 ㉣ 폐쇄관 진입",
   "choices": [
    "A. ㉠→㉡→㉢→㉣",
    "B. ㉠→㉢→㉡→㉣",
    "C. ㉡→㉠→㉢→㉣",
    "D. ㉠→㉡→㉣→㉢"
   ],
   "answer": "A",
   "explanation": "폐쇄신경은 허리신경얼기에서 일어나 위골반문 근처에서 큰허리근 안쪽모서리로 빠져나와, 바깥엉덩동맥 뒤·속엉덩동맥 가쪽을 지나 앞으로 달려 폐쇄관으로 들어간다. 폐쇄동맥·정맥은 신경 아래쪽에서 함께 폐쇄관에 진입한다(강의 14차시 남자골반안 절).",
   "confidence": "medium",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": null,
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "남자골반안"
    }
   ]
  },
  {
   "id": "anatomy-2026-0006",
   "style": "relation",
   "region": "pelvis-perineum",
   "subregion": "pelvic-cavity",
   "examPhase": "tagging-2",
   "stem": "여자 골반안에서 선 자세일 때 복막안의 가장 아래(최하방) 지점이 되는 오목은?",
   "choices": [
    "A. 방광자궁오목 (vesicouterine pouch)",
    "B. 곧창자자궁오목 (rectouterine pouch)",
    "C. 방광옆오목 (paravesical fossa)",
    "D. 곧창자옆오목 (pararectal fossa)"
   ],
   "answer": "B",
   "explanation": "여자에서는 곧창자와 방광 사이에 자궁이 있어 남자의 곧창자방광오목이 방광자궁오목과 곧창자자궁오목으로 나뉜다. 곧창자자궁오목의 가장 아래부분은 자궁이 아니라 질 윗부분을 덮는 복막이 이룬다(강의 14차시 여자골반안 절) — 즉 복막안 최하방.",
   "confidence": "medium",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": null,
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "여자골반안"
    }
   ]
  },
  {
   "id": "anatomy-2026-0007",
   "style": "spotter",
   "region": "pelvis-perineum",
   "subregion": "urinary-bladder",
   "examPhase": "tagging-2",
   "stem": "방광을 열어 속면을 관찰한다. 아래쪽의 속요도구멍과 위쪽의 양쪽 요관구멍을 잇는, 점막주름 없이 매끈한 세모꼴 부위의 이름은? (단답)",
   "choices": null,
   "answer": "방광삼각 (trigone of bladder)",
   "explanation": "방광점막 아래뒤쪽의 매끈한 세모꼴 부위. 꼭짓점은 속요도구멍, 위 두 각은 요관구멍이며 요관사이주름이 양쪽 요관구멍을 가로로 잇는다(강의 14차시 방광 속 절 — 실습 퀴즈 6번과 같은 형식). 빈 방광에서 나머지 점막은 불규칙한 주름이 잡힌다.",
   "confidence": "medium",
   "answerOnlyBacked": true,
   "image": null,
   "imageOrigin": null,
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "방광 속·해부실습14 퀴즈"
    },
    {
     "file": "tagging 2차.pdf",
     "page": null,
     "section": "골반 [방광]"
    }
   ]
  },
  {
   "id": "anatomy-2026-0008",
   "style": "layer-order",
   "region": "pelvis-perineum",
   "subregion": "pelvic-diaphragm",
   "examPhase": "tagging-2",
   "stem": "골반가로막을 이루는 항문올림근 중 가장 앞·안쪽에 있으며, 두덩뼈몸통에서 일어나 항문관을 감싼 뒤 양쪽이 뒤에서 서로 연결되는 근육은?",
   "choices": [
    "A. 두덩곧창자근 (puborectalis)",
    "B. 두덩꼬리근 (pubococcygeus)",
    "C. 엉덩꼬리근 (iliococcygeus)",
    "D. 꼬리근 (coccygeus)"
   ],
   "answer": "A",
   "explanation": "안→가쪽 순서: 두덩곧창자근 → 두덩꼬리근 → 엉덩꼬리근, 그리고 항문올림근 밖 가쪽의 꼬리근. 두덩곧창자근 양쪽 사이 틈새가 비뇨생식구멍이다. 항문올림근은 tagging 2차 자료의 번호 항목(과거 태깅 답 후보 277).",
   "confidence": "medium",
   "answerOnlyBacked": true,
   "image": null,
   "imageOrigin": null,
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "골반가로막"
    },
    {
     "file": "tagging 2차.pdf",
     "page": null,
     "section": "골반 [골반가로막]"
    }
   ]
  },
  {
   "id": "anatomy-2026-0009",
   "style": "distinction",
   "region": "pelvis-perineum",
   "subregion": "pelvic-cavity",
   "examPhase": "tagging-2",
   "stem": "여자 골반안에서 자궁넓은인대를 박리 중이다. 자궁관을 싸고 있으며 난소간막보다 위쪽에 위치하는 자궁넓은인대의 부분은?",
   "choices": [
    "A. 난소간막 (mesovarium)",
    "B. 자궁관간막 (mesosalpinx)",
    "C. 자궁간막 (mesometrium)",
    "D. 난소걸이인대 (suspensory ligament of ovary)"
   ],
   "answer": "B",
   "explanation": "자궁넓은인대의 세 부분: 자궁관간막(자궁관을 싸는 부분, 가장 위) · 난소간막(뒤로 뻗어 난소 지지) · 자궁간막(자궁관간막 아래쪽 나머지). 난소걸이인대는 난소동·정맥이 만드는 별도의 복막주름이다. 자궁관간막(271)·고유난소인대(272)는 tagging 2차 번호 항목.",
   "confidence": "medium",
   "answerOnlyBacked": true,
   "image": null,
   "imageOrigin": null,
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "여자골반안"
    },
    {
     "file": "tagging 2차.pdf",
     "page": null,
     "section": "골반 [여자 골반안]"
    }
   ]
  },
  {
   "id": "anatomy-2026-0010",
   "style": "course-tracing",
   "region": "pelvis-perineum",
   "subregion": "pelvic-cavity",
   "examPhase": "tagging-2",
   "stem": "골반부분 요관을 추적한다. 여성에서 요관이 방광 위가쪽각에 닿기 직전에 아래쪽으로 가로지르는 구조물은?",
   "choices": [
    "A. 자궁원인대 (round ligament of uterus)",
    "B. 자궁넓은인대 (broad ligament of uterus)",
    "C. 고유난소인대 (ligament of ovary)",
    "D. 난소걸이인대 (suspensory ligament of ovary)"
   ],
   "answer": "B",
   "explanation": "요관은 속엉덩동맥 앞에서 아래앞쪽으로 달리고, 여성에서는 자궁넓은인대 아래쪽을 가로질러 방광 위가쪽각에 닿는다(강의 14차시 남자골반안 절 — 요관 항목). 자궁동맥이 요관 위를 지나는 관계는 임상(자궁절제술)에서 중요하다. 요관(267)은 tagging 2차 번호 항목.",
   "confidence": "medium",
   "answerOnlyBacked": true,
   "image": null,
   "imageOrigin": null,
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "남자골반안"
    },
    {
     "file": "tagging 2차.pdf",
     "page": null,
     "section": "골반 [남자 골반안]"
    }
   ]
  },
  {
   "id": "anatomy-2026-0011",
   "style": "relation",
   "region": "pelvis-perineum",
   "subregion": "male-internal-genitalia",
   "examPhase": "tagging-2",
   "stem": "남자 골반에서 전립샘 속을 지나 요도전립샘부분으로 열리는 사정관(ejaculatory duct)을 형성하는 두 구조물의 조합은?",
   "choices": [
    "A. 정관팽대 + 정낭배출관",
    "B. 정관 + 전립샘관",
    "C. 정낭배출관 + 전립샘관",
    "D. 정관팽대 + 망울요도샘관"
   ],
   "answer": "A",
   "explanation": "정관은 정낭 안쪽모서리를 따라 내려가며 넓어져 정관팽대를 이루고, 아래쪽에서 정낭배출관과 만나 사정관을 형성한다. 양쪽 사정관은 전립샘 속을 지나 요도전립샘부분(요도둔덕 옆 사정관구멍)으로 열린다. 정관팽대(269)·정낭(270)·전립샘(268)은 tagging 2차 번호 항목.",
   "confidence": "medium",
   "answerOnlyBacked": true,
   "image": null,
   "imageOrigin": null,
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "정낭과 정관·전립샘"
    },
    {
     "file": "tagging 2차.pdf",
     "page": null,
     "section": "골반 [남자 골반안]"
    }
   ]
  },
  {
   "id": "anatomy-2026-0012",
   "style": "clinical-application",
   "region": "pelvis-perineum",
   "subregion": "anal-canal",
   "examPhase": "tagging-2",
   "stem": "항문관 속면에서 항문판막 아래쪽으로 보이는 부채모양의 선을 확인했다. 이 선을 기준으로 위·아래가 나뉘는 것으로 강의에서 명시된 항목이 아닌 것은?",
   "choices": [
    "A. 동맥 분포",
    "B. 정맥 흐름",
    "C. 신경 분포",
    "D. 림프 흐름",
    "E. 점막의 상피 재생 속도"
   ],
   "answer": "E",
   "explanation": "빗살선(pectinate line)은 항문관 위·아래의 동맥, 정맥, 신경분포, 림프흐름이 나뉘는 기준이다(강의 14차시 항문관 절). 상피 재생 속도는 강의 자료에 없는 항목이다. 위쪽 동맥은 위곧창자동맥(아래창자간막동맥 가지), 아래쪽은 아래곧창자동맥(속음부동맥 가지) 영역.",
   "confidence": "medium",
   "answerOnlyBacked": false,
   "image": null,
   "imageOrigin": null,
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "항문관"
    }
   ]
  },
  {
   "id": "anatomy-2026-0013",
   "style": "spotter",
   "region": "pelvis-perineum",
   "subregion": "pelvic-cavity",
   "examPhase": "tagging-2",
   "stem": "골반 안 동맥 모식도에서 번호 ①~⑤가 가리키는 동맥의 이름을 각각 말하시오. (①방광 쪽 첫 가지 ②엉치뼈 앞면·보통 2개 ③큰궁둥구멍 윗부분으로 나감 ④큰궁둥구멍 아랫부분·궁둥뼈가시 바로 위 ⑤폐쇄관으로 신경과 동행)",
   "choices": null,
   "answer": "① 배꼽동맥(→위방광동맥) ② 가쪽엉치동맥 ③ 위볼기동맥 ④ 속음부동맥 ⑤ 폐쇄동맥",
   "explanation": "행선지로 묶으면: 배꼽동맥은 위방광동맥을 내고, 가쪽엉치동맥은 엉치뼈 앞면을 보통 2개로 내려가며(tagging 답 후보 275), 위볼기동맥은 큰궁둥구멍 윗부분·아래볼기동맥과 속음부동맥은 아랫부분으로 나간다(속음부동맥은 궁둥뼈가시 바로 위). 폐쇄동맥(답 후보 276)은 폐쇄신경 아래쪽에서 함께 폐쇄관으로 들어간다. 도해는 강의 내용을 교과서식 구도(오른반골반 안쪽면)로 재구성한 자체 제작 그림이며, 라벨판은 전체 한·영 병기다.",
   "confidence": "medium",
   "answerOnlyBacked": true,
   "image": "assets/anatomy/diag-internal-iliac-quiz.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "속엉덩동맥"
    },
    {
     "file": "tagging 2차.pdf",
     "page": null,
     "section": "골반 [동맥]"
    }
   ]
  },
  {
   "id": "anatomy-2026-0014",
   "style": "spotter",
   "region": "pelvis-perineum",
   "subregion": "pelvic-diaphragm",
   "examPhase": "tagging-2",
   "stem": "위에서 본 골반가로막 모식도에서 번호 ①~⑤가 가리키는 구조의 이름을 각각 말하시오. (①항문관을 감싸는 가장 앞안쪽 근육 ②그 사이 틈새 ③궁둥뼈가시-폐쇄관을 잇는 노란 점선 ④힘줄활에서 일어나는 가장 가쪽 항문올림근 ⑤궁둥뼈가시에서 꼬리뼈로 가는 근육)",
   "choices": null,
   "answer": "① 두덩곧창자근 ② 비뇨생식구멍 ③ 항문올림근힘줄활 ④ 엉덩꼬리근 ⑤ 꼬리근",
   "explanation": "항문올림근(tagging 답 후보 277)은 안→가쪽으로 두덩곧창자근·두덩꼬리근·엉덩꼬리근이고, 꼬리근은 그 가쪽에서 궁둥뼈가시→꼬리뼈·엉치뼈로 간다. 항문올림근힘줄활은 속폐쇄근막이 선 모양으로 두꺼워진 것(근육이 아닌 근막 구조물)으로 궁둥뼈가시에서 폐쇄관까지 거의 수평하게 뻗고, 엉덩꼬리근이 여기서 일어난다. 두덩곧창자근 양쪽 사이 틈새가 비뇨생식구멍이다. 도해는 교과서식 구도(위에서 본 모습, 좌우대칭·근섬유 결 표현)의 자체 제작 그림이며, 라벨판은 전체 한·영 병기다.",
   "confidence": "medium",
   "answerOnlyBacked": true,
   "image": "assets/anatomy/diag-pelvic-diaphragm-quiz.svg",
   "imageOrigin": "claude-drawn-svg",
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "골반가로막"
    },
    {
     "file": "tagging 2차.pdf",
     "page": null,
     "section": "골반 [골반가로막]"
    }
   ]
  }
 ],
 "daily": [
  {
   "date": "2026-08-13",
   "phase": "t1-prep",
   "examPhase": "tagging-1",
   "regions": [
    "back",
    "lower-limb"
   ],
   "concepts": {
    "preview": [
     "anatomy-2026-0001"
    ],
    "layer": [
     "anatomy-2026-0003"
    ],
    "branch": [
     "anatomy-2026-0002"
    ],
    "relation": []
   },
   "questions": [
    "anatomy-2026-0004",
    "anatomy-2026-0012",
    "anatomy-2026-0010",
    "anatomy-2026-0009",
    "anatomy-2026-0008",
    "anatomy-2026-0011",
    "anatomy-2026-0013",
    "anatomy-2026-0005",
    "anatomy-2026-0006",
    "anatomy-2026-0014",
    "anatomy-2026-0007"
   ],
   "review": {
    "d-1": [
     "anatomy-2026-0004",
     "anatomy-2026-0012",
     "anatomy-2026-0010",
     "anatomy-2026-0009",
     "anatomy-2026-0008",
     "anatomy-2026-0011",
     "anatomy-2026-0007",
     "anatomy-2026-0005",
     "anatomy-2026-0006"
    ],
    "d-3": [],
    "d-7": [],
    "d-14": []
   },
   "estMinutes": 33
  },
  {
   "date": "2026-08-12",
   "phase": "t1-prep",
   "examPhase": "tagging-1",
   "regions": [
    "back",
    "lower-limb"
   ],
   "concepts": {
    "preview": [
     "anatomy-2026-0001"
    ],
    "layer": [
     "anatomy-2026-0003"
    ],
    "branch": [
     "anatomy-2026-0002"
    ],
    "relation": []
   },
   "questions": [
    "anatomy-2026-0004",
    "anatomy-2026-0012",
    "anatomy-2026-0010",
    "anatomy-2026-0009",
    "anatomy-2026-0008",
    "anatomy-2026-0011",
    "anatomy-2026-0007",
    "anatomy-2026-0005",
    "anatomy-2026-0006"
   ],
   "review": {
    "d-1": [],
    "d-3": [],
    "d-7": [],
    "d-14": []
   },
   "estMinutes": 29
  }
 ],
 "glossary": [
  {
   "ko": "가로막 대동맥구멍지나 배로 들어오면서 형성\n\n자율신경얼기",
   "en": "autonomic plexus",
   "region": "abdomen"
  },
  {
   "ko": "가로막대동맥구멍",
   "en": "aortic hiatus",
   "region": "abdomen"
  },
  {
   "ko": "가로잘록창자",
   "en": "transverse colon",
   "region": "abdomen"
  },
  {
   "ko": "가로잘록창자간막",
   "en": "transverse mesocolon",
   "region": "abdomen"
  },
  {
   "ko": "가로창자",
   "en": "transverse colon",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "가로창자간막",
   "en": "transverse mesocolon",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "가슴림프관팽대",
   "en": "cisterna chyli",
   "region": "abdomen"
  },
  {
   "ko": "가슴배벽정맥",
   "en": "thoracoepigastric vein",
   "region": "abdomen"
  },
  {
   "ko": "가슴배신경",
   "en": "thoracoabdominal nerve",
   "region": "abdomen"
  },
  {
   "ko": "가쪽고샅오목",
   "en": "lateral inguinal fossa",
   "region": "abdomen"
  },
  {
   "ko": "가쪽넙다리피부신경",
   "en": "lateral cutaneous nerve of thigh",
   "region": "abdomen"
  },
  {
   "ko": "가쪽눈꺼풀인대",
   "en": "lateral palpebral ligament",
   "region": "abdomen"
  },
  {
   "ko": "가쪽다리",
   "en": "lateral crus",
   "region": "abdomen"
  },
  {
   "ko": "가쪽배꼽주름",
   "en": "lateral umbilical fold",
   "region": "abdomen"
  },
  {
   "ko": "가쪽활꼴인대",
   "en": "lateral arcuate ligament",
   "region": "abdomen"
  },
  {
   "ko": "간 아랫면에서 위작은굽이까지 잇는 간위인대",
   "en": "hepatogastric ligament",
   "region": "abdomen"
  },
  {
   "ko": "간동맥",
   "en": "hepatic artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "간문",
   "en": "porta hepatis",
   "region": "abdomen"
  },
  {
   "ko": "간문맥",
   "en": "hepatic portal vein",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "간샘창자인대",
   "en": "hepatoduodenal ligament",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "간세동이",
   "en": "portal triad",
   "region": "abdomen"
  },
  {
   "ko": "간원인대",
   "en": "round ligament of liver",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "간위인대",
   "en": "hepatogastric ligament",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "갈고리돌기",
   "en": "uncinate process",
   "region": "abdomen"
  },
  {
   "ko": "갈비밑신경",
   "en": "subcostal nerve",
   "region": "abdomen"
  },
  {
   "ko": "갈비부분",
   "en": "costal part",
   "region": "abdomen"
  },
  {
   "ko": "검정색으로 보이는 막이 맥락막",
   "en": "choroid",
   "region": "abdomen"
  },
  {
   "ko": "겉질",
   "en": "cortex",
   "region": "abdomen"
  },
  {
   "ko": "결합힘줄",
   "en": "conjoint tendon",
   "region": "abdomen"
  },
  {
   "ko": "경우에 따라 덧콩팥동맥",
   "en": "accessory renal artery",
   "region": "abdomen"
  },
  {
   "ko": "고샅낫힘줄",
   "en": "inguinal falx",
   "region": "abdomen"
  },
  {
   "ko": "고샅인대",
   "en": "inguinal ligament",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "고유간동맥",
   "en": "proper hepatic artery",
   "region": "abdomen"
  },
  {
   "ko": "고환",
   "en": "testis",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "고환동맥",
   "en": "testicular artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "고환동맥은 깊은고샅구멍",
   "en": "deep inguinal ring",
   "region": "abdomen"
  },
  {
   "ko": "고환사이막",
   "en": "septum of testis",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "고환세로칸",
   "en": "mediastinum of testis",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "고환올림근",
   "en": "cremaster muscle",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "고환올림근막",
   "en": "cremasteric fascia",
   "region": "abdomen"
  },
  {
   "ko": "고환정맥",
   "en": "testicular vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "곧은동맥",
   "en": "vasa recta",
   "region": "abdomen"
  },
  {
   "ko": "곧창자",
   "en": "rectum",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "과 내장복막",
   "en": "visceral peritoneum",
   "region": "abdomen"
  },
  {
   "ko": "과 배곧은근집",
   "en": "rectus sheath",
   "region": "abdomen"
  },
  {
   "ko": "과 위이자샘창자동맥",
   "en": "superior pancreaticoduodenal artery",
   "region": "abdomen"
  },
  {
   "ko": "관상면",
   "en": "coronal plane",
   "region": "abdomen"
  },
  {
   "ko": "관상인대",
   "en": "coronary ligament",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "교감신경줄기",
   "en": "sympathetic trunk",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "구불잘록창자가지",
   "en": "sigmoid branch",
   "region": "abdomen"
  },
  {
   "ko": "구불잘록창자간막",
   "en": "sigmoid mesocolon",
   "region": "abdomen"
  },
  {
   "ko": "구불창자",
   "en": "sigmoid colon",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "구불창자간막",
   "en": "sigmoid mesocolon",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "구불창자동맥",
   "en": "sigmoid arteries",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "그 안에 간원인 대",
   "en": "round ligament of liver",
   "region": "abdomen"
  },
  {
   "ko": "그 주변은 관상인대",
   "en": "coronary ligament",
   "region": "abdomen"
  },
  {
   "ko": "그물막구멍",
   "en": "omental foramen",
   "region": "abdomen"
  },
  {
   "ko": "그물막주머니",
   "en": "omental bursa",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "근육 얇고 근육사이 얇은근막뿐이므로 주의하기 배바깥빗근",
   "en": "external abdominal oblique muscle",
   "region": "abdomen"
  },
  {
   "ko": "근처에서 얕은근막으로 나옴\n\n앞배벽아랫부분에서 얕은근막",
   "en": "superficial investing fascia",
   "region": "abdomen"
  },
  {
   "ko": "깊은고샅구멍",
   "en": "deep inguinal ring",
   "region": "abdomen"
  },
  {
   "ko": "깊은엉덩휘돌이동맥",
   "en": "deep circumflex iliac artery",
   "region": "abdomen"
  },
  {
   "ko": "꼬리엽",
   "en": "caudate lobe",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "나눔힘줄",
   "en": "tendinous intersections",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "난소정맥",
   "en": "ovarian vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "날문관",
   "en": "pyloric canal",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "날문방",
   "en": "pyloric antrum",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "날문부분",
   "en": "pyloric part",
   "region": "abdomen"
  },
  {
   "ko": "날문조임근",
   "en": "pyloric sphincter muscle",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "남자에서 두덩뼈결절 안쪽에서 아래쪽으로 음낭근육층",
   "en": "dartos tunic",
   "region": "abdomen"
  },
  {
   "ko": "낫인대",
   "en": "falciform ligament",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "내림창자",
   "en": "descending colon",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "내장면",
   "en": "visceral surface",
   "region": "abdomen"
  },
  {
   "ko": "내장면 뒤쪽에서 정맥관인대",
   "en": "ligamentum venosum",
   "region": "abdomen"
  },
  {
   "ko": "넙다리신경",
   "en": "femoral nerve",
   "region": "abdomen"
  },
  {
   "ko": "네모엽",
   "en": "quadrate lobe",
   "region": "abdomen"
  },
  {
   "ko": "눈물샘",
   "en": "lacrimal gland",
   "region": "abdomen"
  },
  {
   "ko": "눈물주머니",
   "en": "lacrimal sac",
   "region": "abdomen"
  },
  {
   "ko": "다리사이섬유",
   "en": "intercrural fiber",
   "region": "abdomen"
  },
  {
   "ko": "다소 노란색을 띠는 황반",
   "en": "macula",
   "region": "abdomen"
  },
  {
   "ko": "대동맥구멍",
   "en": "aortic hiatus",
   "region": "abdomen"
  },
  {
   "ko": "대정맥구멍",
   "en": "caval opening",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "더 아래로 내려가 오른위그물 막동맥",
   "en": "right gastroomental artery",
   "region": "abdomen"
  },
  {
   "ko": "덧이자관",
   "en": "accessory pancreatic duct",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "덩굴정맥얼기",
   "en": "pampiniform plexus",
   "region": "abdomen"
  },
  {
   "ko": "덮는 구조물들이 그대로 연장되어 고환 덮는 막됨 고환집막",
   "en": "tunica vaginalis",
   "region": "abdomen"
  },
  {
   "ko": "돌림주름",
   "en": "circular fold",
   "region": "abdomen"
  },
  {
   "ko": "돌막창자입술",
   "en": "",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "돌막창자판막",
   "en": "ileocecal recess valve",
   "region": "abdomen"
  },
  {
   "ko": "돌잘록창자동맥",
   "en": "ileocolic artery",
   "region": "abdomen"
  },
  {
   "ko": "돌잘록창자입술",
   "en": "",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "돌창자",
   "en": "ileum",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "돌창자구멍",
   "en": "ileal orifice",
   "region": "abdomen"
  },
  {
   "ko": "돌창자동맥",
   "en": "ileal artery",
   "region": "abdomen"
  },
  {
   "ko": "되도록 복막과 복막바깥근막",
   "en": "extraperitoneal fascia",
   "region": "abdomen"
  },
  {
   "ko": "두덩결합에서 배꼽까지 정중선에 있는 복막주름",
   "en": "peritoneal fold",
   "region": "abdomen"
  },
  {
   "ko": "두덩부위",
   "en": "public region",
   "region": "abdomen"
  },
  {
   "ko": "드러남 젖히고보면 얕은고샅구멍",
   "en": "superficial inguinal ring",
   "region": "abdomen"
  },
  {
   "ko": "들문부분",
   "en": "cardial part",
   "region": "abdomen"
  },
  {
   "ko": "뚫고나옴 가쪽배피부가지는 중간겨드랑선",
   "en": "midaxillary line",
   "region": "abdomen"
  },
  {
   "ko": "막창자",
   "en": "cecum",
   "region": "abdomen"
  },
  {
   "ko": "막창자간막",
   "en": "mesocecum",
   "region": "abdomen"
  },
  {
   "ko": "막창자꼬리",
   "en": "appendix",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "막창자꼬리간막",
   "en": "mesoappendix",
   "region": "abdomen"
  },
  {
   "ko": "막창자꼬리구멍",
   "en": "orifice of vermiform appendix",
   "region": "abdomen"
  },
  {
   "ko": "막창자꼬리동맥",
   "en": "appendicular artery",
   "region": "abdomen"
  },
  {
   "ko": "막층",
   "en": "membranous layer",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "맥과 왼간동맥이 일찍 나뉘어져 잘린모습으로 보임\n\n간문맥",
   "en": "hepatic portal vein",
   "region": "abdomen"
  },
  {
   "ko": "명치부위",
   "en": "epigastric region",
   "region": "abdomen"
  },
  {
   "ko": "무장막구역",
   "en": "bare area",
   "region": "abdomen"
  },
  {
   "ko": "바깥엉덩동맥",
   "en": "external iliac artery",
   "region": "abdomen"
  },
  {
   "ko": "바깥정삭근막",
   "en": "external spermatic fascia",
   "region": "abdomen"
  },
  {
   "ko": "반달선",
   "en": "linea semilunaris",
   "region": "abdomen"
  },
  {
   "ko": "방광위오목",
   "en": "supravesical fossa",
   "region": "abdomen"
  },
  {
   "ko": "방사선영상",
   "en": "ERCP",
   "region": "abdomen"
  },
  {
   "ko": "배가로근",
   "en": "transversus abdominis muscle",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "배가로근막",
   "en": "transversalis fascia",
   "region": "abdomen"
  },
  {
   "ko": "배곧은근",
   "en": "rectus abdominis muscle",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "배곧은근 나눔힘줄",
   "en": "tendinous intersection",
   "region": "abdomen"
  },
  {
   "ko": "배곧은근집",
   "en": "rectus sheath",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "배꼽부위",
   "en": "umbilical region",
   "region": "abdomen"
  },
  {
   "ko": "배꼽옆정맥",
   "en": "paraumbilical vein",
   "region": "abdomen"
  },
  {
   "ko": "배대동맥",
   "en": "abdominal aorta",
   "region": "abdomen"
  },
  {
   "ko": "배대동맥신경얼기",
   "en": "abdominal aortic plexus",
   "region": "abdomen"
  },
  {
   "ko": "배바깥빗근",
   "en": "external abdominal oblique muscle",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "배세모근",
   "en": "pyramidalis muscle",
   "region": "abdomen"
  },
  {
   "ko": "배속빗근",
   "en": "internal abdominal oblique muscle",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "배속빗근 널힘줄과 합쳐져 고샅낫힘줄",
   "en": "inguinal falx",
   "region": "abdomen"
  },
  {
   "ko": "백색선",
   "en": "linea alba",
   "region": "abdomen"
  },
  {
   "ko": "복강동맥",
   "en": "celiac trunk",
   "region": "abdomen"
  },
  {
   "ko": "복강신경얼기",
   "en": "celiac plexus",
   "region": "abdomen"
  },
  {
   "ko": "복막뒤기관",
   "en": "retroperitoneal organ",
   "region": "abdomen"
  },
  {
   "ko": "복막속기관",
   "en": "intraperitoneal organ",
   "region": "abdomen"
  },
  {
   "ko": "복막인대",
   "en": "peritoneal ligament",
   "region": "abdomen"
  },
  {
   "ko": "복막주렁",
   "en": "omental appendice",
   "region": "abdomen"
  },
  {
   "ko": "복장부분",
   "en": "sternal part",
   "region": "abdomen"
  },
  {
   "ko": "부고환",
   "en": "epididymis",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "부신",
   "en": "suprarenal gland",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "빈창자",
   "en": "jejunum",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "빈창자굽이를 가로막 오른다리에 고정시켜주는 샘창자걸 이근",
   "en": "suspensory muscle of duodenum",
   "region": "abdomen"
  },
  {
   "ko": "빈창자동맥",
   "en": "jejunal artery",
   "region": "abdomen"
  },
  {
   "ko": "빈창자와 돌창자를 앞으로 왼쪽으로 잡아당겨 창자간막뿌리",
   "en": "root of mesentery",
   "region": "abdomen"
  },
  {
   "ko": "빈창자와 만나는 샘빈창자굽이",
   "en": "duodenojejunal flexure",
   "region": "abdomen"
  },
  {
   "ko": "빗장뼈 중간 지나는 양쪽빗장중간선",
   "en": "midclavicular line",
   "region": "abdomen"
  },
  {
   "ko": "상이 맺히지 않으므로 맹점",
   "en": "blind spot",
   "region": "abdomen"
  },
  {
   "ko": "샘빈창자굽이",
   "en": "duodenojejunal flexure",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "샘창자",
   "en": "duodenum",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "샘창자걸이인대",
   "en": "suspensory muscle of duodenum",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "샘창자오목",
   "en": "duodenal recess",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "샘창자주름",
   "en": "duodenal fold",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "섬모체에 둘러 싸인 부분은 섬모체가장자리",
   "en": "ciliary margin",
   "region": "abdomen"
  },
  {
   "ko": "섬유피막",
   "en": "fibrous capsule",
   "region": "abdomen"
  },
  {
   "ko": "속정삭근막",
   "en": "internal spermatic fascia",
   "region": "abdomen"
  },
  {
   "ko": "속질",
   "en": "medulla",
   "region": "abdomen"
  },
  {
   "ko": "시각신경원반",
   "en": "optic disc",
   "region": "abdomen"
  },
  {
   "ko": "식도구멍",
   "en": "esophageal hiatus",
   "region": "abdomen"
  },
  {
   "ko": "쓸개",
   "en": "gall bladder",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "쓸개 속면 싸는 막은 나선주름",
   "en": "spiral fold",
   "region": "abdomen"
  },
  {
   "ko": "쓸개동맥",
   "en": "cystic artery",
   "region": "abdomen"
  },
  {
   "ko": "쓸개바닥",
   "en": "fundus of gallbladder",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "쓸개주머니관",
   "en": "cystic duct",
   "region": "abdomen"
  },
  {
   "ko": "아래가로막동맥",
   "en": "inferior phrenic artery",
   "region": "abdomen"
  },
  {
   "ko": "아래대정맥",
   "en": "inferior vena cava",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "아래로 내려가 코눈물관",
   "en": "nasolacrimal duct",
   "region": "abdomen"
  },
  {
   "ko": "아래배벽동맥",
   "en": "inferior epigastric artery",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "아래부신동맥",
   "en": "inferior suprarenal artery",
   "region": "abdomen"
  },
  {
   "ko": "아래아랫배신경얼기",
   "en": "inferior hypogastric plexus",
   "region": "abdomen"
  },
  {
   "ko": "아래이자샘창자동맥",
   "en": "inferior pancreaticoduodenal artery",
   "region": "abdomen"
  },
  {
   "ko": "아래창자간막동맥",
   "en": "inferior mesenteric artery",
   "region": "abdomen"
  },
  {
   "ko": "아래창자간막신경얼기",
   "en": "inferior mesenteric plexus",
   "region": "abdomen"
  },
  {
   "ko": "아래창자간막정맥",
   "en": "inferior mesenteric vein",
   "region": "abdomen"
  },
  {
   "ko": "안구 가장 속에 있는 망막",
   "en": "retina",
   "region": "abdomen"
  },
  {
   "ko": "안구뒤방",
   "en": "posterior chamber",
   "region": "abdomen"
  },
  {
   "ko": "안구섬유층",
   "en": "fibrous layer of eyeball",
   "region": "abdomen"
  },
  {
   "ko": "안구앞방",
   "en": "anterior chamber",
   "region": "abdomen"
  },
  {
   "ko": "안쪽고샅오목",
   "en": "medial inguinal fossa",
   "region": "abdomen"
  },
  {
   "ko": "안쪽눈꺼풀인대",
   "en": "medial palpebral ligament",
   "region": "abdomen"
  },
  {
   "ko": "안쪽다리",
   "en": "medial crus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "안쪽배꼽주름",
   "en": "medial umbilical fold",
   "region": "abdomen"
  },
  {
   "ko": "안쪽활꼴인대",
   "en": "medial arcuate ligament",
   "region": "abdomen"
  },
  {
   "ko": "앞서 보았던 두 관이 합쳐져 쓸개이자관팽대",
   "en": "hepatopancreatic ampulla",
   "region": "abdomen"
  },
  {
   "ko": "앞에서 세로로 잘라열어 돌창자구멍",
   "en": "ileal orifice",
   "region": "abdomen"
  },
  {
   "ko": "앞쪽에 홍채에 둘러싸여있는 빈부분이 동공",
   "en": "pupil",
   "region": "abdomen"
  },
  {
   "ko": "양쪽 열째갈비연골 아랫면 연결하는 갈비밑면",
   "en": "subcostal plane",
   "region": "abdomen"
  },
  {
   "ko": "양쪽엉덩뼈결절 사이 연결하는 결절사이면",
   "en": "intertubercular plane",
   "region": "abdomen"
  },
  {
   "ko": "얕은고샅구멍",
   "en": "superficial inguinal ring",
   "region": "abdomen"
  },
  {
   "ko": "얕은근막 자르고 아래가쪽 고샅인대방향 젖히면 배바깥빗근",
   "en": "external abdominal oblique muscle",
   "region": "abdomen"
  },
  {
   "ko": "얕은배벽동맥",
   "en": "superficial epigastric artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "얕은배벽정맥",
   "en": "superficial epigastric vein",
   "region": "abdomen"
  },
  {
   "ko": "얕은엉덩휘돌이동맥",
   "en": "superficial circumflex iliac artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "얕은엉덩휘돌이정맥",
   "en": "superifcial circumflex iliac vein",
   "region": "abdomen"
  },
  {
   "ko": "엄지맞섬근",
   "en": "opponens pollicis muscle",
   "region": "abdomen"
  },
  {
   "ko": "엉덩고샅신경",
   "en": "ilioinguinal nerve",
   "region": "abdomen"
  },
  {
   "ko": "엉덩아랫배신경",
   "en": "iliohypogastric nerve",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "에 돌잘록창자입술",
   "en": "ileocolic lip",
   "region": "abdomen"
  },
  {
   "ko": "에 위치하는 배바깥빗근 널힘줄에 의해 형성된 구멍 고샅관",
   "en": "inguinal canal",
   "region": "abdomen"
  },
  {
   "ko": "에는 근막 덮여있지 않음\n\n배벽아래부분에서 엉덩아랫배신경",
   "en": "iliohypogastric nerve",
   "region": "abdomen"
  },
  {
   "ko": "에서 지라콩팥인대",
   "en": "splenorenal ligament",
   "region": "abdomen"
  },
  {
   "ko": "여기로 덧이자관",
   "en": "accessory pancreatic duct",
   "region": "abdomen"
  },
  {
   "ko": "여러 개의 콩팥피라밋",
   "en": "renal pyramid",
   "region": "abdomen"
  },
  {
   "ko": "오른간관",
   "en": "right hepatic duct",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "오른간엽",
   "en": "right lobe of liver",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "오른갈비밑부위",
   "en": "right hypochondrium",
   "region": "abdomen"
  },
  {
   "ko": "오른고샅부위",
   "en": "right inguinal region",
   "region": "abdomen"
  },
  {
   "ko": "오른다리",
   "en": "right crust",
   "region": "abdomen"
  },
  {
   "ko": "오른아래가로막동맥",
   "en": "right inferior phrenic artery",
   "region": "abdomen"
  },
  {
   "ko": "오른옆구리부위",
   "en": "right flank",
   "region": "abdomen"
  },
  {
   "ko": "오른위그물막동맥",
   "en": "right gastroomental artery",
   "region": "abdomen"
  },
  {
   "ko": "오른위동맥",
   "en": "right gastric artery",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "오른잘록창자동맥",
   "en": "right colic artery",
   "region": "abdomen"
  },
  {
   "ko": "오른창자동맥",
   "en": "right colic artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "오름창자",
   "en": "ascending colon",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "오름허리정맥",
   "en": "ascending lumbar vein",
   "region": "abdomen"
  },
  {
   "ko": "온간관",
   "en": "common hepatic duct",
   "region": "abdomen"
  },
  {
   "ko": "온간동맥",
   "en": "common hepatic artery",
   "region": "abdomen"
  },
  {
   "ko": "온쓸개관",
   "en": "common bile duct",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "온엉덩동맥",
   "en": "common iliac artery",
   "region": "abdomen"
  },
  {
   "ko": "온엉덩정맥",
   "en": "common iliac vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "와 가로잘록창자간막",
   "en": "transverse mesocolon",
   "region": "abdomen"
  },
  {
   "ko": "와 간아 랫면에서 샘창자",
   "en": "duodenum",
   "region": "abdomen"
  },
  {
   "ko": "와 세모인대",
   "en": "triangular ligament",
   "region": "abdomen"
  },
  {
   "ko": "와 얕은음경근막",
   "en": "superficial fascia of penis",
   "region": "abdomen"
  },
  {
   "ko": "와 위지라인대",
   "en": "gastrosplenic ligament",
   "region": "abdomen"
  },
  {
   "ko": "왼간관",
   "en": "left hepatic duct",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "왼간동맥",
   "en": "hepatic artery",
   "region": "abdomen"
  },
  {
   "ko": "왼간엽",
   "en": "left lobe of liver",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "왼갈비밑부위",
   "en": "left hypochondrium",
   "region": "abdomen"
  },
  {
   "ko": "왼고샅부위",
   "en": "left inguinal region",
   "region": "abdomen"
  },
  {
   "ko": "왼다리",
   "en": "left crust",
   "region": "abdomen"
  },
  {
   "ko": "왼아래가로막동맥",
   "en": "left inferior phrenic artery",
   "region": "abdomen"
  },
  {
   "ko": "왼옆구리부위",
   "en": "left flank",
   "region": "abdomen"
  },
  {
   "ko": "왼위그물막동맥",
   "en": "left gastroomental artery",
   "region": "abdomen"
  },
  {
   "ko": "왼위동맥",
   "en": "left gastric artery",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "왼위정맥",
   "en": "left gastric vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "왼잘록창자동맥",
   "en": "left colic artery",
   "region": "abdomen"
  },
  {
   "ko": "왼창자동맥",
   "en": "left colic artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "왼콩팥정맥",
   "en": "left renal vein",
   "region": "abdomen"
  },
  {
   "ko": "위가로막인대",
   "en": "gastrophrenic ligament",
   "region": "abdomen"
  },
  {
   "ko": "위곧창자정맥",
   "en": "superior rectal vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "위몸통",
   "en": "body of stomach",
   "region": "abdomen"
  },
  {
   "ko": "위바닥",
   "en": "fundus of stomach",
   "region": "abdomen"
  },
  {
   "ko": "위배벽동맥",
   "en": "superior epigastric artery",
   "region": "abdomen"
  },
  {
   "ko": "위부분 사이 잇는 간샘창자인대",
   "en": "hepatoduodenal ligament",
   "region": "abdomen"
  },
  {
   "ko": "위부신동맥",
   "en": "superior suprarenal arteries",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "위샘창자동맥",
   "en": "gastroduodenal artery",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "위아랫배신경얼기",
   "en": "superior hypogastric plexus",
   "region": "abdomen"
  },
  {
   "ko": "위이자샘창자동맥",
   "en": "superior pancreaticoduodenal artery",
   "region": "abdomen"
  },
  {
   "ko": "위점막주름",
   "en": "gastric folds",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "위지라인대",
   "en": "gastrosplenic ligament",
   "region": "abdomen"
  },
  {
   "ko": "위창자간막동맥",
   "en": "superior mesenteric artery",
   "region": "abdomen"
  },
  {
   "ko": "위창자간막신경얼기",
   "en": "superior mesenteric plexus",
   "region": "abdomen"
  },
  {
   "ko": "위창자간막정맥",
   "en": "superior mesenteric vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "유리체",
   "en": "vitreous body",
   "region": "abdomen"
  },
  {
   "ko": "으로 들 어가고 여자의 난소동맥은 온엉덩동맥",
   "en": "common iliac artery",
   "region": "abdomen"
  },
  {
   "ko": "음낭",
   "en": "scrotum",
   "region": "abdomen"
  },
  {
   "ko": "음낭근육층",
   "en": "dartos muscle layer",
   "region": "abdomen"
  },
  {
   "ko": "음부넙다리신경",
   "en": "genitofemoral nerve",
   "region": "abdomen"
  },
  {
   "ko": "이 부위에서 치밀한 자율신경얼기",
   "en": "autonomic plexus",
   "region": "abdomen"
  },
  {
   "ko": "이 섬유들이 두덩뼈빗",
   "en": "pecten pubis",
   "region": "abdomen"
  },
  {
   "ko": "이들 구조물이 간샘창자인대",
   "en": "hepatoduodenal ligament",
   "region": "abdomen"
  },
  {
   "ko": "이자관",
   "en": "pancreatic duct",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "이자꼬리",
   "en": "tail of pancreas",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "이자머리",
   "en": "head of pancreas",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "이자몸통",
   "en": "body of pancreas",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "인 위입술과 돌막창자입술",
   "en": "ileocecal lip",
   "region": "abdomen"
  },
  {
   "ko": "인 음낭피부 매우 얇고 얕은근막에 단단히 붙어있음\n\n정관",
   "en": "ductus deferens",
   "region": "abdomen"
  },
  {
   "ko": "인대와 창자간막은 벽복막",
   "en": "parietal peritoneum",
   "region": "abdomen"
  },
  {
   "ko": "일곱째에서 열한째갈비신경과 갈비밑신경",
   "en": "subcostal nerve",
   "region": "abdomen"
  },
  {
   "ko": "자궁원인대",
   "en": "round ligament of uterus",
   "region": "abdomen"
  },
  {
   "ko": "작은굽이",
   "en": "lesser curvature",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "작은그물막",
   "en": "lesser omentum",
   "region": "abdomen"
  },
  {
   "ko": "작은그물막 또는 그 부분인 간샘창자인대",
   "en": "hepatoduodenal ligament",
   "region": "abdomen"
  },
  {
   "ko": "작은샘창자유두",
   "en": "minor duodenal papilla",
   "region": "abdomen"
  },
  {
   "ko": "작은콩팥잔",
   "en": "minor calices",
   "region": "abdomen"
  },
  {
   "ko": "작은허리근",
   "en": "psoas minor muscle",
   "region": "abdomen"
  },
  {
   "ko": "잘록창자띠",
   "en": "tenia coli",
   "region": "abdomen"
  },
  {
   "ko": "잘록창자팽대",
   "en": "haustra of colon",
   "region": "abdomen"
  },
  {
   "ko": "잘보존된 망막에서는 중심오목",
   "en": "fovea centralis",
   "region": "abdomen"
  },
  {
   "ko": "정관",
   "en": "ductus deferens",
   "region": "abdomen"
  },
  {
   "ko": "정도 되는 곳에서 위에서 아래로 연속적으로 배곧은근집",
   "en": "rectus sheath",
   "region": "abdomen"
  },
  {
   "ko": "정맥",
   "en": "testicular artery",
   "region": "abdomen"
  },
  {
   "ko": "정맥관인대",
   "en": "ligamentum venosum",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "정삭",
   "en": "spermatic cord",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "정중배꼽주름",
   "en": "median umbilical fold",
   "region": "abdomen"
  },
  {
   "ko": "정중엉치동맥",
   "en": "medial sacral artery",
   "region": "abdomen"
  },
  {
   "ko": "좁은공간에서 배속빗근 속면 지나는 아래쪽 갈 비사이신경",
   "en": "intercostal nerve",
   "region": "abdomen"
  },
  {
   "ko": "주변 근육부분과 이들 근육이 부착하는 가운데 중심널힘줄",
   "en": "central tendon",
   "region": "abdomen"
  },
  {
   "ko": "줄과 만나 서로 합쳐져 백색선 되는 것 확인\n\n배곧은근집",
   "en": "rectus sheath",
   "region": "abdomen"
  },
  {
   "ko": "중간부신동맥",
   "en": "middle suprarenal artery",
   "region": "abdomen"
  },
  {
   "ko": "중간잘록창자동맥",
   "en": "middle colic artery",
   "region": "abdomen"
  },
  {
   "ko": "중간창자동맥",
   "en": "middle colic artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "중심널힘줄",
   "en": "central tendon",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "지라 가로막면",
   "en": "diaphragmatic surface",
   "region": "abdomen"
  },
  {
   "ko": "지라동맥",
   "en": "splenic artery",
   "region": "abdomen"
  },
  {
   "ko": "지라문",
   "en": "splenic hilum",
   "region": "abdomen"
  },
  {
   "ko": "지라정맥",
   "en": "splenic vein",
   "region": "abdomen"
  },
  {
   "ko": "지방층",
   "en": "fatty layer",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "짧은엄지벌림근",
   "en": "abductor pollicis brevis muscle",
   "region": "abdomen"
  },
  {
   "ko": "짧은위동맥",
   "en": "short gastric artery",
   "region": "abdomen"
  },
  {
   "ko": "창자간막",
   "en": "mesentery",
   "region": "abdomen"
  },
  {
   "ko": "창자간막 부착된 맞은편 벽에 위치\n\n막창자",
   "en": "cecum",
   "region": "abdomen"
  },
  {
   "ko": "창자간막뿌리",
   "en": "root of mesentery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "창자동맥",
   "en": "intestinal artery",
   "region": "abdomen"
  },
  {
   "ko": "콩팥겉질",
   "en": "renal cortex",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "콩팥굴",
   "en": "renal sinus",
   "region": "abdomen"
  },
  {
   "ko": "콩팥근막",
   "en": "renal fascia",
   "region": "abdomen"
  },
  {
   "ko": "콩팥기둥",
   "en": "renal column",
   "region": "abdomen"
  },
  {
   "ko": "콩팥깔때기",
   "en": "renal pelvis",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "콩팥동맥",
   "en": "renal artery",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "콩팥문",
   "en": "hilum of kidney",
   "region": "abdomen"
  },
  {
   "ko": "콩팥속질",
   "en": "renal medulla",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "콩팥유두",
   "en": "renal papilla",
   "region": "abdomen"
  },
  {
   "ko": "콩팥정맥",
   "en": "renal vein",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "콩팥주위지방체",
   "en": "pararenal fat body",
   "region": "abdomen"
  },
  {
   "ko": "콩팥주위지방피막",
   "en": "perirenal fat capsule",
   "region": "abdomen"
  },
  {
   "ko": "콩팥피라밋",
   "en": "renal pyramid",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "콩팥피막",
   "en": "renal capsule",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "큰굽이",
   "en": "greater curvature",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "큰그물막",
   "en": "greater omentum",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "큰샘창자유두",
   "en": "major duodenal papilla",
   "region": "abdomen"
  },
  {
   "ko": "큰콩팥잔",
   "en": "major calices",
   "region": "abdomen"
  },
  {
   "ko": "큰허리근",
   "en": "psoas major muscle",
   "region": "abdomen"
  },
  {
   "ko": "통과하여 아래콧길",
   "en": "inferior nasal meatus",
   "region": "abdomen"
  },
  {
   "ko": "표면 덮고 계속되며 음경에서는 음경고리인대",
   "en": "fundiform ligament of penis",
   "region": "abdomen"
  },
  {
   "ko": "허리네모근",
   "en": "quadratus lumborum muscle",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "허리동맥",
   "en": "lumbar artery",
   "region": "abdomen"
  },
  {
   "ko": "허리부분",
   "en": "lumbar part",
   "region": "abdomen"
  },
  {
   "ko": "허리정맥",
   "en": "lumbar vein",
   "region": "abdomen"
  },
  {
   "ko": "홍채 합해서 포도막",
   "en": "uvea",
   "region": "abdomen"
  },
  {
   "ko": "활꼴선",
   "en": "arcuate line",
   "region": "abdomen"
  },
  {
   "ko": "가능한 고리판 가쪽에서 고리판절제술",
   "en": "laminectomy",
   "region": "back"
  },
  {
   "ko": "가시끝인대",
   "en": "supraspinous ligament",
   "region": "back"
  },
  {
   "ko": "가시사이인대",
   "en": "interspinous ligaments",
   "region": "back"
  },
  {
   "ko": "경막밑공간",
   "en": "subdural space",
   "region": "back"
  },
  {
   "ko": "경막바깥공간",
   "en": "epidural space",
   "region": "back"
  },
  {
   "ko": "과 가시돌기",
   "en": "spinous process",
   "region": "back"
  },
  {
   "ko": "뒤세로인대",
   "en": "posterior longitudinal ligament",
   "region": "back"
  },
  {
   "ko": "말총",
   "en": "cauda equina",
   "region": "back"
  },
  {
   "ko": "속척주정맥얼기",
   "en": "internal vertebral venous plexus",
   "region": "back"
  },
  {
   "ko": "와 가시끝인대",
   "en": "supraspinous ligament",
   "region": "back"
  },
  {
   "ko": "종말끈",
   "en": "filum terminale",
   "region": "back"
  },
  {
   "ko": "척수경막",
   "en": "spinal dura mater",
   "region": "back"
  },
  {
   "ko": "척수신경뿌리",
   "en": "spinal nerve root",
   "region": "back"
  },
  {
   "ko": "척수신경절",
   "en": "spinal ganglion",
   "region": "back"
  },
  {
   "ko": "척수신경줄기",
   "en": "trunk of spinal nerve",
   "region": "back"
  },
  {
   "ko": "척수연막",
   "en": "spinal pia mater",
   "region": "back"
  },
  {
   "ko": "척수원뿔",
   "en": "conus medullaris",
   "region": "back"
  },
  {
   "ko": "척추뼈고리판",
   "en": "lamina of vertebral arch",
   "region": "back"
  },
  {
   "ko": "척추사이구멍",
   "en": "intervertebral foramen",
   "region": "back"
  },
  {
   "ko": "척추사이원반",
   "en": "intervertebral disc",
   "region": "back"
  },
  {
   "ko": "치아인대",
   "en": "denticulate ligament",
   "region": "back"
  },
  {
   "ko": "황색인대",
   "en": "ligamenta flava",
   "region": "back"
  },
  {
   "ko": "가로정맥굴",
   "en": "transverse sinus",
   "region": "head"
  },
  {
   "ko": "가슴천자",
   "en": "thoracentesis",
   "region": "head"
  },
  {
   "ko": "가쪽곧은근",
   "en": "lateral rectus muscle",
   "region": "head"
  },
  {
   "ko": "가쪽눈구석",
   "en": "lateral angle of eye",
   "region": "head"
  },
  {
   "ko": "가쪽눈꺼풀연결",
   "en": "lateral palpebral commisure",
   "region": "head"
  },
  {
   "ko": "가쪽정맥주머니",
   "en": "lateral lacunae",
   "region": "head"
  },
  {
   "ko": "각막",
   "en": "cornea",
   "region": "head"
  },
  {
   "ko": "갈비뼈",
   "en": "ribs",
   "region": "head"
  },
  {
   "ko": "갓돌림신경",
   "en": "abducens nerve",
   "region": "head"
  },
  {
   "ko": "개 정 맥굴이 하나로 합쳐져 속뒤통수뼈융기에서 정맥굴합류",
   "en": "confluence of sinuses",
   "region": "head"
  },
  {
   "ko": "거미막",
   "en": "arachnoid mater",
   "region": "head"
  },
  {
   "ko": "거미막과립",
   "en": "arachnoid granulation",
   "region": "head"
  },
  {
   "ko": "거미막밑공간",
   "en": "subarachnoid space",
   "region": "head"
  },
  {
   "ko": "결막",
   "en": "conjunctiva",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "경막",
   "en": "dura mater",
   "region": "head"
  },
  {
   "ko": "경막정맥굴",
   "en": "dural venous sinus",
   "region": "head"
  },
  {
   "ko": "고막",
   "en": "tympanic membrane",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "고막배꼽",
   "en": "umbo of tympanic membrane",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "고실",
   "en": "tympanic cavity",
   "region": "head"
  },
  {
   "ko": "고실끈신경",
   "en": "chorda tympani",
   "region": "head"
  },
  {
   "ko": "고실천장",
   "en": "tegmental wall",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "고유고실",
   "en": "tympanic cavity proper",
   "region": "head"
  },
  {
   "ko": "곧은정맥굴",
   "en": "straight sinus",
   "region": "head"
  },
  {
   "ko": "공막",
   "en": "sclera",
   "region": "head",
   "priority": "high"
  },
  {
   "ko": "과 고실위쪽 고실위오목",
   "en": "epitympanic recess",
   "region": "head"
  },
  {
   "ko": "과 보다 안쪽으로 주행하는 도르래위신경",
   "en": "supratrochlear nerve",
   "region": "head"
  },
  {
   "ko": "관상봉합",
   "en": "coronal suture",
   "region": "head"
  },
  {
   "ko": "관자뼈 광대풀기",
   "en": "aygomaatic process of temparal bone",
   "region": "head"
  },
  {
   "ko": "구불정맥굴",
   "en": "sigmoid sinus",
   "region": "head"
  },
  {
   "ko": "귀관융기",
   "en": "torus tubarius",
   "region": "head",
   "priority": "high"
  },
  {
   "ko": "귀관인두구멍",
   "en": "pharyngeal opening of auditory tube",
   "region": "head",
   "priority": "high"
  },
  {
   "ko": "귀관편도",
   "en": "tubal tonsil",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "귓속뼈",
   "en": "auditory ossicles",
   "region": "head"
  },
  {
   "ko": "그 뒤 눈돌림신경",
   "en": "oculomotor nerve",
   "region": "head"
  },
  {
   "ko": "그 뒤 정중면에 위치한 뇌하수체줄기",
   "en": "hypophyseal stalk",
   "region": "head"
  },
  {
   "ko": "그사이 눈꺼풀틈새",
   "en": "palpebral fissure",
   "region": "head"
  },
  {
   "ko": "그어진 선 따라 머리뼈 바깥판",
   "en": "outer table",
   "region": "head"
  },
  {
   "ko": "긴섬모체신경",
   "en": "long ciliary nerve",
   "region": "head"
  },
  {
   "ko": "꼭지방어귀",
   "en": "aditus to mastoid antrum",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "나비굴",
   "en": "sphenoidal sinus",
   "region": "head"
  },
  {
   "ko": "나비굴구멍",
   "en": "aperture of sphenoidal sinus",
   "region": "head"
  },
  {
   "ko": "날개관신경",
   "en": "nerve of pterygoid canal",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "날개입천장신경절",
   "en": "pterygopalatine ganglion",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "뇌막동맥구멍",
   "en": "foramen spinosum",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "뇌바닥동맥",
   "en": "basilar artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈꺼풀결막",
   "en": "palpebral conjuctiva",
   "region": "head"
  },
  {
   "ko": "눈꺼풀의 눈꺼풀판",
   "en": "tarsus",
   "region": "head"
  },
  {
   "ko": "눈꺼풀판",
   "en": "tarsus",
   "region": "head"
  },
  {
   "ko": "눈돌림신경",
   "en": "oculomotor nerve",
   "region": "head"
  },
  {
   "ko": "눈동맥",
   "en": "ophthalmic artery",
   "region": "head"
  },
  {
   "ko": "눈둘레근",
   "en": "orbicularis oculi muscle",
   "region": "head"
  },
  {
   "ko": "눈물못",
   "en": "lacrimal lake",
   "region": "head"
  },
  {
   "ko": "눈물샘신경",
   "en": "lacrimal nerve",
   "region": "head"
  },
  {
   "ko": "눈물소관",
   "en": "lacrimal canaliculus",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈물언덕",
   "en": "lacrimal caruncle",
   "region": "head"
  },
  {
   "ko": "눈물유두",
   "en": "lacrimal papilla",
   "region": "head"
  },
  {
   "ko": "눈물점",
   "en": "lacrimal punctum",
   "region": "head"
  },
  {
   "ko": "눈살금",
   "en": "procerus muscle",
   "region": "head"
  },
  {
   "ko": "눈확뼈막",
   "en": "periorbita",
   "region": "head"
  },
  {
   "ko": "눈확사이막",
   "en": "orbital septum",
   "region": "head"
  },
  {
   "ko": "눈확위구멍",
   "en": "supraorbital foramen",
   "region": "head"
  },
  {
   "ko": "눈확위신경",
   "en": "supraorbital nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈확위패임",
   "en": "supraorbital notch",
   "region": "head"
  },
  {
   "ko": "눈확천장",
   "en": "obital roof",
   "region": "head"
  },
  {
   "ko": "대뇌낫",
   "en": "falx cerebri",
   "region": "head"
  },
  {
   "ko": "대뇌정맥",
   "en": "cerebral vein",
   "region": "head"
  },
  {
   "ko": "더듬자 사용하여 볏돌기 양 옆 벌집뼈체판",
   "en": "ethmoid cribriform plate",
   "region": "head"
  },
  {
   "ko": "도르래",
   "en": "trochlea",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "도르래신경",
   "en": "trochlear nerve",
   "region": "head"
  },
  {
   "ko": "도르래아래신경",
   "en": "infratrochlear nerve",
   "region": "head"
  },
  {
   "ko": "도르래위신경",
   "en": "supratrochlear nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "동공",
   "en": "pupil",
   "region": "head"
  },
  {
   "ko": "뒤교통동맥",
   "en": "posterior communicating artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "뒤대뇌동맥",
   "en": "posterior cerebral artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "뒤머리뼈우묵",
   "en": "posterior cranial fossa",
   "region": "head"
  },
  {
   "ko": "뒤벌집신경",
   "en": "posterior ethmoidal nerve",
   "region": "head"
  },
  {
   "ko": "뒤아래소뇌동맥",
   "en": "anterior and posterior inferior cerebellar artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "뒤쪽으로는 꼭지방어귀",
   "en": "aditus to mastoid antrum",
   "region": "head"
  },
  {
   "ko": "뒤콧구멍",
   "en": "choana",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "뒤통수정맥굴",
   "en": "occipital sinus",
   "region": "head"
  },
  {
   "ko": "등자뼈",
   "en": "stapes",
   "region": "head"
  },
  {
   "ko": "망막",
   "en": "retina",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "망치모루관절",
   "en": "incudomallear joint",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "망치뼈",
   "en": "malleus",
   "region": "head"
  },
  {
   "ko": "맥락막",
   "en": "choroid",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "머리덮개널힘줄",
   "en": "epicranial aponeurosis",
   "region": "head"
  },
  {
   "ko": "머리덮개뼈 위뒤방향으로 당겨 뇌경막",
   "en": "cranial dura mater",
   "region": "head"
  },
  {
   "ko": "머리뼈 관자놀이점",
   "en": "pterion",
   "region": "head"
  },
  {
   "ko": "머리뼈 속면 덮는 실제적 뼈막인 뼈막층",
   "en": "periosteal layer",
   "region": "head"
  },
  {
   "ko": "모루뼈",
   "en": "incus",
   "region": "head"
  },
  {
   "ko": "목가지",
   "en": "cervical branch",
   "region": "head"
  },
  {
   "ko": "목가지는 여러개\n귀밑샘관",
   "en": "paroid duct",
   "region": "head"
  },
  {
   "ko": "목구멍",
   "en": "fauces",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "목동맥관",
   "en": "carotid canal",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "목뿔혀근",
   "en": "hyoglossus muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "목정맥구멍",
   "en": "jugular foramen",
   "region": "head"
  },
  {
   "ko": "목정맥오목",
   "en": "jugular fossa",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "무 깊이 자르는 경우 뇌막 과 뇌 손상가능하므로 판사이층",
   "en": "diploe",
   "region": "head"
  },
  {
   "ko": "무릎신경절",
   "en": "geniculate ganglion",
   "region": "head"
  },
  {
   "ko": "미로동맥",
   "en": "labyrinthine arteries",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "바깥뒤통수뼈융기",
   "en": "",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "벌집뼈수직판",
   "en": "perpendicular plate",
   "region": "head"
  },
  {
   "ko": "볏돌기",
   "en": "crista galli",
   "region": "head"
  },
  {
   "ko": "보습뼈",
   "en": "vomer",
   "region": "head"
  },
  {
   "ko": "복장뼈각",
   "en": "sternal angle",
   "region": "head"
  },
  {
   "ko": "복장뼈칼돌기",
   "en": "xiphoid process",
   "region": "head"
  },
  {
   "ko": "볼가지",
   "en": "buacal branch",
   "region": "head"
  },
  {
   "ko": "부교감신경섬유",
   "en": "parasympathetic fiber",
   "region": "head"
  },
  {
   "ko": "부분에서 머리마루점",
   "en": "vertex",
   "region": "head"
  },
  {
   "ko": "분계고랑",
   "en": "terminal sulcus",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "삼차신경",
   "en": "trigeminal nerve",
   "region": "head"
  },
  {
   "ko": "섬모체",
   "en": "ciliary body",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "섬모체신경절",
   "en": "ciliary ganglion",
   "region": "head"
  },
  {
   "ko": "성곽유두",
   "en": "vallate papilla",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "셋째큰어금니",
   "en": "third molar tooth",
   "region": "head"
  },
  {
   "ko": "소뇌낫",
   "en": "falx cerebelli",
   "region": "head"
  },
  {
   "ko": "소뇌천막",
   "en": "tentorium cerebelli",
   "region": "head"
  },
  {
   "ko": "속귀 뼈미로",
   "en": "bony labyrinth",
   "region": "head"
  },
  {
   "ko": "속귀신경",
   "en": "vestibulocochlear nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "속귓구멍",
   "en": "internal acoustic opening",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "속목동맥",
   "en": "internal carotid artery",
   "region": "head"
  },
  {
   "ko": "속목정맥",
   "en": "internal jugular vein",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "수막층",
   "en": "meningeal layer",
   "region": "head"
  },
  {
   "ko": "수정체",
   "en": "lens",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "시각신경",
   "en": "optic nerve",
   "region": "head",
   "priority": "high"
  },
  {
   "ko": "시각신경관",
   "en": "optic canal",
   "region": "head"
  },
  {
   "ko": "시상봉합",
   "en": "sagittal suture",
   "region": "head"
  },
  {
   "ko": "시옷봉합",
   "en": "lambdoid suture",
   "region": "head"
  },
  {
   "ko": "시옷점",
   "en": "lambda",
   "region": "head"
  },
  {
   "ko": "아래결막구석",
   "en": "inferior conjuctival fornix",
   "region": "head"
  },
  {
   "ko": "아래곧은근",
   "en": "inferior rectus muscle",
   "region": "head"
  },
  {
   "ko": "아래눈꺼풀",
   "en": "lower eyelid",
   "region": "head"
  },
  {
   "ko": "아래빗근",
   "en": "inferior oblique muscle",
   "region": "head"
  },
  {
   "ko": "아래시상정맥굴",
   "en": "inferior sagittal sinus",
   "region": "head"
  },
  {
   "ko": "아래입술내림",
   "en": "depressor labii inferioris muscle",
   "region": "head"
  },
  {
   "ko": "아래입술내림근",
   "en": "depressor labii inferioris muscle",
   "region": "head"
  },
  {
   "ko": "아래턱뼈 관철들기 관대팝",
   "en": "candylar process ofmandible",
   "region": "head"
  },
  {
   "ko": "아래턱신경",
   "en": "mandibular nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "안 장가로막",
   "en": "diaphragma sellae",
   "region": "head"
  },
  {
   "ko": "안구결막",
   "en": "bulbar conjuctiva",
   "region": "head"
  },
  {
   "ko": "안쪽곧은근",
   "en": "medial rectus muscle",
   "region": "head"
  },
  {
   "ko": "안쪽눈구석",
   "en": "medial angle of eye",
   "region": "head"
  },
  {
   "ko": "안쪽눈꺼풀연결",
   "en": "medial palpebral commissure",
   "region": "head"
  },
  {
   "ko": "앞교통동맥",
   "en": "anterior communicating artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "앞니관",
   "en": "incisive canal",
   "region": "head"
  },
  {
   "ko": "앞대뇌동맥",
   "en": "anterior cerebral artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "앞벌집",
   "en": "anterior ethmoidal cells",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "앞벌집신경",
   "en": "anterior ethmoidal nerve",
   "region": "head"
  },
  {
   "ko": "앞쪽 볏돌기",
   "en": "crista galli",
   "region": "head"
  },
  {
   "ko": "앞쪽으로 벌집뼈",
   "en": "ethmoid bone",
   "region": "head"
  },
  {
   "ko": "앞쪽으로 추적하면 계속 똑바로 주행하는 더 큰 눈확위신경",
   "en": "supraorbital nerve",
   "region": "head"
  },
  {
   "ko": "얼굴동맥",
   "en": "facial artery",
   "region": "head"
  },
  {
   "ko": "얼굴신경",
   "en": "facial nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "얼굴신경의 목가지",
   "en": "cervical branch",
   "region": "head"
  },
  {
   "ko": "에 세로로 달리는 눈살근",
   "en": "procerus muscle",
   "region": "head"
  },
  {
   "ko": "연막",
   "en": "pia mater",
   "region": "head"
  },
  {
   "ko": "온힘줄고리",
   "en": "common tendinous ring",
   "region": "head"
  },
  {
   "ko": "위 턱뼈 코능선",
   "en": "nasal crest",
   "region": "head"
  },
  {
   "ko": "위결막구석",
   "en": "superior conjuctival fornix",
   "region": "head"
  },
  {
   "ko": "위곧은근",
   "en": "superior rectus muscle",
   "region": "head"
  },
  {
   "ko": "위눈꺼풀",
   "en": "upper eyelid",
   "region": "head"
  },
  {
   "ko": "위눈꺼풀올림근",
   "en": "levator palpebrae superioris muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "위눈정맥",
   "en": "superior ophthalmic vein",
   "region": "head"
  },
  {
   "ko": "위눈확틈새",
   "en": "superior orbital fissure",
   "region": "head"
  },
  {
   "ko": "위목정맥팽대",
   "en": "superior bulb of jugular vein",
   "region": "head"
  },
  {
   "ko": "위바위정맥굴",
   "en": "superior petrosal sinus",
   "region": "head"
  },
  {
   "ko": "위빗근",
   "en": "superior oblique muscle",
   "region": "head",
   "priority": "high"
  },
  {
   "ko": "위소뇌동맥",
   "en": "superior cerebellar artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "위시상정맥굴",
   "en": "superior sagittal sinus",
   "region": "head"
  },
  {
   "ko": "위에 놓인 후각망울",
   "en": "olfactory bulb",
   "region": "head"
  },
  {
   "ko": "위입술올림근",
   "en": "levator labit superioris muscle",
   "region": "head"
  },
  {
   "ko": "위입술콧방울올림근",
   "en": "levator labii superforts alaeque nasi muscle",
   "region": "head"
  },
  {
   "ko": "위코선반",
   "en": "superior nasal concha",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "위콧길",
   "en": "superior nasal meatus",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "위턱굴",
   "en": "maxillary sinus",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "이 시신에서는 머 리덮개의 뼈막",
   "en": "periost",
   "region": "head"
  },
  {
   "ko": "이 신경들 손상하지 않으면서 지방 제거하여 위눈꺼풀올림근",
   "en": "levator palpebrae superioris muscle",
   "region": "head"
  },
  {
   "ko": "이것은 눈썹주름근",
   "en": "corrugator supercilii muscle",
   "region": "head"
  },
  {
   "ko": "이를 통해 눈확안 주행하는 이마신경",
   "en": "frontal nerve",
   "region": "head"
  },
  {
   "ko": "이마가지",
   "en": "frontal branch",
   "region": "head"
  },
  {
   "ko": "이마굴",
   "en": "ethmoidal cells",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "이마뼈",
   "en": "frontal bone",
   "region": "head"
  },
  {
   "ko": "이마신경",
   "en": "frontal nerve",
   "region": "head",
   "priority": "high"
  },
  {
   "ko": "인두편도",
   "en": "pharyngeal tonsil",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "입꼬리당김근",
   "en": "risorius muscle",
   "region": "head"
  },
  {
   "ko": "입꼬리올림근",
   "en": "levator anguli oris muscle",
   "region": "head"
  },
  {
   "ko": "입인두",
   "en": "Oropharynx",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "입천장뼈",
   "en": "palatine bone",
   "region": "head"
  },
  {
   "ko": "입천장올림근",
   "en": "levator veli palatini muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "작은광대근",
   "en": "zygomaticus minor muscle",
   "region": "head"
  },
  {
   "ko": "정수리점",
   "en": "bregma",
   "region": "head"
  },
  {
   "ko": "주행방향\n얼굴동맥",
   "en": "facial artery",
   "region": "head"
  },
  {
   "ko": "중간뇌막동맥",
   "en": "middle meningeal artery",
   "region": "head"
  },
  {
   "ko": "중간대뇌동맥",
   "en": "middle cerebral artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "중간벌집",
   "en": "middle ethmoidal cells",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "중간코선반",
   "en": "middle nasal concha",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "중간콧길",
   "en": "middle nasal meatus",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "중심오목",
   "en": "fovea centralis",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "즉 바닥이 달팽이의 타원창",
   "en": "vestibular window",
   "region": "head"
  },
  {
   "ko": "지나 바깥뒤통수뼈융기",
   "en": "external occipital protuberance",
   "region": "head"
  },
  {
   "ko": "짧은섬모체신경",
   "en": "short ciliary nerve",
   "region": "head"
  },
  {
   "ko": "천막패임",
   "en": "tentorial notch",
   "region": "head"
  },
  {
   "ko": "체판",
   "en": "cribriform plate",
   "region": "head"
  },
  {
   "ko": "코뼈",
   "en": "nasal bone",
   "region": "head"
  },
  {
   "ko": "코뿌리점",
   "en": "nasion",
   "region": "head"
  },
  {
   "ko": "코섬모체신경",
   "en": "nasociliary nerve",
   "region": "head"
  },
  {
   "ko": "코중격",
   "en": "nasal septum",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "코중격연골",
   "en": "septal cartilage",
   "region": "head"
  },
  {
   "ko": "콧구멍",
   "en": "nares",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "콧등",
   "en": "dorsum of nose",
   "region": "head"
  },
  {
   "ko": "큰구멍",
   "en": "foramen magnum",
   "region": "head"
  },
  {
   "ko": "큰바위신경",
   "en": "greater petrosal nerve",
   "region": "head"
  },
  {
   "ko": "큰입천장신경",
   "en": "greater palatine nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "큰콧방은연골",
   "en": "majorcalar carilage",
   "region": "head"
  },
  {
   "ko": "타원구멍",
   "en": "foramen ovale",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "택보서리가지",
   "en": "marginal mandibular branch",
   "region": "head"
  },
  {
   "ko": "턱끝근",
   "en": "mentalis muscle",
   "region": "head"
  },
  {
   "ko": "턱끝신경",
   "en": "mental nerve",
   "region": "head"
  },
  {
   "ko": "턱끝혀근",
   "en": "genioglossus muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "턱밑샘",
   "en": "submandibular gland",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "턱밑신경절",
   "en": "submandibular ganglion",
   "region": "head"
  },
  {
   "ko": "턱뼈패임\n아래턱뼈 근육들기",
   "en": "mandibutar match",
   "region": "head"
  },
  {
   "ko": "피부밑조직",
   "en": "subcutaneous tissue",
   "region": "head"
  },
  {
   "ko": "해면정맥굴",
   "en": "cavernous sinus",
   "region": "head"
  },
  {
   "ko": "해부 전 결막주머니",
   "en": "conjuctival sac",
   "region": "head"
  },
  {
   "ko": "혀등",
   "en": "dorsum of tongue",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "혀막구멍",
   "en": "foramen cecum",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "혀밑샘",
   "en": "sublingual gland",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "혀밑신경관",
   "en": "hypoglossal canal",
   "region": "head"
  },
  {
   "ko": "혀밑언덕",
   "en": "sublingual caruncle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "혀밑주름",
   "en": "sublingual fold",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "혀신경",
   "en": "lingual nerve",
   "region": "head",
   "priority": "high"
  },
  {
   "ko": "혀정중고랑",
   "en": "midline sulcus of tongue",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "혹은 미간",
   "en": "glabella",
   "region": "head"
  },
  {
   "ko": "홍채",
   "en": "iris",
   "region": "head"
  },
  {
   "ko": "확 속 사이 나누는 막으로 눈확모서리에 부착하여 눈확뼈막",
   "en": "periobita",
   "region": "head"
  },
  {
   "ko": "황반",
   "en": "macula",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "후각신경",
   "en": "olfactory nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "후각신경섬유",
   "en": "olfactory nerve fiber",
   "region": "head"
  },
  {
   "ko": "후두인두",
   "en": "Laryngopharynx",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "가쪽무릎지지띠",
   "en": "lateral patellar retinaculum",
   "region": "lower-limb"
  },
  {
   "ko": "가쪽발바닥신경",
   "en": "lateral plantar nerve",
   "region": "lower-limb"
  },
  {
   "ko": "개의 바닥쪽발허리동맥",
   "en": "plantar metatarsal artery",
   "region": "lower-limb"
  },
  {
   "ko": "과 긴엄지굽힘근",
   "en": "flexor hallucis longus muscle",
   "region": "lower-limb"
  },
  {
   "ko": "과 발안쪽모서리 차례로 지나 발로 들어온 후 발배뼈거친면",
   "en": "tuberosity of navicular",
   "region": "lower-limb"
  },
  {
   "ko": "과 안쪽 쐐기뼈",
   "en": "medial cuneiform",
   "region": "lower-limb"
  },
  {
   "ko": "교통가지",
   "en": "rami communicantes",
   "region": "lower-limb"
  },
  {
   "ko": "굽힘근지지띠 열어젖히고 그 안에서 힘줄들이 힘줄윤활집",
   "en": "synovial tendon sheath",
   "region": "lower-limb"
  },
  {
   "ko": "굽힘근지지띠 전후로 긴발가락굽힘근",
   "en": "flexor digitorum longus muscle",
   "region": "lower-limb"
  },
  {
   "ko": "궁둥넙다리인대",
   "en": "ischiofemoral ligament",
   "region": "lower-limb"
  },
  {
   "ko": "긴발가락굽힘근",
   "en": "flexor digitorum longus muscle",
   "region": "lower-limb"
  },
  {
   "ko": "긴발가락굽힘근 힘줄은 끝마디뼈",
   "en": "distal phalanx",
   "region": "lower-limb"
  },
  {
   "ko": "긴발바닥인대",
   "en": "long plantar ligament",
   "region": "lower-limb"
  },
  {
   "ko": "긴엄지굽힘근",
   "en": "flexor hallucis longus muscle",
   "region": "lower-limb",
   "priority": "high"
  },
  {
   "ko": "긴종아리근",
   "en": "fibularis longus muscle",
   "region": "lower-limb"
  },
  {
   "ko": "깊은발바닥동맥활",
   "en": "deep plantar arch",
   "region": "lower-limb"
  },
  {
   "ko": "깊은부분은 반달",
   "en": "meniscus",
   "region": "lower-limb"
  },
  {
   "ko": "두덩넙다리인대",
   "en": "pubofemoral ligament",
   "region": "lower-limb"
  },
  {
   "ko": "두종아리근 힘줄이 온힘줄집",
   "en": "common tendinous sheath",
   "region": "lower-limb"
  },
  {
   "ko": "뒤로는 발꿈치뼈 아랫면 전체에 붙고 앞으로는 입방뼈거친면",
   "en": "tuberosity of cuboid",
   "region": "lower-limb"
  },
  {
   "ko": "뒤십자인대",
   "en": "posterior cruciate ligament",
   "region": "lower-limb"
  },
  {
   "ko": "뒤정강근",
   "en": "tibialis posterior muscle",
   "region": "lower-limb"
  },
  {
   "ko": "무릎가로인대",
   "en": "transverse ligament of knee",
   "region": "lower-limb"
  },
  {
   "ko": "무릎위주머니",
   "en": "suprapatellar bursa",
   "region": "lower-limb"
  },
  {
   "ko": "바깥폐쇄근",
   "en": "obturator externus muscle",
   "region": "lower-limb"
  },
  {
   "ko": "바닥쪽 뼈사이근",
   "en": "dorsal and palmar interossei muscle",
   "region": "lower-limb"
  },
  {
   "ko": "반달",
   "en": "meniscus",
   "region": "lower-limb"
  },
  {
   "ko": "발바닥근막",
   "en": "plantar fascia",
   "region": "lower-limb"
  },
  {
   "ko": "발바닥널힘줄",
   "en": "plantar aponeurosis",
   "region": "lower-limb"
  },
  {
   "ko": "발바닥네모근",
   "en": "quadratus plantae muscle",
   "region": "lower-limb"
  },
  {
   "ko": "발바닥으로 들어가면서 목말받침돌기",
   "en": "sustentaculum tali",
   "region": "lower-limb"
  },
  {
   "ko": "벌레근",
   "en": "lumbrical muscle",
   "region": "lower-limb"
  },
  {
   "ko": "빗갈래",
   "en": "oblique head",
   "region": "lower-limb"
  },
  {
   "ko": "빗오금인대",
   "en": "oblique popliteal ligament",
   "region": "lower-limb"
  },
  {
   "ko": "세모인대",
   "en": "triangular ligament",
   "region": "lower-limb"
  },
  {
   "ko": "십자인대",
   "en": "cruciate ligament",
   "region": "lower-limb"
  },
  {
   "ko": "아래종아리근지지띠",
   "en": "inferior fibular retinaculum",
   "region": "lower-limb"
  },
  {
   "ko": "아래쪽에서 발꿈치뼈 가쪽면에 있는 종아리근도르래",
   "en": "fibular trochlea",
   "region": "lower-limb"
  },
  {
   "ko": "안쪽무릎지지띠",
   "en": "medial patellar retinaculum",
   "region": "lower-limb"
  },
  {
   "ko": "앞십자인대",
   "en": "anterior cruciate ligament",
   "region": "lower-limb"
  },
  {
   "ko": "얕은가로발허리인대",
   "en": "superficial transverse metatarsal ligament",
   "region": "lower-limb"
  },
  {
   "ko": "얕은종아리신경",
   "en": "superficial fibular nerve",
   "region": "lower-limb"
  },
  {
   "ko": "엄지모음근",
   "en": "adductor hallucis muscle",
   "region": "lower-limb"
  },
  {
   "ko": "엉덩넙다리인대",
   "en": "iliofemoral ligament",
   "region": "lower-limb"
  },
  {
   "ko": "위오목",
   "en": "superior recess",
   "region": "lower-limb"
  },
  {
   "ko": "위종아리근지지띠",
   "en": "superior fibular retinaculum",
   "region": "lower-limb"
  },
  {
   "ko": "음부가지",
   "en": "genital branch",
   "region": "lower-limb"
  },
  {
   "ko": "음핵몸통",
   "en": "body of clitoris",
   "region": "lower-limb"
  },
  {
   "ko": "의 가로갈래",
   "en": "transverse head",
   "region": "lower-limb"
  },
  {
   "ko": "절구가로인대",
   "en": "transverse acetabular ligament",
   "region": "lower-limb"
  },
  {
   "ko": "절구테두리",
   "en": "acetabular labrum",
   "region": "lower-limb"
  },
  {
   "ko": "종아리근 지지띠",
   "en": "fibular retinaculum",
   "region": "lower-limb"
  },
  {
   "ko": "질긴 섬유띠",
   "en": "lemniscus",
   "region": "lower-limb"
  },
  {
   "ko": "짧은발가락굽힘근 힘줄은 중간마디뼈",
   "en": "middle phalanx",
   "region": "lower-limb"
  },
  {
   "ko": "짧은새끼굽힘근",
   "en": "flexor digiti minimi brevis muscle",
   "region": "lower-limb"
  },
  {
   "ko": "짧은엄지굽힘근",
   "en": "flexor hallucis brevis muscle",
   "region": "lower-limb"
  },
  {
   "ko": "짧은종아리근",
   "en": "fibularis brevis muscle",
   "region": "lower-limb"
  },
  {
   "ko": "큰허리근주머니",
   "en": "psoas bursa",
   "region": "lower-limb"
  },
  {
   "ko": "폐쇄막",
   "en": "obturator membrane",
   "region": "lower-limb"
  },
  {
   "ko": "폐쇄신경",
   "en": "obturator nerve",
   "region": "lower-limb"
  },
  {
   "ko": "허리신경얼기",
   "en": "lumbar plexus",
   "region": "lower-limb"
  },
  {
   "ko": "허리신경절",
   "en": "lumbar ganglia",
   "region": "lower-limb"
  },
  {
   "ko": "활꼴오금인대",
   "en": "arcuate popliteal ligament",
   "region": "lower-limb"
  },
  {
   "ko": "대동맥환",
   "en": "aortic arch",
   "region": "multi"
  },
  {
   "ko": "위대정맥",
   "en": "superion vena cava",
   "region": "multi"
  },
  {
   "ko": "가로막신경",
   "en": "phrenic nerve",
   "region": "neck"
  },
  {
   "ko": "가로모뿔근",
   "en": "transverse arytenoid muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "가로목동맥",
   "en": "transverse cervical artery",
   "region": "neck"
  },
  {
   "ko": "가지인 갑상목동맥",
   "en": "thyrocervical trunk",
   "region": "neck"
  },
  {
   "ko": "가쪽반지모뿔근",
   "en": "lateral cricoarytenoid muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "가쪽방패목뿔인대",
   "en": "lateral thyrohyoid ligament",
   "region": "neck"
  },
  {
   "ko": "각각의 콧길이 코인두길과 뒤콧구멍",
   "en": "choanae",
   "region": "neck"
  },
  {
   "ko": "갑상목동맥",
   "en": "thyrocervical trunk",
   "region": "neck"
  },
  {
   "ko": "거짓성대",
   "en": "false vocal cord",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "과 그보다 깊이 가로로 주행하는 가로모뿔근",
   "en": "transverse arytenoid muscle",
   "region": "neck"
  },
  {
   "ko": "과 뒤로넘어가는 맨위갈비사이동맥",
   "en": "supreme intercostal artery",
   "region": "neck"
  },
  {
   "ko": "귀관인두근",
   "en": "salpingopharyngeus muscle",
   "region": "neck"
  },
  {
   "ko": "귀관인두주름",
   "en": "salpingopharyngeal fold",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "귀인두관구멍",
   "en": "pharyngeal opening of auditory tube",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "그 벽은 밖에서 안으로 볼인두근막",
   "en": "buccopharyngeal fascia",
   "region": "neck"
  },
  {
   "ko": "그 사이는 갑상샘잘록",
   "en": "isthmus",
   "region": "neck"
  },
  {
   "ko": "근육층",
   "en": "muscle layer",
   "region": "neck"
  },
  {
   "ko": "기관 앞에서 갑상샘잘록 아래로 내려가 팔머리정맥",
   "en": "brachiocephalic vein",
   "region": "neck"
  },
  {
   "ko": "나비벌집오목",
   "en": "sphenoethmoidal recess",
   "region": "neck"
  },
  {
   "ko": "나와서 위깊은곳으로 진행하는 깊은목동맥",
   "en": "deep cervical artery",
   "region": "neck"
  },
  {
   "ko": "날개갈고리",
   "en": "pterygoid hamulus",
   "region": "neck"
  },
  {
   "ko": "날개아래턱솔기",
   "en": "pterygomandibular raphe",
   "region": "neck"
  },
  {
   "ko": "더부신경",
   "en": "accessory nerve",
   "region": "neck"
  },
  {
   "ko": "덧가로막신경",
   "en": "accessory phrenic nerve",
   "region": "neck"
  },
  {
   "ko": "되돌이후두신경",
   "en": "recurrent laryngeal nerve",
   "region": "neck"
  },
  {
   "ko": "두꼐는 입천장샘",
   "en": "palatine gland",
   "region": "neck"
  },
  {
   "ko": "뒤목갈비근",
   "en": "scalenus posterior muscle",
   "region": "neck"
  },
  {
   "ko": "뒤반지모뿔근",
   "en": "posterior cricoarythenoid muscle",
   "region": "neck"
  },
  {
   "ko": "등쪽어깨동맥",
   "en": "dorsal scapular artery",
   "region": "neck"
  },
  {
   "ko": "막벽",
   "en": "membranous wall",
   "region": "neck"
  },
  {
   "ko": "맨위코선반",
   "en": "supreme nasal concha",
   "region": "neck"
  },
  {
   "ko": "모뿔근",
   "en": "arytenoid muscle",
   "region": "neck"
  },
  {
   "ko": "모뿔덮개근",
   "en": "aryepiglottic muscle",
   "region": "neck"
  },
  {
   "ko": "모뿔덮개주름",
   "en": "aryepiglottic fold",
   "region": "neck"
  },
  {
   "ko": "모뿔연골",
   "en": "arytenoid cartilage",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "목갈비동맥",
   "en": "costocervical trunk",
   "region": "neck"
  },
  {
   "ko": "목교감신경줄기",
   "en": "cervical sympathetic trunk",
   "region": "neck"
  },
  {
   "ko": "목구멍편도",
   "en": "palatine tonsil",
   "region": "neck"
  },
  {
   "ko": "목젖",
   "en": "uvula",
   "region": "neck"
  },
  {
   "ko": "물렁입천장 위쪽공간\n\n입인두",
   "en": "oropharynx",
   "region": "neck"
  },
  {
   "ko": "미주신경",
   "en": "vagus nerve",
   "region": "neck"
  },
  {
   "ko": "밀알연골",
   "en": "triticeal cartilage",
   "region": "neck"
  },
  {
   "ko": "반달틈새",
   "en": "semilunar hiatus",
   "region": "neck"
  },
  {
   "ko": "반지방패관절",
   "en": "cricothyroid joint",
   "region": "neck"
  },
  {
   "ko": "반지방패근",
   "en": "cricothyroid muscle",
   "region": "neck"
  },
  {
   "ko": "반지방패인대",
   "en": "cricothyroid ligament",
   "region": "neck"
  },
  {
   "ko": "반지연골",
   "en": "cricoid cartilage",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "방패모뿔근",
   "en": "thyroarytenoid muscle",
   "region": "neck"
  },
  {
   "ko": "방패목뿔막",
   "en": "thyrohyoid membrane",
   "region": "neck"
  },
  {
   "ko": "방패연골",
   "en": "thyroid cartilage",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "벌집뼈융기",
   "en": "ethmoidal bulla",
   "region": "neck"
  },
  {
   "ko": "부위에 있는 입천장널힘줄",
   "en": "palatine aponeurosis",
   "region": "neck"
  },
  {
   "ko": "붓인두근",
   "en": "stylopharyngeus muscle",
   "region": "neck"
  },
  {
   "ko": "붓혀근",
   "en": "styloglossus muscle",
   "region": "neck"
  },
  {
   "ko": "비스듬하게 엑스자모양으로 교차하는 빗모뿔근",
   "en": "oblique arytenoid muscle",
   "region": "neck"
  },
  {
   "ko": "빗모뿔근",
   "en": "oblique arytenoid muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "빗장밑동맥",
   "en": "subclavian artery",
   "region": "neck"
  },
  {
   "ko": "빗장밑동맥의 갑상목동맥",
   "en": "thyrocervical trunk",
   "region": "neck"
  },
  {
   "ko": "빗장밑신경고리",
   "en": "ansa subclavia",
   "region": "neck"
  },
  {
   "ko": "빗장밑정맥",
   "en": "subclavian vein",
   "region": "neck"
  },
  {
   "ko": "빗장뼈 밑에있는 빗장밑근",
   "en": "subclavius muscle",
   "region": "neck"
  },
  {
   "ko": "빗장위신경",
   "en": "supraclavicular nerve",
   "region": "neck"
  },
  {
   "ko": "성대근",
   "en": "vocalis muscle",
   "region": "neck"
  },
  {
   "ko": "성대문아래공간",
   "en": "infraglottic cavity",
   "region": "neck"
  },
  {
   "ko": "성대문틈새",
   "en": "rima glottidis",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "성대인대",
   "en": "vocal ligament",
   "region": "neck"
  },
  {
   "ko": "성대주름",
   "en": "vocal fold",
   "region": "neck",
   "priority": "high"
  },
  {
   "ko": "성대틈새",
   "en": "rima glottidis",
   "region": "neck"
  },
  {
   "ko": "속후두신경",
   "en": "internal laryngeal nerve",
   "region": "neck"
  },
  {
   "ko": "쐐기연골",
   "en": "cuneiform cartilage",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "아래갑상동맥",
   "en": "inferior thyroid artery",
   "region": "neck"
  },
  {
   "ko": "아래갑상정맥",
   "en": "inferior thyroid vein",
   "region": "neck"
  },
  {
   "ko": "아래목신경절",
   "en": "inferior cervical ganglion",
   "region": "neck"
  },
  {
   "ko": "아래인두수축근",
   "en": "inferior constrictor muscle",
   "region": "neck"
  },
  {
   "ko": "아래코선반",
   "en": "nasal concha",
   "region": "neck"
  },
  {
   "ko": "아래콧길",
   "en": "nasal meatus",
   "region": "neck"
  },
  {
   "ko": "아래후두신경",
   "en": "inferior laryngeal nerve",
   "region": "neck"
  },
  {
   "ko": "안뜰주름",
   "en": "vestibular fold",
   "region": "neck"
  },
  {
   "ko": "앞교차",
   "en": "anterior commisure",
   "region": "neck"
  },
  {
   "ko": "앞목갈비근",
   "en": "scalenus anterior muscle",
   "region": "neck"
  },
  {
   "ko": "앞으로 달려 날개아래턱솔기",
   "en": "pterygomandibular raphe",
   "region": "neck"
  },
  {
   "ko": "어깨위신경",
   "en": "suprascapular nerve",
   "region": "neck"
  },
  {
   "ko": "연골벽",
   "en": "cartilaginous wall",
   "region": "neck"
  },
  {
   "ko": "오른정맥각",
   "en": "right venous angle",
   "region": "neck"
  },
  {
   "ko": "오름목동맥",
   "en": "ascending cervical artery",
   "region": "neck"
  },
  {
   "ko": "왼정맥각",
   "en": "left venous angle",
   "region": "neck"
  },
  {
   "ko": "위갑상동맥",
   "en": "superior thyroid artery",
   "region": "neck"
  },
  {
   "ko": "위갑상정맥",
   "en": "superior thyroid vein",
   "region": "neck"
  },
  {
   "ko": "위에서 내려오는 속목정맥과 만나서 아래쪽에서 팔머리정맥",
   "en": "brachiocephalic vein",
   "region": "neck"
  },
  {
   "ko": "위인두수축근",
   "en": "superior constrictor muscle",
   "region": "neck"
  },
  {
   "ko": "위후두동맥",
   "en": "superior laryngeal artery",
   "region": "neck"
  },
  {
   "ko": "위후두신경",
   "en": "superior laryngeal nerve",
   "region": "neck"
  },
  {
   "ko": "인두결절근막",
   "en": "pharyngobasilar fascia",
   "region": "neck"
  },
  {
   "ko": "인두솔기",
   "en": "pharyngeal raphe",
   "region": "neck"
  },
  {
   "ko": "인두신경얼기",
   "en": "pharyngeal plexus",
   "region": "neck"
  },
  {
   "ko": "인두오목",
   "en": "pharyngeal recess",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "일반적으로 첫째가슴교감신경절과 만나서 비교적 큰 별신경절",
   "en": "satellite ganglion",
   "region": "neck"
  },
  {
   "ko": "입인두 뒤쪽에서 혀 뒷부분 일부 관찰\n\n후두인두",
   "en": "laryngopharynx",
   "region": "neck"
  },
  {
   "ko": "입천장긴장근",
   "en": "tensor veli palatini muscle",
   "region": "neck"
  },
  {
   "ko": "입천장인두근",
   "en": "palatopharyngeus muscle",
   "region": "neck"
  },
  {
   "ko": "입천장인두활",
   "en": "palatopharyngeal arch",
   "region": "neck"
  },
  {
   "ko": "입천장혀근",
   "en": "palatoglossus muscle",
   "region": "neck",
   "priority": "high"
  },
  {
   "ko": "입천장혀활",
   "en": "palatoglossal arch",
   "region": "neck"
  },
  {
   "ko": "잔뿔연골",
   "en": "corniculate cartilage",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "점막",
   "en": "mucosa",
   "region": "neck"
  },
  {
   "ko": "조롱박오목",
   "en": "piriform fossa",
   "region": "neck"
  },
  {
   "ko": "중간갑상정맥",
   "en": "middle thyroid vein",
   "region": "neck"
  },
  {
   "ko": "중간목갈비근",
   "en": "scalenus medius muscle",
   "region": "neck"
  },
  {
   "ko": "중간목신경절",
   "en": "middle cervical ganglion",
   "region": "neck"
  },
  {
   "ko": "중간인두수축근",
   "en": "middle constrictor muscle",
   "region": "neck"
  },
  {
   "ko": "참성대",
   "en": "true vocal cord",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "척추동맥",
   "en": "vertebral artery",
   "region": "neck"
  },
  {
   "ko": "코눈물관",
   "en": "nasolacrimal duct",
   "region": "neck"
  },
  {
   "ko": "코인두",
   "en": "nasopharynx",
   "region": "neck"
  },
  {
   "ko": "탄력원뿔",
   "en": "conus elasticus",
   "region": "neck"
  },
  {
   "ko": "팔신경얼기",
   "en": "brachial plexus",
   "region": "neck"
  },
  {
   "ko": "피라미드엽",
   "en": "pyramidal lobe",
   "region": "neck"
  },
  {
   "ko": "혀밑신경",
   "en": "hypoglossal nerve",
   "region": "neck"
  },
  {
   "ko": "혀인두신경",
   "en": "glossopharyngeal nerve",
   "region": "neck"
  },
  {
   "ko": "후두덮개",
   "en": "epiglottis",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "후두실",
   "en": "laryngeal ventricle",
   "region": "neck"
  },
  {
   "ko": "후두안뜰",
   "en": "laryngeal vestibule",
   "region": "neck"
  },
  {
   "ko": "후두어귀",
   "en": "laryngeal inlet",
   "region": "neck"
  },
  {
   "ko": "lumbosacral trunk",
   "en": "",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "가쪽엉치동맥",
   "en": "lateral sacral artery",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "개의 뒤음순신경",
   "en": "posterior labial nerve",
   "region": "pelvis-perineum"
  },
  {
   "ko": "경우에 따라 처녀막",
   "en": "hymen",
   "region": "pelvis-perineum"
  },
  {
   "ko": "고유난소인대",
   "en": "ligament of ovary",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "고환날세관",
   "en": "efferent ductule of testis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "고환집막",
   "en": "tunica vaginalis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "고환집막 속면에서 고환전체 둘러싸는 두꺼운 섬유피막",
   "en": "fibrous capsule",
   "region": "pelvis-perineum"
  },
  {
   "ko": "고환집막공간",
   "en": "cavum of tunica vaginalis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "곧창자가로주름",
   "en": "transverse folds of rectum",
   "region": "pelvis-perineum"
  },
  {
   "ko": "곧창자방광오목",
   "en": "rectovesical pouch",
   "region": "pelvis-perineum"
  },
  {
   "ko": "곧창자방광주름",
   "en": "rectovesical fold",
   "region": "pelvis-perineum"
  },
  {
   "ko": "곧창자옆오목",
   "en": "pararectal fossa",
   "region": "pelvis-perineum"
  },
  {
   "ko": "곧창자자궁오목",
   "en": "rectouterine pouch",
   "region": "pelvis-perineum"
  },
  {
   "ko": "곧창자팽대",
   "en": "rectal ampulla",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "골반가로막",
   "en": "pelvic diaphragm",
   "region": "pelvis-perineum"
  },
  {
   "ko": "과 꼬리근",
   "en": "coccygeus muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "궁둥구멍근",
   "en": "piriformis",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "궁둥뼈가시",
   "en": "ischial spine",
   "region": "pelvis-perineum"
  },
  {
   "ko": "궁둥해면체근",
   "en": "ischiocavernosus muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "근육섬유로 된 두꺼운 고리모양으로 샅중심체",
   "en": "perineal body",
   "region": "pelvis-perineum"
  },
  {
   "ko": "깊은샅가로근",
   "en": "deep transverse perineal muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "깊은샅공간",
   "en": "deep perineal space",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "깊은음경동맥",
   "en": "deep artery of penis",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "깊은음경등정맥",
   "en": "deep dorsal vein of penis",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "꼬리근",
   "en": "coccygeus muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "꼬리뼈",
   "en": "coccyx",
   "region": "pelvis-perineum"
  },
  {
   "ko": "난소",
   "en": "ovary",
   "region": "pelvis-perineum"
  },
  {
   "ko": "난소간막",
   "en": "mesovarium",
   "region": "pelvis-perineum"
  },
  {
   "ko": "난소걸이인대",
   "en": "suspensory ligament of ovary",
   "region": "pelvis-perineum"
  },
  {
   "ko": "난소동맥",
   "en": "ovarian artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "남자요도막부분",
   "en": "membranous urethra",
   "region": "pelvis-perineum"
  },
  {
   "ko": "낭 안쪽모서리 따라 아래안쪽으로 달리다가 넓어져 정관팽대",
   "en": "ampulla of ductus deferens",
   "region": "pelvis-perineum"
  },
  {
   "ko": "대음순",
   "en": "labia majora",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "대음순틈새",
   "en": "pudendal cleft",
   "region": "pelvis-perineum"
  },
  {
   "ko": "두덩결합",
   "en": "pubic symphysis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "두덩곧창자근",
   "en": "puborectalis muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "두덩꼬리근",
   "en": "pubococcygeus muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "두덩뒤공간",
   "en": "retropubic space",
   "region": "pelvis-perineum"
  },
  {
   "ko": "두덩방광인대",
   "en": "pubovesical ligament",
   "region": "pelvis-perineum"
  },
  {
   "ko": "두덩전립샘인대",
   "en": "puboprostatic ligament",
   "region": "pelvis-perineum"
  },
  {
   "ko": "뒤음낭동맥",
   "en": "posterior scrotal branch",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "뒤음낭신경",
   "en": "posterior scrotal nerve",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "뒤음순동맥",
   "en": "posterior labial artery",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "뒤음순신경",
   "en": "posterior labial nerve",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "뒤음순연결",
   "en": "posterior commisure",
   "region": "pelvis-perineum"
  },
  {
   "ko": "막요도",
   "en": "membranous urethra",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "망울요도샘",
   "en": "bulbourethral gland",
   "region": "pelvis-perineum"
  },
  {
   "ko": "망울해면체근",
   "en": "bulbospongiosus muscle",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "바깥요도구멍",
   "en": "external urethral orifice",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "바깥요도조임근",
   "en": "external urethral sphincter muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "바깥항문조임근",
   "en": "external anal sphincter muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "방광",
   "en": "urinary bladder",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "방광꼭대기",
   "en": "apex of bladder",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "방광목",
   "en": "neck of bladder",
   "region": "pelvis-perineum"
  },
  {
   "ko": "방광배뇨근",
   "en": "detrusor muscle",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "방광삼각",
   "en": "trigone of bladder",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "방광옆오목",
   "en": "paravesical fossa",
   "region": "pelvis-perineum"
  },
  {
   "ko": "방광자궁오목",
   "en": "vesicouterine pouch",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "배꼽동맥",
   "en": "umbilical artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "백색막",
   "en": "tunica albuginea",
   "region": "pelvis-perineum"
  },
  {
   "ko": "불두덩",
   "en": "mons pubis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "비뇨생식구멍",
   "en": "urogenital hiatus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "비뇨생식부위",
   "en": "urogenital triangle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "빗살선",
   "en": "pectinate line",
   "region": "pelvis-perineum"
  },
  {
   "ko": "사정관",
   "en": "ejaculatory duct",
   "region": "pelvis-perineum"
  },
  {
   "ko": "사정관구멍",
   "en": "orifice of ejaculatory duct",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "샅",
   "en": "perineum",
   "region": "pelvis-perineum"
  },
  {
   "ko": "샅가로인대",
   "en": "transverse perineal ligament",
   "region": "pelvis-perineum"
  },
  {
   "ko": "샅동맥",
   "en": "perineal artery",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "샅막",
   "en": "perineal membrane",
   "region": "pelvis-perineum"
  },
  {
   "ko": "샅신경",
   "en": "perineal nerve",
   "region": "pelvis-perineum"
  },
  {
   "ko": "샅중심체",
   "en": "perineal body",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "샅중심체에서 바깥항문조임근",
   "en": "external anal sphincter muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "소음순",
   "en": "labium minus",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "속엉덩동맥",
   "en": "internal iliac artery",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "속요도구멍",
   "en": "internal urethral orifice",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "속음부동맥",
   "en": "internal pudendal artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "속자궁구멍",
   "en": "internal os of uterus",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "속폐쇄근",
   "en": "obturator internus muscle",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "속폐쇄근막",
   "en": "obturator fascia",
   "region": "pelvis-perineum"
  },
  {
   "ko": "속항문조임근",
   "en": "internal anal sphincter muscle",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "손목관절",
   "en": "wrist joint",
   "region": "pelvis-perineum"
  },
  {
   "ko": "수 있음\n\n남자비뇨생식부위에 위치한 바깥생식기관인 음낭",
   "en": "scrotum",
   "region": "pelvis-perineum"
  },
  {
   "ko": "아래곧창자동맥",
   "en": "inferior anal artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "아래곧창자신경",
   "en": "inferior anal nerve",
   "region": "pelvis-perineum"
  },
  {
   "ko": "아래곧창자혈관",
   "en": "inferior rectal vessel",
   "region": "pelvis-perineum"
  },
  {
   "ko": "아래두덩인대",
   "en": "inferior pubic ligament",
   "region": "pelvis-perineum"
  },
  {
   "ko": "아래방광동맥",
   "en": "inferior vesical artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "아래볼기동맥",
   "en": "inferior gluteal artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "아래안쪽각에서 좁아져 뚜렷하게 보이지 않지만 정낭배출관",
   "en": "excretory duct",
   "region": "pelvis-perineum"
  },
  {
   "ko": "아래쪽에서 음경망울",
   "en": "bulb of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "안쪽면 따라 소음순",
   "en": "labium minus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "안쪽배꼽인대",
   "en": "medial umbilical ligament",
   "region": "pelvis-perineum"
  },
  {
   "ko": "앞에서 열었다면 요도능선",
   "en": "urethral crest",
   "region": "pelvis-perineum"
  },
  {
   "ko": "양쪽 궁둥두덩가지",
   "en": "ischiopubic ramus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "양쪽 궁둥뼈결절",
   "en": "ischial tuberosity",
   "region": "pelvis-perineum"
  },
  {
   "ko": "양쪽대음순",
   "en": "labium majus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "얕은샅가로근",
   "en": "superficial transverse perineal muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "얕은샅공간",
   "en": "superficial perineal space",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "얕은음경등정맥",
   "en": "superficial dorsal veins of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "엉덩근가지",
   "en": "iliacus branch",
   "region": "pelvis-perineum"
  },
  {
   "ko": "엉덩꼬리근",
   "en": "iliococcygeus muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "엉덩허리동맥",
   "en": "iliolumbar artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "엉치가시인대",
   "en": "sacrospinous ligament",
   "region": "pelvis-perineum"
  },
  {
   "ko": "엉치결절인대",
   "en": "sacrotuberous ligament",
   "region": "pelvis-perineum"
  },
  {
   "ko": "엉치신경얼기",
   "en": "sacral plexus",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "여자에서는 대음순",
   "en": "labium majus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "와 더 깊이있는 음경등신경",
   "en": "dorsal nerve of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "요관",
   "en": "ureter",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "요관구멍",
   "en": "ureteric orifice",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "요관사이구멍",
   "en": "interureteric fold",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "요도",
   "en": "urethra",
   "region": "pelvis-perineum"
  },
  {
   "ko": "요도 막부분",
   "en": "membranous urethra",
   "region": "pelvis-perineum"
  },
  {
   "ko": "요도 배오목",
   "en": "navicular fossa",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "요도 해면체부분",
   "en": "spongy urethra",
   "region": "pelvis-perineum"
  },
  {
   "ko": "요도능선",
   "en": "urethral crest",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "요도둔덕",
   "en": "seminal colliculus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "요도배오목",
   "en": "navicular fossa",
   "region": "pelvis-perineum"
  },
  {
   "ko": "요도전립샘부분",
   "en": "prostatic urethra",
   "region": "pelvis-perineum"
  },
  {
   "ko": "요도해면체",
   "en": "corpus spongiosum of penis",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "위곧창자동맥",
   "en": "superior rectal artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "위방광동맥",
   "en": "superior vesical artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "위볼기동맥",
   "en": "superior gluteal artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경걸이인대",
   "en": "suspensory ligament of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경고리인대",
   "en": "fundiform ligament of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경귀두",
   "en": "glans penis",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "음경꺼풀",
   "en": "prepuce",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경꺼풀주름띠",
   "en": "frenulum of prepuce",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경다리",
   "en": "crus of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경등동맥",
   "en": "dorsal artery of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경등신경",
   "en": "dorsal nerve of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경망울",
   "en": "bulb of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경망울동맥",
   "en": "artery of bulb of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경몸통",
   "en": "body of penis",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음경뿌리 이루는 음경해면체",
   "en": "corpus cavernosum of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음경해면체",
   "en": "corpus cavernosum of penis",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음낭사이막",
   "en": "septum of scrotum",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음부신경",
   "en": "pudendal nerve",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "음핵귀두",
   "en": "glans of clitoris",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음핵꺼풀",
   "en": "prepuce of clitoris",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음핵등신경",
   "en": "dorsal nerve of clitoris",
   "region": "pelvis-perineum"
  },
  {
   "ko": "음핵주름띠",
   "en": "frenulum of clitoris",
   "region": "pelvis-perineum"
  },
  {
   "ko": "의 가지들로 음부신경관",
   "en": "pudendal canal",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁",
   "en": "uterus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁간막",
   "en": "mesometrium",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁관",
   "en": "uterine tube",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "자궁관간막",
   "en": "mesosalpinx",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "자궁관깔때기",
   "en": "infundibulum",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "자궁관배안구멍",
   "en": "abdominal ostium",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁관술",
   "en": "fimbriae",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁관자궁구멍",
   "en": "uterine ostium",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "자궁관잘록",
   "en": "isthmus",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "자궁관팽대",
   "en": "ampulla",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "자궁구멍",
   "en": "external os of uterus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁넓은인대",
   "en": "broad ligament of uterus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁동맥",
   "en": "uterine artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁목",
   "en": "cervix of uterus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁몸통",
   "en": "body of uterus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁몸통과 자궁목 사이 좁아진 부분\n골반가로막",
   "en": "pelvic diaphragm",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁바닥",
   "en": "fundus of uterus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁뿔",
   "en": "uterine horn",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자궁잘록",
   "en": "isthmus of uterus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "자율신경얼기",
   "en": "autonomic plexus",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "전립샘",
   "en": "prostate",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "전립샘관",
   "en": "prostatic duct",
   "region": "pelvis-perineum"
  },
  {
   "ko": "전립샘굴",
   "en": "prostatic sinus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "전립샘소실",
   "en": "prostatic utricle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "전립샘요도",
   "en": "prostatic urethra",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "정관팽대",
   "en": "ampulla of ductus deferens",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "정낭",
   "en": "seminal vesicle",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "정세관",
   "en": "seminiferous tubule",
   "region": "pelvis-perineum"
  },
  {
   "ko": "정중배꼽인대",
   "en": "median umbilical ligament",
   "region": "pelvis-perineum"
  },
  {
   "ko": "중간곧창자동맥",
   "en": "middle rectal artery",
   "region": "pelvis-perineum"
  },
  {
   "ko": "지만 앞쪽과 가쪽에서는 전립샘과 근막 사이 전립샘정맥얼기",
   "en": "prostatic venous plexus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "질",
   "en": "vagina",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "질구멍",
   "en": "vaginal orifice",
   "region": "pelvis-perineum"
  },
  {
   "ko": "질어귀",
   "en": "vestibule",
   "region": "pelvis-perineum"
  },
  {
   "ko": "질어귀망울",
   "en": "bulb of vestibule",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "질이 자궁구멍 위쪽 앞과 뒤로 뻗어있는 곳\n자궁",
   "en": "uterus",
   "region": "pelvis-perineum"
  },
  {
   "ko": "질주름",
   "en": "vaginal rugae",
   "region": "pelvis-perineum"
  },
  {
   "ko": "질천장",
   "en": "vaginal fornix",
   "region": "pelvis-perineum"
  },
  {
   "ko": "큰볼기근",
   "en": "gluteus maximus muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "큰질어귀샘",
   "en": "greater vestibular gland",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "큰질어귀샘관",
   "en": "duct of greater vestibular gland",
   "region": "pelvis-perineum"
  },
  {
   "ko": "폐쇄관",
   "en": "obturator canal",
   "region": "pelvis-perineum"
  },
  {
   "ko": "폐쇄동맥",
   "en": "obturator artery",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "항문곧창자연결",
   "en": "anorectal junction",
   "region": "pelvis-perineum"
  },
  {
   "ko": "항문과 궁둥뼈결절 중간부위에서 칼을 궁둥항문오목지방덩이",
   "en": "fat body of ischioanal fossa",
   "region": "pelvis-perineum"
  },
  {
   "ko": "항문굴",
   "en": "anal sinuses",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "항문기둥",
   "en": "anal columns",
   "region": "pelvis-perineum"
  },
  {
   "ko": "항문부위",
   "en": "anal triangle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "항문올림근",
   "en": "levator ani muscle",
   "region": "pelvis-perineum",
   "priority": "high"
  },
  {
   "ko": "항문올림근힘줄활",
   "en": "tendinous arch of levator ani muscle",
   "region": "pelvis-perineum"
  },
  {
   "ko": "항문판막",
   "en": "anal valves",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "해면체요도",
   "en": "spongy urethra",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "허리가지",
   "en": "lumbar branch",
   "region": "pelvis-perineum"
  },
  {
   "ko": "가끔 가장 아래쪽 목교감신경절과 합쳐져 큰별신경절",
   "en": "greater stellate ganglion",
   "region": "thorax"
  },
  {
   "ko": "가로막면",
   "en": "diaphragmatic surface",
   "region": "thorax"
  },
  {
   "ko": "가슴대동맥",
   "en": "thoracic aorta",
   "region": "thorax"
  },
  {
   "ko": "가슴대동맥 앞쪽으로 당겨서 쌍으로 된 뒤갈비사이동맥",
   "en": "posterior intercostal artery",
   "region": "thorax"
  },
  {
   "ko": "가슴등동맥",
   "en": "thoracodorsal artery",
   "region": "thorax"
  },
  {
   "ko": "가슴막안",
   "en": "plenral cavity",
   "region": "thorax"
  },
  {
   "ko": "가슴봉우리동맥",
   "en": "thoracoacromial artery",
   "region": "thorax"
  },
  {
   "ko": "가쪽가슴동맥",
   "en": "lateral thoracic artery",
   "region": "thorax"
  },
  {
   "ko": "각 허파에는 갈비면",
   "en": "costal surface",
   "region": "thorax"
  },
  {
   "ko": "각각의 갈비사이공간",
   "en": "intercostal space",
   "region": "thorax"
  },
  {
   "ko": "고 가슴벽에 붙어있는 나머지 벽가슴막 제거하기 섬유심장막",
   "en": "fibrous pericardium",
   "region": "thorax"
  },
  {
   "ko": "과해 내려감 각각의 가슴교감신경절은 이웃하는 갈비사이신경",
   "en": "intercostal nerve",
   "region": "thorax"
  },
  {
   "ko": "구역기관지",
   "en": "segmental bronchus",
   "region": "thorax"
  },
  {
   "ko": "기관 내려오면서 기관용골",
   "en": "carina of trachea",
   "region": "thorax"
  },
  {
   "ko": "기관갈림",
   "en": "tracheal bifurcation",
   "region": "thorax"
  },
  {
   "ko": "기관지나무",
   "en": "bronchial tree",
   "region": "thorax"
  },
  {
   "ko": "기관지동맥",
   "en": "bronchial artery",
   "region": "thorax"
  },
  {
   "ko": "내림대동맥고랑",
   "en": "groove for descending aorta",
   "region": "thorax"
  },
  {
   "ko": "높이 각각의 기관지는 아래가쪽으로 달려 각각의 허파뿌리",
   "en": "root of lung",
   "region": "thorax"
  },
  {
   "ko": "대동맥활고랑",
   "en": "groove for aortic arch",
   "region": "thorax"
  },
  {
   "ko": "대동맥활에서 동맥관인대",
   "en": "ligamentum arteriosum",
   "region": "thorax"
  },
  {
   "ko": "덧반홀정맥",
   "en": "accessory hemiazygos vein",
   "region": "thorax"
  },
  {
   "ko": "뒤갈비사이동맥",
   "en": "posterior intercostal artery",
   "region": "thorax"
  },
  {
   "ko": "뒤미주신경줄기",
   "en": "posterior vagal trunk",
   "region": "thorax"
  },
  {
   "ko": "뒤에 위치 위로 올라와 목의 뿌리 부분에서 왼빗장밑정맥",
   "en": "left subclavian vein",
   "region": "thorax"
  },
  {
   "ko": "뒤위팔휘돌이동맥",
   "en": "posterior circumflex humeral artery",
   "region": "thorax",
   "priority": "high"
  },
  {
   "ko": "뒷벽에서 빗심장막굴",
   "en": "oblique pericardial sinus",
   "region": "thorax"
  },
  {
   "ko": "반홀정맥",
   "en": "semiazygos vein",
   "region": "thorax"
  },
  {
   "ko": "배오른쪽 오름허리정맥",
   "en": "ascending lumbar vein",
   "region": "thorax"
  },
  {
   "ko": "보통 맨위갈비사이동맥",
   "en": "supreme intercostal artery",
   "region": "thorax"
  },
  {
   "ko": "빗장밑동맥고랑",
   "en": "groove for subclavian artery",
   "region": "thorax"
  },
  {
   "ko": "세로칸면",
   "en": "mediastinal surface",
   "region": "thorax"
  },
  {
   "ko": "세모근가지 나오면서 위로갈라져 봉우리로 간 봉우리가지",
   "en": "acromial branch",
   "region": "thorax"
  },
  {
   "ko": "속가슴동맥",
   "en": "internal thorasica",
   "region": "thorax"
  },
  {
   "ko": "식 도고랑",
   "en": "groove for esophagus",
   "region": "thorax"
  },
  {
   "ko": "식도 고랑",
   "en": "groove for esophagus",
   "region": "thorax"
  },
  {
   "ko": "식도에서는 여러가지로 나뉘어 신경식도얼기",
   "en": "esophageal plexus",
   "region": "thorax"
  },
  {
   "ko": "심방귀",
   "en": "auricde",
   "region": "thorax"
  },
  {
   "ko": "심장자국",
   "en": "cardiac impression",
   "region": "thorax"
  },
  {
   "ko": "싸는 가슴막은 아래쪽으로 뻗어 허파인대 이룸\n\n기관지동맥",
   "en": "bronchial artery",
   "region": "thorax"
  },
  {
   "ko": "아래엽기관지",
   "en": "lobar bronchus",
   "region": "thorax"
  },
  {
   "ko": "어감 왼기관지 앞에서 허파동맥이 왼허파동맥과 오른허파동맥",
   "en": "pulmonary artery",
   "region": "thorax"
  },
  {
   "ko": "어깨밑동맥",
   "en": "subscapular artery",
   "region": "thorax"
  },
  {
   "ko": "어깨세모근 젖히면서 자른 세모근가지",
   "en": "deltoid branch",
   "region": "thorax"
  },
  {
   "ko": "어깨휘돌이동맥",
   "en": "circumflex scapular artery",
   "region": "thorax"
  },
  {
   "ko": "에서 왼기관지와 오른기관지",
   "en": "main bronchus",
   "region": "thorax"
  },
  {
   "ko": "에서 이차기관지",
   "en": "secondary bronchus",
   "region": "thorax"
  },
  {
   "ko": "열째등뼈높이에서 가로막 근육부분에 있는 식도구멍",
   "en": "esophageal hiatus",
   "region": "thorax"
  },
  {
   "ko": "오른허파는 10개의 기관지허파구역",
   "en": "bronchopulmonary segment",
   "region": "thorax"
  },
  {
   "ko": "와 백색교통가지",
   "en": "white ramus communicans",
   "region": "thorax"
  },
  {
   "ko": "왼오름허리정맥",
   "en": "left ascending lumbar vein",
   "region": "thorax"
  },
  {
   "ko": "왼허파혀",
   "en": "lingula of left lung",
   "region": "thorax"
  },
  {
   "ko": "위가슴동맥",
   "en": "superior thoracic artery",
   "region": "thorax"
  },
  {
   "ko": "위대정맥고랑",
   "en": "groove for superior vena cava",
   "region": "thorax"
  },
  {
   "ko": "위팔휘돌이동맥",
   "en": "circumflex humeral artery",
   "region": "thorax"
  },
  {
   "ko": "위팔휘돌이동맥과 가쪽으로 달리면서 위팔뼈 외과목",
   "en": "surgical neck of humerus",
   "region": "thorax"
  },
  {
   "ko": "으로 2개의 연결 가지는데 이들 작은 가지를 회색교통가지",
   "en": "gray ramus communicans",
   "region": "thorax"
  },
  {
   "ko": "이나 왼속목정맥",
   "en": "left internal jugular vein",
   "region": "thorax"
  },
  {
   "ko": "일차기관지",
   "en": "primary bronchus",
   "region": "thorax"
  },
  {
   "ko": "작고 빗장밑근으로 가서 분포하는 빗장가지",
   "en": "clavicular branch",
   "region": "thorax"
  },
  {
   "ko": "작은내장신경",
   "en": "lesser splanchnic nerve",
   "region": "thorax"
  },
  {
   "ko": "작은세로칸가지",
   "en": "small mediastinal branch",
   "region": "thorax"
  },
  {
   "ko": "작은식도가지",
   "en": "small esophageal branch",
   "region": "thorax"
  },
  {
   "ko": "전체길이가 뒤세로칸 따라 내려가다 가 가로막 대동맥구멍",
   "en": "aortic hiatus of diaphragm",
   "region": "thorax"
  },
  {
   "ko": "젖꼭기 위치\n넷째 갈비사이공간\n젖꼭지",
   "en": "nipple",
   "region": "thorax"
  },
  {
   "ko": "젖몸통",
   "en": "body of breast",
   "region": "thorax"
  },
  {
   "ko": "젖샘걸어인대",
   "en": "suspensory ligament ofbreast",
   "region": "thorax"
  },
  {
   "ko": "큰가슴근",
   "en": "pectoralis major muscle",
   "region": "thorax"
  },
  {
   "ko": "큰가슴근과 작은가슴근에 분포하는 가슴근가지",
   "en": "pectoral branch",
   "region": "thorax"
  },
  {
   "ko": "큰내장신경",
   "en": "greater splanchnic nerve",
   "region": "thorax"
  },
  {
   "ko": "큰심장자국",
   "en": "cardiac impression",
   "region": "thorax"
  },
  {
   "ko": "팔신경얼기의 긴가슴신경",
   "en": "long thoracic nerve",
   "region": "thorax"
  },
  {
   "ko": "허파쪽 가슴막",
   "en": "risceral pleura",
   "region": "thorax"
  },
  {
   "ko": "형성하며 허파문",
   "en": "hilum of lung",
   "region": "thorax"
  },
  {
   "ko": "홀정맥",
   "en": "azygos vein",
   "region": "thorax"
  },
  {
   "ko": "홀정맥고랑",
   "en": "groove for azygos vein",
   "region": "thorax"
  },
  {
   "ko": "가로섬유",
   "en": "transverse fiber",
   "region": "upper-limb"
  },
  {
   "ko": "가슴등신경",
   "en": "thoracodorsal nerve",
   "region": "upper-limb"
  },
  {
   "ko": "가시아래근",
   "en": "infraspinatus muscle",
   "region": "upper-limb"
  },
  {
   "ko": "가시위근",
   "en": "supraspinatus muscle",
   "region": "upper-limb"
  },
  {
   "ko": "가쪽가슴근신경",
   "en": "lateral pectoral nerve",
   "region": "upper-limb"
  },
  {
   "ko": "가쪽곁인대",
   "en": "radial collateral ligament",
   "region": "upper-limb"
  },
  {
   "ko": "가쪽근육사이막",
   "en": "lateral intermuscular septum",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "가쪽다발",
   "en": "lateral cord",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "가쪽벽",
   "en": "lateral wall",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "가쪽아래팔피부신경",
   "en": "lateral cutaneous nerve of forearm",
   "region": "upper-limb"
  },
  {
   "ko": "각각 손등정맥그물",
   "en": "dorsal venous network of hand",
   "region": "upper-limb"
  },
  {
   "ko": "갈고리뼈",
   "en": "hamate",
   "region": "upper-limb"
  },
  {
   "ko": "갈고리뼈갈고리",
   "en": "hook of hamate",
   "region": "upper-limb"
  },
  {
   "ko": "갈비근과 중간목갈비근 사이 관찰 잘 하기위해서 부리위팔근",
   "en": "coracobrachialis muscle",
   "region": "upper-limb"
  },
  {
   "ko": "갈비사이위팔피부신경",
   "en": "intrercostobrachial cutaneous nerve",
   "region": "upper-limb"
  },
  {
   "ko": "겨드랑꼭대기",
   "en": "apex of axilla",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "겨드랑동맥",
   "en": "axillary artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "겨드랑림프절",
   "en": "axillary lymph nodes",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "겨드랑바닥",
   "en": "base of axilla",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "겨드랑신경",
   "en": "axillary nerve",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "겨드랑정맥",
   "en": "axillary vein",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "겨드랑집",
   "en": "axillary sheath",
   "region": "upper-limb"
  },
  {
   "ko": "결절사이고랑",
   "en": "intertubercular groove",
   "region": "upper-limb"
  },
  {
   "ko": "고리부분",
   "en": "anular part",
   "region": "upper-limb"
  },
  {
   "ko": "고유바닥쪽손가락동맥",
   "en": "prper palmar digital artery",
   "region": "upper-limb"
  },
  {
   "ko": "과 함꼐 위팔뼈 노신경고랑",
   "en": "groove for radial nerve",
   "region": "upper-limb"
  },
  {
   "ko": "관절원반",
   "en": "articular disc",
   "region": "upper-limb"
  },
  {
   "ko": "굽힘근지지띠",
   "en": "flexor retinaculum",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "근육피부신경",
   "en": "musculocutaneous nerve",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "긴가슴신경",
   "en": "long thoracic nerve",
   "region": "upper-limb"
  },
  {
   "ko": "긴갈래와 안쪽갈래 벌린틈새 위쪽에서 큰원근",
   "en": "teres major muscle",
   "region": "upper-limb"
  },
  {
   "ko": "긴노쪽손목폄근",
   "en": "extensor carpi radialis longus muscle",
   "region": "upper-limb"
  },
  {
   "ko": "긴손바닥근",
   "en": "palmaris longus muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "긴엄지벌림근",
   "en": "abductor pollicis longus muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "긴엄지폄근",
   "en": "extensor pollicis longus muscle",
   "region": "upper-limb"
  },
  {
   "ko": "깊은손가락굽힘근",
   "en": "flexor digitorum profundus muscle",
   "region": "upper-limb"
  },
  {
   "ko": "깊은손바닥동맥활",
   "en": "deep palmar arch",
   "region": "upper-limb"
  },
  {
   "ko": "깊은위팔동맥",
   "en": "deep brachial artery",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "네모엎침근",
   "en": "pronator quadratus muscle",
   "region": "upper-limb"
  },
  {
   "ko": "노동맥",
   "en": "radial artery",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "노뼈머리띠인대",
   "en": "anular ligament of radius",
   "region": "upper-limb"
  },
  {
   "ko": "노뼈몸통앞선의 빗선에서 일어나는 노갈래",
   "en": "radial head",
   "region": "upper-limb"
  },
  {
   "ko": "노신경",
   "en": "radial nerve",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "노신경 깊은가지",
   "en": "deep branch of radial nerve",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "노신경 얕은가지",
   "en": "superficial branch of radial nerve",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "노신경깊은가지",
   "en": "deep branch of radial nerve",
   "region": "upper-limb"
  },
  {
   "ko": "노쪽되돌이동맥",
   "en": "radial recurrent artery",
   "region": "upper-limb"
  },
  {
   "ko": "노쪽손목굽힘근",
   "en": "flexor carpi radialis muscle",
   "region": "upper-limb"
  },
  {
   "ko": "노쪽피부정맥",
   "en": "cephalic vein",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "돌림근띠",
   "en": "rotator cuff",
   "region": "upper-limb"
  },
  {
   "ko": "동반정맥",
   "en": "vena comitans",
   "region": "upper-limb"
  },
  {
   "ko": "되돌이가지",
   "en": "recurrent branch",
   "region": "upper-limb"
  },
  {
   "ko": "뒤겨드랑주름",
   "en": "posterior axillary fold",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "뒤다발",
   "en": "posterior cord",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "뒤뼈사이동맥",
   "en": "posterior interosseous artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "뒤뼈사이신경",
   "en": "posterior interossoeus nerve",
   "region": "upper-limb"
  },
  {
   "ko": "뒤아래팔피부신경",
   "en": "posterior cutaneous nerve of forearm",
   "region": "upper-limb"
  },
  {
   "ko": "뒤위팔피부신경",
   "en": "posterior cutaneous nerve of arm",
   "region": "upper-limb"
  },
  {
   "ko": "뒷벽",
   "en": "posterior wall",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "등쪽뼈사이근",
   "en": "dorsal interossei muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "뚫고 지나가는 근육피부신경",
   "en": "musculocutaneous nerve",
   "region": "upper-limb"
  },
  {
   "ko": "락이 굽혀져 있어 하기 어려운데 이럴때는 깊은손가락굽힘근",
   "en": "flexor digitorum profundus muscle",
   "region": "upper-limb"
  },
  {
   "ko": "마름인대",
   "en": "trapezoid ligament",
   "region": "upper-limb"
  },
  {
   "ko": "목겨드랑관",
   "en": "cervicoaxillary canal",
   "region": "upper-limb"
  },
  {
   "ko": "몸쪽노자관절",
   "en": "proximal radioulnar joint",
   "region": "upper-limb"
  },
  {
   "ko": "바닥쪽뼈사이근",
   "en": "palmar interossei muscle",
   "region": "upper-limb"
  },
  {
   "ko": "바닥쪽손목인대",
   "en": "palmar carpal ligament",
   "region": "upper-limb"
  },
  {
   "ko": "반달뼈",
   "en": "lunate",
   "region": "upper-limb"
  },
  {
   "ko": "봉우리빗장인대",
   "en": "acromioclavicular ligament",
   "region": "upper-limb"
  },
  {
   "ko": "부리봉우리인대",
   "en": "coracoacromial ligament",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "부리빗장인대",
   "en": "coracoclavicular ligament",
   "region": "upper-limb"
  },
  {
   "ko": "부리위팔근",
   "en": "coracobrachialis muscle",
   "region": "upper-limb"
  },
  {
   "ko": "부리위팔인대",
   "en": "coracohumeral ligament",
   "region": "upper-limb"
  },
  {
   "ko": "부에서 각각의 손가락끝으로 가는 선\n\n손바닥에서 엄지두덩",
   "en": "thenar eminence",
   "region": "upper-limb"
  },
  {
   "ko": "빗장밑근",
   "en": "subclavius muscle",
   "region": "upper-limb"
  },
  {
   "ko": "빗장뼈 봉우리끝",
   "en": "acromial end of clavicle",
   "region": "upper-limb"
  },
  {
   "ko": "삼차신경 → 눈확밑신경",
   "en": "",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "새끼맞섬근",
   "en": "opponens digiti minimi muscle",
   "region": "upper-limb"
  },
  {
   "ko": "새끼벌림근",
   "en": "abductor digiti minimi muscle",
   "region": "upper-limb"
  },
  {
   "ko": "새끼폄근",
   "en": "extensor digiti minimi muscle",
   "region": "upper-limb"
  },
  {
   "ko": "세모뼈",
   "en": "triquetrum",
   "region": "upper-limb"
  },
  {
   "ko": "손가락굽힘근 힘줄",
   "en": "flexor digitorum muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "손가락굽힘근온힘줄집",
   "en": "common flexor sheat",
   "region": "upper-limb"
  },
  {
   "ko": "손가락섬유집",
   "en": "fibrous sheaths of digits of hand",
   "region": "upper-limb"
  },
  {
   "ko": "손가락폄근",
   "en": "extensor digitorum muscle",
   "region": "upper-limb"
  },
  {
   "ko": "손뒤침근",
   "en": "supinator muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "손등정맥그물",
   "en": "dorsal venous network of hand",
   "region": "upper-limb"
  },
  {
   "ko": "손목굴",
   "en": "carpal tunnel",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "손바닥에서 자동맥 깊은가지와 만나서 깊은손바닥동맥활",
   "en": "deep palmar arch",
   "region": "upper-limb"
  },
  {
   "ko": "손배뼈",
   "en": "scaphoid",
   "region": "upper-limb"
  },
  {
   "ko": "십자부분",
   "en": "cruciform part",
   "region": "upper-limb"
  },
  {
   "ko": "십자섬유",
   "en": "cruciate fiber",
   "region": "upper-limb"
  },
  {
   "ko": "아 겨드랑동맥",
   "en": "axillary artery",
   "region": "upper-limb"
  },
  {
   "ko": "아래가쪽위팔피부신경",
   "en": "inferior lateral cutaneous nerve of arm",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "아래어깨밑신경",
   "en": "inferior subscapular nerve",
   "region": "upper-limb"
  },
  {
   "ko": "아래자쪽곁동맥",
   "en": "inferior ulnar collateral artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "아래팔 먼쪽 절반에서 자쪽손목굽힘근",
   "en": "flexor carpi ulnaris muscle",
   "region": "upper-limb"
  },
  {
   "ko": "안쪽가슴근신경",
   "en": "medial pectoral nerve",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "안쪽곁인대",
   "en": "ulnar collateral ligament",
   "region": "upper-limb"
  },
  {
   "ko": "안쪽근육사이막",
   "en": "medial intermuscular septum",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "안쪽다발",
   "en": "medial cord",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "안쪽두갈래근고랑",
   "en": "medial bicipital groove",
   "region": "upper-limb"
  },
  {
   "ko": "안쪽벽",
   "en": "medial wall",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "안쪽아래팔피부신경",
   "en": "medial cutaneous nerve of forearm",
   "region": "upper-limb"
  },
  {
   "ko": "안쪽위팔피부신경",
   "en": "medial cutaneous nerve of arm",
   "region": "upper-limb"
  },
  {
   "ko": "안쪽으로 주행하여 새끼두덩근육들",
   "en": "hypothenar muscle",
   "region": "upper-limb"
  },
  {
   "ko": "앞겨드랑주름",
   "en": "anterior axillary fold",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "앞벽",
   "en": "anterior wall",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "앞뼈사이동맥",
   "en": "anterior interosseous artery",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "앞뼈사이신경",
   "en": "anterior interosseous nerve",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "앞위팔휘돌이동맥",
   "en": "anterior circumflex humeral artery",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "앞톱니근",
   "en": "serratus anterior muscle",
   "region": "upper-limb"
  },
  {
   "ko": "얕은손가락굽힘근",
   "en": "flexor digitorum superficialis muscle",
   "region": "upper-limb"
  },
  {
   "ko": "얕은손바닥가지",
   "en": "superficial palmar branch",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "얕은손바닥동맥활",
   "en": "superficial palmar arch",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "어 일어남\n\n위팔세갈래근이 아래로 내려가 자뼈 팔꿈치머리",
   "en": "olecranon",
   "region": "upper-limb"
  },
  {
   "ko": "어깨밑근",
   "en": "subscapularis muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "어깨밑근힘줄밑주머니",
   "en": "subtendinous bursa of subscapularis muscle",
   "region": "upper-limb"
  },
  {
   "ko": "어깨밑신경",
   "en": "subscapular nerve",
   "region": "upper-limb"
  },
  {
   "ko": "어깨뼈밑오목",
   "en": "subscapular fossa",
   "region": "upper-limb"
  },
  {
   "ko": "엄지두덩근막",
   "en": "thenar fascia",
   "region": "upper-limb"
  },
  {
   "ko": "에 붙어있는 널힘줄에서 일 어나 콩알뼈",
   "en": "pisiform",
   "region": "upper-limb"
  },
  {
   "ko": "온바닥쪽손가락동맥",
   "en": "common palmar digital artery",
   "region": "upper-limb"
  },
  {
   "ko": "온바닥쪽손가락신경",
   "en": "common palmar digital nerve",
   "region": "upper-limb"
  },
  {
   "ko": "온뼈사이동맥",
   "en": "common interosseous artery",
   "region": "upper-limb"
  },
  {
   "ko": "와 새끼두덩",
   "en": "hypothenar eminence",
   "region": "upper-limb"
  },
  {
   "ko": "와 안쪽깊은곳의 자동맥",
   "en": "ulnar artery",
   "region": "upper-limb"
  },
  {
   "ko": "원뿔인대",
   "en": "conoid ligament",
   "region": "upper-limb"
  },
  {
   "ko": "원엎침근",
   "en": "pronator teres muscle",
   "region": "upper-limb"
  },
  {
   "ko": "위가쪽위팔피부신경",
   "en": "superior lateral cutaneous nerve of arm",
   "region": "upper-limb"
  },
  {
   "ko": "위어깨밑신경",
   "en": "superior subscapular nerve",
   "region": "upper-limb"
  },
  {
   "ko": "위에 서 내려오는 자쪽곁동맥",
   "en": "ulnar collateral artery",
   "region": "upper-limb"
  },
  {
   "ko": "위자쪽곁동맥",
   "en": "superior ulnar collateral artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "위팔가로인대",
   "en": "transverse humeral ligament",
   "region": "upper-limb"
  },
  {
   "ko": "위팔근",
   "en": "brachialis muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "위팔근막",
   "en": "brachial fascia",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "위팔노근",
   "en": "brachiradialis muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "위팔동맥",
   "en": "brachial artery",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "위팔두갈래근",
   "en": "biceps brachii muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "위팔두갈래근 널힘줄",
   "en": "bicipital aponeurosis",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "위팔두갈래근 힘줄",
   "en": "bicipital tendon",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "위팔두갈래근널힘줄",
   "en": "bicipital aponeurosis",
   "region": "upper-limb"
  },
  {
   "ko": "위팔뼈 안쪽위관절융기와 갈고리돌기에서 일어나는 위팔자갈래",
   "en": "humeroulnar head",
   "region": "upper-limb"
  },
  {
   "ko": "위팔세갈래근",
   "en": "triceps brachii muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "이를 연결하는 힘줄사이연결",
   "en": "intertendinous connection",
   "region": "upper-limb"
  },
  {
   "ko": "자동맥",
   "en": "ulnar artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "자동맥 깊은가지",
   "en": "deep branch of ulnar artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "자동맥 얕은가지",
   "en": "superficial branch of ulnar artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "자뼈 뒤침근능선",
   "en": "supinator crest",
   "region": "upper-limb"
  },
  {
   "ko": "자신경",
   "en": "ulnar nerve",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "자신경 깊은가지",
   "en": "deep branch",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "자신경 얕은가지",
   "en": "superficial branch",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "자신경굴",
   "en": "ulnar canal",
   "region": "upper-limb"
  },
  {
   "ko": "자쪽곁동맥",
   "en": "ulnar collateral artery",
   "region": "upper-limb"
  },
  {
   "ko": "자쪽되돌이동맥",
   "en": "ulnar recurrent artery",
   "region": "upper-limb"
  },
  {
   "ko": "자쪽손목굽힘근",
   "en": "flexor carpi ulnaris muscle",
   "region": "upper-limb"
  },
  {
   "ko": "자쪽손목폄근",
   "en": "extensor carpi ulnaris muscle",
   "region": "upper-limb"
  },
  {
   "ko": "자쪽피부정맥",
   "en": "basilic vein",
   "region": "upper-limb"
  },
  {
   "ko": "작은원근",
   "en": "teres minor muscle",
   "region": "upper-limb"
  },
  {
   "ko": "접시위팔인대",
   "en": "glenohumeral ligament",
   "region": "upper-limb"
  },
  {
   "ko": "접시테두리",
   "en": "glenoid labrum",
   "region": "upper-limb"
  },
  {
   "ko": "정중신경",
   "en": "median nerve",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "정중신경 되돌이가지",
   "en": "recurrent branch of median nerve",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "지나 위로올라가 접시위결절",
   "en": "supraglenoid tubercle",
   "region": "upper-limb"
  },
  {
   "ko": "집게폄근",
   "en": "extensor indicis muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "짧은노쪽손목폄근",
   "en": "extensor carpi radialis brevis muscle",
   "region": "upper-limb"
  },
  {
   "ko": "짧은손바닥근",
   "en": "palmaris brevis muscle",
   "region": "upper-limb"
  },
  {
   "ko": "짧은엄지폄근",
   "en": "extensor pollicis brevis muscle",
   "region": "upper-limb"
  },
  {
   "ko": "콩알뼈",
   "en": "pisiform",
   "region": "upper-limb"
  },
  {
   "ko": "큰마름뼈",
   "en": "trapezium",
   "region": "upper-limb"
  },
  {
   "ko": "팔꿈치근",
   "en": "anconeus muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "팔신경얼기 신경다발",
   "en": "cords of brachial plexus",
   "region": "upper-limb"
  },
  {
   "ko": "팔오금까지 추적 위팔동맥",
   "en": "brachial artery",
   "region": "upper-limb"
  },
  {
   "ko": "팔오금에서 가쪽 노동맥",
   "en": "radial artery",
   "region": "upper-limb"
  },
  {
   "ko": "팔오금에서 굵은힘줄 되어 가쪽노 뼈 거친면",
   "en": "radial tuberosity",
   "region": "upper-limb"
  },
  {
   "ko": "팔오금중간정맥",
   "en": "median cubital vein",
   "region": "upper-limb"
  },
  {
   "ko": "폄근널힘줄",
   "en": "extensor expansion",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "폄근지지띠",
   "en": "extensor retinaculum",
   "region": "upper-limb"
  },
  {
   "ko": "해부학코담배갑",
   "en": "anatomical snuffbox",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "확인 긴갈래 힘줄 따라 올라가서 이 힘줄이 접시아래결절",
   "en": "infraglenoid tubercle",
   "region": "upper-limb"
  },
  {
   "ko": "힘줄끈",
   "en": "vincula tendinum",
   "region": "upper-limb"
  },
  {
   "ko": "힘줄사이연결",
   "en": "intertendinous connection",
   "region": "upper-limb"
  },
  {
   "ko": "힘줄윤활집",
   "en": "synovial tendon sheath",
   "region": "upper-limb"
  }
 ],
 "answersStats": {
  "total": 713,
  "numbered": 82,
  "byRegion": {
   "multi": 1,
   "upper-limb": 143,
   "head": 140,
   "neck": 50,
   "abdomen": 216,
   "pelvis-perineum": 163
  }
 },
 "sources": [
  {
   "name": "2회차(0818) 김홍태pf.pdf",
   "folder": "해부1",
   "status": "text_ingested",
   "pages": null,
   "session": 2
  },
  {
   "name": "3회차(0825) 허미선pf.pdf",
   "folder": "해부1",
   "status": "text_ingested",
   "pages": null,
   "session": 3
  },
  {
   "name": "4회차(0828) 허미선pf.pdf",
   "folder": "해부1",
   "status": "text_ingested",
   "pages": null,
   "session": 4
  },
  {
   "name": "5회차(0829) 김홍태pf.pdf",
   "folder": "해부1",
   "status": "text_ingested",
   "pages": null,
   "session": 5
  },
  {
   "name": "6회차(0901) 문용석pf.pdf",
   "folder": "해부1",
   "status": "listed",
   "pages": null,
   "session": 6
  },
  {
   "name": "7회차(0904) 문용석pf.pdf",
   "folder": "해부1",
   "status": "text_ingested",
   "pages": null,
   "session": 7
  },
  {
   "name": "해부 수업계획서.xlsx",
   "folder": "해부2",
   "status": "listed",
   "pages": null,
   "session": null
  },
  {
   "name": "9차시(0911) 김홍태pf.pdf",
   "folder": "해부2",
   "status": "text_ingested",
   "pages": null,
   "session": 9
  },
  {
   "name": "10차시(0918) 허미선pf.pdf",
   "folder": "해부2",
   "status": "text_ingested",
   "pages": null,
   "session": 10
  },
  {
   "name": "11차시(0922) 허미선pf.pdf",
   "folder": "해부2",
   "status": "text_ingested",
   "pages": null,
   "session": 11
  },
  {
   "name": "12차시(0925) 문용석pf.pdf",
   "folder": "해부2",
   "status": "text_ingested",
   "pages": null,
   "session": 12
  },
  {
   "name": "13차시(0929) 김홍태pf.pdf",
   "folder": "해부2",
   "status": "text_ingested",
   "pages": null,
   "session": 13
  },
  {
   "name": "14차시(0930) 문용석pf.pdf",
   "folder": "해부2",
   "status": "text_ingested",
   "pages": null,
   "session": 14
  },
  {
   "name": "15차시(1013) 허미선pf.pdf",
   "folder": "해부2",
   "status": "text_ingested",
   "pages": null,
   "session": 15
  },
  {
   "name": "tagging 2차.pdf",
   "folder": "해부2",
   "status": "text_ingested",
   "pages": null,
   "session": null
  },
  {
   "name": "missing",
   "folder": "missing_source",
   "status": "missing_source",
   "pages": null,
   "session": null
  }
 ]
};
