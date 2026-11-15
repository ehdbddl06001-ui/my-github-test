---
id: cn.cardio.sustained-vt.wide-complex-tachycardia-management
type: concept
topic: Cardiology
see_also: [cn.cardio.pvc-nsvt.structural-heart-risk-first, cn.cardio.svt.av-nodal-blockade-response]
date: 2026-11-15
updated: 2026-11-15
version: 2
outline: h254            # 기본틀 슬롯 — 해리슨 22판 261장 Sustained Ventricular Tachycardia
confidence: high
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 [gap] 으로 쓴 정리본(오답 연결 없음)
title: "지속성 심실빈맥 — 넓은 QRS 빈맥은 VT 로 보고 처치"
objective: "규칙적인 넓은 QRS 빈맥 환자에서 혈역학 상태와 바탕 심장으로 동기화 심율동전환·아데노신·아미오다론·ICD 중 다음 처치를 고른다"
objective_kind: 다음 처치
condition: 지속성 단형 심실빈맥(sustained monomorphic ventricular tachycardia, VT)·넓은 QRS 빈맥(wide-complex tachycardia)
exams: [kmle, usmle]
summary:
  - "결론: 저혈압·의식 저하·폐부종이 있으면 즉시 QRS 동기화 심율동전환, 안정하면 심질환 환자에서 정맥 아미오다론 [[harrison-22: 261장 p.1964]]"
  - "시험 단서: 심근경색 병력·박출률 저하 + 넓은 QRS 빈맥, 방실 해리·융합 박동(fusion beat), V1–V6 일치(concordance), aVR 의 R."
  - "왜: 알려진 심질환에서 넓은 QRS 빈맥은 모양과 관계없이 VT 가 가장 흔하다 — 혈압이 버틴다고 상심실성은 아니다 [[harrison-22: 261장 p.1964]]"
  - "아데노신은 안정·규칙적일 때만 시도(심장이식·불규칙·불안정이면 금지). 회복 뒤 입원해 바탕 심질환을 찾는다."
  - "구조 심질환의 지속성 VT 는 ICD 로 2차 예방(1년 이상 생존 기대) — 항부정맥제만으로는 생존이 늘지 않는다 [[harrison-22: 261장 p.1965]]"
