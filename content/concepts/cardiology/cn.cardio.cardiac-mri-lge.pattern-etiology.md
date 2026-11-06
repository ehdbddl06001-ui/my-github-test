---
id: cn.cardio.cardiac-mri-lge.pattern-etiology
type: concept
topic: Cardiology
see_also: []
date: 2026-11-07
updated: 2026-11-07
version: 1
outline: h241            # 기본틀 슬롯 — 해리슨 22판 248장 Noninvasive Cardiac Imaging
confidence: high
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 [gap] 으로 쓴 정리본(오답 연결 없음)
title: "심장 MRI 지연조영 — 층과 분포가 원인을 가른다"
objective: "심장 MRI 지연 가돌리늄 조영증강(LGE)의 층과 분포로 심근경색과 비허혈성 심근질환(심근염·아밀로이드증·비후성 심근병증·사르코이드증)을 가른다"
objective_kind: 진단
condition: 심장 자기공명영상(cardiac magnetic resonance, CMR)의 지연 가돌리늄 조영증강(late gadolinium enhancement, LGE)
exams: [kmle, usmle]
summary:
  - "결론: 심내막하에서 시작해 관상동맥 영역을 따르는 LGE 는 경색, 중층·심외막하에 영역을 따르지 않으면 비허혈성이다 [[harrison-22: 248장 p.1894]]"
  - "시험 단서: 흉통·트로포닌 상승, 관상동맥 정상인 젊은 환자의 심외막하·중층 다발 LGE(late gadolinium enhancement) = 심근염."
  - "왜: LGE 는 흉터·섬유화에 남은 조영제라, 경색은 한 관상동맥 영역의 심내막부터, 염증·침윤은 영역과 무관하게 남는다 [[harrison-22: 248장 p.1887, p.1894]]"
  - "부하 관류결손에 LGE 가 없으면 허혈(살아 있는 심근), 있으면 흉터다 [[harrison-22: 248장 p.1887–1888]]"
  - "중증 신기능 저하·투석도 group II(대환형) 가돌리늄은 안전하다 — 검사 전 eGFR 확인은 더 권하지 않는다 [[harrison-22: 248장 p.1884]]"
criteria:
  - id: lge-infarct-detection
    name: LGE 의 경색 검출
    kind: 진단
    population: "급성·만성 심근경색이 의심되는 성인"
    statement: "LGE 는 경색의 유무와 범위를 보는 가장 좋은 검사다. 다기관 연구에서 경색 위치를 정확히 찾았고 급성 경색 민감도 99 %, 만성 경색 94 % 였다. 관상동맥 영역의 LGE 는 경색에 거의 특이적이다 [[harrison-22: 248장 p.1882, p.1893]]"
    exceptions: "경색 안의 어두운 핵(밝은 LGE 로 둘러싸인 저신호)은 미세혈관 폐쇄(no-reflow)이고, LGE 와 함께 위험 증가의 표지다 [[harrison-22: 248장 p.1893]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
  - id: gbca-renal-safety
    name: 가돌리늄 조영제와 신기능
    kind: 금기
    population: "CMR 적응이 있는 만성 신질환·투석 환자"
    statement: "신원성 전신섬유증(nephrogenic systemic fibrosis, NSF)은 옛 group I(선형) 가돌리늄을 eGFR < 30 mL/min/1.73 m² · 투석 · 급성 신기능 악화에서 고용량 쓸 때 생겼다. group II(대환형)는 중증 신기능 저하·투석에서도 안전하다고 보며 검사 전 eGFR 확인을 더 권하지 않는다 [[harrison-22: 248장 p.1884]]"
    exceptions: "가벼운 반응(가려움·발적)은 약 1 %, 중증·아나필락시스는 약 20만 명에 1명 [[harrison-22: 248장 p.1884]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 248: Noninvasive Cardiac Imaging: Echocardiography, Nuclear Cardiology, and Magnetic Resonance/Computed Tomography Imaging"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 248장 p.1882–1897"
    checked_at: 2026-11-07
    checked: "드라이브 22판 장별 문서 H22_248 본문 대조 — 관상동맥 영역 LGE 는 경색에 거의 특이적, 비허혈성 심근병증은 전반적 확장·기능 저하(p.1882) · GBCA 안전성: 가벼운 반응 ~1 %, 중증 ~1/200,000, group I 선형 GBCA 와 NSF 위험인자(eGFR < 30, 투석, eGFR < 15, 급성 신기능 악화, 염증 질환), group II 대환형은 중증 신기능 저하·투석에서 안전(ACR), eGFR 사전 확인 더는 권하지 않음(p.1884) · 부하 관류 CMR: 관류결손 = 저신호, 수 분 뒤 LGE = 밝은 흉터, 관류결손과 경색 비교로 허혈 정량, SPECT 가 놓치는 심내막하 허혈·경색 검출(p.1887), 그림 248-14 전벽에 LGE 없음 → 관류결손은 허혈(LAD 협착)(p.1888) · CMR 이 ACS 흉내(급성 심근염·타코츠보·심낭염) 감별, 그림 248-16 급성 심근염 LGE 는 심외막 쪽·심내막 보존·측벽 다발(바이러스 심근염)(p.1890) · LGE 가 경색 검출 최선, 급성 99 %·만성 94 % 민감도, 미세혈관 폐쇄 = 밝은 경색 안 어두운 영역, LGE·MVO 는 위험 표지(p.1893) · LGE 패턴: 경색은 심내막하에서 시작해 관상동맥 영역, 침윤·염증성 심근병증은 중층·심외막하에 영역 무관, T1/T2 지도로 부종, T2* 로 철 침착, 아밀로이드증 양심실 벽 두꺼움·양심방 확대·좌심실과 심방의 미만성 심내막 침윤, 변형률 심첨부 보존, 뼈 스캔으로 ATTR(강한 99mTc 섭취) vs AL, 비후성 심근병증은 비대 부위의 강한 LGE(p.1894) · 그림 248-26 광범위 LGE = 흉터·생존 불가 심근(p.1895) · 그림 248-27 경색 = 하벽 심내막 LGE + 벽 얇아짐, 아밀로이드 = 좌심실·좌심방·심방중격 미만성 LGE + 어두운 혈액풀, 22세 흉통·트로포닌 상승의 중층 다발 LGE = 급성 심근염, 그림 248-28 아밀로이드 원주형 심내막하 우세 미만성 LGE·PYP 섭취(p.1896) · 그림 248-29 HCM 중격 비후 부위 LGE = 섬유화, 그림 248-30 완전방실차단 45세의 좌심실 전벽·전중격 심외막하 + 우심실 자유벽 LGE 와 같은 부위 FDG 섭취 = 활동성 사르코이드증, PET 는 사르코이드 염증·치료 반응 추적(p.1894, p.1897)"
    verified: text
