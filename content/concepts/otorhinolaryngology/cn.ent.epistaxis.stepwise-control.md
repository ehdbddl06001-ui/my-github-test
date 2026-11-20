---
id: cn.ent.epistaxis.stepwise-control
type: concept
topic: Otorhinolaryngology
see_also: [Emergency Medicine]
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: ent.sinus   # 기본틀 슬롯(content/outline/subjects.yaml) — 이비인후과 손 슬롯 「비염·부비동염과 비출혈」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "비출혈 — 압박에서 시작해 한 단계씩 올린다"
objective: "비출혈 환자에서 활력징후와 출혈 부위(앞쪽 키셀바흐 부위 vs 뒤쪽)에 따라 압박 → 혈관수축제·소작 → 앞쪽 패킹 → 뒤쪽 패킹 → 동맥 결찰·색전의 다음 단계를 고른다"
objective_kind: 다음 처치
condition: 비출혈(epistaxis) — 앞쪽 비출혈(anterior epistaxis) · 뒤쪽 비출혈(posterior epistaxis)
exams: [kmle, usmle]
figures_none: "처치 순서를 고르는 목표 — 영상 소견이 시험 단서가 아니다"
summary:
  - "결론: 활력징후를 먼저 보고, 코 아래 1/3 압박 → 보이는 출혈점은 혈관수축제·소작 → 안 보이면 패킹 순으로 올린다."
  - "시험 단서: 코피+앞으로 숙여 압박, 전비경에 비중격 앞쪽 출혈점(Kiesselbach), 양쪽 앞쪽 패킹에도 목뒤로 넘어가는 피."
  - "왜: 대부분이 비중격 앞쪽 키셀바흐 부위에서 나 압박·소작으로 멎고, 뒤쪽은 그 자리에 압박이 닿지 않는다."
  - "뒤쪽 출혈·패킹이 실패하면 뒤쪽 패킹+입원, 그래도 지속·재발하면 접형구개동맥 결찰 또는 색전술."
  - "항응고제 복용자도 생명을 위협하는 출혈이 아니면 1차 처치를 먼저 하고, 역전·중단은 그 뒤 판단한다."
pitfalls:
  - contrast: "항응고제 복용 중 코피 → 먼저 와파린 중단·역전?"
    point: "생명을 위협하는 출혈이 아니면 압박·패킹·소작 같은 1차 처치를 수혈·항응고 역전·중단보다 먼저 한다. 출혈이 조절되면 항응고는 이어 가는 것이 기본이다 [[aao-epistaxis-2020: KAS 11]] [[beck-epistaxis-2018: Anticoagulants]]."
  - contrast: "압박 → 곧바로 뒤쪽 패킹?"
    point: "뒤쪽 패킹은 앞쪽 처치(소작·앞쪽 패킹)가 실패했거나 뒤쪽 출혈이 확인될 때다. 풍선은 반드시 앞쪽 패킹과 함께 넣고, 뒤쪽 패킹 환자는 입원해 관찰한다 [[beck-epistaxis-2018: Posterior packing]]."
  - contrast: "양쪽 비중격을 한 번에 소작?"
    point: "양쪽 비중격을 동시에 소작하면 비중격 천공 위험이 있다. 국소마취 뒤 활동성·의심 출혈 부위에만 소작한다 [[beck-epistaxis-2018: Cauterization]] [[aao-epistaxis-2020: KAS 9]]."
  - contrast: "패킹이 실패한 뒤쪽 출혈 → 패킹을 반복?"
    point: "패킹·소작으로 조절되지 않는 지속·재발 출혈은 수술적 동맥 결찰이나 혈관 내 색전술 대상인지 평가한다. 한 후향 연구에서 뒤쪽 출혈의 수술 성공률은 97 %, 패킹은 62 %였다 [[aao-epistaxis-2020: KAS 10]] [[beck-epistaxis-2018: Abstract — Results]]."
  - contrast: "출혈장애·항응고제 환자에게 일반 패킹?"
    point: "출혈장애가 의심되거나 항응고제·항혈소판제를 쓰는 환자에게는 흡수성 패킹을 쓴다 — 제거할 때 다시 출혈하는 것을 피한다 [[aao-epistaxis-2020: KAS 3b]]."