criteria:
  - id: sustained-vt-def
    name: 지속성 단형 심실빈맥
    kind: 진단
    population: "넓은 QRS 의 규칙적 빈맥"
    statement: "넓은 QRS 의 심실 부정맥이 30초 이상 지속되거나, 끝내는 데 항빈맥 조율·심율동전환 같은 개입이 필요하면 지속성. 모든 QRS 가 같은 모양이면 한 초점이나 고정된 회귀 회로에서 반복해 나온다는 뜻이다 [[harrison-22: 261장 p.1963]]"
    exceptions: "30초 미만이고 저절로 끝나면 비지속성(NSVT) — 처치 원칙이 다르다(짝 정리본 cn.cardio.pvc-nsvt.structural-heart-risk-first)."
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
  - id: vt-secondary-icd
    name: 지속성 VT 뒤 ICD(2차 예방)
    kind: 치료
    population: "구조 심질환과 함께 지속성 VT 로 내원한 환자"
    statement: "구조 심질환에 동반한 지속성 VT 는 급사 2차 예방으로 ICD 가 필요하다. 관동맥질환에서는 1년 이상 괜찮은 기능 상태로 생존이 기대될 때 분명한 적응이다. 항부정맥제에 비해 ICD 는 연간 사망률을 12.3 % 에서 8.8 % 로, 부정맥 사망을 50 % 줄였다 [[harrison-22: 261장 p.1964–1965]]"
    exceptions: "구조 정상 심장의 특발성 VT 는 급사가 드물어 ICD 를 권하지 않는다 [[harrison-22: 261장 p.1967]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 261: Sustained Ventricular Tachycardia"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 261장 p.1963–1968"
    checked_at: 2026-11-15
    checked: "드라이브 22판 장별 문서 H22_261 본문 대조 — 지속성 단형 VT 정의(30초 이상 또는 개입 필요)·같은 모양 = 초점 또는 고정 회귀 회로, 구조 심질환의 기질은 경색·섬유화·염증·수술 흉터, 흉터 회귀 VT 는 급사 위험 / 특발성 VT 는 양성, 임상상은 속도·심기능·자율신경에 따름(심기능 정상이면 두근거림만), 빠르거나 구조 심질환이면 VF 로 악화(p.1963) · 감별 대상(변행 SVT·부전도로·조율), 알려진 심질환이면 QRS 모양과 무관하게 VT 가 가장 흔함, 흉터 시사(병적 Q파·분절 벽운동 이상·지연 가돌리늄 증강), 혈역학 안정성은 감별에 도움 안 됨, 방실 해리는 심방 속도가 느릴 때 믿을 만한 VT 표지, QRS 마다 P파가 따라와도 VT 배제 못함(1:1 역전도), aVR 단상 R·Rs, V1–V6 일치는 비교적 특이, 각차단 환자에서 동율동과 같은 모양이면 SVT 쪽이나 절대적이지 않음(각차단 회귀), 전기생리검사·잡음 인공물, 표 261-1(특발성 유출로·속가지·유두근, 허혈·비허혈 심근병증, ARVC, 팔로 교정, 비대 심근병증, 유전 증후군), 처치: ACLS, 저혈압·의식 저하·폐부종이면 QRS 동기화 심율동전환(의식 있으면 진정 뒤), 안정하면 아데노신 시도 합리적(심장이식·불규칙·불안정이면 금지), 심질환 있으면 정맥 아미오다론이 선택 약, 회복 뒤 입원·바탕 심질환 평가, 트로포닌·CK-MB 상승은 대개 VT 중 저혈압에 의한 2차 손상이고 급성 경색은 지속성 단형 VT 의 드문 원인, 잦거나 끊이지 않으면 항부정맥제·도자절제, 대개 단발이나 재발 위험 높음, 구조 심질환 지속성 VT 에 ICD 2차 예방(p.1964) · 관동맥질환: 오래전 큰 경색·재형성·박출률 저하, 2년 내 재발 최대 70 %, 흉터 회귀는 허혈 의존이 아니라 재관류술로 재발 예방 어려움, ICD(1년 생존 기대), 연간 사망 12.3→8.8 %·부정맥 사망 50 % 감소, 항부정맥제는 ICD 없이는 생존 개선 없음, ICD 뒤 5년 사망 > 30 %·베타차단제·ACE 억제제, ICD 충격·항빈맥 조율은 심부전·사망 증가와 연관 → 재발 VT 는 약물 또는 도자절제, VANISH(절제가 아미오다론 증량보다 나음), BERLIN VT, 비허혈 심근병증: 흉터 회귀·MRI 벽내/심외막 증강·판륜 근처, 사르코이드증·샤가스병·Lamin A/C, ICD 적응(지속성 VT·실신·NYHA II–III), 절제 성공률 낮음(p.1965) · ARVC: 데스모솜 유전자, 약 50 % 상염색체 우성, 낙소스병·카르바할 증후군, 20~50대 두근거림·실신·심정지, 좌각차단꼴 VT, 동율동 심전도 > 85 % 에서 이상(V1–V3 T파 역위·QRS > 110 ms·엡실론파), ICD 권고, 운동 유발이면 베타차단제·운동 제한, 소탈롤·플레카이니드·아미오다론, 절제 70 %(p.1966) · 팔로 교정 뒤 VT 3–14 %·급사 위험 인자(교정 나이 > 5세·QRS > 180 ms 등), 각차단 회귀 VT(약 5 %, 좌각차단꼴, 우각 절제로 소실), 특발성 VT: 두근거림·어지럼·드물게 실신, 교감 자극 또는 운동 직후, 동율동 심전도 정상·가족력 없음·영상 정상, 반복 단형 VT 는 빈맥 유발 심근병증, 급사 드묾·ICD 권하지 않음, 유출로 VT(우심실 유출로 = 좌각차단꼴·하방 축, V1/V2 R 우세면 좌심실), ARVC 배제가 먼저, 좌심실 속가지 VT(베라파밀 민감·우각차단꼴·하방 유도 음성·운동 유발·남자에 많음·양성 경과)(p.1967) · 특발성 VT 치료: 증상 또는 심기능 저하 시, 베타차단제·칼슘통로차단제·플레카이니드(구조 정상·MRI 섬유화 없음), 도자절제 성공 약 80 %·우심실 유출로에서 가장 좋음, 속가지 VT 는 정맥 베라파밀로 종료(p.1968)"
    verified: text
