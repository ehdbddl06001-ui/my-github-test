---
id: cn.physio.ventricular-repolarization.long-qt
type: concept
topic: Physiology
see_also: [Cardiology, Pharmacology]
date: 2026-11-24
updated: 2026-11-24
version: 1
outline: physio.cardiac   # 생리학 책 「심장 — 전기 활동과 펌프 기능」
layer: basic            # 기초 정리본 — 임상 정리본의 roots 가 가리키는 기전 단위
discipline: physiology
system: cardiovascular
objective_kind: 기전
textbook_check: pending
confidence: medium
review_status: unreviewed
note_form: 2
title: "심실 재분극 — 칼륨 전류가 줄면 QT 가 길어진다"
objective: "심실 활동전위의 3기 재분극을 IKr·IKs 가 끝낸다는 것으로 QT 간격을 설명하고, 칼륨 전류 감소(유전·약물·저칼륨)나 나트륨 전류 지연이 QT 를 늘려 조기후탈분극 → 토르사드를 일으키는 경로와 유전형별 방아쇠의 차이를 설명한다"
condition: QT 연장과 토르사드 드 푸앵트의 이온 기전(선천·후천 QT연장증후군)
exams: [usmle, kmle]
summary:
  - "결론: QT 는 심실 활동전위 길이이고, 3기 재분극을 끝내는 IKr·IKs 가 줄면 QT 가 길어진다."
  - "시험 단서: 운동·수영 중 실신 + 긴 QTc = LQT1(IKs, KCNQ1), 소리·감정 = LQT2(IKr, KCNH2), 수면 중 = LQT3(INa, SCN5A)."
  - "왜: 길어진 2~3기에 조기후탈분극(early afterdepolarization)이 생기고, 재분극이 고르지 않은 심실에서 토르사드가 된다."
  - "QT 를 늘리는 약 대부분은 IKr 을 막는다 — Ⅲ군·IA군 항부정맥제, 마크롤라이드, 항정신병약, 메타돈."
pitfalls:
  - contrast: "QT 연장 = 탈분극이 느린 것?"
    point: "QT 는 QRS 시작부터 T 파 끝까지이고, 길어지는 몫은 대개 2기(ST 분절)·3기(T 파) — 재분극이다. 3기는 칼슘 전류가 꺼지고 IKr·IKs 가 계속 열려 끝나므로 이 칼륨 통로가 늦게 닫히거나 약해지면 QT 가 는다 [[harrison-22: 250장 p.1910–1911]]. QRS 가 넓어지는 것(탈분극·전도 지연)과 다르다."
  - contrast: "토르사드의 방아쇠 — 빠른 심박 vs 느린 심박"
    point: "후천 QT 연장의 토르사드는 기외수축 뒤 긴 휴지(긴–짧은 간격)에서 시작하는 휴지 의존형이고 서맥·저칼륨·저마그네슘이 거든다 — 그래서 급성기엔 마그네슘과 심박 올리기(이소프로테레놀·조율 100~120회/분)가 듣는다 [[harrison-22: 262장 p.1969]]. 반면 LQT1 은 운동(특히 수영) 중에 사건이 나 비선택 베타차단제가 예방약이다 [[harrison-22: 262장 p.1970]]."
tables:
  - id: lqt-genotypes
    title: "유전형 — 무엇이 줄고 언제 터지나"
    role: comparison
    span: column
    section: "고장 — 재분극 예비력이 깎이면"
    columns: ["유형", "유전자 · 전류", "사건이 나는 때"]
    rows:
      - ["LQT1", "KCNQ1 · IKs 감소", "운동, 특히 수영"]
      - ["LQT2", "KCNH2 · IKr 감소", "갑작스러운 소리 · 감정"]
      - ["LQT3", "SCN5A · INa 비활성화 지연", "수면 중"]
    note: "세 유형이 선천 QT연장증후군의 80~90 % [[harrison-22: 262장 p.1970]]"