tables:
  - id: steps
    section: "선택 — 단계별 처치와 다음 단계로 넘어가는 조건"
    title: "비출혈 처치 단계"
    role: treatment
    span: column
    columns: ["단계", "무엇을", "다음 단계로 넘어가는 조건"]
    rows:
      - ["0. 첫 평가", "기도·호흡·순환, 혈압 측정. 저혈량이면 정맥로·수액 [[beck-epistaxis-2018: Initial measures]]. 즉시 처치가 필요한 환자를 가린다 [[aao-epistaxis-2020: KAS 1]]", "—"]
      - ["1. 압박", "앉아서 앞으로 숙이고 코 아래 1/3 을 단단히 5분 이상 계속 누른다 [[aao-epistaxis-2020: KAS 2]]. 옥시메타졸린 분무를 더한다 [[beck-epistaxis-2018: Initial measures]]", "압박 뒤에도 출혈 · 출혈로 부위를 볼 수 없음"]
      - ["2. 부위 확인 · 소작", "응혈을 빼고 전비경 [[aao-epistaxis-2020: KAS 6]]. 보이는 출혈점은 혈관수축제 · 국소마취 뒤 그 자리만 소작(질산은 · 전기) [[aao-epistaxis-2020: KAS 8, KAS 9]]", "부위가 안 보이는 활동성 출혈 · 소작 실패"]
      - ["3. 앞쪽 패킹", "스펀지 · 팽창형 · 거즈 패킹. 출혈장애 · 항응고 환자는 흡수성 [[aao-epistaxis-2020: KAS 3a, KAS 3b]]. 비흡수성은 48시간 뒤 제거 [[beck-epistaxis-2018: Anterior packing]]", "앞쪽 패킹에도 출혈(뒤쪽 출혈 의심)"]
      - ["4. 뒤쪽 패킹 · 내시경", "비인두 풍선(+앞쪽 패킹 필수) 또는 Bellocq. 입원 관찰 · 항생제 예방 [[beck-epistaxis-2018: Posterior packing]]. 내시경으로 뒤쪽 출혈 부위를 찾는다 [[aao-epistaxis-2020: KAS 7a]]", "패킹 · 소작으로 조절 안 되는 지속 · 재발 출혈"]
      - ["5. 결찰 · 색전", "내시경 접형구개동맥 결찰 · 응고(약 98 % 조절) 또는 혈관 내 색전(87–93 %, 마취 위험이 높거나 수술 실패 때) [[beck-epistaxis-2018: Surgery, Embolization]] [[aao-epistaxis-2020: KAS 10]]", "—"]
    note: "단계 1 압박 시간: AAO-HNSF 지침은 5분 이상, Beck 2018 종설은 15–20분(시험 쟁점 Z1). 단계 4·5 의 세부(풍선 용량 · 성공률)는 Beck 2018 종설 — 지침 본문은 초록만 확인."
criteria:
  - id: prompt-mgmt
    name: 즉시 처치가 필요한 비출혈
    kind: 분류
    population: "의료진에게 연락·내원한 비출혈 환자(3세 이상)"
    statement: "처음 접촉할 때 즉시 처치가 필요한 환자와 아닌 환자를 가른다. 즉시 처치 대상의 활동성 출혈은 코 아래 1/3 을 5분 이상 단단히 계속 압박해 치료한다 [[aao-epistaxis-2020: KAS 1, KAS 2]]"
    exceptions: "「즉시 처치가 필요한」 세부 기준(출혈 시간 · 활력징후 수치)은 지침 본문에서 확인하지 못했다(초록만 읽음 — 검토 항목)"
    source: aao-epistaxis-2020
    basis: current
    exams: [kmle, usmle]