tables:
  - id: lge-pattern-table
    title: "LGE 패턴 — 어느 층·어느 분포인가"
    role: differential
    span: column
    section: "가르는 소견 — 층과 분포"
    columns: ["LGE 패턴", "생각할 질환", "같이 보는 소견"]
    rows:
      - ["심내막하에서 시작, 한 관상동맥 영역", "심근경색(허혈성)", "그 영역 벽이 얇음·벽운동 이상, 안쪽 어두운 핵 = 미세혈관 폐쇄 [[harrison-22: 248장 p.1893–1894, p.1896]]"]
      - ["심외막하·중층 다발, 심내막 보존(측벽 흔함)", "급성 심근염", "흉통·트로포닌 상승, T1/T2 지도의 부종 [[harrison-22: 248장 p.1890, p.1894, p.1896]]"]
      - ["미만성, 원주형 심내막하 우세, 심방·심방중격까지", "심장 아밀로이드증", "양심실 벽 두꺼움·양심방 확대·어두운 혈액풀, 뼈 스캔으로 ATTR vs AL [[harrison-22: 248장 p.1894, p.1896]]"]
      - ["가장 두꺼운 부위(중격)에 강한 LGE", "비후성 심근병증", "비대·유출로 폐쇄, LGE = 섬유화 [[harrison-22: 248장 p.1894, p.1897]]"]
      - ["심외막하 전벽·전중격 + 우심실 자유벽", "심장 사르코이드증", "전도 차단(완전방실차단), 같은 부위 FDG-PET 섭취 [[harrison-22: 248장 p.1894, p.1897]]"]
    note: "층(심내막하 vs 중층·심외막하)과 분포(관상동맥 영역 vs 무관)를 따로 읽는다."