tables:
  - id: vt-vs-svt-table
    title: "넓은 QRS 빈맥 — VT 쪽 소견과 한계"
    role: differential
    span: column
    section: "가르는 소견 — VT 쪽으로 기우는 것"
    columns: ["소견", "의미와 한계"]
    rows:
      - ["알려진 심질환·경색 병력·박출률 저하", "QRS 모양과 관계없이 VT 가 가장 흔하다 [[harrison-22: 261장 p.1964]]"]
      - ["방실(심실-심방) 해리·융합 박동", "심방 속도가 심실보다 느리면 믿을 만한 VT 표지 — 심방세동 중에는 평가 불가 [[harrison-22: 261장 p.1964–1965]]"]
      - ["aVR 단상 R·Rs, V1–V6 일치", "비교적 특이 — 중증 심질환에서는 모양 기준 모두 덜 믿을 만하다 [[harrison-22: 261장 p.1964]]"]
      - ["QRS 마다 P파", "1:1 역전도가 있을 수 있어 VT 를 배제하지 못한다 [[harrison-22: 261장 p.1964]]"]
      - ["동율동 때와 같은 각차단 모양", "SVT 쪽이나 절대적이지 않다 — 각차단 회귀 VT 는 평소 QRS 와 닮는다 [[harrison-22: 261장 p.1964, p.1967]]"]
      - ["혈역학이 안정하다", "감별에 도움이 안 된다 [[harrison-22: 261장 p.1964]]"]
    note: "어느 기준도 VT 를 배제하지 못한다 — 확실하지 않으면 VT 로 처치하고, 확진은 전기생리검사로."
  - id: vt-substrate-table
    title: "바탕 심장에 따른 지속성 VT 의 다음 처치"
    role: treatment
    span: column
    section: "선택 — 회복 뒤 무엇을 하나"
    columns: ["바탕", "처치"]
    rows:
      - ["오래된 경색 흉터(허혈 심근병증)", "ICD 2차 예방 + 심부전 표준 약물. 재발하면 도자절제가 아미오다론 증량보다 낫다 [[harrison-22: 261장 p.1965]]"]
      - ["비허혈 심근병증(사르코이드증·샤가스병·Lamin A/C)", "지속성 VT·실신·NYHA II–III 면 ICD, 재발에 약물·절제(성공률은 더 낮음) [[harrison-22: 261장 p.1965]]"]
      - ["부정맥 유발 우심실 심근병증", "ICD 권고. 운동 유발이면 베타차단제·운동 제한, 소탈롤·플레카이니드·아미오다론, 절제(대개 심외막) [[harrison-22: 261장 p.1966]]"]
      - ["구조 정상 — 특발성 VT", "ICD 권하지 않음. 증상·심기능 저하 때 베타차단제·칼슘통로차단제·플레카이니드 또는 도자절제(약 80 %) [[harrison-22: 261장 p.1967–1968]]"]