sources:
  - id: aao-epistaxis-2020
    org: "AAO-HNSF (Tunkel DE, Anne S, Payne SC, et al.)"
    title: "Clinical Practice Guideline: Nosebleed (Epistaxis)"
    kind: guideline
    year: 2020
    citation: "Otolaryngol Head Neck Surg 2020;162(1_suppl):S1-S38"
    doi: "10.1177/0194599819890327"
    pmid: "31910111"
    checked_at: 2026-11-20
    checked: "PubMed 초록(PMID 31910111)과 요약판 초록(PMID 31910122)에서 핵심 행동 지침(KAS) 1~14 문장을 읽음 — 즉시 처치 대상 가르기(1), 코 아래 1/3 5분 이상 압박(2), 부위가 안 보이면 패킹(3a), 출혈장애·항응고·항혈소판은 흡수성 패킹(3b), 위험 요인 기록(5), 응혈 제거 뒤 전비경(6), 재발·한쪽 반복 출혈은 내시경(7a), 혈관수축제·소작·보습제(8), 소작은 마취 뒤 출혈 부위에만(9), 패킹·소작 실패는 결찰·색전 평가(10), 생명 위협이 아니면 1차 처치를 수혈·항응고 역전·중단보다 먼저(11), HHT 평가(12). 전문은 SAGE·Wiley 접근이 막혀(403) 읽지 못했다 — KAS 의 근거 본문·세부 수치는 대조하지 않음"
    verified: abstract
  - id: beck-epistaxis-2018
    org: "Beck R, Sorge M, Schneider A, Dietz A"
    title: "Current Approaches to Epistaxis Treatment in Primary and Secondary Care"
    kind: review
    year: 2018
    citation: "Dtsch Arztebl Int 2018;115(1-02):12-22"
    doi: "10.3238/arztebl.2018.0012"
    pmid: "29345234"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5778404/"
    checked_at: 2026-11-20
    checked: "PMC5778404 전문(PMC 웹판)을 참고문헌 앞까지 읽음 — 키셀바흐 부위 90–95 %·뒤쪽 5–10 %, 내·외경동맥 양쪽 공급; 1차 처치(ABC·혈압·앞으로 숙임·양쪽 압박 15–20분·옥시메타졸린, 성공 65–75 %, 30분 관찰); 무증상 고혈압 >180/120 은 24–48시간에 걸쳐 경구로 천천히; 소작(질산은 vs 전기 78 % vs 88 %, 양쪽 비중격 동시 소작 금지 — 천공); 앞쪽 패킹 48시간 제거; 뒤쪽 풍선(앞쪽 패킹 필수, 24시간 안 부분 감압)·Bellocq; 패킹 합병증(후방 이탈·흡인·독성 쇼크 증후군); 항생제(앞쪽 48시간 초과·뒤쪽 전부); 패킹 환자 입원; 접형구개동맥 결찰·응고 약 98 %, 수술 실패 3 % vs 패킹 38 %; 색전 87–93 %·뇌허혈·안면신경 마비; 항응고·항혈소판 처리. 그림 2(단계 알고리즘)는 그림이라 글로 읽지 못했다"
    verified: text
diagram:
  title: "비출혈 — 압박에서 결찰·색전까지"
  nodes:
    - {id: start, kind: start, text: "코피 — 지금 출혈 중"}
    - {id: abc, kind: decision, text: "기도·순환 불안정?"}
    - {id: resus, kind: step, text: "ABC · 정맥로 · 수액 → 압박 병행"}
    - {id: press, kind: step, text: "앞으로 숙여 코 아래 1/3 압박 ≥5분 · 혈관수축제"}
    - {id: look, kind: decision, text: "전비경에 출혈점 보임?"}
    - {id: cautery, kind: end, text: "국소마취 → 그 자리만 소작"}
    - {id: apack, kind: step, text: "앞쪽 패킹(항응고 → 흡수성)"}
    - {id: still, kind: decision, text: "앞쪽 패킹에도 출혈?"}
    - {id: home, kind: end, text: "패킹 교육 · 48시간 뒤 제거"}
    - {id: scope, kind: info, text: "내시경으로 뒤쪽 출혈 부위 찾기"}
    - {id: ppack, kind: step, text: "뒤쪽 패킹 + 앞쪽 패킹 · 입원"}
    - {id: fail, kind: decision, text: "패킹·소작으로 조절됨?"}
    - {id: ok, kind: end, text: "입원 관찰 · 패킹 제거 계획"}
    - {id: ligate, kind: alert, text: "접형구개동맥 결찰 또는 색전술"}
  edges:
    - {from: start, to: abc}
    - {from: abc, to: resus, label: "예"}
    - {from: abc, to: press, label: "아니오"}
    - {from: resus, to: press}
    - {from: press, to: look}
    - {from: look, to: cautery, label: "보임"}
    - {from: look, to: apack, label: "출혈로 안 보임"}
    - {from: apack, to: still}
    - {from: still, to: home, label: "멎음"}
    - {from: still, to: scope, label: "지속"}
    - {from: scope, to: ppack}
    - {from: ppack, to: fail}
    - {from: fail, to: ok, label: "예"}
    - {from: fail, to: ligate, label: "아니오·재발"}