pitfalls:
  - contrast: "급성 심근염 vs 심근경색 — 둘 다 흉통·트로포닌 상승"
    point: "LGE 가 심내막을 침범하느냐가 가른다. 경색은 심내막하에서 시작해 관상동맥 영역을 따르고, 심근염은 심외막 쪽·중층에 다발로 생기며 심내막을 남긴다 [[harrison-22: 248장 p.1890, p.1894]]"
    exception: "CMR 은 타코츠보·심낭염 같은 다른 ACS 흉내도 가른다 — 관상동맥 정상만으로 심근염을 확정하지 않는다 [[harrison-22: 248장 p.1890]]"
  - contrast: "부하 관류결손 vs LGE — 「결손이면 다 경색」?"
    point: "관류결손은 부하 때 혈류가 모자란 것, LGE 는 이미 생긴 흉터다. 관류결손 자리에 LGE 가 없으면 허혈(살아 있는 심근)이고, 광범위 LGE 는 생존 불가 심근이다 [[harrison-22: 248장 p.1887–1888, p.1895]]"
    exception: "부하 CMR 은 SPECT 가 놓치는 심내막하 허혈·경색까지 본다 — 공간 해상도가 높기 때문이다 [[harrison-22: 248장 p.1887]]"
  - contrast: "아밀로이드증의 심내막하 LGE vs 경색 — 「심내막하면 허혈」?"
    point: "분포가 가른다. 아밀로이드증은 관상동맥 영역과 무관하게 좌심실 전 분절과 심방·심방중격까지 미만성으로 퍼지고 혈액풀이 어둡다. 경색은 한 영역에 국한되고 그 벽이 얇다 [[harrison-22: 248장 p.1894, p.1896]]"
    exception: "아밀로이드형 확인은 뼈 스캔이 맡는다 — ATTR 은 99mTc 섭취가 강하고 AL 은 약하다 [[harrison-22: 248장 p.1894]]"
  - contrast: "투석 환자에게 가돌리늄은 금기?"
    point: "아니다. 신원성 전신섬유증은 옛 group I(선형) 조영제의 문제였고, group II(대환형)는 중증 신기능 저하·투석에서도 안전하다고 본다 [[harrison-22: 248장 p.1884]]"
    exception: "group I 을 고용량 쓸 때의 위험인자: eGFR < 30, 투석, 급성 신기능 악화, 전신 염증 질환 [[harrison-22: 248장 p.1884]]"
diagram:
  title: "심장 MRI LGE — 층과 분포로 원인 가르기"
  nodes:
    - {id: start, kind: start, text: "원인 미상 심근 손상 — CMR 시행"}
    - {id: lge, kind: decision, text: "지연조영증강(LGE)이 있나?"}
    - {id: stress, kind: info, text: "부하 관류·T1/T2 지도를 추가로 본다"}
    - {id: ischemia, kind: end, text: "관류결손만 — 허혈, 생존 심근"}
    - {id: layer, kind: decision, text: "심내막하·관상 영역을 따르나?"}
    - {id: infarct, kind: end, text: "심근경색 흉터 — 허혈성"}
    - {id: pattern, kind: decision, text: "어느 층·분포인가?"}
    - {id: myocarditis, kind: alert, text: "심외막하·중층 다발 — 심근염"}
    - {id: amyloid, kind: end, text: "미만성·심방까지 — 아밀로이드증"}
    - {id: hcm, kind: end, text: "비대 부위 — 비후성 심근병증"}
    - {id: sarcoid, kind: end, text: "심외막하+우심실 — 사르코이드증"}
  edges:
    - {from: start, to: lge}
    - {from: lge, to: stress, label: "없음"}
    - {from: stress, to: ischemia, label: "부하 결손"}
    - {from: lge, to: layer, label: "있음"}
    - {from: layer, to: infarct, label: "예"}
    - {from: layer, to: pattern, label: "아니오"}
    - {from: pattern, to: myocarditis, label: "다발·심내막 보존"}
    - {from: pattern, to: amyloid, label: "미만성"}
    - {from: pattern, to: hcm, label: "두꺼운 벽"}
    - {from: pattern, to: sarcoid, label: "우심실·전도차단"}
diagram_notes:
  - "경색 LGE 안의 어두운 핵은 미세혈관 폐쇄(no-reflow) — 위험 증가의 표지."
  - "아밀로이드증: 양심실 벽 두꺼움·양심방 확대·어두운 혈액풀, ATTR vs AL 은 뼈 스캔. 사르코이드 염증·치료 반응은 FDG-PET."
  - "group II(대환형) 가돌리늄은 중증 신기능 저하·투석에서도 쓴다."
checks:
  - q: "22세 흉통·트로포닌 상승, 관상동맥 정상. CMR 에서 측벽 심외막하에 다발성 LGE 가 있고 심내막은 보존된다. 진단은?"
    a: "급성(바이러스) 심근염 — 경색은 심내막하에서 시작해 관상동맥 영역을 따른다."
  - q: "부하 관류 CMR 에서 전벽 관류결손이 있지만 같은 부위에 LGE 가 없다. 의미는?"
    a: "허혈(살아 있는 심근) — 흉터가 아니므로 협착(LAD)을 찾는다."
  - q: "좌심실 전 분절과 심방중격까지 미만성 LGE, 혈액풀이 어둡다. 다음으로 아형을 가를 검사는?"
    a: "뼈 스캔(99mTc) — ATTR 은 섭취가 강하고 AL 은 약하다."
  - q: "투석 환자에게 CMR 이 필요하다. 가돌리늄 조영제를 쓸 수 있나?"
    a: "group II(대환형) 조영제는 안전하다고 본다 — NSF 는 옛 group I 의 문제였다."
