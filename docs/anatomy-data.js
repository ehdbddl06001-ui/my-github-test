// 자동 생성 파일 — 수정하지 마세요.
// 원본: content/anatomy/**/*.md → `python pipelines/export_anatomy_web.py`
window.MEDKOS_ANATOMY = {
 "generated": "2026-08-12",
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
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "어깨관절"
    }
   ],
   "body": "## 어깨관절을 안정화하는 구조물 (실습 응용과제 1번 그대로)\n\n**돌림근띠(rotator cuff)** — 힘줄이 관절주머니에 단단히 붙어 안정성을 만든다:\n\n| 근육 | 관절주머니에서의 위치 |\n|---|---|\n| 어깨밑근 (subscapularis) | **앞** |\n| 가시위근 (supraspinatus) | 위 |\n| 가시아래근 (infraspinatus) | 뒤위 |\n| 작은원근 (teres minor) | 뒤아래 |\n\n보조 구조물:\n\n- **접시테두리(glenoid labrum)** — 접시오목의 깊이를 깊게 함\n- **접시위팔인대(glenohumeral ligament)** — 관절주머니 앞부분이 두꺼워진 띠.\n  겉보다 **관절주머니 속에서** 더 잘 보인다(위·중간·아래 구분)\n- **부리위팔인대(coracohumeral ligament)** — 부리돌기 가쪽모서리 → 위팔뼈 큰결절\n- **위팔두갈래근 긴갈래** — 위팔가로인대 깊은쪽 결절사이고랑을 지난다\n\n## 관계 문장(말로 설명하기)\n\n1. 어깨밑근은 관절주머니 **앞**을 덮고, 어깨밑근힘줄밑주머니는 관절주머니\n   섬유막구멍과 연결된다.\n2. 관절주머니 섬유막은 안쪽으로 접시오목 모서리, 가쪽으로 위팔뼈 **해부목**에 붙는다.\n3. 부리빗장인대(마름인대 가쪽 + 원뿔인대 안쪽)는 봉우리빗장관절을 간접 지지한다."
  }
 ],
 "questions": [
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
   "refs": [
    {
     "file": "14차시(0930) 문용석pf.pdf",
     "page": null,
     "section": "항문관"
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
   "ko": "가로막면",
   "en": "diaphragmatic surface",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "가로막신경",
   "en": "phrenic nerve",
   "region": "abdomen",
   "priority": "normal"
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
   "ko": "가슴배신경",
   "en": "thoracoabdominal nerve",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "가쪽고샅오목",
   "en": "lateral inguinal fossa",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "가쪽넙다리피부신경",
   "en": "lateral cutaneous nerve of thigh",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "가쪽다리",
   "en": "lateral crus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "가쪽배꼽주름",
   "en": "lateral umbilical fold",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "가쪽활꼴인대",
   "en": "lateral arcuate ligament",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "고환",
   "en": "testis",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "고환날세관",
   "en": "efferent ductule of testis",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "고환동맥",
   "en": "testicular artery",
   "region": "abdomen",
   "priority": "normal"
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
   "ko": "고환정맥",
   "en": "testicular vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "고환집막",
   "en": "tunica vaginalis",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "곧창자",
   "en": "rectum",
   "region": "abdomen",
   "priority": "normal"
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
   "ko": "그물막구멍",
   "en": "omental foramen",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "그물막주머니",
   "en": "omental bursa",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "깊은고샅구멍",
   "en": "deep inguinal ring",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "날문조임근",
   "en": "pyloric sphincter muscle",
   "region": "abdomen",
   "priority": "high"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "넙다리신경",
   "en": "femoral nerve",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "네모엽",
   "en": "quadrate lobe",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "다리사이섬유",
   "en": "intercrural fibers",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "대동맥구멍",
   "en": "aortic hiatus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "대정맥구멍",
   "en": "caval opening",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "돌림주름",
   "en": "circular folds",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "돌막창자입술",
   "en": "",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "돌잘록창자동맥",
   "en": "ileocolic artery",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "돌창자동맥",
   "en": "ileal arteries",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "들문부분",
   "en": "cardial part",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "막창자",
   "en": "cecum",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "막창자꼬리동맥",
   "en": "appendicular artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "막층",
   "en": "membranous layer",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "무장막구역",
   "en": "bare area",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "바깥엉덩동맥",
   "en": "external iliac artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "바깥정삭근막",
   "en": "external spermatic fascia",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "반달선",
   "en": "linea semilunaris",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "방광위오목",
   "en": "supravesical fossa",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "배곧은근",
   "en": "rectus abdominis muscle",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "배곧은근집",
   "en": "rectus sheath",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "배대동맥신경얼기",
   "en": "abdominal aortic plexus",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "배속빗근",
   "en": "internal abdominal oblique muscle",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "백색막",
   "en": "tunica albuginea",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "백색선",
   "en": "linea alba",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "복강동맥",
   "en": "celiac trunk",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "복강신경얼기",
   "en": "celiac plexus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "복막주렁",
   "en": "omental appendices",
   "region": "abdomen",
   "priority": "normal"
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
   "ko": "빈창자동맥",
   "en": "jejunal arteries",
   "region": "abdomen",
   "priority": "normal"
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
   "ko": "세모인대",
   "en": "triangular ligament",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "속정삭근막",
   "en": "internal spermatic fascia",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "식도구멍",
   "en": "esophageal hiatus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "쓸개",
   "en": "gall bladder",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "아래가로막동맥",
   "en": "inferior phrenic artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "아래대정맥",
   "en": "inferior vena cava",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "아래아랫배신경얼기",
   "en": "inferior hypogastric plexus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "아래이자샘창자동맥",
   "en": "inferior pancreaticoduodenal artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "아래창자간막동맥",
   "en": "inferior mesenteric artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "아래창자간막신경얼기",
   "en": "inferior mesenteric plexus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "안쪽고샅오목",
   "en": "medial inguinal fossa",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "안쪽활꼴인대",
   "en": "medial arcuate ligament",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "얕은고샅구멍",
   "en": "superficial inguinal ring",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "얕은배벽동맥",
   "en": "superficial epigastric artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "얕은엉덩휘돌이동맥",
   "en": "superficial circumflex iliac artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "엉덩고샅신경",
   "en": "ilioinguinal nerve",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "엉덩아랫배신경",
   "en": "iliohypogastric nerve",
   "region": "abdomen",
   "priority": "high"
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
   "ko": "오른다리",
   "en": "right crus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "오른위그물막동맥",
   "en": "right gastroomental artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "오른위동맥",
   "en": "right gastric artery",
   "region": "abdomen",
   "priority": "high"
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
   "ko": "온간동맥",
   "en": "common hepatic artery",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "온엉덩정맥",
   "en": "common iliac vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "왼간관",
   "en": "left hepatic duct",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "왼간엽",
   "en": "left lobe of liver",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "왼다리",
   "en": "left crus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "왼위그물막동맥",
   "en": "left gastroomental artery",
   "region": "abdomen",
   "priority": "normal"
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
   "ko": "왼창자동맥",
   "en": "left colic artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "위가로막인대",
   "en": "gastrophrenic ligament",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "위바닥",
   "en": "fundus of stomach",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "위배벽동맥",
   "en": "superior epigastric artery",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "위이자샘창자동맥",
   "en": "superior pancreaticoduodenal artery",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "위창자간막동맥",
   "en": "superior mesenteric artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "위창자간막신경얼기",
   "en": "superior mesenteric plexus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "위창자간막정맥",
   "en": "superior mesenteric vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "음낭사이막",
   "en": "septum of scrotum",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "음부넙다리신경",
   "en": "genitofemoral nerve",
   "region": "abdomen",
   "priority": "normal"
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
   "ko": "작은굽이",
   "en": "lesser curvature",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "작은그물막",
   "en": "lesser omentum",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "작은샘창자유두",
   "en": "minor duodenal papilla",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "작은콩팥잔",
   "en": "minor calices",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "작은허리근",
   "en": "psoas minor muscle",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "잘록창자띠",
   "en": "teniae coli",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "잘록창자팽대",
   "en": "haustra of colon",
   "region": "abdomen",
   "priority": "normal"
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
   "ko": "정세관",
   "en": "seminiferous tubule",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "정중배꼽주름",
   "en": "median umbilical fold",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "정중엉치동맥",
   "en": "",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "중간부신동맥",
   "en": "middle suprarenal artery",
   "region": "abdomen",
   "priority": "normal"
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
   "ko": "지라동맥",
   "en": "splenic artery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "지라문",
   "en": "splenic hilum",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "지라정맥",
   "en": "splenic vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "지방층",
   "en": "fatty layer",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "짧은위동맥",
   "en": "short gastric arteries",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "창자간막",
   "en": "mesentery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "창자간막뿌리",
   "en": "root of mesentery",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "콩팥겉질",
   "en": "renal cortex",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "콩팥근막",
   "en": "renal fascia",
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "콩팥정맥",
   "en": "renal veins",
   "region": "abdomen",
   "priority": "high"
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
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "큰콩팥잔",
   "en": "major calices",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "큰허리근",
   "en": "psoas major muscle",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "허리네모근",
   "en": "quadratus lumborum muscle",
   "region": "abdomen",
   "priority": "high"
  },
  {
   "ko": "허리동맥",
   "en": "lumbar arteries",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "허리신경얼기",
   "en": "lumbar plexus",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "허리정맥",
   "en": "lumbar vein",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "활꼴선",
   "en": "arcuate line",
   "region": "abdomen",
   "priority": "normal"
  },
  {
   "ko": "가쪽곧은근",
   "en": "lateral rectus muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "가쪽눈꺼풀인대",
   "en": "lateral palpebral ligament",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "각막",
   "en": "cornea",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "갓돌림신경",
   "en": "abducens nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "결막",
   "en": "conjunctiva",
   "region": "head",
   "priority": "normal"
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
   "ko": "고실천장",
   "en": "tegmental wall",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "공막",
   "en": "sclera",
   "region": "head",
   "priority": "high"
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
   "ko": "긴섬모체신경",
   "en": "long ciliary nerve",
   "region": "head",
   "priority": "normal"
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
   "region": "head",
   "priority": "normal"
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
   "ko": "눈꺼풀판",
   "en": "tarsal plate",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈돌림신경",
   "en": "oculomotor nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈동맥",
   "en": "ophthalmic artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈둘레근",
   "en": "",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈물샘",
   "en": "lacrimal gland",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈물샘신경",
   "en": "lacrimal nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈물소관",
   "en": "lacrimal canaliculus",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈확뼈막",
   "en": "periorbita",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈확사이막",
   "en": "orbital septum",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "눈확위신경",
   "en": "supraorbital nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "더부신경",
   "en": "accessory nerve",
   "region": "head",
   "priority": "normal"
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
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "도르래아래신경",
   "en": "infratrochlear nerve",
   "region": "head",
   "priority": "normal"
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
   "region": "head",
   "priority": "normal"
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
   "ko": "뒤벌집신경",
   "en": "posterior ethmoidal nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "뒤아래소뇌동맥",
   "en": "anterior and posterior inferior cerebellar artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "뒤콧구멍",
   "en": "choana",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "등자뼈",
   "en": "stapes",
   "region": "head",
   "priority": "normal"
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
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "맥락막",
   "en": "choroid",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "모루뼈",
   "en": "incus",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "목구멍",
   "en": "fauces",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "목구멍편도",
   "en": "palatine tonsil",
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
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "목정맥오목",
   "en": "jugular fossa",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "미로동맥",
   "en": "labyrinthine arteries",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "미주신경",
   "en": "vagus nerve",
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
   "ko": "반달틈새",
   "en": "semilunar hiatus",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "분계고랑",
   "en": "terminal sulcus",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "붓혀근",
   "en": "styloglossus muscle",
   "region": "head",
   "priority": "normal"
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
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "성곽유두",
   "en": "vallate papilla",
   "region": "head",
   "priority": "normal"
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
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "속목정맥",
   "en": "internal jugular vein",
   "region": "head",
   "priority": "normal"
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
   "ko": "시각신경원반",
   "en": "optic disc",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "아래곧은근",
   "en": "inferior rectus muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "아래빗근",
   "en": "inferior oblique muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "아래코선반",
   "en": "inferior nasal concha",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "아래콧길",
   "en": "inferior nasal meatus",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "아래턱신경",
   "en": "mandibular nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "안쪽곧은근",
   "en": "medial rectus muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "안쪽눈꺼풀인대",
   "en": "medial palpebral ligament",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "앞교통동맥",
   "en": "anterior communicating artery",
   "region": "head",
   "priority": "normal"
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
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "얼굴신경",
   "en": "facial nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "온힘줄고리",
   "en": "common tendinous ring",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "위곧은근",
   "en": "superior rectus muscle",
   "region": "head",
   "priority": "normal"
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
   "region": "head",
   "priority": "normal"
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
   "ko": "유리체",
   "en": "vitreous body",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "이마굴",
   "en": "ethmoidal cells",
   "region": "head",
   "priority": "normal"
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
   "ko": "입인두",
   "en": "Oropharynx",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "입천장긴장근",
   "en": "tensor veli palatini muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "입천장올림근",
   "en": "levator veli palatini muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "입천장인두근",
   "en": "palatopharyngeus muscle",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "입천장인두활",
   "en": "palatopharyngeal arch",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "입천장혀근",
   "en": "palatoglossus muscle",
   "region": "head",
   "priority": "high"
  },
  {
   "ko": "입천장혀활",
   "en": "palatoglossal arch",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "정수리점",
   "en": "",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "조롱박오목",
   "en": "piriform fossa",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "중간뇌막동맥",
   "en": "middle meningeal artery",
   "region": "head",
   "priority": "normal"
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
   "ko": "척추동맥",
   "en": "vertebral artery",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "코눈물관",
   "en": "nasolacrimal duct",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "코섬모체신경",
   "en": "nasociliary nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "코인두",
   "en": "Nasopharynx",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "코중격",
   "en": "nasal septum",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "콧구멍",
   "en": "nares",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "큰입천장신경",
   "en": "greater palatine nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "타원구멍",
   "en": "foramen ovale",
   "region": "head",
   "priority": "normal"
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
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "해면정맥굴",
   "en": "cavernous sinus",
   "region": "head",
   "priority": "normal"
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
   "ko": "혀밑신경",
   "en": "hypoglossal nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "혀밑신경관",
   "en": "hypoglossal canal",
   "region": "head",
   "priority": "normal"
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
   "ko": "혀인두신경",
   "en": "glossopharyngeal nerve",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "혀정중고랑",
   "en": "midline sulcus of tongue",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "홍채",
   "en": "iris",
   "region": "head",
   "priority": "normal"
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
   "ko": "후두어귀",
   "en": "laryngeal inlet",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "후두인두",
   "en": "Laryngopharynx",
   "region": "head",
   "priority": "normal"
  },
  {
   "ko": "뒤세로인대",
   "en": "",
   "region": "multi",
   "priority": "normal"
  },
  {
   "ko": "가로모뿔근",
   "en": "transverse arytenoid muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "가쪽반지모뿔근",
   "en": "lateral cricoarytenoid muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "거짓성대",
   "en": "false vocal cord",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "귀관인두근",
   "en": "salpingopharyngeus muscle",
   "region": "neck",
   "priority": "normal"
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
   "ko": "날개아래턱솔기",
   "en": "pterygomandibular raphe",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "되돌이후두신경",
   "en": "recurrent laryngeal nerve",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "뒤반지모뿔근",
   "en": "posterior cricoarytenoid muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "모뿔덮개근",
   "en": "aryepiglottic muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "모뿔덮개주름",
   "en": "aryepiglottic fold",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "모뿔연골",
   "en": "arytenoid cartilage",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "반지방패근",
   "en": "cricothyroid muscle",
   "region": "neck",
   "priority": "normal"
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
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "방패연골",
   "en": "thyroid cartilage",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "붓인두근",
   "en": "stylopharyngeus muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "빗모뿔근",
   "en": "oblique arytenoid muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "성대문아래공간",
   "en": "infraglottic cavity",
   "region": "neck",
   "priority": "normal"
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
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "성대주름",
   "en": "vocal fold",
   "region": "neck",
   "priority": "high"
  },
  {
   "ko": "쐐기연골",
   "en": "cuneiform cartilage",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "아래인두수축근",
   "en": "inferior constrictor muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "아래후두신경",
   "en": "inferior laryngeal nerve",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "안뜰주름",
   "en": "vestibular fold",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "위인두수축근",
   "en": "superior constrictor muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "위후두신경",
   "en": "superior laryngeal nerve",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "인두솔기",
   "en": "pharyngeal raphe",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "인두신경얼기",
   "en": "pharyngeal plexus",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "인두오목",
   "en": "pharyngeal recess",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "잔뿔연골",
   "en": "corniculate cartilage",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "중간인두수축근",
   "en": "middle constrictor muscle",
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "참성대",
   "en": "true vocal cord",
   "region": "neck",
   "priority": "normal"
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
   "region": "neck",
   "priority": "normal"
  },
  {
   "ko": "후두안뜰",
   "en": "laryngeal vestibule",
   "region": "neck",
   "priority": "normal"
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
   "ko": "고유난소인대",
   "en": "ligament of ovary",
   "region": "pelvis-perineum",
   "priority": "high"
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
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "깊은샅가로근",
   "en": "deep transverse perineal muscle",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "en": "posterior labial commissure",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "en": "external urethral sphincter",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "바깥항문조임근",
   "en": "external anal sphincter muscle",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "ko": "불두덩",
   "en": "mons pubis",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "비뇨생식구멍",
   "en": "urogenital hiatus",
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
   "ko": "샅동맥",
   "en": "perineal artery",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "샅막",
   "en": "perineal membrane",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "샅신경",
   "en": "perineal nerve",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "샅중심체",
   "en": "perineal body",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "소음순",
   "en": "labia minora",
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
   "ko": "아래곧창자동맥",
   "en": "inferior rectal artery",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "아래곧창자신경",
   "en": "inferior rectal nerve",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "ko": "얕은샅가로근",
   "en": "superficial transverse perineal muscle",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "ko": "엉치결절인대",
   "en": "",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "엉치신경얼기",
   "en": "sacral plexus",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음경고리인대",
   "en": "fundiform ligament of penis",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음경꺼풀주름띠",
   "en": "frenulum of prepuce",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음경다리",
   "en": "crus of penis",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음경등동맥",
   "en": "dorsal artery of penis",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음경등신경",
   "en": "dorsal nerve of penis",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음경망울",
   "en": "bulb of penis",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음경몸통",
   "en": "body of penis",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음경해면체",
   "en": "corpus cavernosum of penis",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음핵꺼풀",
   "en": "prepuce of clitoris",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "음핵주름띠",
   "en": "frenulum of clitoris",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "ko": "자궁원인대",
   "en": "round ligament of uterus",
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
   "ko": "정관",
   "en": "ductus deferens",
   "region": "pelvis-perineum"
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
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "질어귀",
   "en": "vestibule of vagina",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "ko": "큰질어귀샘",
   "en": "greater vestibular gland",
   "region": "pelvis-perineum",
   "priority": "normal"
  },
  {
   "ko": "큰질어귀샘관",
   "en": "duct of greater vestibular gland",
   "region": "pelvis-perineum",
   "priority": "normal"
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
   "ko": "폐쇄신경",
   "en": "obturator nerve",
   "region": "pelvis-perineum"
  },
  {
   "ko": "항문곧창자연결",
   "en": "anorectal junction",
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
   "ko": "가슴등동맥",
   "en": "thoracodorsal artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "가슴등신경",
   "en": "thoracodorsal nerve",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "가슴봉우리동맥",
   "en": "thoracoacromial artery",
   "region": "upper-limb",
   "priority": "normal"
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
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "가쪽가슴동맥",
   "en": "lateral thoracic artery",
   "region": "upper-limb",
   "priority": "normal"
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
   "region": "upper-limb",
   "priority": "normal"
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
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "고유바닥쪽손가락동맥",
   "en": "proper palmar digital arteries",
   "region": "upper-limb",
   "priority": "normal"
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
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "긴노쪽손목폄근",
   "en": "extensor carpi radialis longus muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "긴손바닥근",
   "en": "palmaris longus muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "긴엄지굽힘근",
   "en": "flexor pollicis longus muscle",
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
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "깊은손가락굽힘근",
   "en": "flexor digitorum profundus muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "깊은손바닥동맥활",
   "en": "deep palmar arch",
   "region": "upper-limb",
   "priority": "normal"
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
   "region": "upper-limb",
   "priority": "normal"
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
   "ko": "노쪽되돌이동맥",
   "en": "radial recurrent artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "노쪽손목굽힘근",
   "en": "flexor carpi radialis muscle",
   "region": "upper-limb",
   "priority": "normal"
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
   "en": "posterior interosseous nerve",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "뒤위팔피부신경",
   "en": "posterior cutaneous nerve of arm",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "뒤위팔휘돌이동맥",
   "en": "posterior circumflex humeral artery",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "뒷벽",
   "en": "posterior wall",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "등쪽뼈사이근",
   "en": "dorsal interossei muscles",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "마름인대",
   "en": "trapezoid ligament",
   "region": "upper-limb"
  },
  {
   "ko": "몸쪽노자관절",
   "en": "proximal radioulnar joint",
   "region": "upper-limb"
  },
  {
   "ko": "바닥쪽뼈사이근",
   "en": "palmar interossei muscles",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "반달뼈",
   "en": "lunate",
   "region": "upper-limb"
  },
  {
   "ko": "벌레근",
   "en": "lumbrical muscles",
   "region": "upper-limb",
   "priority": "normal"
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
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "부리위팔인대",
   "en": "coracohumeral ligament",
   "region": "upper-limb"
  },
  {
   "ko": "빗장밑근",
   "en": "subclavius muscle",
   "region": "upper-limb",
   "priority": "normal"
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
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "새끼벌림근",
   "en": "abductor digiti minimi muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "새끼폄근",
   "en": "extensor digiti minimi muscle",
   "region": "upper-limb",
   "priority": "normal"
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
   "ko": "손가락섬유집",
   "en": "fibrous sheaths of digits of hand",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "손가락폄근",
   "en": "extensor digitorum muscle",
   "region": "upper-limb",
   "priority": "normal"
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
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "손목굴",
   "en": "carpal tunnel",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "손배뼈",
   "en": "scaphoid",
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
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "아래자쪽곁동맥",
   "en": "inferior ulnar collateral artery",
   "region": "upper-limb",
   "priority": "normal"
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
   "ko": "안쪽벽",
   "en": "medial wall",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "안쪽아래팔피부신경",
   "en": "medial cutaneous nerve of forearm",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "안쪽위팔피부신경",
   "en": "medial cutaneous nerve of arm",
   "region": "upper-limb",
   "priority": "normal"
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
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "얕은손가락굽힘근",
   "en": "flexor digitorum superficialis muscle",
   "region": "upper-limb",
   "priority": "normal"
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
   "ko": "어깨밑동맥",
   "en": "subscapular artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "어깨휘돌이동맥",
   "en": "circumflex scapular artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "엄지맞섬근",
   "en": "opponens pollicis muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "엄지모음근",
   "en": "adductor pollicis muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "온바닥쪽손가락동맥",
   "en": "common palmar digital arteries",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "온뼈사이동맥",
   "en": "common interosseous artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "원뿔인대",
   "en": "conoid ligament",
   "region": "upper-limb"
  },
  {
   "ko": "원엎침근",
   "en": "pronator teres muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "위가슴동맥",
   "en": "superior thoracic artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "위가쪽위팔피부신경",
   "en": "superior lateral cutaneous nerve of arm",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "위어깨밑신경",
   "en": "superior subscapular nerves",
   "region": "upper-limb",
   "priority": "normal"
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
   "en": "brachioradialis muscle",
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
   "ko": "위팔세갈래근",
   "en": "triceps brachii muscle",
   "region": "upper-limb",
   "priority": "normal"
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
   "ko": "자쪽되돌이동맥",
   "en": "ulnar recurrent artery",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "자쪽손목굽힘근",
   "en": "flexor carpi ulnaris muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "자쪽손목폄근",
   "en": "extensor carpi ulnaris muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "자쪽피부정맥",
   "en": "basilic vein",
   "region": "upper-limb",
   "priority": "normal"
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
   "ko": "집게폄근",
   "en": "extensor indicis muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "짧은노쪽손목폄근",
   "en": "extensor carpi radialis brevis muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "짧은새끼굽힘근",
   "en": "flexor digiti minimi brevis muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "짧은손바닥근",
   "en": "palmaris brevis muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "짧은엄지굽힘근",
   "en": "flexor pollicis brevis muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "짧은엄지벌림근",
   "en": "abductor pollicis brevis muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "짧은엄지폄근",
   "en": "extensor pollicis brevis muscle",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "팔꿈치근",
   "en": "anconeus muscle",
   "region": "upper-limb",
   "priority": "high"
  },
  {
   "ko": "팔오금중간정맥",
   "en": "median cubital vein",
   "region": "upper-limb",
   "priority": "normal"
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
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "해부학코담배갑",
   "en": "anatomical snuffbox",
   "region": "upper-limb",
   "priority": "normal"
  },
  {
   "ko": "힘줄사이연결",
   "en": "intertendinous connections",
   "region": "upper-limb",
   "priority": "normal"
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
   "status": "listed",
   "pages": null,
   "session": 2
  },
  {
   "name": "3회차(0825) 허미선pf.pdf",
   "folder": "해부1",
   "status": "listed",
   "pages": null,
   "session": 3
  },
  {
   "name": "4회차(0828) 허미선pf.pdf",
   "folder": "해부1",
   "status": "listed",
   "pages": null,
   "session": 4
  },
  {
   "name": "5회차(0829) 김홍태pf.pdf",
   "folder": "해부1",
   "status": "listed",
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
   "status": "listed",
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
   "status": "listed",
   "pages": null,
   "session": 9
  },
  {
   "name": "10차시(0918) 허미선pf.pdf",
   "folder": "해부2",
   "status": "listed",
   "pages": null,
   "session": 10
  },
  {
   "name": "11차시(0922) 허미선pf.pdf",
   "folder": "해부2",
   "status": "listed",
   "pages": null,
   "session": 11
  },
  {
   "name": "12차시(0925) 문용석pf.pdf",
   "folder": "해부2",
   "status": "listed",
   "pages": null,
   "session": 12
  },
  {
   "name": "13차시(0929) 김홍태pf.pdf",
   "folder": "해부2",
   "status": "listed",
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
   "status": "listed",
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