diagram_notes:
  - "소작 뒤 재발하거나 한쪽에서 반복되면 내시경으로 출혈 부위와 숨은 병변(종양 등)을 찾는다 [[aao-epistaxis-2020: KAS 7a, KAS 7b]]."
  - "뒤쪽 풍선은 반드시 앞쪽 패킹과 함께, 24시간 안에 적어도 일부 감압한다 — 압박 괴사 · 후방 이탈 · 흡인 위험 [[beck-epistaxis-2018: Posterior packing, Packing complications]]."
  - "색전술은 전신마취 위험이 높거나 수술이 실패한 환자 — 합병증으로 뇌허혈 · 안면신경 마비가 있다 [[beck-epistaxis-2018: Embolization]]."
  - "양쪽 반복 코피나 가족력이 있으면 코 · 구강 점막의 모세혈관확장을 보아 유전성 출혈성 모세혈관확장증(HHT)을 평가한다 [[aao-epistaxis-2020: KAS 12]]."
checks:
  - q: "항응고제를 먹는 70세 남자가 활력징후는 안정적이고 앞쪽 코피가 난다. 첫 처치는?"
    a: "앞으로 숙여 코 아래 1/3 을 5분 이상 압박하고, 보이는 출혈점은 소작, 안 되면 흡수성 패킹. 생명 위협이 아니면 항응고 역전·중단보다 1차 처치가 먼저다."
  - q: "양쪽 앞쪽 패킹 뒤에도 피가 목뒤로 넘어간다. 다음 단계는?"
    a: "뒤쪽 출혈을 생각해 내시경으로 부위를 찾고 뒤쪽 패킹(앞쪽 패킹과 함께)을 넣은 뒤 입원 관찰한다. 그래도 조절되지 않으면 접형구개동맥 결찰이나 색전술."
  - q: "왜 양쪽 비중격을 한 번에 소작하지 않나?"
    a: "비중격 천공 위험이 있다 — 국소마취 뒤 활동성 · 의심 출혈 부위에만 소작한다."
---

## 판단 — 왜 압박이 먼저이고 한 단계씩 올리나
- 처음 접촉에서 **즉시 처치가 필요한 환자인지**부터 가른다 — 기도·호흡·순환을 보고, 저혈량이면 정맥로·수액을 시작하며 혈압을 잰다 [[aao-epistaxis-2020: KAS 1]] [[beck-epistaxis-2018: Initial measures]].
- 출혈의 90–95 %가 앞쪽 키셀바흐 부위(Kiesselbach's area, Little's area)라 **압박이 닿는 곳**이다 — 앞으로 숙여 코 아래 1/3 을 5분 이상 계속 누른다 [[beck-epistaxis-2018: Anatomy]] [[aao-epistaxis-2020: KAS 2]]. 압박·혈관수축제만으로 65–75 %가 멎는다 [[beck-epistaxis-2018: Initial measures]].
- 다음 단계로 넘어가는 기준은 **출혈 부위가 보이느냐**다 — 보이면 그 자리만 소작, 출혈 때문에 안 보이면 패킹 [[aao-epistaxis-2020: KAS 3a, KAS 8]].
- 침습적인 단계(뒤쪽 패킹 · 결찰 · 색전)는 앞 단계가 실패했을 때 올린다 — 뒤쪽 패킹은 후방 이탈 · 흡인 같은 위험이 있어 입원이 필요하다 [[beck-epistaxis-2018: Packing complications, Inpatient admission]].

## 기전 — 앞쪽과 뒤쪽은 왜 다르게 멎나
- 키셀바흐 부위는 비중격 앞쪽에서 **내경동맥과 외경동맥 가지가 함께 모이는** 곳이다. 콧방울을 누르면 이 부위가 직접 눌려 멎는다 [[beck-epistaxis-2018: Anatomy]].
- 뒤쪽 출혈(5–10 %)은 비강 뒤쪽에서 나며, 콧방울 압박이 닿지 않고 피가 인두로 넘어간다. 수술로 막는 주 혈관은 접형구개동맥(sphenopalatine artery)이다 — 사골동맥과의 문합이 있어 결찰 뒤에도 그 영역의 허혈은 크지 않다 [[beck-epistaxis-2018: Anatomy, Surgery]].
- 그래서 앞쪽은 압박 · 소작 · 앞쪽 패킹으로 대부분 끝나고, 뒤쪽은 **비인두를 막는 패킹**(풍선 · Bellocq)이나 **혈관 자체를 막는 처치**(결찰 · 색전)가 필요하다 [[beck-epistaxis-2018: Posterior packing, Surgery, Embolization]].