figures_wanted:
- source: PMC_OA
  shows: 급성 심근염의 심외막하·중층 LGE(심내막 보존)
  at: 가르는 소견 — 층과 분포
  query: '"myocarditis" AND "late gadolinium enhancement" AND "case report"'
  caption_terms:
  - late gadolinium
  - myocarditis
  modality: MR
---

## 판단 — 층을 먼저, 분포를 다음에
- **LGE 는 흉터·섬유화를 밝게 보여 준다.** 조영제 주입 수 분 뒤 정상 심근은 어둡고 흉터는 희게 남는다 [[harrison-22: 248장 p.1887]].
- **심내막하에서 시작해 한 관상동맥 영역을 따르면 경색이다.** 그 영역의 벽이 얇고 벽운동이 떨어지면 허혈성 원인을 강하게 시사한다 [[harrison-22: 248장 p.1882, p.1894]].
- **중층·심외막하에 영역과 무관하게 있으면 비허혈성이다** — 그다음 분포(다발·미만·비대 부위·우심실)로 질환을 고른다. 무엇을 생각할지는 표에 한 번만 모았다 [[harrison-22: 248장 p.1894]].
- **LGE 가 없으면 끝이 아니다.** 부하 관류결손이 있으면 허혈, T1/T2 지도의 부종은 급성 염증을 시사한다 [[harrison-22: 248장 p.1887, p.1894]].

## 기전 — 조영제가 남는 자리
가돌리늄 조영제(gadolinium-based contrast agent, GBCA)는 킬레이트로 묶여 콩팥으로 나간다 [[harrison-22: 248장 p.1884]]. 부하 관류 영상에서는 조영제가 처음 지나갈 때 혈류가 모자란 부위가 어둡게(관류결손) 보이고, 수 분 뒤 지연 영상에서는 흉터 부위가 밝게 남는다. 그래서 같은 자리를 두 영상으로 비교하면 「혈류는 모자라지만 살아 있는 심근(허혈)」과 「이미 죽은 심근(경색)」을 가를 수 있다 [[harrison-22: 248장 p.1887–1888]].

어디에 남는지가 원인을 말한다. 경색은 막힌 관상동맥이 먹이는 영역의 심내막하에서 시작한다. 반면 심근염·사르코이드증 같은 염증과 아밀로이드증 같은 침윤은 혈관 영역과 상관없이 중층·심외막하나 심근 전체에 생긴다 [[harrison-22: 248장 p.1894]]. 아밀로이드증은 침착이 심실과 심방에 미만성으로 퍼지고 조영제가 몸 곳곳의 아밀로이드로 빠져 혈액풀이 어둡게 보인다 [[harrison-22: 248장 p.1896]]. 비후성 심근병증은 가장 두꺼운 부위의 섬유화가 LGE 로 보인다 [[harrison-22: 248장 p.1897]].

## 가르는 소견 — 층과 분포
- 급성 심근염과 경색은 둘 다 흉통·트로포닌 상승으로 온다 — 심내막 침범 여부가 가른다(혼동 항목) [[harrison-22: 248장 p.1890]].
- 경색 LGE 안의 어두운 핵은 미세혈관 폐쇄다. 벽 안 혈전도 어둡게 보이지만 혈전은 첫 관류에서 조영되지 않고 「검은 테두리에 밝은 가운데」 모양을 보인다 [[harrison-22: 248장 p.1893, p.1898]].
- 음성 결과의 한계: LGE 는 흉터를 보므로 흉터가 없는 허혈은 부하 관류로, 활동성 염증의 정도는 T1/T2 지도나 FDG-PET 로 따로 본다 [[harrison-22: 248장 p.1887, p.1894]].

## 권고와 예외
- 경색 유무·범위는 LGE 가 가장 좋다(급성 민감도 99 %, 만성 94 %). LGE 와 미세혈관 폐쇄는 위험 증가의 표지다 [[harrison-22: 248장 p.1893]].
- 아밀로이드증 아형은 뼈 스캔으로 가르고, 사르코이드증은 FDG-PET 로 활동성 염증과 면역억제 치료 반응을 추적한다 [[harrison-22: 248장 p.1894]].
- group II 가돌리늄은 중증 신기능 저하·투석에서도 쓴다. 가벼운 반응은 약 1 %, 중증은 약 20만 명에 1명이다 [[harrison-22: 248장 p.1884]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 248장 p.1882~1898)