pitfalls:
  - contrast: "혈압이 유지되는 넓은 QRS 빈맥 = 변행 전도 SVT?"
    point: "혈역학 안정성은 VT 와 SVT 를 가르지 못한다. 심근경색 병력이나 박출률 저하가 있으면 모양과 관계없이 VT 가 가장 흔하므로 VT 로 처치한다 — 베라파밀 같은 방실결절 차단제를 넣지 않는다 [[harrison-22: 261장 p.1964]]"
    exception: "구조 정상 심장의 좌심실 속가지 VT(우각차단꼴·하방 유도 음성)는 정맥 베라파밀로 끝난다 [[harrison-22: 261장 p.1967–1968]]"
  - contrast: "트로포닌 상승 = 급성 경색이 VT 를 일으켰다 → 재관류술로 해결?"
    point: "급성 경색은 지속성 단형 VT 의 드문 원인이다. 효소 상승은 대개 VT 중 저혈압에 의한 2차 손상이고, 원인은 오래된 흉터다. 흉터 회귀는 허혈에 의존하지 않아 재관류술로 재발을 막지 못한다 — 2차 예방은 ICD [[harrison-22: 261장 p.1964–1965]]"
    exception: "다형성 VT·심실세동은 허혈 평가를 해야 한다 [[harrison-22: 261장 p.1964]]"
  - contrast: "아미오다론으로 리듬이 돌아왔다 = 항부정맥제를 계속하면 된다?"
    point: "ICD 없이 항부정맥제만으로는 생존이 늘지 않는다. 구조 심질환의 지속성 VT 뒤에는 ICD 가 연간 사망률·부정맥 사망을 줄인다. 약물은 증상 완화와 ICD 작동(충격·항빈맥 조율) 줄이기용이다 [[harrison-22: 261장 p.1965]]"
  - contrast: "젊은 사람의 좌각차단꼴·하방 축 VT = 특발성, 바로 안심?"
    point: "유출로 모양은 특발성 쪽이지만 부정맥 유발 우심실 심근병증도 같은 자리에서 VT 를 낸다. 동율동 심전도(V1–V3 T파 역위·엡실론파)·영상·가족력으로 이 질환을 먼저 배제한다 [[harrison-22: 261장 p.1966–1967]]"
diagram:
  title: "규칙적인 넓은 QRS 빈맥 — 다음 처치"
  nodes:
    - {id: start, kind: start, text: "규칙적인 넓은 QRS 빈맥"}
    - {id: unstable, kind: decision, text: "저혈압·의식 저하·폐부종?"}
    - {id: dccv, kind: step, text: "QRS 동기화 심율동전환(진정 뒤)"}
    - {id: heart, kind: decision, text: "알려진 심질환·경색 병력?"}
    - {id: amio, kind: step, text: "VT 로 보고 정맥 아미오다론"}
    - {id: adeno, kind: end, text: "아데노신 시도 — 변행 SVT 확인"}
    - {id: work, kind: info, text: "입원·심초음파·MRI·12유도 동율동"}
    - {id: struct, kind: decision, text: "구조 심질환이 있나?"}
    - {id: icd, kind: alert, text: "ICD 2차 예방(재발 시 절제)"}
    - {id: idio, kind: end, text: "특발성 — 약물·절제, ICD 없음"}
  edges:
    - {from: start, to: unstable}
    - {from: unstable, to: dccv, label: "예"}
    - {from: unstable, to: heart, label: "아니오"}
    - {from: heart, to: amio, label: "있음"}
    - {from: heart, to: adeno, label: "없음"}
    - {from: dccv, to: work}
    - {from: amio, to: work}
    - {from: work, to: struct}
    - {from: struct, to: icd, label: "있음"}
    - {from: struct, to: idio, label: "없음"}
diagram_notes:
  - "아데노신은 심장이식 환자, 불규칙하거나 불안정한 넓은 QRS 리듬에는 쓰지 않는다."
  - "트로포닌·CK-MB 상승은 대개 VT 중 저혈압에 의한 2차 손상 — 급성 경색은 지속성 단형 VT 의 드문 원인이다."
  - "ICD 는 1년 이상 괜찮은 기능 상태로 생존이 기대될 때. 잦거나 끊이지 않는 VT 는 항부정맥제·도자절제로 먼저 안정시킨다."
  - "아데노신 뒤에도 끝나지 않거나 VT 로 판명되면 VT 처치로 간다. 확진이 안 되면 전기생리검사."