checks:
  - q: "IKr 차단제가 QT 를 늘리는 이유는?"
    a: "3기 재분극을 끝내는 칼륨 유출이 줄어 활동전위가 길어지고, 그 길이가 표면 심전도의 QT 이기 때문이다."
  - q: "조기후탈분극과 지연후탈분극은 활동전위의 어느 시기에 생기나?"
    a: "조기후탈분극은 2~3기(QT 연장 → 토르사드), 지연후탈분극은 4기(세포 안 칼슘 과부하 — 디기탈리스 독성 · 양방향 심실빈맥)."
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 22e. 250장 Principles of Clinical Cardiac Electrophysiology p.1910–1913; 262장 Polymorphic Ventricular Tachycardia and Ventricular Fibrillation p.1969–1970"
    checked_at: 2026-11-24
    checked: "본문 대조(드라이브 문서 H22_250 · H22_262) — p.1910–1911 그림 250-1 활동전위 0~4기와 심전도 대응(0기 QRS, 1~2기 ST, 3기 T), 2기 고평부 = 칼륨 재분극 전류와 칼슘 전류의 균형, 3기 = 칼슘 전류 불활성화 + IKr·IKs 지속, IKr = KCNH2(HERG)·IKs = KCNQ1, 칼륨 통로를 늦게 닫는 변이가 선천 QT 연장; p.1913 조기후탈분극 2~3기·세포 안 칼슘 부하가 돕고 불균일 QT 연장에서 토르사드, QT 연장 약·저칼륨·저마그네슘·서맥, 지연후탈분극 4기(디기탈리스·허혈·카테콜아민, 양방향 VT), 표 250-1; p.1969 후천 QT 연장 휴지 의존형 시작, 칼륨 재분극 전류를 막는 약(소탈롤·도페틸라이드·이부틸라이드·에리트로마이신·할로페리돌·메타돈), 마그네슘 1~2 g·이소프로테레놀/조율 100~120회/분; p.1970 표 262-1 LQT1 IKs(KCNQ1)·LQT2 IKr(KCNH2)·LQT3 INa 비활성화 지연(SCN5A) 80~90 %, LQT1 운동·수영·LQT2 소리·감정·LQT3 수면, 비선택 베타차단제(나돌롤·프로프라놀롤)"
    verified: text
variants:
  - id: v1
    flip: true
    changed: "운동 중 실신 대신 새벽 알람 소리에 놀라 쓰러진 병력과 T 파가 낮고 갈라진 모양을 주었다 → 깎인 전류가 IKs 에서 IKr 로 바뀌어 답이 KCNH2(IKr) 가 된다"
    context: "단서를 바꿔 답이 바뀌는 변형 — 소리 · 감정 방아쇠"
    stem: "17세 여자가 새벽에 휴대전화 알람 소리에 깬 직후 쓰러졌다가 1분 만에 깨어났다. 전에도 크게 놀랐을 때 비슷한 일이 있었다. 복용 약은 없고 혈청 칼륨·마그네슘은 정상이다. 12유도 심전도에서 QTc 는 510 ms 이고 T 파는 낮고 갈라져 있다. 이 환자에서 기능이 줄어든 것으로 가장 가능성이 높은 것은?"
    choices:
      - "A. 3기 재분극의 느린 지연 정류 칼륨 전류(IKs)"
      - "B. 3기 재분극의 빠른 지연 정류 칼륨 전류(IKr)"
      - "C. 0기 나트륨 전류의 비활성화"
      - "D. 4기 내향 정류 칼륨 전류(IK1)"
      - "E. 1기 일과성 외향 칼륨 전류(Ito)"
    answer: "B"
    explanation: "갑작스러운 소리·감정에 사건이 나는 것은 LQT2 이고, KCNH2 변이로 IKr 이 줄어 3기 재분극이 늦어진다 [[harrison-22: 262장 p.1970]]. 운동·수영 중이었다면 IKs(KCNQ1, LQT1 — A), 수면 중이었다면 나트륨 전류 비활성화 지연(SCN5A, LQT3)이 답이다. 나트륨 전류는 비활성화가 늦어지는 것이지 기능이 줄어든 것이 아니어서 C 는 방향이 반대다. IK1 은 안정 막전위를, Ito 는 1기를 정하고 Ito 이상은 브루가다 증후군 쪽이다."
    kind: application
figures_none: 기전 목표 — 전류 표로 충분하다(심전도 그림은 임상 정리본 몫)
---