## 선택 — 단계별 처치와 다음 단계로 넘어가는 조건
- 표가 단계 0~5 의 처치와 넘어가는 조건을 한 줄씩 놓는다.
- 소작: 응혈을 빼고 혈관수축제 · 국소마취를 묻힌 솜으로 시야를 얻은 뒤, 질산은(chemical) 또는 전기 소작을 한다. 한 후향 연구에서 성공률은 78 % 대 88 % [[beck-epistaxis-2018: Cauterization]].
- 앞쪽 패킹: 출혈장애 · 항응고 · 항혈소판 환자는 흡수성 [[aao-epistaxis-2020: KAS 3b]]. 패킹 환자에게 종류 · 제거 시기 · 다시 와야 할 증상을 설명한다 [[aao-epistaxis-2020: KAS 4]].
- 항생제 예방: 앞쪽 패킹은 48시간을 넘길 때만, 뒤쪽 패킹은 모두 — 근거는 제한적이다 [[beck-epistaxis-2018: Antibiotics]].
- 결찰 vs 색전: 내시경 접형구개동맥 결찰 · 응고가 약 98 % 조절해 뒤쪽 출혈의 우선 방법이고, 색전은 전신마취 위험이 높거나 수술이 실패했을 때다. 미국 비교 자료에서 수혈 · 뇌졸중 · 사망은 차이가 없었고 수술이 비용 · 재원 기간이 적었다 [[beck-epistaxis-2018: Surgery, Embolization]].

## 권고와 예외
- **항응고 · 항혈소판제**: 생명을 위협하지 않으면 1차 처치를 수혈 · 역전 · 중단보다 먼저 한다 [[aao-epistaxis-2020: KAS 11]]. 출혈이 조절되면 항응고를 이어 가고 INR 을 확인한다. 항혈소판제를 끊어도 지혈 회복에 최대 10일이 걸려 급성기에는 도움이 되지 않는다 [[beck-epistaxis-2018: Anticoagulants]].
- **고혈압**: 출혈 중 혈압이 높아도 직접 원인이라는 근거는 없다. 무증상으로 >180/120 mmHg 가 반복되면 경구약으로 24–48시간에 걸쳐 천천히 낮춘다 [[beck-epistaxis-2018: Initial measures, Hypertension]].
- **반복 · 한쪽 출혈**: 패킹 · 소작 뒤에도 반복되거나 한쪽에서 되풀이되면 내시경 — 종양 등 숨은 병변을 놓치지 않는다 [[aao-epistaxis-2020: KAS 7a, KAS 7b]].
- 패킹 합병증: 후방 이탈(치명적 흡인 보고) · 점막 괴사 · 이관 기능장애 · 독성 쇼크 증후군(패킹 제거 · 정맥 항생제 · 중환자실) [[beck-epistaxis-2018: Packing complications]].
- 급성 세균성 부비동염의 항생제 기준은 이 정리본의 목표 밖이다(같은 슬롯의 다른 목표).
- 국내 교과서 · KMLE 해설의 단계 문구는 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 압박 시간** — 시험 기준: 코 아래 1/3 을 5분 이상 단단히 계속 압박 [[aao-epistaxis-2020: KAS 2]] / 다른 기준: 양쪽을 15–20분 계속 압박 [[beck-epistaxis-2018: Initial measures]] / 왜 다른가: 미국 다학제 지침은 「최소」 시간을 권고 문장으로 정했고, 독일 종설은 1차 진료의 실제 처치 시간을 경험 · 문헌으로 적었다 — 둘 다 「충분히 오래, 중간에 떼지 않고」가 핵심이다 / 시험에서는: KMLE 는 국내 교과서와 대조하지 않았다(검토 항목) · USMLE 는 「앞으로 숙이고 콧방울을 계속 압박」을 첫 처치로 고른다. 분 수 자체로 답이 갈리는 보기는 이 판단(내 추론)으로 풀지 않는다.
- **Z2 맥락 · 비흡수성 패킹 제거 시기와 항생제** — 시험 기준: 앞쪽 패킹 48시간 뒤 제거, 항생제는 48시간 초과 앞쪽 · 모든 뒤쪽 패킹 [[beck-epistaxis-2018: Anterior packing, Antibiotics]] / 다른 기준: AAO-HNSF 지침 초록은 패킹 환자 교육(제거 시기 · 계획)만 권고 문장으로 두고 항생제 예방은 KAS 로 다루지 않는다 [[aao-epistaxis-2020: KAS 4]] / 왜 다른가: 항생제 예방의 근거가 제한적이라는 점은 종설도 인정한다 — 지침 본문의 해당 서술은 대조하지 못했다 / 시험에서는: 일상적 항생제 여부를 묻는 문항은 근거 수준을 함께 확인해야 한다(검토 항목).