checks:
  - q: "8년 전 큰 전벽 경색, 박출률 30 %. 분당 170회 규칙적 넓은 QRS 빈맥, 혈압 70/40·의식 혼미. 다음 처치는?"
    a: "QRS 동기화 심율동전환(가능하면 진정 뒤) — 불안정하면 감별 전에 전기 치료."
  - q: "같은 환자가 혈압 118/70 으로 안정할 때 첫 약은? 변행 SVT 로 보고 베라파밀을 주면 안 되는 이유는?"
    a: "정맥 아미오다론. 경색 병력이 있으면 모양과 관계없이 VT 가 가장 흔하고, 혈압이 버틴다고 SVT 가 아니다."
  - q: "VT 를 멈춘 뒤 트로포닌이 조금 올랐다. 관동맥 재관류술이 재발을 막는가?"
    a: "아니다 — 효소 상승은 대개 2차 손상이고 원인은 오래된 흉터 회귀다. 2차 예방은 ICD."
  - q: "심초음파·MRI·동율동 심전도가 정상인 25세, 운동 중 좌각차단꼴·하방 축 VT. ICD 를 넣나?"
    a: "아니다 — 특발성(유출로) VT 는 급사가 드물다. 증상 조절에 베타차단제·칼슘통로차단제 또는 도자절제. 먼저 ARVC 를 배제한다."
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc13581952_figure1-0-115-1600-1085.png
  kind: ecg
  at: 가르는 소견 — VT 쪽으로 기우는 것
  shows: 넓은 QRS 의 규칙적 단형 빈맥(심실빈맥)
  look_for:
  - 모든 유도에서 QRS 가 넓고 모양이 한결같다
  - RR 간격이 규칙적이고 빠르다(약 188회/분)
  label: '「The patient''s ECG showing ventricular tachycardia.」 — Case Report: Left ventricular pseudoaneurysm presenting with ventricular tachycardia'
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: 'Case Report: Left ventricular pseudoaneurysm presenting with ventricular tachycardia. Frontiers in Cardiovascular Medicine'
  doi: 10.3389/fcvm.2026.1903760
  credit: 'Case Report: Left ventricular pseudoaneurysm presenting with ventricular tachycardia. Front Cardiovasc Med. 2026 Sep 3;13:1903760. doi: 10.3389/fcvm.2026.1903760 (CC BY) — Figure 1'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC13581952/
  asset: PMC-PMC13581952_Figure1
  privacy_check: 얼굴·문신 없음. 이름 칸은 비어 있고 병원명 없음. 날짜·기기 문자가 있는 머리줄과 아래 줄은 잘라냈다
  crop: 0,115,1600,1085
---

## 판단 — 왜 「VT 로 보고」가 먼저인가
- **불안정하면 감별보다 전기 치료가 먼저다.** 저혈압·의식 저하·폐부종이 있으면 QRS 동기화 심율동전환(의식이 있으면 진정 뒤)을 한다 [[harrison-22: 261장 p.1964]].
- **안정해도 VT 를 배제할 수 없다.** 혈역학 안정성은 VT 와 다른 넓은 QRS 빈맥을 가르지 못하고, 심기능이 정상이면 빠른 VT 도 두근거림만으로 버틴다 [[harrison-22: 261장 p.1963–1964]].
- **알려진 심질환이면 모양과 관계없이 VT 가 가장 흔하다** — 그래서 심질환 환자의 안정 VT 에는 정맥 아미오다론이 선택 약이다 [[harrison-22: 261장 p.1964]].
- **변행 SVT 가 의심되는 안정·규칙적 빈맥**에서는 아데노신 시도가 합리적이다(진단에 도움). 심장이식, 불규칙하거나 불안정한 리듬에는 쓰지 않는다 [[harrison-22: 261장 p.1964]].
- **리듬이 돌아온 뒤가 진짜 판단이다** — 입원해 바탕 심질환을 정하고, 구조 심질환이면 ICD 로 2차 예방한다 [[harrison-22: 261장 p.1964]].