## 정상 — 3기 재분극이 QT 의 끝을 정한다
심실 활동전위의 각 시기가 표면 심전도에 그대로 찍힌다 — 0기(나트륨 전류의 빠른 상승)는 QRS, 1~2기는 ST 분절, 3기 재분극은 T 파다 [[harrison-22: 250장 p.1910]]. 2기 고평부는 들어오는 L형 칼슘 전류와 나가는 칼륨 전류의 균형이고, 칼슘 전류가 꺼진 뒤 **지연 정류 칼륨 전류 IKr(KCNH2/HERG)·IKs(KCNQ1)** 가 계속 열려 3기를 끝낸다 [[harrison-22: 250장 p.1911]]. 그래서 QT 간격은 심실 활동전위 길이의 표면 지표다. 두 전류가 서로를 보완해 하나가 약해져도 다른 하나가 재분극을 끝내는 여유를 재분극 예비력(repolarization reserve)이라 부른다.

## 고장 — 재분극 예비력이 깎이면
- 칼륨 통로를 늦게 닫거나 약하게 만드는 변이가 선천 QT연장증후군의 대부분이다 [[harrison-22: 250장 p.1911]]. 세 유형이 80~90 %이고 깎이는 전류가 달라 방아쇠가 다르다(표) [[harrison-22: 262장 p.1970]].
- LQT3 은 반대 방향 — 나트륨 통로가 제때 닫히지 않아 고평부에 들어오는 전류가 남는다 [[harrison-22: 262장 p.1970]]. 심박이 느릴수록 고평부가 길어 수면 중 사건이 난다.
- IKs 는 교감 자극(β 수용체 → cAMP)으로 커져 빠른 심박에서 활동전위를 줄이는 전류다. 이것이 없는 LQT1 은 운동 중 QT 가 제대로 짧아지지 못해 운동·수영이 방아쇠가 된다.
- 후천형은 같은 통로를 바깥에서 누른다 — 칼륨 재분극 전류를 막는 약(소탈롤·도페틸라이드·이부틸라이드, 에리트로마이신, 할로페리돌, 메타돈), 저칼륨·저마그네슘·저칼슘, 서맥 [[harrison-22: 262장 p.1969–1970]]. 유전 변이가 있으면 같은 약에도 더 쉽게 길어진다.

## 소견으로 — 조기후탈분극에서 토르사드로
- 2~3기가 길어지면 그 사이 칼슘 통로가 다시 열려 **조기후탈분극(EAD)** 이 생기고, 세포 안 칼슘 부하가 이를 돕는다 [[harrison-22: 250장 p.1913]].
- QT 연장이 심실마다 고르지 않으면 EAD 가 만든 박동이 비정상 파면을 퍼뜨려 QRS 축이 꼬이듯 바뀌는 다형 심실빈맥 — **토르사드 드 푸앵트(torsades de pointes)** 가 된다 [[harrison-22: 250장 p.1913]]. 대개 저절로 멈춰 실신으로 끝나고, 지속되면 심실세동이 된다 [[harrison-22: 262장 p.1969]].
- 후천형은 기외수축 → 보상 휴지 → 다음 박동의 QT 가 더 길어진 자리에 기외수축이 떨어지는 **휴지 의존형(긴–짧은 간격)** 으로 시작한다 [[harrison-22: 262장 p.1969]].
- 4기에 생기는 **지연후탈분극(DAD)** 은 다른 기전이다 — 세포 안 칼슘 과부하(디기탈리스 독성 · 허혈 · 카테콜아민)로 양방향 심실빈맥을 만들고 QT 와 무관하다 [[harrison-22: 250장 p.1913]].

## 임상 판단으로 — 어느 전류를 어떻게 돕나
- 선천형(특히 LQT1·LQT2)의 예방은 교감 방아쇠를 끊는 비선택 베타차단제(나돌롤·프로프라놀롤)이고, 모든 유형에서 QT 를 늘리는 약(대부분 IKr 차단)을 피한다 [[harrison-22: 262장 p.1970]]. 단계별 선택·위험도는 임상 정리본 `cn.cardio.long-qt-syndrome.first-line-drug`.
- 후천형의 급성 토르사드는 휴지 의존형이라 정맥 마그네슘, 그래도 반복되면 심박을 100~120회/분으로 올려(이소프로테레놀·조율) 휴지를 없애고, 원인 약·전해질을 바로잡는다 [[harrison-22: 262장 p.1969]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 250장 p.1910–1913 · 262장 p.1969–1970)