## 기전 — 흉터가 회로를 만든다
구조 심질환에서 VT 의 기질은 대개 경색·섬유화·염증·심장 수술로 생긴 조각난 치환 섬유화다. 흉터 안에 살아 있는 심근 다발이 느리게 전도하는 통로가 되어 해부적·기능적 회귀 회로를 만들고, 같은 출구에서 반복해 나가므로 QRS 가 모두 같은 단형 VT 가 된다 [[harrison-22: 261장 p.1963]]. 드물게 병든 퍼킨제계의 회귀나 자동능(각차단 회귀 VT 등)도 원인이다 [[harrison-22: 261장 p.1963, p.1967]].

이 회로는 **허혈에 의존하지 않는** 고정된 기질이다. 그래서 관동맥질환의 지속성 VT 는 대개 수년 전 큰 경색과 재형성된 심실, 크게 떨어진 박출률에서 생기고, 2년 안에 최대 70 % 가 재발하며, 재관류술로 재발을 막기 어렵다 [[harrison-22: 261장 p.1965]]. 빠르거나 구조 심질환에 동반한 단형 VT 는 심실세동으로 악화할 수 있어 급사 위험과 이어진다 [[harrison-22: 261장 p.1963]]. 반대로 구조가 정상인 특발성 VT 는 한 초점의 유발 자동능(유출로)이나 작은 퍼킨제 회귀(속가지)에서 나와 경과가 양성이다 [[harrison-22: 261장 p.1967]].

## 가르는 소견 — VT 쪽으로 기우는 것
- 감별 대상은 각차단·변행 전도를 동반한 상심실성 빈맥(SVT), 부전도로를 타는 SVT, 조율기·제세동기의 빠른 조율이다 [[harrison-22: 261장 p.1963–1964]].
- 흉터의 단서 — 병적 Q파, 심초음파·핵의학의 분절 벽운동 이상, MRI 지연 가돌리늄 증강 [[harrison-22: 261장 p.1964]].
- 음성 결과의 한계: 표의 어느 기준도 VT 를 배제하지 못하고, 중증 심질환에서는 모양 기준이 모두 덜 믿을 만하다. 확진이 필요하면 전기생리검사를 하고, 감시 장치의 잡음·움직임 인공물이 VT 를 흉내 낼 수 있음도 기억한다 [[harrison-22: 261장 p.1964]].

## 선택 — 회복 뒤 무엇을 하나
- 지속성 단형 VT 는 대개 한 번 오지만 재발 위험이 높다. 잦거나 끊이지 않으면 항부정맥제나 도자절제로 먼저 안정시킨다 [[harrison-22: 261장 p.1964]].
- 허혈 심근병증: ICD 를 넣은 뒤에도 5년 사망이 30 % 를 넘어 베타차단제·ACE 억제제 등 심부전 표준 약물이 중요하다. ICD 충격·항빈맥 조율 자체가 심부전·사망 증가와 연관되므로 재발 VT 는 약물이나 도자절제로 줄인다 — VANISH 에서 절제가 항부정맥제(특히 아미오다론) 증량보다 나았다 [[harrison-22: 261장 p.1965]].
- 비허혈 심근병증의 흉터는 벽내·심외막·판륜 근처에 많아 심내막 절제 성공률이 낮고, MRI·CT 로 섬유화를 그려 절제를 이끈다 [[harrison-22: 261장 p.1965]].

## 권고와 예외
- 특발성 VT 는 증상이 있거나 잦은 빈맥이 심기능을 떨어뜨릴 때만 치료한다. 플레카이니드는 구조 심질환에서 보통 권하지 않지만 동율동 심전도가 정상이고 MRI 섬유화가 없으면 쓸 수 있다 [[harrison-22: 261장 p.1967–1968]].
- 반복 단형 VT 는 빈맥 유발 심근병증을 일으킬 수 있고, 빈맥을 억제하면 심기능이 회복된다 [[harrison-22: 261장 p.1967]].
- 팔로 사징 교정 뒤 VT 는 수술 흉터 둘레 회귀가 흔하다. 자발 VT 가 있으면 대개 ICD, 위험 인자가 여럿이면 ICD 를 고려한다 [[harrison-22: 261장 p.1967]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 261장 p.1963~1968)
