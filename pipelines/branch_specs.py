"""
branch_specs.py — 회차별 **신경·동맥 분지 계보** 스펙. `branch_tree.py` 가 읽어 SVG를 찍는다.

여기만 고치면 라벨판·퀴즈판이 함께 갱신된다. 가지를 추가할 때 좌표를 만지지 않는다.
회차 배정은 **부위 기준**(anatomy_schedule.session_for_region) — 교수명·과거 학기 날짜가 아니다.

노드 키: kr(한글) · en(원어) · note(한 줄 메모) · star(빈출) · terminal(종말가지) · children
"""
from __future__ import annotations


def _n(kr, en="", note="", star=False, terminal=False, children=None, kind=None):
    d = {"kr": kr}
    if kind:
        d["kind"] = kind
    if en:
        d["en"] = en
    if note:
        d["note"] = note
    if star:
        d["star"] = True
    if terminal:
        d["terminal"] = True
    if children:
        d["children"] = children
    return d


SPECS: dict[str, dict] = {

# ── 1회차 (2026-08-18) 등·다리 피부벗기기 / 얕은층 ──────────────────────
"s01-nerve": {
    "title": "척수신경에서 피부신경까지", "en": "spinal nerve → cutaneous nerves",
    "subtitle": "1회차 · 등·다리 얕은층 — 앞가지/뒤가지가 갈린 뒤로는 영역이 겹치지 않는다",
    "kind": "nerve", "source": "1회차 과제 §앞가지·뒤가지 + Lower limb Superficial layer",
    "footer": [
        "뒤가지 계열은 얼기를 만들지 않는다 — 분절 배열이 그대로 유지된다.",
        "볼기피부신경 3형제 중 아래볼기만 앞가지 계열 — 이름이 같아도 뿌리가 다르다.",
    ],
    "root": _n("척수신경", "spinal n.", "앞뿌리(운동)+뒤뿌리(감각)가 합쳐진 것", children=[
        _n("뒤가지", "dorsal ramus", "가늘다 · 얼기 없음", star=True, children=[
            _n("안쪽가지", "medial br.", "위쪽 등에서 피부로", children=[
                _n("등 피부", terminal=True)]),
            _n("가쪽가지", "lateral br.", "아래쪽 등·허리에서 피부로", children=[
                _n("위볼기피부신경", "superior cluneal nn.", "L1–L3 · 엉덩뼈능선을 넘는다",
                   star=True, terminal=True),
                _n("중간볼기피부신경", "middle cluneal nn.", "S1–S3 · 뒤엉치구멍", terminal=True)]),
        ]),
        _n("앞가지", "ventral ramus", "굵다 · 얼기를 이룬다", star=True, children=[
            _n("엉치신경얼기", "sacral plexus", "L4–S4", children=[
                _n("뒤넙다리피부신경", "post. cut. n. of thigh", "S1–S3 · 궁둥구멍근 아래구멍",
                   star=True, children=[
                    _n("아래볼기피부신경", "inferior cluneal nn.", "큰볼기근 아래모서리를 감아",
                       star=True, terminal=True),
                    _n("관통가지", "perforating br.", "넓적다리 뒤 피부", terminal=True)]),
                _n("궁둥신경", "sciatic n.", "L4–S3", children=[
                    _n("정강신경", "tibial n.", children=[
                        _n("안쪽장딴지피부신경", "medial sural cut. n.", terminal=True)]),
                    _n("온종아리신경", "common fibular n.", children=[
                        _n("장딴지신경교통가지", "sural communicating br.", terminal=True)])]),
            ]),
            _n("허리신경얼기", "lumbar plexus", "L1–L4", children=[
                _n("넙다리신경 → 두렁신경", "femoral → saphenous n.",
                   "종아리·발 안쪽 피부(뒤칸 신경이 아니다)", terminal=True)]),
        ]),
    ]),
},

"s01-vessel": {
    "title": "다리의 얕은정맥과 깊은정맥", "en": "superficial & deep veins of the limb",
    "subtitle": "1회차 · 얕은근막 안에 있는 것과 깊은근막 아래 있는 것",
    "kind": "vein", "legend_kinds": ["vein"],
    "source": "1회차 §피부벗기기 — 얕은근막의 내용물",
    "footer": [
        "얕은정맥은 얕은근막 안, 깊은정맥은 깊은근막 아래 — 피부벗기기에서 갈리는 층.",
        "관통정맥의 판막은 깊은 쪽으로만 열린다 — 망가지면 역류해 하지정맥류.",
    ],
    "root": _n("발등정맥활", "dorsal venous arch of foot", children=[
        _n("큰두렁정맥", "great saphenous v.", "안쪽복사 **앞**", star=True, children=[
            _n("덧두렁정맥", "accessory saphenous v.", terminal=True),
            _n("두렁정맥구멍", "saphenous opening", "넓은근막의 구멍", star=True, children=[
                _n("넙다리정맥", "femoral v.", terminal=True)]),
        ]),
        _n("작은두렁정맥", "small saphenous v.", "가쪽복사 **뒤** · 장딴지신경 동반",
           star=True, children=[
            _n("오금정맥", "popliteal v.", terminal=True)]),
        _n("관통정맥", "perforating vv.", "얕은↔깊은 연결 · 판막은 깊은 쪽으로만",
           children=[_n("깊은정맥", "deep vv.", terminal=True)]),
    ]),
},

# ── 2회차 (2026-08-20) 등 근육 / 볼기·넓적다리 뒤 ───────────────────────
"s02-nerve": {
    "title": "등·볼기의 신경 계보", "en": "nerves of the back & gluteal region",
    "subtitle": "2회차 · 등에 있다고 다 뒤가지가 아니다 — 이주근육은 앞가지·더부신경",
    "kind": "nerve", "source": "2회차 §등 얕은층~깊은층 · 볼기부위",
    "footer": [
        "고유등근육만 뒤가지 지배 — 등세모근·넓은등근·마름근은 이주근육이라 예외.",
        "볼기: 큰볼기근=아래볼기신경 / 중간·작은볼기근=위볼기신경 (크기와 이름이 반대).",
    ],
    "root": _n("등·볼기의 운동신경", children=[
        _n("더부신경 XI", "accessory n.", "뇌신경 — 목정맥구멍으로", star=True, children=[
            _n("등세모근", "trapezius", "얕은층인데 뇌신경 지배", star=True, terminal=True),
            _n("목빗근", "sternocleidomastoid", terminal=True)]),
        _n("팔신경얼기", "brachial plexus", "C5–T1 앞가지", children=[
            _n("등쪽어깨신경 C5", "dorsal scapular n.", children=[
                _n("마름근·어깨올림근", star=True, terminal=True)]),
            _n("가슴등신경 C6–8", "thoracodorsal n.", children=[
                _n("넓은등근", "latissimus dorsi", terminal=True)]),
            _n("긴가슴신경 C5–7", "long thoracic n.", children=[
                _n("앞톱니근", "serratus anterior", "마비 → 날개어깨뼈", terminal=True)])]),
        _n("척수신경 뒤가지", "dorsal rami", "고유등근육 전부", star=True, children=[
            _n("척주세움근", "erector spinae", "엉덩갈비–가장긴–가시", terminal=True),
            _n("가로돌기가시근육", "transversospinalis", "반가시–뭇갈래–돌림", terminal=True),
            _n("뒤통수밑근육", "suboccipital mm.", "뒤통수밑신경 C1", terminal=True)]),
        _n("엉치신경얼기", "sacral plexus", "L4–S4 앞가지", children=[
            _n("위볼기신경 L4–S1", "superior gluteal n.", "위구멍으로", star=True, children=[
                _n("중간·작은볼기근·넙다리근막긴장근", "Trendelenburg 징후", terminal=True)]),
            _n("아래볼기신경 L5–S2", "inferior gluteal n.", "아래구멍으로", star=True, children=[
                _n("큰볼기근 단독", terminal=True)]),
            _n("궁둥신경 L4–S3", "sciatic n.", "인체 최대 말초신경", star=True, children=[
                _n("정강부분 → 햄스트링", "반힘줄·반막·두갈래근 긴갈래", terminal=True),
                _n("온종아리부분 → 두갈래근 짧은갈래", "이 갈래만 예외", star=True, terminal=True)])]),
    ]),
},

"s02-vessel": {
    "title": "등·볼기의 혈관 계보", "en": "arteries & veins of the back / gluteal region",
    "subtitle": "2회차 · 동맥은 속엉덩동맥에서 갈리고, 정맥은 같은 이름으로 되돌아온다",
    "kind": "artery", "legend_kinds": ["artery", "vein"],
    "source": "2회차 §볼기부위 혈관 · 등 얕은층 혈관",
    "footer": [
        "위볼기동맥만 속엉덩동맥 **뒤갈래** — 아래볼기·속음부는 앞갈래.",
        "볼기부위 정맥은 동맥과 같은 이름·같은 구멍으로 되돌아와 속엉덩정맥으로 모인다.",
    ],
    "root": _n("배대동맥", "abdominal aorta", children=[
        _n("온엉덩동맥", "common iliac a.", children=[
            _n("속엉덩동맥", "internal iliac a.", star=True, children=[
                _n("뒤갈래", "posterior division", children=[
                    _n("위볼기동맥", "superior gluteal a.", "궁둥구멍근 **위**구멍",
                       star=True, terminal=True)]),
                _n("앞갈래", "anterior division", children=[
                    _n("아래볼기동맥", "inferior gluteal a.", "아래구멍", terminal=True),
                    _n("속음부동맥", "internal pudendal a.",
                       "아래구멍 → 작은궁둥구멍 재진입", star=True, terminal=True)])])]),
        _n("속엉덩정맥", "internal iliac v.", "동맥과 짝을 이뤄 되돌아온다",
           kind="vein", star=True, children=[
            _n("위·아래볼기정맥", "gluteal vv.", "같은 구멍으로", kind="vein", terminal=True),
            _n("속음부정맥", "internal pudendal v.", kind="vein", terminal=True),
            _n("엉치정맥얼기", "sacral venous plexus",
               "판막이 없어 골반↔척주 사이 역류 가능(Batson 얼기)",
               kind="vein", star=True, terminal=True)]),
    ]),
},

# ── 3회차 (2026-08-24) 뒤통수밑삼각 / 어깨뼈부위 / 다리오금 ─────────────
"s03-nerve": {
    "title": "궁둥신경에서 발까지", "en": "sciatic n. → foot",
    "subtitle": "3회차 · 다리오금에서 갈리고, 종아리뼈목에서 다친다",
    "kind": "nerve", "source": "3회차 §다리오금·종아리 뒤부위",
    "footer": [
        "온종아리신경이 종아리뼈목을 감아도는 자리가 가장 흔한 손상 부위 → 발처짐.",
        "장딴지신경 = 안쪽장딴지피부신경(정강) + 교통가지(온종아리) — 순수 감각, 공여신경.",
    ],
    "root": _n("궁둥신경", "sciatic n.", "L4–S3 · 오금 위에서 갈린다", star=True, children=[
        _n("정강신경", "tibial n.", "오금 한가운데를 수직으로", star=True, children=[
            _n("안쪽장딴지피부신경", "medial sural cut. n.", terminal=True),
            _n("종아리 뒤칸 근육 전부", "얕은층+깊은층", terminal=True),
            _n("발목굴 통과", "tarsal tunnel", children=[
                _n("안쪽발바닥신경", "medial plantar n.", terminal=True),
                _n("가쪽발바닥신경", "lateral plantar n.", terminal=True)])]),
        _n("온종아리신경", "common fibular n.", "두갈래근 힘줄 안쪽 → 종아리뼈목",
           star=True, children=[
            _n("가쪽장딴지피부신경", "lateral sural cut. n.", terminal=True),
            _n("장딴지신경교통가지", "sural communicating br.", children=[
                _n("장딴지신경", "sural n.", "둘이 합쳐진 것", star=True, terminal=True)]),
            _n("얕은종아리신경", "superficial fibular n.", "가쪽칸 근육 + 발등 피부", terminal=True),
            _n("깊은종아리신경", "deep fibular n.", "앞칸 근육 + 첫째 발샅 피부",
               star=True, terminal=True)]),
    ]),
},

"s03-vessel": {
    "title": "빗장밑동맥과 오금동맥", "en": "subclavian & popliteal arteries",
    "subtitle": "3회차 · 어깨동맥그물과 무릎동맥그물 — 곁순환이 만들어지는 두 자리",
    "kind": "artery", "legend_kinds": ["artery", "vein"],
    "source": "3회차 §뒤통수밑삼각·어깨뼈부위·다리오금",
    "footer": [
        "무릎동맥 5가지 중 **중간무릎동맥만** 관절주머니를 뚫고 십자인대로 간다.",
        "어깨위동맥은 위가로어깨인대 **위**로, 어깨위신경은 인대 **아래**로 — 짝지어 외운다.",
    ],
    "root": _n("빗장밑동맥 / 넙다리동맥", "두 계통을 한 장에", children=[
        _n("빗장밑동맥", "subclavian a.", star=True, children=[
            _n("척추동맥", "vertebral a.", "C6–C1 가로돌기구멍 → 뒤통수밑삼각",
               star=True, terminal=True),
            _n("갑상목동맥", "thyrocervical trunk", children=[
                _n("어깨위동맥", "suprascapular a.", "위가로어깨인대 **위**로",
                   star=True, terminal=True),
                _n("가로목동맥", "transverse cervical a.", terminal=True)]),
            _n("등쪽어깨동맥", "dorsal scapular a.", "마름근 깊은면", terminal=True)]),
        _n("겨드랑동맥", "axillary a.", "작은가슴근 기준 3부", children=[
            _n("어깨밑동맥", "subscapular a.", "3부", children=[
                _n("어깨휘돌이동맥", "circumflex scapular a.", "세모공간", star=True, terminal=True),
                _n("가슴등동맥", "thoracodorsal a.", "넓은등근", terminal=True)]),
            _n("뒤위팔휘돌이동맥", "post. circumflex humeral a.",
               "네모공간 · 겨드랑신경 동반", star=True, terminal=True)]),
        _n("오금동맥", "popliteal a.", "넙다리동맥이 모음근구멍을 지나 개명",
           star=True, children=[
            _n("무릎동맥 5가지", "genicular aa.", "위·아래 각 2 + 중간 1", children=[
                _n("중간무릎동맥", "middle genicular a.",
                   "유일하게 관절주머니 관통 → 십자인대", star=True, terminal=True)]),
            _n("앞정강동맥", "anterior tibial a.", "종아리 앞칸 → 발등동맥", terminal=True),
            _n("뒤정강동맥", "posterior tibial a.", "뒤칸 → 발바닥동맥", children=[
                _n("종아리동맥", "fibular a.", terminal=True)])]),
        _n("오금정맥", "popliteal v.", "오금에서 동맥보다 **얕다**", kind="vein",
           star=True, children=[
            _n("작은두렁정맥 합류", "small saphenous v.", "장딴지신경과 나란히",
               kind="vein", terminal=True),
            _n("앞·뒤정강정맥", "tibial vv.", "동반정맥 두 줄씩", kind="vein", terminal=True),
            _n("넙다리정맥", "femoral v.", "모음근구멍을 지나 개명", kind="vein", terminal=True)]),
    ]),
},

# ── 6회차 (2026-09-03) 목의 삼각 / 넓적다리 앞·안쪽 ─────────────────────
"s06-nerve": {
    "title": "목·다리 앞의 신경 계보", "en": "cervical plexus & lumbar plexus",
    "subtitle": "6회차 · 목신경얼기는 한 점(신경점)에서, 허리신경얼기는 큰허리근 뒤에서",
    "kind": "nerve", "source": "6회차 §목의 삼각 · 넓적다리 앞칸·안쪽칸",
    "footer": [
        "넓은목근은 목신경이 아니라 **얼굴신경 목가지** — 운동이면 얼굴신경, 감각이면 가로목신경.",
        "폐쇄신경 앞가지는 짧은모음근 **앞면**, 뒤가지는 **뒷면** — 층을 가르는 지표.",
    ],
    "root": _n("목·다리 앞의 신경", children=[
        _n("목신경얼기", "cervical plexus", "C1–C4 앞가지", star=True, children=[
            _n("피부가지 4개", "신경점(Erb point)에서 한 점처럼", star=True, children=[
                _n("작은뒤통수신경", "lesser occipital n.", terminal=True),
                _n("큰귓바퀴신경", "great auricular n.", terminal=True),
                _n("가로목신경", "transverse cervical n.", "앞목삼각 피부(감각)",
                   star=True, terminal=True),
                _n("빗장위신경", "supraclavicular nn.", terminal=True)]),
            _n("목신경고리", "ansa cervicalis", "위뿌리 C1 + 아래뿌리 C2–3", children=[
                _n("목뿔아래근육", "infrahyoid mm.", "어깨목뿔근 포함", terminal=True)]),
            _n("가로막신경 C3–5", "phrenic n.", "C3·4·5 keeps the diaphragm alive",
               star=True, terminal=True)]),
        _n("얼굴신경 VII", "facial n.", "붓꼭지구멍 → 귀밑샘 속에서 5가지", children=[
            _n("목가지", "cervical br.", "넓은목근(표정근육)", star=True, terminal=True)]),
        _n("허리신경얼기", "lumbar plexus", "L1–L4 · 큰허리근 뒤", star=True, children=[
            _n("넙다리신경 L2–L4", "femoral n.", "넙다리삼각에서 가장 가쪽(NAVEL)",
               star=True, children=[
                _n("앞피부가지", "ant. cutaneous brr.", terminal=True),
                _n("넙다리네갈래근·넙다리빗근", terminal=True),
                _n("두렁신경", "saphenous n.", "모음근굴을 지나 종아리 안쪽 피부",
                   star=True, terminal=True)]),
            _n("폐쇄신경 L2–L4", "obturator n.", "폐쇄관 통과", star=True, children=[
                _n("앞가지", "anterior br.", "짧은모음근 **앞면**", star=True, children=[
                    _n("긴모음근·두덩정강근·짧은모음근", terminal=True),
                    _n("앞피부가지", "넓적다리 안쪽 피부 · 무릎 연관통", terminal=True)]),
                _n("뒤가지", "posterior br.", "짧은모음근 **뒷면**", children=[
                    _n("바깥폐쇄근·큰모음근 모음부분", terminal=True)])]),
            _n("가쪽넙다리피부신경 L2–3", "lat. femoral cut. n.",
               "눌리면 감각이상넓적다리통증", terminal=True)]),
    ]),
},

"s06-vessel": {
    "title": "바깥목동맥과 넙다리동맥", "en": "external carotid & femoral arteries",
    "subtitle": "6회차 · 목동맥삼각에서 갈리고, 넙다리삼각에서 갈린다",
    "kind": "artery", "legend_kinds": ["artery", "vein"],
    "source": "6회차 §목동맥삼각 · 넙다리삼각",
    "footer": [
        "온목동맥은 갈리기 전까지 **가지를 내지 않는다** — 방패연골 위모서리(C4)에서 갈림.",
        "안쪽넙다리휘돌이동맥이 넙다리뼈 머리·목의 주 공급원 — 끊기면 무혈성괴사.",
    ],
    "root": _n("온목동맥 / 넙다리동맥", "두 계통을 한 장에", children=[
        _n("온목동맥", "common carotid a.", "가지 없음 · C4에서 갈림", star=True, children=[
            _n("속목동맥", "internal carotid a.", "목에서는 가지 없음 → 머리속으로",
               star=True, terminal=True),
            _n("바깥목동맥", "external carotid a.", star=True, children=[
                _n("앞가지", children=[
                    _n("위갑상동맥", "superior thyroid a.", "첫 가지 · 위후두동맥을 냄",
                       star=True, terminal=True),
                    _n("혀동맥", "lingual a.", terminal=True),
                    _n("얼굴동맥", "facial a.", "턱밑샘을 파고 지나간다", star=True, terminal=True)]),
                _n("뒤가지", children=[
                    _n("뒤통수동맥", "occipital a.", terminal=True),
                    _n("뒤귓바퀴동맥", "post. auricular a.", terminal=True)]),
                _n("안쪽가지", children=[
                    _n("오름인두동맥", "ascending pharyngeal a.", terminal=True)]),
                _n("종말가지", children=[
                    _n("위턱동맥", "maxillary a.", "중간뇌막동맥을 냄", terminal=True),
                    _n("얕은관자동맥", "superficial temporal a.", terminal=True)])])]),
        _n("넙다리동맥", "femoral a.", "고샅인대 중간점 아래에서 촉지", star=True, children=[
            _n("깊은넙다리동맥", "profunda femoris a.", "고샅인대 아래 ~4 cm", star=True, children=[
                _n("안쪽넙다리휘돌이동맥", "medial circumflex femoral a.",
                   "엉덩허리근·두덩근 사이 → 넙다리뼈 머리·목", star=True, terminal=True),
                _n("가쪽넙다리휘돌이동맥", "lat. circumflex femoral a.", terminal=True),
                _n("관통동맥 3–4개", "perforating aa.", "큰모음근을 뚫고 뒤칸으로", terminal=True)]),
            _n("모음근구멍 통과", "adductor hiatus", children=[
                _n("오금동맥", "popliteal a.", "이름이 바뀐다", star=True, terminal=True)])]),
        _n("속목정맥", "internal jugular v.", "목혈관신경집에서 동맥 **가쪽**",
           kind="vein", star=True, children=[
            _n("얼굴정맥·혀정맥·위갑상정맥", "common facial v. 로 합류", kind="vein", terminal=True),
            _n("빗장밑정맥과 합류", "→ 팔머리정맥", kind="vein", terminal=True)]),
        _n("바깥목정맥", "external jugular v.", "목빗근을 **가로질러** 얕게 — 피부밑",
           kind="vein", star=True, children=[
            _n("빗장밑정맥", "subclavian v.", kind="vein", terminal=True)]),
        _n("넙다리정맥", "femoral v.", "넙다리삼각에서 동맥 **안쪽**(NAVEL)",
           kind="vein", star=True, children=[
            _n("큰두렁정맥", "great saphenous v.", "두렁정맥구멍으로 합류",
               kind="vein", star=True, terminal=True),
            _n("깊은넙다리정맥", "profunda femoris v.", kind="vein", terminal=True)]),
    ]),
},

# ── 신경혈관다발: 동맥·정맥·신경이 **같이 지나는 자리** ────────────────────
# 통로(구멍·굴·집)를 뿌리 아래 두고, 그 안을 지나는 셋을 색으로 묶어 보여준다.
# 태깅에서 "여기 지나는 것 세 개" 를 묻는 형태가 그대로 그림이 된다.

"s02-bundle": {
    "title": "함께 지나는 것 — 등·볼기", "en": "neurovascular bundles",
    "subtitle": "2회차 · 구멍마다 동맥·정맥·신경이 한 다발로 지나간다",
    "kind": "mixed", "legend_kinds": ["artery", "vein", "nerve"],
    "source": "2회차 §볼기부위 — 큰궁둥구멍 통과 구조물",
    "footer": [
        "볼기의 다발은 모두 **같은 이름 3종 세트** — 위볼기 A·V·N, 아래볼기 A·V·N.",
        "궁둥신경만 동반 동맥이 따로 없다(아래볼기동맥이 곁가지로 먹여 준다).",
    ],
    "root": _n("큰궁둥구멍", "greater sciatic foramen", "궁둥구멍근이 위·아래로 가른다",
               star=True, children=[
        _n("위구멍", "suprapiriform", "궁둥구멍근 **위** — 셋뿐", star=True, children=[
            _n("위볼기동맥", "superior gluteal a.", kind="artery", terminal=True),
            _n("위볼기정맥", "superior gluteal v.", kind="vein", terminal=True),
            _n("위볼기신경", "superior gluteal n.", "중간·작은볼기근",
               kind="nerve", star=True, terminal=True)]),
        _n("아래구멍", "infrapiriform", "궁둥구멍근 **아래** — 나머지 전부", star=True, children=[
            _n("아래볼기 A·V", "inferior gluteal a. & v.", kind="artery", terminal=True),
            _n("아래볼기신경", "inferior gluteal n.", "큰볼기근 단독",
               kind="nerve", terminal=True),
            _n("궁둥신경", "sciatic n.", "가장 굵고 가장 가쪽", kind="nerve",
               star=True, terminal=True),
            _n("뒤넙다리피부신경", "post. cut. n. of thigh", kind="nerve", terminal=True),
            _n("속음부 A·V", "internal pudendal a. & v.", kind="artery", terminal=True),
            _n("음부신경", "pudendal n.", "셋이 함께 작은궁둥구멍으로 재진입",
               kind="nerve", star=True, terminal=True)]),
        _n("어깨뼈 안쪽모서리", "along medial border of scapula",
           "마름근 깊은면에서 나란히", children=[
            _n("등쪽어깨동맥", "dorsal scapular a.", kind="artery", terminal=True),
            _n("등쪽어깨신경", "dorsal scapular n.", "C5", kind="nerve", terminal=True)]),
    ]),
},

"s03-bundle": {
    "title": "함께 지나는 것 — 오금·어깨뼈", "en": "neurovascular bundles",
    "subtitle": "3회차 · 다리오금은 얕은 것부터 신경–정맥–동맥 순으로 겹쳐 있다",
    "kind": "mixed", "legend_kinds": ["artery", "vein", "nerve"],
    "source": "3회차 §다리오금 · 어깨뼈부위",
    "footer": [
        "오금의 깊이 순서 '신–정–동' — 맥박이 안 잡히는 이유가 동맥이 가장 깊어서다.",
        "어깨뼈패임: 동맥은 인대 **위**, 신경은 인대 **아래** — 같은 이름인데 층이 갈린다.",
    ],
    "root": _n("세 자리", children=[
        _n("다리오금", "popliteal fossa", "뒤(얕은) → 앞(깊은) 순서", star=True, children=[
            _n("① 정강신경", "tibial n.", "가장 얕다", kind="nerve", star=True, terminal=True),
            _n("② 오금정맥", "popliteal v.", "중간", kind="vein", terminal=True),
            _n("③ 오금동맥", "popliteal a.", "가장 깊다", kind="artery",
               star=True, terminal=True)]),
        _n("네모공간", "quadrangular space", "위팔세갈래근 긴갈래 **가쪽**", star=True, children=[
            _n("뒤위팔휘돌이동맥", "post. circumflex humeral a.", kind="artery", terminal=True),
            _n("겨드랑신경", "axillary n.", "외과목 골절에서 손상", kind="nerve",
               star=True, terminal=True)]),
        _n("어깨뼈패임", "scapular notch", "위가로어깨인대가 덮어 구멍이 된다",
           star=True, children=[
            _n("어깨위동맥", "suprascapular a.", "인대 **위**로", kind="artery",
               star=True, terminal=True),
            _n("어깨위신경", "suprascapular n.", "인대 **아래** 구멍으로", kind="nerve",
               star=True, terminal=True)]),
    ]),
},

"s06-bundle": {
    "title": "함께 지나는 것 — 목·넙다리", "en": "neurovascular bundles",
    "subtitle": "6회차 · 목혈관신경집과 넙다리혈관집 — 두 '집' 의 배열을 나란히 본다",
    "kind": "mixed", "legend_kinds": ["artery", "vein", "nerve"],
    "source": "6회차 §목동맥삼각 · 넙다리삼각",
    "footer": [
        "목혈관신경집: 동맥 안쪽 · 정맥 가쪽 · 미주신경은 둘 사이 **뒤**.",
        "넙다리삼각 NAVEL: 가쪽부터 신경–동맥–정맥–빈공간–림프. 정맥이 동맥 **안쪽**이다.",
    ],
    "root": _n("두 개의 '집'", children=[
        _n("목혈관신경집", "carotid sheath", "목빗근 깊은면", star=True, children=[
            _n("온목동맥", "common carotid a.", "**안쪽**", kind="artery",
               star=True, terminal=True),
            _n("속목정맥", "internal jugular v.", "**가쪽** · 중심정맥삽입 표적",
               kind="vein", star=True, terminal=True),
            _n("미주신경 X", "vagus n.", "둘 사이 **뒤**", kind="nerve",
               star=True, terminal=True)]),
        _n("넙다리혈관집", "femoral sheath", "고샅인대 아래 · NAVEL", star=True, children=[
            _n("넙다리신경", "femoral n.", "가장 **가쪽** — 집 밖에 있다", kind="nerve",
               star=True, terminal=True),
            _n("넙다리동맥", "femoral a.", "가쪽칸 · 채혈·카테터 자리", kind="artery",
               star=True, terminal=True),
            _n("넙다리정맥", "femoral v.", "가운데칸 · 동맥 **안쪽**", kind="vein",
               star=True, terminal=True),
            _n("넙다리관 + 림프절", "femoral canal", "안쪽칸 — 넙다리탈장 입구",
               star=True, terminal=True)]),
        _n("모음근굴", "adductor canal", "넙다리빗근 아래", children=[
            _n("넙다리동·정맥", "femoral a. & v.", "모음근구멍으로 빠져 뒤로",
               kind="artery", terminal=True),
            _n("두렁신경", "saphenous n.", "혈관과 헤어져 앞안쪽으로", kind="nerve",
               star=True, terminal=True)]),
        _n("방패목뿔막", "thyrohyoid membrane", "뚫고 후두로", children=[
            _n("위후두동맥", "superior laryngeal a.", kind="artery", terminal=True),
            _n("위후두신경 속가지", "internal br. of sup. laryngeal n.", "성대문 위 감각",
               kind="nerve", star=True, terminal=True)]),
    ]),
},

"s01-bundle": {
    "title": "함께 지나는 것 — 얕은층", "en": "superficial neurovascular pairs",
    "subtitle": "1회차 · 얕은근막 안에서 정맥과 피부신경은 짝을 지어 다닌다",
    "kind": "mixed", "legend_kinds": ["vein", "nerve"],
    "source": "1회차 §피부벗기기 — 얕은근막의 내용물",
    "footer": [
        "짝을 외우면 하나를 찾으면 다른 하나가 따라온다 — 피부벗기기의 요령.",
        "복사 기준: 큰두렁정맥은 안쪽복사 **앞**, 작은두렁정맥은 가쪽복사 **뒤**.",
    ],
    "root": _n("얕은근막 속의 짝", "in the superficial fascia", children=[
        _n("종아리·발 안쪽", star=True, children=[
            _n("큰두렁정맥", "great saphenous v.", "안쪽복사 앞", kind="vein",
               star=True, terminal=True),
            _n("두렁신경", "saphenous n.", "넙다리신경 가지", kind="nerve",
               star=True, terminal=True)]),
        _n("종아리 뒤·발 가쪽", star=True, children=[
            _n("작은두렁정맥", "small saphenous v.", "가쪽복사 뒤", kind="vein",
               star=True, terminal=True),
            _n("장딴지신경", "sural n.", "생검·이식 공여신경", kind="nerve",
               star=True, terminal=True)]),
        _n("등의 얕은층", children=[
            _n("뒤가지의 피부가지", "cutaneous brr. of dorsal rami", kind="nerve", terminal=True),
            _n("동반 피부정맥", kind="vein", terminal=True)]),
    ]),
},

# ── 4회차 (2026-08-27) 큰가슴근부위·가슴벽 / 얼굴·귀밑샘·씹기근육 ─────────
"s04-nerve": {
    "title": "얼굴의 두 신경 — VII과 V", "en": "facial (VII) & trigeminal (V) nerves",
    "subtitle": "4회차 · 표정근육은 얼굴신경, 씹기근육과 피부감각은 삼차신경 — 인두굽이가 갈랐다",
    "kind": "nerve",
    "source": "4회차 §얼굴신경 · 삼차신경 · 씹기근육 (부위 기준 배정)",
    "footer": [
        "얼굴신경은 귀밑샘을 **지나가기만** 한다 — 귀밑샘 분비는 IX → 귀신경절 → 귓바퀴관자신경.",
        "표정근육=둘째 인두굽이=VII, 씹기근육=첫째 인두굽이=V3 — 근육의 족보가 신경을 정한다.",
    ],
    "root": _n("얼굴에 오는 뇌신경", "cranial nn. of the face", children=[
        _n("얼굴신경 VII", "facial n.", "붓꼭지구멍 → 귀밑샘 속에서 갈림 · **운동**",
           star=True, children=[
            _n("뒤귓바퀴신경", "post. auricular n.", "귀밑샘 들어가기 **전**에 갈린다 · 뒤통수힘살",
               terminal=True),
            _n("관자가지", "temporal br.", "이마힘살·눈둘레근 위쪽", star=True, terminal=True),
            _n("광대가지", "zygomatic br.", "눈둘레근 — 각막반사 날개", star=True, terminal=True),
            _n("볼가지", "buccal br.", "여러 개 · 볼근·입 주위 근육", star=True, terminal=True),
            _n("턱모서리가지", "marginal mandibular br.", "턱밑샘 수술에서 손상 1순위",
               star=True, terminal=True),
            _n("목가지", "cervical br.", "넓은목근 — 감각인 가로목신경과 구분", star=True,
               terminal=True),
        ]),
        _n("삼차신경 V", "trigeminal n.", "얼굴 **피부감각** + 씹기근육 운동", star=True, children=[
            _n("눈신경 V1", "ophthalmic n.", "위눈확틈새 · 순수 감각", children=[
                _n("눈확위신경", "supraorbital n.", "눈확위구멍 · 이마·머리덮개 앞",
                   star=True, terminal=True),
                _n("도르래위신경", "supratrochlear n.", "그보다 **안쪽**", terminal=True),
                _n("눈물·코섬모체신경", "lacrimal/nasociliary n.",
                   "V1↔V2 경계는 **위눈꺼풀 / 아래눈꺼풀**", terminal=True)]),
            _n("위턱신경 V2", "maxillary n.", "원형구멍 · 순수 감각", star=True, children=[
                _n("눈확아래신경", "infraorbital n.", "눈확아래구멍 · 뺨·**윗입술**",
                   star=True, terminal=True),
                _n("광대얼굴·광대관자가지", "zygomaticofacial/temporal", terminal=True)]),
            _n("아래턱신경 V3", "mandibular n.", "타원구멍 · **감각+운동**", star=True, children=[
                _n("귓바퀴관자신경", "auriculotemporal n.", "중간뇌막동맥을 두 뿌리로 감쌈 · "
                   "귀밑샘 분비섬유를 **얹어 나름**", star=True, terminal=True),
                _n("턱끝신경", "mental n.", "턱끝구멍 · **아랫입술**·턱", star=True, terminal=True),
                _n("씹기근육 운동가지", "nn. to muscles of mastication",
                   "깨물근·깊은관자·날개근신경", star=True, terminal=True)]),
        ]),
    ]),
},

"s04-vessel": {
    "title": "얼굴·가슴벽의 동맥과 정맥", "en": "arteries & veins of face and thoracic wall",
    "subtitle": "4회차 · 바깥목동맥 계열과 겨드랑·속가슴·가슴대동맥 계열을 한 장에",
    "kind": "mixed", "legend_kinds": ["artery", "vein"],
    "source": "4회차 §얼굴동맥·얕은관자동맥 · 큰가슴근부위 · 가슴벽",
    "footer": [
        "가로얼굴동맥은 **얕은관자동맥** 가지 — 얼굴동맥 가지가 아니다(태깅 단골 함정).",
        "얼굴정맥은 판막이 없어 눈구석정맥–위눈정맥을 거쳐 **해면정맥굴**과 통한다(위험삼각).",
    ],
    "root": _n("얼굴·가슴벽의 혈관", children=[
        _n("바깥목동맥", "external carotid a.", "방패연골 위모서리(C4)에서 갈린 뒤",
           kind="artery", star=True, children=[
            _n("얼굴동맥", "facial a.", "깨물근 앞모서리에서 **아래턱뼈를 넘어** 올라온다 · 구불구불",
               kind="artery", star=True, children=[
                _n("아래입술동맥", "inferior labial a.", kind="artery", terminal=True),
                _n("위입술동맥", "superior labial a.", kind="artery", terminal=True),
                _n("가쪽코동맥", "lateral nasal a.", kind="artery", terminal=True),
                _n("눈구석동맥", "angular a.", "종말가지 — 눈동맥과 문합", kind="artery",
                   star=True, terminal=True)]),
            _n("얕은관자동맥", "superficial temporal a.", "귀 앞 박동 촉지점",
               kind="artery", star=True, children=[
                _n("가로얼굴동맥", "transverse facial a.", "귀밑샘관 **위**를 가로로",
                   kind="artery", star=True, terminal=True),
                _n("이마가지", "frontal br.", kind="artery", terminal=True),
                _n("마루가지", "parietal br.", kind="artery", terminal=True)]),
            _n("위턱동맥", "maxillary a.", "관자아래우묵으로", kind="artery", children=[
                _n("중간뇌막동맥", "middle meningeal a.", "경막외혈종", kind="artery",
                   star=True, terminal=True),
                _n("눈확아래동맥", "infraorbital a.", kind="artery", terminal=True)]),
        ]),
        _n("얼굴의 정맥", "veins of the face", "판막 없음", kind="vein", star=True, children=[
            _n("얼굴정맥", "facial v.", "동맥 **뒤**를 곧게", kind="vein", star=True, children=[
                _n("온얼굴정맥", "common facial v.", "속목정맥으로", kind="vein", terminal=True)]),
            _n("아래턱뒤정맥", "retromandibular v.", "얕은관자정맥 + 위턱정맥",
               kind="vein", star=True, children=[
                _n("앞가지", "ant. division", "얼굴정맥과 합류", kind="vein", terminal=True),
                _n("뒤가지", "post. division", "뒤귓바퀴정맥과 → **바깥목정맥**",
                   kind="vein", star=True, terminal=True)]),
        ]),
        _n("가슴벽의 혈관", "vessels of the thoracic wall", children=[
            _n("겨드랑동맥", "axillary a.", "작은가슴근이 1·2·3부로 나눈다",
               kind="artery", star=True, children=[
                _n("가슴봉우리동맥", "thoracoacromial a.", "2부 · 가슴근·봉우리·빗장·어깨세모",
                   kind="artery", star=True, terminal=True),
                _n("가쪽가슴동맥", "lateral thoracic a.", "2부 · 앞톱니근·젖샘",
                   kind="artery", terminal=True)]),
            _n("속가슴동맥", "internal thoracic a.", "빗장밑동맥 가지 · 복장뼈 가쪽 1–2 cm",
               kind="artery", star=True, children=[
                _n("앞갈비사이동맥", "ant. intercostal aa.", kind="artery", terminal=True),
                _n("근육가로막·위배벽동맥", "musculophrenic / sup. epigastric a.",
                   kind="artery", terminal=True)]),
            _n("가슴대동맥", "thoracic aorta", kind="artery", children=[
                _n("뒤갈비사이동맥", "post. intercostal aa.", "3–11번 · 갈비사이고랑으로",
                   kind="artery", star=True, terminal=True)]),
        ]),
    ]),
},

# ── 7회차 (2026-09-07) 목의 뿌리·인두 / 종아리 가쪽·발목 안쪽면·발바닥 ──────
"s07-nerve": {
    "title": "목뿌리·발목의 신경", "en": "nerves of the root of neck & ankle",
    "subtitle": "7회차 · 위가슴문을 지나는 신경과, 굽힘근지지띠 밑을 지나는 신경",
    "kind": "nerve", "source": "7회차 §목의 뿌리·인두 · 종아리 가쪽 · 발목 안쪽면",
    "footer": [
        "되돌이후두신경은 좌우 경로가 다르다 — 오른쪽 빗장밑동맥 / 왼쪽 대동맥활.",
        "정강신경은 굽힘근지지띠 **아래**에서 안쪽·가쪽 발바닥신경으로 갈린다(발목굴증후군).",
    ],
    "root": _n("7회차의 신경", children=[
        _n("미주신경 X", "vagus n.", "목혈관신경집 안에서 내려간다", star=True, children=[
            _n("되돌이후두신경(오른)", "right recurrent laryngeal n.",
               "**빗장밑동맥**을 감아 올라간다", star=True, terminal=True),
            _n("되돌이후두신경(왼)", "left recurrent laryngeal n.",
               "**대동맥활**(동맥관인대)을 감아 — 더 길다", star=True, terminal=True),
            _n("위후두신경", "superior laryngeal n.", "속가지(감각)+바깥가지(반지방패근)",
               terminal=True)]),
        _n("가로막신경", "phrenic n.", "C3–5 · **앞목갈비근 앞면**을 타고 내려간다",
           star=True, children=[
            _n("가로막", "diaphragm", "C3-4-5 keeps the diaphragm alive", terminal=True)]),
        _n("팔신경얼기", "brachial plexus", "앞·중간목갈비근 **사이**(목갈비근틈새)",
           star=True, children=[
            _n("위가슴문 통과", "through superior thoracic aperture",
               "빗장밑동맥과 같은 틈새 — 정맥은 앞목갈비근 **앞**", star=True, terminal=True)]),
        _n("온종아리신경", "common fibular n.", "종아리뼈목을 감아 돈다 — 발처짐",
           star=True, children=[
            _n("얕은종아리신경", "superficial fibular n.",
               "가쪽칸(긴·짧은종아리근) + 발등 피부", star=True, terminal=True),
            _n("깊은종아리신경", "deep fibular n.",
               "앞칸 근육 + **첫째 발가락사이 피부**", star=True, terminal=True)]),
        _n("정강신경", "tibial n.", "굽힘근지지띠 밑 **발목굴**을 지난다", star=True, children=[
            _n("안쪽발바닥신경", "medial plantar n.", "손의 정중신경에 해당", star=True,
               terminal=True),
            _n("가쪽발바닥신경", "lateral plantar n.", "손의 자신경에 해당", star=True,
               terminal=True),
            _n("안쪽발꿈치가지", "medial calcaneal br.", "지지띠를 **뚫고** 나온다 — 발꿈치 감각",
               terminal=True)]),
    ]),
},

"s07-vessel": {
    "title": "목뿌리·종아리의 동맥과 정맥", "en": "vessels of the root of neck & leg",
    "subtitle": "7회차 · 빗장밑동맥 3부와 오금동맥 아래 갈래를 나란히",
    "kind": "mixed", "legend_kinds": ["artery", "vein"],
    "source": "7회차 §목의 뿌리 · 종아리 가쪽·뒤 · 발바닥",
    "footer": [
        "빗장밑동맥은 **앞목갈비근**이 1·2·3부로 나눈다 — 겨드랑동맥을 작은가슴근이 나누는 것과 같은 꼴.",
        "발바닥동맥활은 **가쪽발바닥동맥**이 주로 만든다 — 손의 깊은손바닥동맥활에 해당.",
    ],
    "root": _n("7회차의 혈관", children=[
        _n("빗장밑동맥", "subclavian a.", "앞목갈비근이 3부로 나눈다", kind="artery",
           star=True, children=[
            _n("1부 — 척추동맥", "vertebral a.", "가로구멍으로 올라간다", kind="artery",
               star=True, terminal=True),
            _n("1부 — 속가슴동맥", "internal thoracic a.", "아래로 — 앞갈비사이동맥",
               kind="artery", terminal=True),
            _n("1부 — 갑상목동맥", "thyrocervical trunk", "아래갑상·어깨위·목가로동맥",
               kind="artery", star=True, terminal=True),
            _n("2부 — 갈비목동맥", "costocervical trunk", kind="artery", terminal=True)]),
        _n("목의 정맥", "veins of the neck", kind="vein", children=[
            _n("속목정맥", "internal jugular v.", "빗장밑정맥과 만나 팔머리정맥",
               kind="vein", star=True, terminal=True),
            _n("빗장밑정맥", "subclavian v.", "앞목갈비근 **앞** — 동맥은 뒤", kind="vein",
               star=True, terminal=True)]),
        _n("오금동맥", "popliteal a.", "오금근 아래모서리에서 갈린다", kind="artery",
           star=True, children=[
            _n("앞정강동맥", "anterior tibial a.", "뼈사이막을 **뚫고** 앞칸으로 → 발등동맥",
               kind="artery", star=True, terminal=True),
            _n("뒤정강동맥", "posterior tibial a.", "발목 안쪽면 → 안쪽·가쪽발바닥동맥",
               kind="artery", star=True, terminal=True),
            _n("종아리동맥", "fibular a.", "뒤정강동맥 가지 · 가쪽칸에는 **자기 동맥이 없다**",
               kind="artery", star=True, terminal=True)]),
        _n("발의 동맥활", "arches of the foot", kind="artery", children=[
            _n("깊은발바닥동맥활", "deep plantar arch", "주로 **가쪽발바닥동맥**",
               kind="artery", star=True, terminal=True),
            _n("발등동맥", "dorsalis pedis a.", "긴엄지폄근힘줄 **가쪽** 촉지",
               kind="artery", star=True, terminal=True)]),
    ]),
},

"s07-bundle": {
    "title": "함께 지나는 것 — 위가슴문·발목", "en": "neurovascular bundles",
    "subtitle": "7회차 · 목갈비근이 가르는 목의 통로와, 굽힘근지지띠 밑 발목굴",
    "kind": "mixed", "legend_kinds": ["artery", "vein", "nerve"],
    "source": "7회차 §목의 뿌리 · 발목 안쪽면 · 종아리 가쪽",
    "footer": [
        "앞목갈비근이 기준: **정맥은 앞, 동맥·팔신경얼기는 뒤**(목갈비근틈새).",
        "발목굴 앞→뒤 'Tom, Dick, And Very Nervous Harry' — 동맥·신경이 가운데 낀다.",
    ],
    "root": _n("세 개의 통로", children=[
        _n("목갈비근틈새", "scalene triangle", "앞·중간목갈비근 사이", star=True, children=[
            _n("빗장밑정맥", "subclavian v.", "앞목갈비근 **앞** — 틈새 밖", kind="vein",
               star=True, terminal=True),
            _n("빗장밑동맥 2부", "subclavian a.", "틈새 **안**", kind="artery",
               star=True, terminal=True),
            _n("팔신경얼기", "brachial plexus", "동맥과 같은 틈새", kind="nerve",
               star=True, terminal=True)]),
        _n("발목굴(굽힘근지지띠 밑)", "tarsal tunnel", "안쪽복사 뒤 · 앞→뒤 순서", star=True,
           children=[
            _n("① 뒤정강근 힘줄", "Tibialis posterior", "**T**om", kind="mixed", terminal=True),
            _n("② 긴발가락굽힘근 힘줄", "flexor Digitorum longus", "**D**ick", kind="mixed",
               terminal=True),
            _n("③ 뒤정강동맥", "posterior tibial Artery", "**A**nd", kind="artery",
               star=True, terminal=True),
            _n("④ 정강신경", "tibial Nerve", "**V**ery **N**ervous", kind="nerve",
               star=True, terminal=True),
            _n("⑤ 긴엄지굽힘근 힘줄", "flexor Hallucis longus", "**H**arry", kind="mixed",
               star=True, terminal=True)]),
        _n("종아리근지지띠 밑", "fibular retinacula", "가쪽복사 뒤", star=True, children=[
            _n("긴종아리근 힘줄", "fibularis longus", "발바닥을 가로질러 첫째 발허리뼈로",
               kind="mixed", star=True, terminal=True),
            _n("짧은종아리근 힘줄", "fibularis brevis", "다섯째 발허리뼈 거친면", kind="mixed",
               terminal=True),
            _n("얕은종아리신경", "superficial fibular n.", "가쪽칸을 지배 — **동맥은 없다**",
               kind="nerve", star=True, terminal=True)]),
    ]),
},

"s04-bundle": {
    "title": "함께 지나는 것 — 귀밑샘·갈비사이", "en": "neurovascular bundles",
    "subtitle": "4회차 · 귀밑샘은 얕은 것부터 신경–정맥–동맥, 갈비사이고랑은 위부터 정맥–동맥–신경",
    "kind": "mixed", "legend_kinds": ["artery", "vein", "nerve"],
    "source": "4회차 §귀밑샘 · 가슴벽 갈비사이 · 세모가슴근고랑",
    "footer": [
        "귀밑샘 속 순서 '신–정–동'(얕은→깊은) — 다리오금과 같은 순서로 묶어 외운다.",
        "갈비사이고랑은 위부터 '정–동–신'(VAN) — 천자는 반드시 갈비뼈 **위모서리**를 따라.",
    ],
    "root": _n("네 개의 통로", children=[
        _n("귀밑샘 속", "within the parotid gland", "얕은 → 깊은", star=True, children=[
            _n("① 얼굴신경 VII", "facial n.", "가장 얕다 · 샘을 얕은/깊은엽으로 가른다",
               kind="nerve", star=True, terminal=True),
            _n("② 아래턱뒤정맥", "retromandibular v.", "중간", kind="vein", terminal=True),
            _n("③ 바깥목동맥", "external carotid a.", "가장 깊다", kind="artery",
               star=True, terminal=True)]),
        _n("갈비사이고랑", "costal groove", "위 → 아래 · VAN", star=True, children=[
            _n("① 갈비사이정맥", "post. intercostal v.", "가장 **위**", kind="vein",
               terminal=True),
            _n("② 갈비사이동맥", "post. intercostal a.", "가운데", kind="artery", terminal=True),
            _n("③ 갈비사이신경", "intercostal n.", "가장 **아래**·가장 얕다 — 천자 주의",
               kind="nerve", star=True, terminal=True)]),
        _n("세모가슴근고랑", "deltopectoral groove", "빗장뼈 아래 삼각", star=True, children=[
            _n("노쪽피부정맥", "cephalic v.", "겨드랑정맥으로 합류", kind="vein",
               star=True, terminal=True),
            _n("어깨세모가지", "deltoid br. of thoracoacromial a.", kind="artery",
               terminal=True)]),
        _n("얼굴의 구멍 짝", "foramina of the face", "신경과 동맥이 같은 이름으로 함께",
           children=[
            _n("눈확위구멍", "supraorbital foramen", "눈확위신경(V1) + 눈확위동맥",
               kind="nerve", star=True, terminal=True),
            _n("눈확아래구멍", "infraorbital foramen", "눈확아래신경(V2) + 눈확아래동맥",
               kind="nerve", star=True, terminal=True),
            _n("턱끝구멍", "mental foramen", "턱끝신경(V3) + 턱끝동맥 · 세 구멍은 거의 수직선",
               kind="nerve", star=True, terminal=True)]),
    ]),
},

# ── 5회차 (2026-08-31) 가슴안·가슴막·위세로칸·심장막·심장 / 관자·관자아래부위 ──
"s05-nerve": {
    "title": "가슴안과 관자아래우묵의 신경", "en": "nerves of the thoracic cavity & infratemporal fossa",
    "subtitle": "5회차 · 목에서 내려온 신경이 허파뿌리를 앞뒤로 가르고, V3가 관자아래우묵을 채운다",
    "kind": "nerve", "source": "5회차 §가슴안·세로칸·심장 · 관자아래부위 (부위 기준 배정)",
    "footer": [
        "가로막신경은 허파뿌리 **앞**, 미주신경은 허파뿌리 **뒤** — 세로칸에서 둘을 가르는 유일한 기준.",
        "고실끈신경은 얼굴신경(VII) 가지인데 **혀신경(V3)에 얹혀** 간다 — 미각·침샘은 V가 아니다.",
    ],
    "root": _n("5회차의 신경", children=[
        _n("가로막신경", "phrenic n.", "C3·C4·C5 — 'C3,4,5 keeps the diaphragm alive'",
           star=True, children=[
            _n("허파뿌리 앞으로", "ant. to the root of the lung", "미주신경과 갈리는 지점",
               star=True, children=[
                _n("심장막가지", "pericardial br.", "섬유·벽쪽장막심장막 **감각**",
                   star=True, terminal=True),
                _n("가로막 운동", "motor to diaphragm", "유일한 운동 지배", star=True,
                   terminal=True),
                _n("가로막가슴막·배막 감각", "central diaphragmatic sensory",
                   "자극되면 **어깨 연관통**(C3–C5 피부분절)", star=True, terminal=True)]),
        ]),
        _n("미주신경 X", "vagus n.", "허파뿌리 **뒤**로 내려간다", star=True, children=[
            _n("왼되돌이후두신경", "left recurrent laryngeal n.",
               "**대동맥활**(동맥관인대)을 감아 올라간다", star=True, terminal=True),
            _n("허파가지·식도얼기", "pulmonary/esophageal plexus", "부교감 — 기관지 수축",
               terminal=True),
            _n("심장가지", "cardiac br.", "부교감 — 심박수 **감소**", star=True, terminal=True),
        ]),
        _n("갈비사이신경", "intercostal nn.", "T1–T11 앞가지 · 얼기를 만들지 않는다",
           star=True, children=[
            _n("벽쪽가슴막 감각", "parietal pleura", "갈비·가로막 **주변부** — 통증에 예민",
               star=True, terminal=True),
            _n("가쪽·앞피부가지", "lateral/ant. cutaneous br.", terminal=True)]),
        _n("아래턱신경 V3", "mandibular n.", "타원구멍 → 관자아래우묵 · **감각+운동**",
           star=True, children=[
            _n("앞줄기", "ant. division", "대부분 **운동**", children=[
                _n("깊은관자신경", "deep temporal nn.", "관자근", star=True, terminal=True),
                _n("깨물근신경", "masseteric n.", "턱뼈패임을 지난다", terminal=True),
                _n("가쪽날개근신경", "n. to lateral pterygoid", terminal=True),
                _n("볼신경", "buccal n.", "앞줄기의 **유일한 감각** — 볼 점막",
                   star=True, terminal=True)]),
            _n("뒤줄기", "post. division", "대부분 **감각**", star=True, children=[
                _n("귓바퀴관자신경", "auriculotemporal n.", "중간뇌막동맥을 두 뿌리로 감싼다",
                   star=True, terminal=True),
                _n("혀신경", "lingual n.", "혀 앞 2/3 **일반감각** · 고실끈신경이 합류",
                   star=True, terminal=True),
                _n("아래이틀신경", "inferior alveolar n.", "턱뼈구멍 → 턱끝신경으로 나온다",
                   star=True, children=[
                    _n("턱목뿔근신경", "n. to mylohyoid", "구멍 **들어가기 전**에 갈린 운동가지",
                       star=True, terminal=True)])]),
        ]),
        _n("얹혀 가는 섬유", "hitchhiking fibers", "V3 가지를 길로 쓰는 다른 뇌신경",
           star=True, children=[
            _n("고실끈신경", "chorda tympani", "**VII** · 혀 앞 2/3 미각 + 턱밑·혀밑샘 분비",
               star=True, terminal=True),
            _n("귀신경절", "otic ganglion", "**IX** 부교감이 갈아타는 곳 → 귓바퀴관자신경 → 귀밑샘",
               star=True, terminal=True)]),
    ]),
},

"s05-vessel": {
    "title": "대동맥활·심장동맥과 위턱동맥", "en": "aortic arch, coronary & maxillary arteries",
    "subtitle": "5회차 · 세로칸의 큰 줄기와, 관자아래우묵을 채우는 위턱동맥 3부",
    "kind": "mixed", "legend_kinds": ["artery", "vein"],
    "source": "5회차 §대동맥활·심장 · 관자아래부위 위턱동맥",
    "footer": [
        "위턱동맥은 아래턱뼈목에서 갈려 **3부**로 나뉜다 — 1부는 구멍으로, 2부는 근육으로, 3부는 우묵으로.",
        "심장정맥굴은 **왼심방 뒤 방실고랑**을 지나 오른심방으로 — 동맥과 반대 방향으로 훑는다.",
    ],
    "root": _n("5회차의 혈관", children=[
        _n("대동맥활", "aortic arch", "위세로칸 · 가지 3개", kind="artery", star=True, children=[
            _n("팔머리동맥", "brachiocephalic trunk", "**오른쪽만** 있다", kind="artery",
               star=True, children=[
                _n("오른온목동맥", "right common carotid a.", kind="artery", terminal=True),
                _n("오른빗장밑동맥", "right subclavian a.",
                   "오른되돌이후두신경이 감는다", kind="artery", star=True, terminal=True)]),
            _n("왼온목동맥", "left common carotid a.", "활에서 **직접**", kind="artery",
               star=True, terminal=True),
            _n("왼빗장밑동맥", "left subclavian a.", kind="artery", terminal=True)]),
        _n("오름대동맥", "ascending aorta", "대동맥동굴에서 심장동맥이 나온다",
           kind="artery", star=True, children=[
            _n("오른심장동맥", "right coronary a.", "오른심방귀와 허파동맥줄기 사이",
               kind="artery", star=True, children=[
                _n("굴심방결절가지", "SA nodal br.", "약 60%에서 오른쪽 기원", kind="artery",
                   star=True, terminal=True),
                _n("오른모서리가지", "right marginal br.", kind="artery", terminal=True),
                _n("뒤심실사이가지", "post. interventricular br.",
                   "약 70%가 오른쪽 우세(right dominance)", kind="artery", star=True,
                   terminal=True)]),
            _n("왼심장동맥", "left coronary a.", "짧은 줄기 뒤 곧 갈린다", kind="artery",
               star=True, children=[
                _n("앞심실사이가지", "ant. interventricular br. (LAD)",
                   "'widow-maker' · 심실사이막 앞 2/3", kind="artery", star=True,
                   terminal=True),
                _n("휘돌이가지", "circumflex br.", "왼방실고랑을 돌아 뒤로", kind="artery",
                   star=True, children=[
                    _n("왼모서리가지", "left marginal br.", kind="artery", terminal=True)])]),
        ]),
        _n("심장의 정맥", "cardiac veins", "심장정맥굴로 모인다", kind="vein", star=True,
           children=[
            _n("심장정맥굴", "coronary sinus", "**오른심방**으로 열린다", kind="vein",
               star=True, children=[
                _n("큰심장정맥", "great cardiac v.", "앞심실사이가지와 동행", kind="vein",
                   terminal=True),
                _n("중간심장정맥", "middle cardiac v.", "뒤심실사이가지와 동행", kind="vein",
                   terminal=True),
                _n("작은심장정맥", "small cardiac v.", kind="vein", terminal=True)]),
        ]),
        _n("위대정맥", "superior vena cava", "왼·오른 팔머리정맥이 합쳐", kind="vein",
           star=True, children=[
            _n("홀정맥", "azygos v.", "허파뿌리 **위**를 활처럼 넘어 합류", kind="vein",
               star=True, terminal=True)]),
        _n("위턱동맥", "maxillary a.", "바깥목동맥 종말가지 · 아래턱뼈목에서",
           kind="artery", star=True, children=[
            _n("1부 아래턱부", "1st (mandibular) part", "아래턱뼈가지 **안쪽** · 구멍으로 간다",
               kind="artery", star=True, children=[
                _n("중간뇌막동맥", "middle meningeal a.", "가시구멍 · **경막외혈종**",
                   kind="artery", star=True, terminal=True),
                _n("아래이틀동맥", "inferior alveolar a.", "턱뼈구멍 — 같은 이름 신경과 동행",
                   kind="artery", star=True, terminal=True)]),
            _n("2부 날개근부", "2nd (pterygoid) part", "씹기근육으로만 간다", kind="artery",
               children=[
                _n("깊은관자동맥", "deep temporal aa.", kind="artery", terminal=True),
                _n("깨물동맥·날개근가지", "masseteric/pterygoid br.", kind="artery",
                   terminal=True),
                _n("볼동맥", "buccal a.", kind="artery", terminal=True)]),
            _n("3부 날개입천장부", "3rd (pterygopalatine) part", "날개위턱틈새 → 우묵으로",
               kind="artery", star=True, children=[
                _n("눈확아래동맥", "infraorbital a.", kind="artery", terminal=True),
                _n("나비입천장동맥", "sphenopalatine a.", "코피(epistaxis)의 주범",
                   kind="artery", star=True, terminal=True)]),
        ]),
        _n("날개정맥얼기", "pterygoid venous plexus", "가쪽날개근 주위 · 판막 없음",
           kind="vein", star=True, children=[
            _n("위턱정맥", "maxillary v.", "→ 아래턱뒤정맥", kind="vein", terminal=True),
            _n("해면정맥굴과 교통", "→ cavernous sinus", "감염 전파 경로", kind="vein",
               star=True, terminal=True)]),
    ]),
},

"s05-bundle": {
    "title": "함께 지나는 것 — 허파뿌리·심장막굴·관자아래우묵",
    "en": "neurovascular bundles & spaces",
    "subtitle": "5회차 · 배열 순서가 그대로 태깅 문제가 되는 세 자리",
    "kind": "mixed", "legend_kinds": ["artery", "vein", "nerve"],
    "source": "5회차 §허파뿌리 · 심장막 · 관자아래우묵",
    "footer": [
        "허파뿌리 앞→뒤는 좌우 공통 **정–동–기(VAB)**, 위→아래만 좌우가 다르다.",
        "심장막가로굴 앞벽=대동맥+허파동맥줄기, 뒤벽=위대정맥+왼심방 — 손가락이 통과한다.",
    ],
    "root": _n("세 개의 자리", children=[
        _n("허파뿌리", "root of the lung", "앞→뒤 공통: 정맥–동맥–기관지", star=True, children=[
            _n("앞→뒤 순서", "ant. → post.", "좌우 공통", star=True, children=[
                _n("① 허파정맥", "pulmonary vv.", "가장 앞·아래", kind="vein", star=True,
                   terminal=True),
                _n("② 허파동맥", "pulmonary a.", kind="artery", terminal=True),
                _n("③ 기관지", "main bronchus", "가장 뒤", kind="mixed", star=True,
                   terminal=True)]),
            _n("위→아래(오른쪽)", "right, sup. → inf.", "**기관지가 동맥보다 위**(eparterial)",
               star=True, terminal=True),
            _n("위→아래(왼쪽)", "left, sup. → inf.", "**동맥이 가장 위** — 대동맥활을 넘어야 해서",
               star=True, terminal=True),
            _n("가로막신경", "phrenic n.", "뿌리 **앞**", kind="nerve", star=True, terminal=True),
            _n("미주신경", "vagus n.", "뿌리 **뒤**", kind="nerve", star=True, terminal=True)]),
        _n("심장막굴", "pericardial sinuses", "장막심장막이 접혀 생긴 막다른 공간", star=True,
           children=[
            _n("가로굴", "transverse sinus", "앞=대동맥+허파동맥줄기 / 뒤=위대정맥+왼심방 · "
               "심장수술 교차겸자 자리", star=True, terminal=True),
            _n("빗굴", "oblique sinus", "왼심방 **뒤** · 허파정맥에 둘러싸인 막다른 골목",
               star=True, terminal=True),
            _n("심장막 감각", "pericardial sensory", "**가로막신경**(C3–C5) → 어깨 연관통",
               kind="nerve", star=True, terminal=True)]),
        _n("관자아래우묵", "infratemporal fossa", "아래턱뼈가지 **안쪽** · 얕은→깊은", star=True,
           children=[
            _n("① 가쪽날개근", "lateral pterygoid m.", "두 갈래 사이로 위턱동맥이 지난다 · "
               "**턱을 여는** 유일한 씹기근육", kind="mixed", star=True, terminal=True),
            _n("② 날개정맥얼기", "pterygoid venous plexus", "근육 주위를 채운다", kind="vein",
               star=True, terminal=True),
            _n("③ 위턱동맥", "maxillary a.", "가쪽날개근의 얕은쪽/깊은쪽을 지난다(변이)",
               kind="artery", star=True, terminal=True),
            _n("④ 아래이틀신경·혀신경", "inf. alveolar & lingual nn.",
               "안쪽날개근 앞 · 혀신경이 **더 앞·안쪽**", kind="nerve", star=True,
               terminal=True),
            _n("⑤ 안쪽날개근", "medial pterygoid m.", "가장 깊다 · 깨물근과 아래턱뼈가지를 "
               "샌드위치처럼 낀다", kind="mixed", star=True, terminal=True)]),
        _n("갈비가로막오목", "costodiaphragmatic recess", "가슴막안의 **가장 깊은 곳**",
           star=True, children=[
            _n("가슴막 아래경계 8·10·12", "pleural reflection",
               "빗장중간선 8 · 중간겨드랑선 10 · 척주옆선 12번 갈비", star=True, terminal=True),
            _n("허파 아래경계 6·8·10", "inferior border of lung",
               "가슴막보다 항상 **두 갈비 위** — 그 차이가 오목이다", star=True, terminal=True),
            _n("갈비뼈 위모서리로", "above the rib", "갈비사이고랑의 VAN을 피한다",
               star=True, terminal=True)]),
    ]),
},

# ── 9회차 (2026-09-14) 팔 얕은근막·겨드랑 / 기관·기관지·허파·뒤세로칸 ──────
"s09-nerve": {
    "title": "팔신경얼기와 가슴의 신경", "en": "brachial plexus & nerves of the thorax",
    "subtitle": "9회차 · 다섯 단계(뿌리–줄기–갈래–다발–가지)와 뒤세로칸의 자율신경",
    "kind": "nerve",
    "source": "9회차 실습주제(팔 얕은근막·겨드랑 / 뒤세로칸) + e-Anatomy Upper limb — Axilla 0:00~30:33",
    "footer": [
        "다발 이름은 겨드랑동맥 **2부**를 기준으로 붙는다 — 가쪽·안쪽·뒤.",
        "뿌리에서 바로 나오는 가지(긴가슴·등쪽어깨)는 다발을 거치지 않는다 — 그래서 따로 다친다.",
    ],
    "root": _n("9회차의 신경", children=[
        _n("팔신경얼기", "brachial plexus", "C5–T1 앞가지 · 목갈비근틈새 → 겨드랑",
           star=True, children=[
            _n("뿌리", "roots, C5–T1", "곧바로 나오는 가지 2개", star=True, children=[
                _n("등쪽어깨신경", "dorsal scapular n.", "C5 · 마름근·어깨올림근",
                   star=True, terminal=True),
                _n("긴가슴신경", "long thoracic n.", "C5–C7 · **앞톱니근** · 다치면 날개어깨",
                   star=True, terminal=True)]),
            _n("줄기", "trunks", "위 C5+C6 · 중간 C7 · 아래 C8+T1", star=True, children=[
                _n("빗장밑근신경", "n. to subclavius", "위줄기", terminal=True),
                _n("어깨위신경", "suprascapular n.", "위줄기 · 가시위근·가시아래근 · "
                   "어깨뼈패임을 지난다", star=True, terminal=True)]),
            _n("갈래", "divisions", "앞갈래=굽힘근 / 뒤갈래=폄근 · 첫째갈비뼈 뒤에서",
               star=True, terminal=True),
            _n("가쪽다발", "lateral cord", "앞갈래(위+중간)", star=True, children=[
                _n("가쪽가슴근신경", "lateral pectoral n.", "큰가슴근", terminal=True),
                _n("근육피부신경", "musculocutaneous n.", "위팔 앞칸 3근 → "
                   "가쪽아래팔피부신경", star=True, terminal=True),
                _n("정중신경 가쪽뿌리", "lateral root of median n.", "감각 위주",
                   star=True, terminal=True)]),
            _n("안쪽다발", "medial cord", "아래줄기 앞갈래(C8–T1)", star=True, children=[
                _n("안쪽가슴근신경", "medial pectoral n.", "작은가슴근+큰가슴근",
                   terminal=True),
                _n("안쪽위팔피부신경", "medial brachial cut. n.", terminal=True),
                _n("안쪽아래팔피부신경", "medial antebrachial cut. n.", terminal=True),
                _n("자신경", "ulnar n.", "손 내재근의 주인 · C8–T1", star=True,
                   terminal=True),
                _n("정중신경 안쪽뿌리", "medial root of median n.",
                   "두 뿌리가 겨드랑동맥 앞에서 **M자**를 만든다", star=True,
                   terminal=True)]),
            _n("뒤다발", "posterior cord", "세 줄기의 뒤갈래가 모두 모인다",
               star=True, children=[
                _n("위·아래 어깨밑신경", "upper & lower subscapular nn.",
                   "어깨밑근 · 큰원근", terminal=True),
                _n("가슴등신경", "thoracodorsal n.", "**넓은등근** · 겨드랑 뒤벽 수술 주의",
                   star=True, terminal=True),
                _n("겨드랑신경", "axillary n.", "위팔뼈 **외과목**을 감는다 · 어깨세모근 · "
                   "어깨탈구·외과목골절에 취약", star=True, terminal=True),
                _n("노신경", "radial n.", "위팔뼈 **노신경고랑** · 모든 폄근",
                   star=True, terminal=True)]),
        ]),
        _n("뒤세로칸의 신경", "nerves of the posterior mediastinum", star=True, children=[
            _n("미주신경", "vagus n. (X)", "허파뿌리 **뒤**를 지나 식도로", star=True,
               children=[
                _n("식도신경얼기", "esophageal plexus", "앞·뒤미주줄기로 다시 모인다 · "
                   "앞=왼미주, 뒤=오른미주", star=True, terminal=True),
                _n("왼되돌이후두신경", "left recurrent laryngeal n.",
                   "**대동맥활**(동맥관인대)을 감아 올라간다", star=True, terminal=True),
                _n("오른되돌이후두신경", "right recurrent laryngeal n.",
                   "오른**빗장밑동맥**을 감는다 — 가슴으로 내려오지 않는다", star=True,
                   terminal=True)]),
            _n("교감신경줄기", "sympathetic trunk", "갈비뼈머리 앞 · 척추뼈몸통 가쪽",
               star=True, children=[
                _n("백색교통가지", "white ramus communicans", "T1–L2만 · 절전(말이집)",
                   star=True, terminal=True),
                _n("회색교통가지", "grey ramus communicans", "모든 높이 · 절후(민말이집)",
                   star=True, terminal=True),
                _n("큰내장신경", "greater splanchnic n.", "T5–T9 → **복강신경절**",
                   star=True, terminal=True),
                _n("작은내장신경", "lesser splanchnic n.", "T10–T11 → 대동맥콩팥신경절",
                   terminal=True),
                _n("가장작은내장신경", "least splanchnic n.", "T12 → 콩팥신경얼기",
                   terminal=True),
                _n("별신경절", "stellate ganglion", "아래목신경절+첫째가슴신경절 · "
                   "손상 시 호르너증후군", star=True, terminal=True)]),
        ]),
    ]),
},

"s09-vessel": {
    "title": "겨드랑동맥과 홀정맥계통", "en": "axillary artery & azygos system",
    "subtitle": "9회차 · 근육이 동맥을 셋으로 나누고, 홀정맥이 가슴의 피를 되받는다",
    "kind": "mixed", "legend_kinds": ["artery", "vein"],
    "source": "9회차 실습주제 + e-Anatomy Upper limb — Axilla · Thorax — Posterior mediastinum",
    "footer": [
        "겨드랑동맥의 부(part) 번호 = 작은가슴근 기준 **안쪽 1 · 뒤 2 · 가쪽 3** 이고 "
        "가지 수도 1–2–3개다.",
        "홀정맥은 위대정맥으로, 가슴림프관은 **왼정맥각**으로 — 액체 둘의 종착이 다르다.",
    ],
    "root": _n("9회차의 혈관", children=[
        _n("겨드랑동맥", "axillary a.", "첫째갈비뼈 가쪽모서리 ~ 큰원근 아래모서리",
           kind="artery", star=True, children=[
            _n("1부 (가지 1)", "medial to pec. minor", kind="artery", star=True, children=[
                _n("위가슴동맥", "superior thoracic a.", "1–2번 갈비사이", kind="artery",
                   terminal=True)]),
            _n("2부 (가지 2)", "posterior to pec. minor", kind="artery", star=True,
               children=[
                _n("가슴봉우리동맥", "thoracoacromial a.", "네 가지: 봉우리·빗장·"
                   "어깨세모·가슴 — **ABCD**", kind="artery", star=True, terminal=True),
                _n("가쪽가슴동맥", "lateral thoracic a.", "앞톱니근·유방 가쪽",
                   kind="artery", star=True, terminal=True)]),
            _n("3부 (가지 3)", "lateral to pec. minor", kind="artery", star=True, children=[
                _n("어깨밑동맥", "subscapular a.", "겨드랑동맥의 **가장 굵은** 가지",
                   kind="artery", star=True, children=[
                    _n("가슴등동맥", "thoracodorsal a.", "넓은등근", kind="artery",
                       terminal=True),
                    _n("어깨휘돌이동맥", "circumflex scapular a.",
                       "세모공간을 지나 어깨뼈 뒤 문합에 낀다", kind="artery", star=True,
                       terminal=True)]),
                _n("뒤위팔휘돌이동맥", "post. circumflex humeral a.",
                   "겨드랑신경과 함께 **네모공간**을 지난다", kind="artery", star=True,
                   terminal=True),
                _n("앞위팔휘돌이동맥", "ant. circumflex humeral a.",
                   "위팔뼈 외과목 앞 · 위팔두갈래근 긴갈래에 가지", kind="artery",
                   terminal=True)]),
            _n("→ 위팔동맥", "brachial a.", "큰원근 아래모서리에서 이름이 바뀐다",
               kind="artery", star=True, terminal=True)]),
        _n("허파순환·기관지동맥", "pulmonary & bronchial vessels", star=True, children=[
            _n("허파동맥줄기", "pulmonary trunk", "**정맥혈**을 허파로", kind="artery",
               star=True, terminal=True),
            _n("허파정맥 4개", "pulmonary vv.", "**동맥혈**을 왼심방으로 · 구역 사이를 달린다",
               kind="vein", star=True, terminal=True),
            _n("기관지동맥", "bronchial aa.", "오른 1개(대개 3번 뒤갈비사이동맥에서) · "
               "왼 2개(가슴대동맥에서) — 허파조직 자체를 먹인다", kind="artery", star=True,
               terminal=True),
            _n("기관지정맥", "bronchial vv.", "오른→홀정맥 · 왼→반홀정맥", kind="vein",
               terminal=True)]),
        _n("홀정맥계통", "azygos system", "가슴벽의 피를 위대정맥으로 되돌린다",
           kind="vein", star=True, children=[
            _n("홀정맥", "azygos v.", "오른허리올림정맥 + 오른갈비밑정맥 → 오른쪽을 올라 "
               "**T4에서 활을 그려** 위대정맥으로", kind="vein", star=True, terminal=True),
            _n("반홀정맥", "hemiazygos v.", "왼쪽 아래(T9–T11) → **T9에서 건너가** 홀정맥으로",
               kind="vein", star=True, terminal=True),
            _n("덧반홀정맥", "accessory hemiazygos v.", "왼쪽 위(T5–T8) → T8에서 건너간다",
               kind="vein", star=True, terminal=True),
            _n("대정맥 우회로", "cavocaval anastomosis", "아래대정맥이 막히면 이 길이 커진다",
               kind="vein", star=True, terminal=True)]),
        _n("가슴림프관", "thoracic duct", "가슴우리 오른쪽에서 시작해 T5에서 **왼쪽으로** 건넌다",
           kind="vein", star=True, children=[
            _n("왼정맥각", "left venous angle", "왼속목정맥 + 왼빗장밑정맥이 만나는 자리 — "
               "종착", kind="vein", star=True, terminal=True),
            _n("오른림프관", "right lymphatic duct", "오른쪽 위반신만 · 오른정맥각으로",
               kind="vein", terminal=True)]),
    ]),
},

"s09-bundle": {
    "title": "함께 지나는 것 — 겨드랑·허파뿌리·뒤세로칸",
    "en": "neurovascular bundles of the axilla & mediastinum",
    "subtitle": "9회차 · 배열 순서가 그대로 태깅 문제가 되는 세 자리",
    "kind": "mixed", "legend_kinds": ["artery", "vein", "nerve"],
    "source": "9회차 §겨드랑 내용물 · 허파뿌리 · 뒤세로칸",
    "footer": [
        "겨드랑에서 **정맥이 가장 안쪽·앞**이다 — 중심정맥길이 여기로 난다.",
        "허파뿌리 앞→뒤는 좌우 공통 **정–동–기**, 위→아래만 좌우가 다르다.",
    ],
    "root": _n("세 개의 자리", children=[
        _n("겨드랑", "axilla", "네 벽 · 꼭대기 · 바닥으로 둘러싸인 피라미드", star=True,
           children=[
            _n("네 벽", "walls", star=True, children=[
                _n("앞벽", "ant. — 큰가슴근·작은가슴근", star=True, terminal=True),
                _n("뒤벽", "post. — 어깨밑근·넓은등근·큰원근", star=True, terminal=True),
                _n("안쪽벽", "medial — 가슴우리 1–4번 + 앞톱니근", star=True,
                   terminal=True),
                _n("가쪽벽", "lateral — 위팔뼈 결절사이고랑", terminal=True)]),
            _n("꼭대기 = 목겨드랑관", "cervicoaxillary canal",
               "첫째갈비뼈 · 빗장뼈 · 어깨뼈위모서리", star=True, terminal=True),
            _n("내용물 안쪽→가쪽", "contents", star=True, children=[
                _n("① 겨드랑정맥", "axillary v.", "가장 **안쪽·앞** · 중심정맥삽입",
                   kind="vein", star=True, terminal=True),
                _n("② 겨드랑동맥", "axillary a.", "정맥의 가쪽 · 겨드랑집 안", kind="artery",
                   star=True, terminal=True),
                _n("③ 팔신경얼기 다발", "cords", "동맥 **2부**를 둘러싼다 — 그래서 이름이 "
                   "가쪽·안쪽·뒤", kind="nerve", star=True, terminal=True),
                _n("④ 겨드랑림프절 5군", "axillary lymph nodes",
                   "가슴근·어깨밑·위팔·중심·꼭대기 — 유방암 병기의 자리", kind="vein",
                   star=True, terminal=True)]),
            _n("겨드랑집", "axillary sheath", "목의 척추앞근막이 늘어난 것 — "
               "동맥과 얼기를 함께 싼다(정맥은 대개 밖)", star=True, terminal=True)]),
        _n("허파뿌리", "root of the lung", "가슴막이 감싸 허파인대로 늘어진다", star=True,
           children=[
            _n("앞→뒤 (좌우 공통)", "ant. → post.", star=True, children=[
                _n("① 허파정맥", "pulmonary vv.", "가장 앞·아래", kind="vein", star=True,
                   terminal=True),
                _n("② 허파동맥", "pulmonary a.", kind="artery", terminal=True),
                _n("③ 기관지", "main bronchus", "가장 뒤", star=True, terminal=True)]),
            _n("위→아래 오른쪽", "right", "**기관지가 가장 위**(eparterial bronchus)",
               star=True, terminal=True),
            _n("위→아래 왼쪽", "left", "**동맥이 가장 위** — 대동맥활을 넘어야 하므로",
               star=True, terminal=True),
            _n("가로막신경", "phrenic n.", "뿌리 **앞**", kind="nerve", star=True,
               terminal=True),
            _n("미주신경", "vagus n.", "뿌리 **뒤**", kind="nerve", star=True,
               terminal=True)]),
        _n("뒤세로칸", "posterior mediastinum", "위 T4/T5 · 아래 가로막 · 앞 심장막 · "
           "뒤 T5–T12", star=True, children=[
            _n("앞→뒤 층 순서", "ant. → post.", star=True, children=[
                _n("① 식도 + 식도신경얼기", "esophagus", "심장막 바로 뒤", kind="nerve",
                   star=True, terminal=True),
                _n("② 가슴대동맥", "descending thoracic aorta", "식도의 왼쪽 → 아래로 "
                   "가면서 **뒤**로", kind="artery", star=True, terminal=True),
                _n("③ 가슴림프관", "thoracic duct", "식도와 대동맥 **사이·뒤**",
                   kind="vein", star=True, terminal=True),
                _n("④ 홀정맥", "azygos v.", "척추 오른쪽", kind="vein", star=True,
                   terminal=True),
                _n("⑤ 교감신경줄기", "sympathetic trunk", "가장 가쪽 · 갈비뼈머리 앞",
                   kind="nerve", star=True, terminal=True)]),
            _n("가로막 구멍 3개", "diaphragmatic apertures", star=True, children=[
                _n("대정맥구멍 T8", "caval opening", "아래대정맥 + 오른가로막신경",
                   kind="vein", star=True, terminal=True),
                _n("식도구멍 T10", "esophageal hiatus", "식도 + **앞·뒤미주줄기**",
                   kind="nerve", star=True, terminal=True),
                _n("대동맥구멍 T12", "aortic hiatus", "대동맥 + 가슴림프관 + 홀정맥 — "
                   "근육이 아니라 **인대 뒤**라 눌리지 않는다", kind="artery", star=True,
                   terminal=True)]),
        ]),
    ]),
},
# ── 10회차 (2026-09-17) 위팔 앞칸·팔오금·아래팔 앞칸·손바닥 / 배벽·고샅관·정삭·고환 ──
"s10-nerve": {
    "title": "위팔에서 손까지의 신경과 배벽의 신경",
    "en": "nerves of the arm, forearm, hand & abdominal wall",
    "subtitle": "10회차 · 세 신경이 칸을 나눠 갖고, 배벽은 갈비사이신경이 이어진다",
    "kind": "nerve",
    "source": "10회차 실습주제(위팔 앞칸·팔오금·아래팔 앞칸·손바닥 / 배벽·고샅관) + "
              "e-Anatomy Upper limb — Arm·Forearm·Hand / Abdomen — Abdominal wall",
    "footer": [
        "칸이 신경을 정한다 — 앞칸은 **정중·자**, 뒤칸은 **노**(뒤뼈사이)가 맡는다.",
        "손의 근육은 **자신경 깊은가지**가 거의 다 맡고, 정중신경은 엄지두덩 3근 + 벌레근 1·2뿐이다.",
        "배벽 신경은 새로 생기지 않는다 — 갈비사이신경(T7–T11)이 그대로 내려와 이름만 바뀐다.",
    ],
    "root": _n("10회차의 신경", children=[
        _n("정중신경", "median nerve", "C6–T1 · 가쪽뿌리+안쪽뿌리 · 위팔에서 **가지를 안 낸다**",
           star=True, children=[
            _n("위팔 구간", "in the arm", "위팔동맥과 동반 · 가쪽→앞→안쪽으로 건너간다",
               star=True, terminal=True),
            _n("팔오금 통과", "at the cubital fossa",
               "**위팔두갈래근널힘줄 깊이** · 원엎침근 두 갈래 사이로 들어간다",
               star=True, terminal=True),
            _n("아래팔 앞칸 얕은층", "superficial flexors",
               "원엎침근·노쪽손목굽힘근·긴손바닥근·얕은손가락굽힘근 — "
               "**자쪽손목굽힘근만 빼고** 다 맡는다", star=True, terminal=True),
            _n("앞뼈사이신경", "anterior interosseous n.",
               "깊은층 — 긴엄지굽힘근 · 깊은손가락굽힘근 **가쪽 절반** · 네모엎침근 · **순수 운동**",
               star=True, terminal=True),
            _n("손바닥피부가지", "palmar cutaneous branch",
               "손목굴 **위로** 지난다 → 손목굴증후군에서 손바닥 감각은 남는다",
               star=True, terminal=True),
            _n("손목굴 통과", "through the carpal tunnel",
               "굽힘근지지띠 **깊이** · 굽힘근힘줄 9개와 함께", star=True, children=[
                _n("되돌이가지", "recurrent branch",
                   "엄지두덩 3근(짧은엄지벌림·짧은엄지굽힘 얕은갈래·엄지맞섬)",
                   star=True, terminal=True),
                _n("온바닥쪽손가락신경", "common palmar digital nn.",
                   "가쪽 3.5손가락 감각 + **벌레근 1·2**", star=True, terminal=True)]),
        ]),
        _n("자신경", "ulnar nerve", "C8–T1 · 안쪽다발 · **위팔에서 가지를 안 낸다**",
           star=True, children=[
            _n("안쪽위관절융기 뒤", "behind the medial epicondyle",
               "자신경고랑 — 피부 바로 밑이라 **가장 잘 다치는 자리**", star=True, terminal=True),
            _n("아래팔 앞칸", "in the forearm",
               "자쪽손목굽힘근 + 깊은손가락굽힘근 **안쪽 절반**(4·5지)", star=True, terminal=True),
            _n("손등가지", "dorsal branch",
               "아래팔 먼쪽 1/3에서 자쪽손목굽힘근 **깊이로 빠져나간다**", star=True, terminal=True),
            _n("자신경굴(Guyon)", "ulnar canal",
               "**콩알뼈와 갈고리뼈갈고리 사이** · 굽힘근지지띠 **위**를 지난다",
               star=True, children=[
                _n("얕은가지", "superficial br.",
                   "짧은손바닥근 + 안쪽 1.5손가락 감각", star=True, terminal=True),
                _n("깊은가지", "deep br.",
                   "새끼두덩 3근 · **뼈사이근 전부** · 벌레근 3·4 · **엄지모음근** · "
                   "짧은엄지굽힘근 깊은갈래", star=True, terminal=True)]),
        ]),
        _n("노신경", "radial nerve", "C5–T1 · 뒤칸의 신경 — 이 회차에서는 뒤칸·팔오금 가쪽",
           star=True, children=[
            _n("깊은가지 → 뒤뼈사이신경", "posterior interosseous n.",
               "손뒤침근을 뚫고 뒤칸 깊은층으로", star=True, terminal=True),
            _n("얕은가지", "superficial br.",
               "위팔노근 **깊이** · 손등 가쪽 3.5손가락 감각", star=True, terminal=True),
            _n("위팔노근·긴/짧은노쪽손목폄근", "brachioradialis, ECRL/ECRB",
               "갈림 **전에** 나오는 가지", terminal=True),
        ]),
        _n("근육피부신경", "musculocutaneous nerve",
           "C5–C7 · 부리위팔근을 **뚫고** 위팔두갈래근·위팔근 사이로", star=True, children=[
            _n("가쪽아래팔피부신경", "lateral antebrachial cutaneous n.",
               "위팔두갈래근 힘줄 **가쪽**에서 나온다 — 팔오금 얕은층의 끝가지",
               star=True, terminal=True)]),
        _n("배벽의 신경 — 갈비사이신경의 연속", "nerves of the abdominal wall",
           "T7–T11 갈비사이신경 + 갈비밑신경(T12) + L1", star=True, children=[
            _n("가슴배신경", "thoracoabdominal nn.",
               "T7–T11 · **배속빗근과 배가로근 사이**로 달린다 — 이 면이 신경면",
               star=True, children=[
                _n("가쪽배피부가지", "lateral cutaneous br.",
                   "**중간겨드랑선**에서 뚫고 나온다", star=True, terminal=True),
                _n("앞배피부가지", "anterior cutaneous br.",
                   "**배곧은근집**을 뚫고 나온다", star=True, terminal=True)]),
            _n("갈비밑신경", "subcostal n.", "T12 · 열두째갈비뼈 아래",
               star=True, terminal=True),
            _n("엉덩아랫배신경", "iliohypogastric n.", "L1 · 두덩부위 위 피부",
               star=True, terminal=True),
            _n("엉덩고샅신경", "ilioinguinal n.",
               "L1 · **고샅관 속을 지나 얕은고샅구멍으로 나온다** · 음낭/큰음순 앞쪽",
               star=True, terminal=True),
            _n("음부넙다리신경 생식가지", "genital br. of genitofemoral n.",
               "L1–L2 · **고환올림근** · 고환올림근반사의 운동다리",
               star=True, terminal=True)]),
    ]),
},

"s10-vessel": {
    "title": "위팔에서 손까지의 혈관과 배벽의 혈관",
    "en": "arteries & veins of the arm, forearm, hand and abdominal wall",
    "subtitle": "10회차 · 위팔동맥이 팔오금에서 둘로 갈리고, 손에서 두 개의 활로 다시 만난다",
    "kind": "mixed",
    "legend_kinds": ["artery", "vein"],
    "source": "10회차 §위팔동맥 · 노동맥 · 자동맥 · 손바닥동맥활 · 얕은근막 · 배곧은근집",
    "footer": [
        "팔의 동맥은 **갈라졌다가 다시 만난다** — 얕은/깊은 손바닥동맥활이 닫힌 고리다.",
        "얕은활은 **자동맥**이, 깊은활은 **노동맥**이 주인이다(Allen 검사의 근거).",
        "배벽은 **위·아래배벽동맥이 배꼽에서 문합**한다 — 대동맥과 엉덩동맥을 잇는 샛길.",
    ],
    "root": _n("10회차의 혈관", children=[
        _n("위팔동맥", "brachial a.",
           "큰원근 아래모서리에서 겨드랑동맥이 이름을 바꾼다 · **안쪽두갈래근고랑**",
           kind="artery", star=True, children=[
            _n("깊은위팔동맥", "deep brachial a. (profunda brachii)",
               "노신경과 함께 **노신경고랑**으로", kind="artery", star=True, terminal=True),
            _n("자쪽곁동맥(위·아래)", "sup./inf. ulnar collateral a.",
               "팔꿈치 문합에 참여", kind="artery", star=True, terminal=True),
            _n("동반정맥", "venae comitantes", "동맥을 좌우로 끼고 달린다",
               kind="vein", terminal=True),
            _n("노동맥", "radial a.",
               "팔오금에서 **가쪽** · 위팔노근 힘줄 **안쪽**에서 만져진다(채혈·맥박)",
               kind="artery", star=True, children=[
                _n("노쪽되돌이동맥", "radial recurrent a.", "팔꿈치 문합",
                   kind="artery", star=True, terminal=True),
                _n("해부코담배갑 통과", "through the anatomical snuffbox",
                   "손등으로 넘어가 **첫째등쪽뼈사이근**을 뚫는다",
                   kind="artery", star=True, terminal=True),
                _n("깊은손바닥동맥활", "deep palmar arch",
                   "**노동맥이 주인** · 자동맥 깊은가지가 닫는다 · 얕은활보다 **몸쪽**",
                   kind="artery", star=True, terminal=True)]),
            _n("자동맥", "ulnar a.",
               "팔오금에서 **안쪽·깊은곳** · 먼쪽 절반은 자쪽손목굽힘근 가쪽",
               kind="artery", star=True, children=[
                _n("자쪽되돌이동맥", "ulnar recurrent a.", "팔꿈치 문합",
                   kind="artery", star=True, terminal=True),
                _n("온뼈사이동맥", "common interosseous a.",
                   "곧 **앞·뒤뼈사이동맥**으로 갈린다", kind="artery", star=True, terminal=True),
                _n("얕은손바닥동맥활", "superficial palmar arch",
                   "**자동맥이 주인** · 노동맥 손바닥가지가 닫는다 · 깊은활보다 **먼쪽**",
                   kind="artery", star=True, children=[
                    _n("온바닥쪽손가락동맥", "common palmar digital aa.",
                       kind="artery", star=True, terminal=True),
                    _n("고유바닥쪽손가락동맥", "proper palmar digital aa.",
                       "손가락 양쪽 가장자리", kind="artery", star=True, terminal=True)])]),
        ]),
        _n("배벽의 동맥", "arteries of the abdominal wall",
           "위·아래 두 방향에서 들어와 배꼽에서 만난다", kind="artery", star=True, children=[
            _n("위배벽동맥", "superior epigastric a.",
               "속가슴동맥의 끝가지 — **위에서 내려온다**", kind="artery", star=True,
               terminal=True),
            _n("아래배벽동맥", "inferior epigastric a.",
               "**바깥엉덩동맥**에서 · 깊은고샅구멍 **안쪽** · 가쪽배꼽주름을 만든다",
               kind="artery", star=True, terminal=True),
            _n("깊은엉덩휘돌이동맥", "deep circumflex iliac a.",
               "바깥엉덩동맥 · 엉덩뼈능선을 따라", kind="artery", star=True, terminal=True),
            _n("배꼽 문합", "periumbilical anastomosis",
               "위+아래배벽동맥이 **배곧은근집 안에서** 만난다 — 대동맥↔엉덩동맥 샛길",
               kind="artery", star=True, terminal=True)]),
        _n("배벽의 얕은정맥", "superficial veins of the abdominal wall",
           "**가슴배벽정맥**이 위·아래대정맥을 잇는다", kind="vein", star=True, children=[
            _n("얕은배벽정맥", "superficial epigastric v.",
               "큰두렁정맥 → 넙다리정맥", kind="vein", star=True, terminal=True),
            _n("얕은엉덩휘돌이정맥", "superficial circumflex iliac v.",
               kind="vein", star=True, terminal=True),
            _n("가슴배벽정맥", "thoracoepigastric v.",
               "**아래대정맥 막히면 굵어진다**(caput medusae와 구별)",
               kind="vein", star=True, terminal=True),
            _n("배꼽옆정맥", "paraumbilical vv.",
               "간문맥과 연결 — **문맥고혈압에서 caput medusae**",
               kind="vein", star=True, terminal=True)]),
        _n("덩굴정맥얼기", "pampiniform plexus",
           "정삭 안 · 고환동맥을 감싸 **열교환** · 왼쪽은 왼콩팥정맥으로 직각 유입 → "
           "**정계정맥류가 왼쪽에 많다**", kind="vein", star=True, terminal=True),
    ]),
},

"s10-bundle": {
    "title": "함께 지나는 것 — 팔오금 · 손목굴 · 고샅관",
    "en": "neurovascular bundles: cubital fossa, carpal tunnel, inguinal canal",
    "subtitle": "10회차 · 배열 순서와 벽의 구성이 그대로 태깅 문제가 되는 세 자리",
    "kind": "mixed",
    "legend_kinds": ["artery", "vein", "nerve"],
    "source": "10회차 §팔오금 구조물 · 손목굴 · 고샅관 · 정삭",
    "footer": [
        "팔오금은 가쪽→안쪽 **힘줄–동맥–신경(TAN)**, 위를 널힘줄이 덮는다.",
        "손목굴을 지나는 것은 **힘줄 9개 + 정중신경 1개**뿐 — 동맥도 자신경도 안 지난다.",
        "고샅관의 세 층은 배벽 세 근육에서 **순서대로** 받아 온다.",
    ],
    "root": _n("세 개의 자리", children=[
        _n("팔오금", "cubital fossa", "아래로 뒤집힌 삼각형", star=True, children=[
            _n("경계", "boundaries", star=True, children=[
                _n("위변", "sup. — 위관절융기 사이 가상선", star=True, terminal=True),
                _n("가쪽변", "lat. — 위팔노근", star=True, terminal=True),
                _n("안쪽변", "med. — 원엎침근", star=True, terminal=True),
                _n("바닥", "floor — 위팔근 + 손뒤침근", terminal=True),
                _n("지붕", "roof — 깊은근막 + **위팔두갈래근널힘줄**",
                   "널힘줄이 동맥·신경을 **덮어 보호**한다", star=True, terminal=True)]),
            _n("내용물 가쪽→안쪽 (TAN)", "contents", star=True, children=[
                _n("① 위팔두갈래근 힘줄", "biceps tendon", "→ 노뼈거친면",
                   star=True, terminal=True),
                _n("② 위팔동맥", "brachial a.", "힘줄 **안쪽** · 혈압 측정 자리",
                   kind="artery", star=True, terminal=True),
                _n("③ 정중신경", "median n.", "가장 **안쪽** · 원엎침근 두 갈래 사이로",
                   kind="nerve", star=True, terminal=True)]),
            _n("얕은층", "superficial", star=True, children=[
                _n("팔오금중간정맥", "median cubital v.", "정맥천자 — **널힘줄 위**",
                   kind="vein", star=True, terminal=True),
                _n("가쪽아래팔피부신경", "lat. antebrachial cutaneous n.",
                   "천자 시 다칠 수 있다", kind="nerve", star=True, terminal=True)]),
        ]),
        _n("손목굴", "carpal tunnel", "뼈 고랑 + 굽힘근지지띠가 만든 **닫힌 굴**",
           star=True, children=[
            _n("네 기둥", "four pillars", star=True, children=[
                _n("몸쪽 가쪽 — 손배뼈결절", "scaphoid tubercle", star=True, terminal=True),
                _n("몸쪽 안쪽 — 콩알뼈", "pisiform", star=True, terminal=True),
                _n("먼쪽 가쪽 — 큰마름뼈결절", "tubercle of trapezium",
                   star=True, terminal=True),
                _n("먼쪽 안쪽 — 갈고리뼈갈고리", "hook of hamate", star=True, terminal=True)]),
            _n("지나는 것 = 10개", "contents", "힘줄 9 + 신경 1", star=True, children=[
                _n("얕은손가락굽힘근 힘줄 4", "FDS ×4", star=True, terminal=True),
                _n("깊은손가락굽힘근 힘줄 4", "FDP ×4", star=True, terminal=True),
                _n("긴엄지굽힘근 힘줄 1", "FPL ×1", star=True, terminal=True),
                _n("정중신경", "median n.",
                   "**가장 얕고 노쪽** — 그래서 눌린다", kind="nerve", star=True,
                   terminal=True)]),
            _n("지나지 않는 것", "NOT in the tunnel",
               "자신경·자동맥(**자신경굴**) · 노동맥(코담배갑) · "
               "정중신경 **손바닥피부가지** · 긴손바닥근 힘줄", star=True, terminal=True),
        ]),
        _n("고샅관", "inguinal canal",
           "고샅인대와 나란한 4cm 통로 · **깊은고샅구멍 → 얕은고샅구멍**", star=True,
           children=[
            _n("네 벽", "walls", star=True, children=[
                _n("앞벽", "ant. — 배바깥빗근 널힘줄 (+가쪽 1/3 배속빗근)",
                   star=True, terminal=True),
                _n("뒤벽", "post. — **배가로근막** (+안쪽 1/3 고샅낫힘줄)",
                   "여기가 약하면 **직접고샅탈장**", star=True, terminal=True),
                _n("지붕", "roof — 배속빗근·배가로근의 활꼴 아래모서리",
                   star=True, terminal=True),
                _n("바닥", "floor — 고샅인대의 도랑 (+안쪽 오목인대)",
                   star=True, terminal=True)]),
            _n("두 구멍", "two rings", star=True, children=[
                _n("깊은고샅구멍", "deep inguinal ring",
                   "배가로근막의 구멍 · **아래배벽동맥 가쪽** = 가쪽고샅오목",
                   star=True, terminal=True),
                _n("얕은고샅구멍", "superficial inguinal ring",
                   "배바깥빗근 널힘줄의 틈 · 안쪽다리·가쪽다리·다리사이섬유",
                   star=True, terminal=True)]),
            _n("탈장 감별", "hernia", star=True, children=[
                _n("속고샅탈장", "indirect — 깊은구멍으로 · **동맥 가쪽** · 정삭 속",
                   star=True, terminal=True),
                _n("직접고샅탈장", "direct — 뒤벽(Hesselbach)으로 · **동맥 안쪽**",
                   star=True, terminal=True)]),
            _n("정삭 — 세 막 세 근육", "spermatic cord coverings", star=True, children=[
                _n("바깥정삭근막", "external spermatic fascia",
                   "← **배바깥빗근** 널힘줄", star=True, terminal=True),
                _n("고환올림근·근막", "cremaster m. & fascia",
                   "← **배속빗근**", star=True, terminal=True),
                _n("속정삭근막", "internal spermatic fascia",
                   "← **배가로근막**", star=True, terminal=True)]),
            _n("정삭 내용물", "cord contents", star=True, children=[
                _n("정관", "ductus deferens", "만지면 **질긴 실 같은** 느낌",
                   star=True, terminal=True),
                _n("고환동맥", "testicular a.", "배대동맥에서 직접",
                   kind="artery", star=True, terminal=True),
                _n("덩굴정맥얼기", "pampiniform plexus", kind="vein", star=True,
                   terminal=True),
                _n("음부넙다리신경 생식가지", "genital br.", "고환올림근",
                   kind="nerve", star=True, terminal=True)]),
            _n("여성", "in the female", "**자궁원인대** + 엉덩고샅신경",
               star=True, terminal=True),
        ]),
    ]),
},
# ── 11회차 (2026-09-21) 위팔 뒤칸·아래팔 뒤칸·손등 / 복막·위·지라·간·창자·이자 ────
"s11-nerve": {
    "title": "뒤칸의 신경과 배안의 자율신경",
    "en": "radial nerve in the posterior compartment & autonomic plexuses of the abdomen",
    "subtitle": "11회차 · 팔 뒤칸은 노신경 하나가 다 맡고, 배안은 얼기가 동맥을 타고 간다",
    "kind": "nerve",
    "source": "11회차 실습주제(위팔 뒤칸·아래팔 뒤칸·손등 / 복막·위·지라·간·작은창자·큰창자·샘창자·이자) + "
              "인제스트 섹션 a2-s11 §노신경 · §손뒤침근 · §손등표면 · §주변혈관관찰 · §위창자간막동맥",
    "footer": [
        "팔 뒤칸에는 신경이 **하나뿐이다** — 노신경. 앞칸의 정중·자처럼 나눠 갖지 않는다.",
        "노신경은 손뒤침근에서 **둘로 갈린다** — 깊은가지(뒤뼈사이, 운동)와 얕은가지(감각).",
        "배안의 자율신경은 길을 따로 내지 않는다 — **동맥을 감싸고 같은 이름으로** 따라간다.",
    ],
    "root": _n("11회차의 신경", children=[
        _n("노신경", "radial n.", "C5–T1 · 뒤다발의 끝가지 · **뒤칸 전체의 주인**",
           star=True, children=[
            _n("위팔 뒤칸 구간", "in the posterior compartment of the arm",
               "**깊은위팔동맥과 함께 노신경고랑**을 돌아 내려간다 — "
               "위팔뼈 몸통 골절에서 같이 다친다", star=True, children=[
                _n("위팔세갈래근 가지", "branches to triceps brachii",
                   "긴갈래·가쪽갈래·안쪽갈래를 **갈림 전에** 따로 받는다",
                   star=True, terminal=True),
                _n("팔꿈치근 가지", "branch to anconeus",
                   "안쪽갈래 가지가 이어진 것", terminal=True),
                _n("뒤아래팔피부신경", "post. antebrachial cutaneous n.",
                   "아래팔 뒤면 피부 — 감각만", star=True, terminal=True)]),
            _n("가쪽근육사이막 관통", "piercing the lateral intermuscular septum",
               "여기서 **앞칸으로 건너와** 위팔노근과 위팔근 사이에 눕는다",
               star=True, terminal=True),
            _n("갈림 전 가지", "before the split",
               "위팔노근 · 긴노쪽손목폄근 · (짧은노쪽손목폄근)",
               star=True, terminal=True),
            _n("깊은가지", "deep br. of radial n.",
               "**손뒤침근 두 층 사이(Frohse 활)를 뚫는다** — 뚫고 나오면 이름이 바뀐다",
               star=True, children=[
                _n("뒤뼈사이신경", "posterior interosseous n.",
                   "**순수 운동** · 뒤칸 깊은층 — 긴엄지벌림·짧은엄지폄·긴엄지폄·집게폄",
                   star=True, terminal=True),
                _n("손뒤침근·자쪽손목폄근·손가락폄근·새끼폄근", "to the superficial extensors",
                   "뚫기 **전후**로 얕은층 근육을 맡는다", star=True, terminal=True)]),
            _n("얕은가지", "superficial br. of radial n.",
               "**순수 감각** · 위팔노근 힘줄 **깊이**로 내려가다 먼쪽에서 피부로 나온다",
               star=True, children=[
                _n("손등가쪽 3.5손가락", "dorsal digital nn.",
                   "**손톱 바닥은 정중·자신경 몫** — 끝마디는 앞쪽 신경이 돌아 올라온다",
                   star=True, terminal=True),
                _n("해부코담배갑 위 피부", "over the anatomical snuffbox",
                   "피부밑에서 만져지는 자리 — 노뼈붓돌기 골절에서 다친다",
                   star=True, terminal=True)]),
        ]),
        _n("자신경 손등가지", "dorsal br. of ulnar n.",
           "자쪽손목굽힘근 **깊이로 빠져** 손등 안쪽 1.5손가락 — 손등의 나머지 절반",
           star=True, terminal=True),
        _n("배안의 자율신경얼기", "autonomic plexuses of the abdomen",
           "**동맥 이름을 그대로 물려받는다**", star=True, children=[
            _n("복강신경얼기", "celiac plexus",
               "복강동맥 뿌리를 감싼 **치밀한 얼기** · 큰·작은내장신경(T5–T12)이 들어온다",
               star=True, children=[
                _n("간얼기", "hepatic plexus", "고유간동맥을 따라 간문으로",
                   star=True, terminal=True),
                _n("위얼기·지라얼기", "gastric & splenic plexuses",
                   "왼위동맥·지라동맥을 따라", terminal=True)]),
            _n("위창자간막신경얼기", "superior mesenteric plexus",
               "위창자간막동맥 뿌리 · **중간창자(샘창자 중간~가로잘록창자 2/3)** 담당",
               star=True, terminal=True),
            _n("아래창자간막신경얼기", "inferior mesenteric plexus",
               "아래창자간막동맥 뿌리 · **뒤창자** 담당", star=True, terminal=True),
            _n("미주신경 앞·뒤줄기", "ant./post. vagal trunks",
               "식도구멍으로 들어와 **부교감** — 앞=왼미주, 뒤=오른미주",
               star=True, terminal=True)]),
    ]),
},

"s11-vessel": {
    "title": "뒤칸의 혈관과 배안 세 동맥·간문맥계",
    "en": "vessels of the posterior compartment & the three unpaired abdominal arteries",
    "subtitle": "11회차 · 배대동맥의 홀동맥 셋이 앞창자·중간창자·뒤창자를 나눠 먹는다",
    "kind": "mixed",
    "legend_kinds": ["artery", "vein"],
    "source": "11회차 인제스트 섹션 a2-s11 §주변혈관관찰 · §위의 혈관분포 · §지라 · "
              "§위창자간막동맥 · §아래창자간막동맥 · §이자 · §손등표면",
    "footer": [
        "홀동맥 셋 = **복강동맥(앞창자) · 위창자간막동맥(중간창자) · 아래창자간막동맥(뒤창자)**.",
        "세 동맥은 **가장자리동맥(Drummond)**과 이자샘창자활로 서로 이어진다 — 문합이 곧 샛길이다.",
        "정맥은 동맥을 따라가되 **심장이 아니라 간으로** 모인다 — 그것이 간문맥계다.",
    ],
    "root": _n("11회차의 혈관", children=[
        _n("깊은위팔동맥", "deep brachial a. (profunda brachii)",
           "위팔동맥의 첫 큰 가지 · **노신경과 함께 노신경고랑**",
           kind="artery", star=True, children=[
            _n("중간곁동맥·노쪽곁동맥", "middle & radial collateral aa.",
               "팔꿈치 둘레 문합에 참여", kind="artery", star=True, terminal=True)]),
        _n("온뼈사이동맥", "common interosseous a.",
           "자동맥에서 나와 곧 둘로 갈린다", kind="artery", star=True, children=[
            _n("뒤뼈사이동맥", "posterior interosseous a.",
               "뼈사이막 **위모서리를 넘어** 뒤칸으로 — 뒤뼈사이신경과 동행",
               kind="artery", star=True, terminal=True),
            _n("앞뼈사이동맥", "anterior interosseous a.",
               "뼈사이막 앞면 · 먼쪽에서 **뚫고 넘어와** 뒤칸 먼쪽을 먹인다",
               kind="artery", star=True, terminal=True)]),
        _n("노동맥 손등 구간", "radial a. in the snuffbox",
           "**해부코담배갑 바닥**을 지나 첫째등쪽뼈사이근을 뚫는다 → 깊은손바닥동맥활",
           kind="artery", star=True, children=[
            _n("손등동맥그물", "dorsal carpal arch",
               "등쪽손허리동맥 → 등쪽손가락동맥", kind="artery", star=True, terminal=True)]),
        _n("손등정맥그물", "dorsal venous network of the hand",
           "**노쪽 → 노쪽피부정맥 · 자쪽 → 자쪽피부정맥** — 정맥주사 자리",
           kind="vein", star=True, terminal=True),
        _n("복강동맥", "celiac trunk",
           "T12 · **가로막대동맥구멍 바로 아래** · 앞창자 — 세 가지로 갈린다",
           kind="artery", star=True, children=[
            _n("왼위동맥", "left gastric a.",
               "위작은굽이 · 식도가지를 낸다", kind="artery", star=True, terminal=True),
            _n("지라동맥", "splenic a.",
               "이자 위모서리를 **구불구불** 왼쪽으로 → 지라문", kind="artery", star=True,
               children=[
                _n("짧은위동맥", "short gastric aa.",
                   "위지라인대 속 · 위바닥", kind="artery", star=True, terminal=True),
                _n("왼위그물막동맥", "left gastroomental a.",
                   "위큰굽이 왼쪽", kind="artery", star=True, terminal=True),
                _n("이자가지", "pancreatic brr.", "큰이자동맥 등",
                   kind="artery", terminal=True)]),
            _n("온간동맥", "common hepatic a.", "오른쪽으로", kind="artery", star=True,
               children=[
                _n("고유간동맥", "proper hepatic a.",
                   "**간샘창자인대 속을 올라간다** — 간세동이의 동맥",
                   kind="artery", star=True, children=[
                    _n("오른간동맥 → 쓸개동맥", "right hepatic a. → cystic a.",
                       "**쓸개세모(Calot)** 안에서 나온다 — 쓸개절제술의 표지",
                       kind="artery", star=True, terminal=True),
                    _n("왼간동맥", "left hepatic a.", kind="artery", terminal=True)]),
                _n("위샘창자동맥", "gastroduodenal a.",
                   "샘창자 첫부분 **뒤로** 내려간다 — 뒤벽 궤양이 뚫으면 여기서 출혈",
                   kind="artery", star=True, children=[
                    _n("오른위그물막동맥", "right gastroomental a.",
                       "위큰굽이 오른쪽 → 왼위그물막동맥과 만난다",
                       kind="artery", star=True, terminal=True),
                    _n("위이자샘창자동맥", "superior pancreaticoduodenal a.",
                       "**아래이자샘창자동맥과 활을 이룬다**(복강↔위창자간막 문합)",
                       kind="artery", star=True, terminal=True)]),
                _n("오른위동맥", "right gastric a.",
                   "위작은굽이 오른쪽 → 왼위동맥과 만난다", kind="artery", star=True,
                   terminal=True)]),
        ]),
        _n("위창자간막동맥", "superior mesenteric a.",
           "L1 · **이자목 뒤 → 갈고리돌기 앞** · 중간창자", kind="artery", star=True,
           children=[
            _n("아래이자샘창자동맥", "inferior pancreaticoduodenal a.",
               "첫 가지 · 위쪽 짝과 활을 이룬다", kind="artery", star=True, terminal=True),
            _n("빈창자·돌창자동맥", "jejunal & ileal aa.",
               "**왼쪽으로** 15~18개 · 활(arcade)을 만들고 **곧은동맥**으로 끝난다",
               kind="artery", star=True, children=[
                _n("곧은동맥", "vasa recta",
                   "빈창자는 **활 적고 곧은동맥 길다**, 돌창자는 반대 — 감별 포인트",
                   kind="artery", star=True, terminal=True)]),
            _n("중간잘록창자동맥", "middle colic a.",
               "**오른쪽으로** · 가로잘록창자간막 속", kind="artery", star=True, terminal=True),
            _n("오른잘록창자동맥", "right colic a.", "오름잘록창자",
               kind="artery", star=True, terminal=True),
            _n("돌잘록창자동맥", "ileocolic a.", "끝가지", kind="artery", star=True,
               children=[
                _n("막창자꼬리동맥", "appendicular a.",
                   "**막창자꼬리간막 속** · 끝동맥이라 막히면 괴사",
                   kind="artery", star=True, terminal=True)]),
        ]),
        _n("아래창자간막동맥", "inferior mesenteric a.",
           "L3 · 뒤창자(가로잘록창자 왼쪽 1/3~곧창자 위)", kind="artery", star=True,
           children=[
            _n("왼잘록창자동맥", "left colic a.",
               "내림잘록창자 · 중간잘록창자동맥과 **가장자리동맥으로 이어진다**",
               kind="artery", star=True, terminal=True),
            _n("구불잘록창자가지", "sigmoid brr.", kind="artery", star=True, terminal=True),
            _n("위곧창자동맥", "superior rectal a.", "끝가지", kind="artery", terminal=True),
            _n("가장자리동맥", "marginal a. of Drummond",
               "잘록창자 안쪽모서리를 따라 **위·아래창자간막동맥을 잇는 고리**",
               kind="artery", star=True, terminal=True)]),
        _n("간문맥계", "hepatic portal system",
           "**모세혈관 → 정맥 → 간에서 다시 모세혈관** — 두 번 거른다",
           kind="vein", star=True, children=[
            _n("간문맥", "hepatic portal v.",
               "**이자목 뒤에서 지라정맥 + 위창자간막정맥**이 합쳐져 생긴다",
               kind="vein", star=True, children=[
                _n("위창자간막정맥", "superior mesenteric v.",
                   "동맥 **오른쪽**에서 나란히", kind="vein", star=True, terminal=True),
                _n("지라정맥", "splenic v.",
                   "이자 **뒤면**을 따라 오른쪽으로 · **아래창자간막정맥을 받는다**",
                   kind="vein", star=True, terminal=True),
                _n("아래창자간막정맥", "inferior mesenteric v.",
                   "동맥과 길이 다르다 — 지라정맥(또는 합류점)으로 올라간다",
                   kind="vein", star=True, terminal=True),
                _n("간샘창자인대 속 배열", "in the hepatoduodenal ligament",
                   "**문맥이 가장 뒤**, 앞에 왼쪽=동맥 · 오른쪽=온쓸개관",
                   kind="vein", star=True, terminal=True)]),
            _n("문맥–대정맥 연결", "portosystemic anastomoses",
               "막히면 굵어지는 네 자리(응용과제)", kind="vein", star=True, children=[
                _n("식도정맥", "esophageal — 왼위정맥 ↔ 홀정맥",
                   "**식도정맥류**", kind="vein", star=True, terminal=True),
                _n("배꼽옆정맥", "paraumbilical ↔ 배벽정맥",
                   "**caput medusae**", kind="vein", star=True, terminal=True),
                _n("곧창자정맥", "rectal — 위 ↔ 중간·아래곧창자정맥",
                   "치질", kind="vein", star=True, terminal=True),
                _n("복막뒤 정맥", "retroperitoneal (Retzius)",
                   "잘록창자·샘창자 뒤면", kind="vein", terminal=True)]),
        ]),
    ]),
},

"s11-bundle": {
    "title": "함께 지나는 것 — 폄근지지띠 · 코담배갑 · 간세동이",
    "en": "retinaculum compartments, snuffbox & portal triad",
    "subtitle": "11회차 · 칸과 경계가 그대로 태깅 문제가 되는 다섯 자리",
    "kind": "mixed",
    "legend_kinds": ["artery", "vein", "nerve"],
    "source": "11회차 인제스트 섹션 a2-s11 §폄근지지띠 섬유칸 · §손등표면 · §간의 겉모습 · "
              "§간의 적출 · §그물막주머니 · §이자관",
    "footer": [
        "폄근지지띠 밑은 **여섯 칸** — 노쪽 1번부터 자쪽 6번까지 번호가 곧 답이다.",
        "간세동이는 **문맥이 뒤, 앞에 동맥(왼)·쓸개관(오른)** — 세 개의 위치가 문제로 나온다.",
        "그물막구멍은 **앞이 간샘창자인대** — 손가락을 넣어 Pringle법으로 잡는 자리다.",
    ],
    "root": _n("다섯 자리", children=[
        _n("폄근지지띠 여섯 칸", "six compartments under the extensor retinaculum",
           "노쪽 → 자쪽 순서", star=True, children=[
            _n("1칸", "APL + EPB",
               "긴엄지벌림근 · 짧은엄지폄근 — **de Quervain 힘줄윤활막염**",
               star=True, terminal=True),
            _n("2칸", "ECRL + ECRB",
               "긴·짧은노쪽손목폄근 — 코담배갑 **바닥**을 이룬다", star=True, terminal=True),
            _n("3칸", "EPL",
               "긴엄지폄근 — **리스터결절을 도르래처럼 돌아** 가쪽으로 꺾인다",
               star=True, terminal=True),
            _n("4칸", "ED + EI",
               "손가락폄근 · 집게폄근 — **뒤뼈사이신경이 이 칸 바닥으로** 지난다",
               star=True, terminal=True),
            _n("5칸", "EDM", "새끼폄근 — 먼쪽노자관절 바로 위", star=True, terminal=True),
            _n("6칸", "ECU",
               "자쪽손목폄근 — 자뼈머리의 고랑 속", star=True, terminal=True)]),
        _n("해부코담배갑", "anatomical snuffbox", "엄지를 폈을 때 생기는 삼각 오목",
           star=True, children=[
            _n("경계", "boundaries", star=True, children=[
                _n("노쪽(앞)벽", "ant. — 긴엄지벌림근 + 짧은엄지폄근 힘줄 (1칸)",
                   star=True, terminal=True),
                _n("자쪽(뒤)벽", "post. — 긴엄지폄근 힘줄 (3칸)", star=True, terminal=True),
                _n("바닥", "floor — **손배뼈 + 큰마름뼈**",
                   "여기를 누르면 아픈 것이 **손배뼈 골절**", star=True, terminal=True),
                _n("몸쪽 꼭짓점", "prox. — 노뼈붓돌기", terminal=True)]),
            _n("내용물·지나는 것", "contents", star=True, children=[
                _n("노동맥", "radial a.",
                   "**바닥 위를 가로지른다** — 맥박이 만져진다",
                   kind="artery", star=True, terminal=True),
                _n("노신경 얕은가지", "superficial br. of radial n.",
                   "**지붕(피부밑)** 위를 지난다 — 안이 아니다",
                   kind="nerve", star=True, terminal=True),
                _n("노쪽피부정맥 시작", "cephalic v.",
                   "손등정맥그물의 노쪽에서 올라온다", kind="vein", star=True,
                   terminal=True)]),
        ]),
        _n("간세동이", "portal triad", "**간샘창자인대** 속 · 간문으로 들어간다",
           star=True, children=[
            _n("간문맥", "hepatic portal v.",
               "**가장 뒤·가장 굵다** · 간 혈류의 70~75%", kind="vein", star=True,
               terminal=True),
            _n("고유간동맥", "proper hepatic a.",
               "앞쪽 **왼쪽**", kind="artery", star=True, terminal=True),
            _n("온쓸개관", "common bile duct",
               "앞쪽 **오른쪽** · 온간관 + 쓸개주머니관이 합쳐진 것",
               star=True, terminal=True),
            _n("쓸개세모", "cystic (Calot) triangle",
               "쓸개주머니관 · 온간관 · 간아래면이 이루는 삼각 — **쓸개동맥**이 그 안",
               star=True, terminal=True),
            _n("Pringle법", "Pringle manoeuvre",
               "그물막구멍에 손가락을 넣어 **인대 전체를 집는다** → 간 출혈 일시 차단",
               star=True, terminal=True)]),
        _n("그물막구멍", "omental foramen (of Winslow)",
           "큰복막안 ↔ 그물막주머니를 잇는 유일한 문", star=True, children=[
            _n("앞", "ant. — **간샘창자인대**(간세동이)", star=True, terminal=True),
            _n("뒤", "post. — **아래대정맥**", star=True, terminal=True),
            _n("위", "sup. — 간 꼬리엽", star=True, terminal=True),
            _n("아래", "inf. — 샘창자 첫부분", star=True, terminal=True)]),
        _n("쓸개이자관팽대", "hepatopancreatic ampulla (of Vater)",
           "온쓸개관 + 이자관이 합쳐져 **큰샘창자유두**로 열린다", star=True, children=[
            _n("큰샘창자유두", "major duodenal papilla",
               "샘창자 **내림부분 뒤안쪽벽** · Oddi조임근", star=True, terminal=True),
            _n("작은샘창자유두", "minor duodenal papilla",
               "**덧이자관**이 따로 열린다 · 큰유두보다 몸쪽·위", star=True, terminal=True)]),
    ]),
},

# ── 12회차 (2026-09-28) 척주·척수막 / 샅·항문삼각·비뇨생식삼각·바깥생식기관 ──────
"s12-nerve": {
    "title": "척수신경의 시작과 샅의 신경 — 음부신경",
    "en": "spinal nerve roots & the pudendal nerve",
    "subtitle": "12회차 · 척주관에서 신경이 태어나고, 샅에서는 음부신경 하나가 거의 전부를 맡는다",
    "kind": "nerve",
    "source": "12회차 실습주제(척주·척수막 / 샅·항문삼각·비뇨생식삼각·남녀 바깥생식기관) + "
              "인제스트 섹션 a2-s13 §척주관 관찰 · §척수막 · §척수 · §궁둥항문오목의 혈관과 신경 · "
              "§얕은샅공간 · §얕은샅공간2",
    "footer": [
        "척수는 **L1–L2에서 끝나지만 척주관은 계속 간다** — 그 길이차가 허리천자를 가능하게 한다.",
        "샅은 **음부신경(S2–S4) 하나**가 거의 전부 — 가지 셋의 이름이 그대로 답이다.",
        "음부신경은 **골반을 한 번 나갔다 다시 들어온다** — 궁둥구멍 두 개를 연달아 쓴다.",
    ],
    "root": _n("12회차의 신경", children=[
        _n("척수신경의 시작", "roots of the spinal nerve", "척주관을 열면 보이는 순서",
           star=True, children=[
            _n("앞뿌리", "ventral root", "운동 — 척수 앞가쪽고랑에서 여러 뿌리실로 나온다",
               star=True, terminal=True),
            _n("뒤뿌리", "dorsal root", "감각 — 뒤가쪽고랑으로 들어간다", star=True, children=[
                _n("척수신경절", "spinal ganglion",
                   "**척추사이구멍 안**에 부푼 덩이 — 거짓홑극신경세포의 집",
                   star=True, terminal=True)]),
            _n("척수신경줄기", "trunk of spinal n.",
               "앞뿌리+뒤뿌리가 **척추사이구멍에서** 합쳐진 짧은 줄기", star=True, children=[
                _n("앞가지", "ventral ramus", "굵다 · 얼기를 만든다", star=True, terminal=True),
                _n("뒤가지", "dorsal ramus", "가늘다 · 등 깊은층과 등 피부",
                   star=True, terminal=True)]),
            _n("말총", "cauda equina",
               "**척수원뿔(L1–L2) 아래** 거미막밑공간을 채운 뿌리 다발 — 허리천자 바늘이 밀어낸다",
               star=True, terminal=True),
            _n("종말끈", "filum terminale",
               "연막이 이어진 실 · 속(경막 안)과 겉(꼬리뼈에 붙음)으로 나뉜다",
               star=True, terminal=True),
            _n("치아인대", "denticulate lig.",
               "연막이 **앞뒤뿌리 사이에서** 톱니처럼 뻗어 경막에 붙는다 — 척수를 가운데 매단다",
               star=True, terminal=True)]),
        _n("음부신경", "pudendal n.", "**S2–S4 앞가지** · 샅의 주인",
           star=True, children=[
            _n("골반을 나가는 길", "course out of and back into the pelvis",
               "**큰궁둥구멍(궁둥구멍근 아래)으로 나갔다가 엉치가시인대를 돌아 "
               "작은궁둥구멍으로 다시 들어온다**", star=True, children=[
                _n("엉치가시인대 뒤", "behind the sacrospinous lig.",
                   "**음부신경 차단의 표지 — 궁둥뼈가시**", star=True, terminal=True),
                _n("음부신경관", "pudendal canal (Alcock)",
                   "속폐쇄근막이 만든 관 · **신경과 속음부동·정맥이 함께** 지난다",
                   star=True, terminal=True)]),
            _n("아래곧창자신경", "inferior anal (rectal) n.",
               "관에서 **가장 먼저** 갈라져 궁둥항문오목을 가로지른다",
               star=True, children=[
                _n("바깥항문조임근", "ext. anal sphincter m.", "운동",
                   star=True, terminal=True),
                _n("항문 주위 피부", "perianal skin", "감각", terminal=True)]),
            _n("샅신경", "perineal n.", "관의 **아래쪽 끝가지** — 얕은샅공간으로",
               star=True, children=[
                _n("깊은(근육)가지", "deep br.",
                   "얕은샅가로근 · 궁둥해면체근 · 망울해면체근 + **바깥요도조임근**",
                   star=True, terminal=True),
                _n("뒤음낭신경 / 뒤음순신경", "post. scrotal / labial nn.",
                   "남·녀 바깥생식기 피부 감각", star=True, terminal=True)]),
            _n("음경등신경 / 음핵등신경", "dorsal n. of penis / of clitoris",
               "관의 **위쪽 끝가지** · 깊은샅공간을 지나 샅막을 뚫고 등쪽으로",
               star=True, children=[
                _n("음경·음핵 귀두 감각", "glans", "**성감각의 주 경로**",
                   star=True, terminal=True)]),
        ]),
        _n("샅을 함께 맡는 곁들", "other nerves reaching the perineum",
           "음부신경만으로 다 덮이지 않는 가장자리", children=[
            _n("엉덩샅굴신경", "ilioinguinal n.", "L1 — 음낭·대음순 **앞쪽** 피부",
               star=True, terminal=True),
            _n("넓적다리뒤피부신경 샅가지", "perineal br. of post. femoral cutaneous n.",
               "S1–S3 — 샅의 **가쪽** 피부", terminal=True),
            _n("항문꼬리신경", "anococcygeal nn.", "S4–Co — 꼬리뼈 주위 피부",
               terminal=True)]),
    ]),
},

"s12-vessel": {
    "title": "척주관의 정맥얼기와 샅의 동맥 — 속음부동맥",
    "en": "vertebral venous plexuses & the internal pudendal artery",
    "subtitle": "12회차 · 경막바깥공간은 정맥얼기로 차 있고, 샅의 피는 속엉덩동맥 앞가지에서 온다",
    "kind": "mixed",
    "legend_kinds": ["artery", "vein"],
    "source": "12회차 인제스트 섹션 a2-s13 §척주관열기 · §궁둥항문오목의 혈관과 신경 · "
              "§깊은샅공간 · §음경",
    "footer": [
        "속척주정맥얼기는 **판막이 없다** — 그래서 배·골반의 암이 척주·머리뼈로 곧장 퍼진다.",
        "샅의 동맥은 **속음부동맥 하나**가 음부신경과 같은 관을 타고 들어와 나눠 준다.",
        "음경등정맥은 **깊은 것과 얕은 것의 행선지가 다르다** — 깊은쪽이 전립샘정맥얼기로 간다.",
    ],
    "root": _n("12회차의 혈관", children=[
        _n("척주정맥얼기", "vertebral venous plexuses (Batson)",
           "**판막이 없는 정맥 그물** · 배안 압력이 오르면 피가 이쪽으로 밀린다",
           kind="vein", star=True, children=[
            _n("속척주정맥얼기", "internal vertebral venous plexus",
               "**경막바깥공간을 채운다** — 고리판절제술에서 출혈하는 자리",
               kind="vein", star=True, children=[
                _n("앞얼기", "ant. internal plexus",
                   "뒤세로인대 양옆 · 척추뼈몸통의 **바닥정맥**을 받는다",
                   kind="vein", star=True, terminal=True),
                _n("뒤얼기", "post. internal plexus",
                   "고리판 앞면 — 바늘이 먼저 만나는 쪽", kind="vein", terminal=True)]),
            _n("바깥척주정맥얼기", "ext. vertebral venous plexus",
               "척추뼈 겉면 · 홀정맥계·허리정맥과 이어진다",
               kind="vein", star=True, terminal=True),
            _n("전이 경로", "route of metastasis",
               "**전립샘암 → 허리뼈·골반**, 유방암 → 척주 — 허파를 거치지 않는다",
               kind="vein", star=True, terminal=True)]),
        _n("속엉덩동맥 앞가지", "ant. division of internal iliac a.",
           "샅으로 가는 피의 출처", kind="artery", star=True, children=[
            _n("속음부동맥", "internal pudendal a.",
               "**음부신경과 같은 길** — 큰궁둥구멍으로 나갔다 작은궁둥구멍으로 되들어와 "
               "음부신경관을 지난다", kind="artery", star=True, children=[
                _n("아래곧창자동맥", "inferior anal (rectal) a.",
                   "궁둥항문오목의 지방덩이를 가로질러 항문관으로",
                   kind="artery", star=True, terminal=True),
                _n("샅동맥", "perineal a.",
                   "얕은샅공간 — **뒤음낭동맥 / 뒤음순동맥**으로 끝난다",
                   kind="artery", star=True, terminal=True),
                _n("음경망울동맥 / 질어귀망울동맥", "a. of bulb",
                   "깊은샅공간에서 **망울(요도해면체·질어귀망울)** 속으로",
                   kind="artery", star=True, terminal=True),
                _n("깊은음경동맥 / 깊은음핵동맥", "deep a. of penis / clitoris",
                   "**해면체 속 나선동맥** — 발기의 주 동맥",
                   kind="artery", star=True, terminal=True),
                _n("음경등동맥 / 음핵등동맥", "dorsal a. of penis / clitoris",
                   "샅막을 뚫고 등쪽으로 · **음경등신경과 나란히**",
                   kind="artery", star=True, terminal=True)]),
            _n("아래방광동맥 / 질동맥", "inferior vesical / vaginal a.",
               "깊은샅공간 위쪽 기관으로 — 13회차와 이어진다",
               kind="artery", terminal=True)]),
        _n("바깥음부동맥", "ext. pudendal aa.",
           "**넓적다리동맥**에서 나와 음낭·대음순 **앞쪽**을 맡는다 — 속음부와 짝",
           kind="artery", star=True, terminal=True),
        _n("음경의 정맥 — 둘의 행선지가 다르다", "veins of the penis",
           kind="vein", star=True, children=[
            _n("얕은음경등정맥", "superficial dorsal v. of penis",
               "**얕은근막 속** → 바깥음부정맥 → 큰두렁정맥",
               kind="vein", star=True, terminal=True),
            _n("깊은음경등정맥", "deep dorsal v. of penis",
               "**깊은근막 밑·두 동맥 사이 한 줄** → 샅막과 아래두덩인대 사이로 들어가 "
               "**전립샘정맥얼기**", kind="vein", star=True, terminal=True)]),
    ]),
},

"s12-bundle": {
    "title": "함께 지나는 것 — 척주관의 세 공간 · 음부신경관 · 두 샅주머니",
    "en": "vertebral canal, pudendal canal & perineal pouches",
    "subtitle": "12회차 · 막과 근막이 만든 '공간'의 경계가 그대로 태깅 문제다",
    "kind": "mixed",
    "legend_kinds": ["artery", "vein", "nerve"],
    "source": "12회차 인제스트 섹션 a2-s13 §척주관열기 · §척주관 관찰 · §척수막 · §샅의 경계 · "
              "§궁둥항문오목 · §얕은샅공간 · §깊은샅공간 + SESSION_DETAILS 응용과제"
              "(척주관·척수 길이차와 허리천자 / 골반바닥손상·episiotomy)",
    "footer": [
        "허리천자 바늘이 뚫는 순서는 **인대 셋 → 경막바깥공간 → 경막·거미막 → 거미막밑공간**이다.",
        "샅주머니를 가르는 것은 **샅막 한 장** — 위가 깊은주머니, 아래가 얕은주머니다.",
        "샅중심체는 **여러 근육이 모이는 매듭** — 여기가 찢어지면 골반바닥이 함께 무너진다.",
    ],
    "root": _n("세 자리", children=[
        _n("척주관의 층과 공간", "layers of the vertebral canal",
           "**뒤에서 바늘이 들어가는 순서대로**", star=True, children=[
            _n("가시끝인대", "supraspinous lig.", "가시돌기 끝을 잇는다 — 맨 처음",
               star=True, terminal=True),
            _n("가시사이인대", "interspinous lig.", "가시돌기 사이", star=True, terminal=True),
            _n("황색인대", "ligamenta flava",
               "**탄력섬유라 노랗다** · 고리판 사이 — 뚫을 때 **저항이 갑자기 사라진다**",
               star=True, terminal=True),
            _n("경막바깥공간", "epidural space",
               "**지방 + 속척주정맥얼기** — 경막바깥마취 자리", kind="vein",
               star=True, terminal=True),
            _n("척수경막·거미막", "spinal dura & arachnoid mater",
               "둘이 맞붙어 있다 · 사이의 **경막밑공간은 잠재공간**", star=True, terminal=True),
            _n("거미막밑공간", "subarachnoid space",
               "**뇌척수액** · 여기서 액을 뽑는다 — 아래로 **S2까지** 내려간다",
               star=True, terminal=True),
            _n("척수연막", "spinal pia mater",
               "척수에 밀착 · 치아인대와 종말끈이 여기서 나온다", terminal=True),
            _n("찌르는 높이", "level of puncture",
               "**L3–L4 또는 L4–L5(야코비선)** — 척수는 L1–L2에서 끝나므로 말총만 밀린다",
               star=True, terminal=True)]),
        _n("음부신경관", "pudendal canal (Alcock's canal)",
           "궁둥항문오목 **가쪽벽의 속폐쇄근막** 속 통로", star=True, children=[
            _n("음부신경", "pudendal n.", "S2–S4", kind="nerve", star=True, terminal=True),
            _n("속음부동맥", "internal pudendal a.", kind="artery", star=True, terminal=True),
            _n("속음부정맥", "internal pudendal v.", kind="vein", terminal=True),
            _n("들어오는 자리", "entrance",
               "**작은궁둥구멍** — 엉치가시인대를 돌아 들어온다", star=True, terminal=True)]),
        _n("궁둥항문오목", "ischioanal fossa",
           "항문 양옆의 **쐐기 모양 지방 공간** — 항문이 벌어질 자리를 비워 둔다",
           star=True, children=[
            _n("안쪽벽", "medial — 골반가로막(항문올림근) + 바깥항문조임근",
               star=True, terminal=True),
            _n("가쪽벽", "lateral — 궁둥뼈 + **속폐쇄근·속폐쇄근막**(음부신경관)",
               star=True, terminal=True),
            _n("뒤", "post. — 엉치결절인대 + 큰볼기근", star=True, terminal=True),
            _n("내용물", "contents — 지방덩이 · **아래곧창자 혈관·신경**",
               "감염이 고이면 **항문주위농양** → 말굽고름집으로 반대쪽까지",
               kind="nerve", star=True, terminal=True)]),
        _n("샅의 두 주머니", "the two perineal pouches",
           "**샅막(perineal membrane) 한 장**이 위아래를 가른다", star=True, children=[
            _n("얕은샅공간", "superficial perineal pouch",
               "샅막 **아래** · 지붕=샅막, 바닥=Colles근막", star=True, children=[
                _n("얕은샅가로근", "superficial transverse perineal m.",
                   "샅중심체를 가로로 잡아 준다", star=True, terminal=True),
                _n("궁둥해면체근", "ischiocavernosus m.",
                   "**음경다리·음핵다리**를 덮는다 — 정맥 유출을 막아 발기 유지",
                   star=True, terminal=True),
                _n("망울해면체근", "bulbospongiosus m.",
                   "남=음경망울을 덮어 **요도를 비운다** / 여=질어귀망울을 덮고 질구멍을 좁힌다",
                   star=True, terminal=True),
                _n("발기조직 뿌리", "roots of erectile tissue",
                   "음경해면체(다리) · 요도해면체(망울) / 질어귀망울",
                   star=True, terminal=True)]),
            _n("깊은샅공간", "deep perineal pouch",
               "샅막 **위** · 골반가로막 **아래**", star=True, children=[
                _n("바깥요도조임근", "ext. urethral sphincter m.",
                   "**맘대로근** — 요자제의 주역", star=True, terminal=True),
                _n("깊은샅가로근", "deep transverse perineal m.",
                   "샅가로인대와 함께 샅막을 보강", star=True, terminal=True),
                _n("남자요도 막부분", "membranous urethra",
                   "요도에서 **가장 짧고 가장 잘 찢어지는** 부분", star=True, terminal=True),
                _n("망울요도샘", "bulbourethral gland (Cowper)",
                   "**남자만** · 깊은주머니에 있지만 **관은 얕은주머니의 요도해면체로** 열린다",
                   star=True, terminal=True),
                _n("음경등신경·속음부동맥", "dorsal n. & internal pudendal a.",
                   "주머니를 지나 샅막을 뚫고 등쪽으로", kind="nerve", star=True,
                   terminal=True)]),
        ]),
        _n("샅중심체", "perineal body",
           "**항문과 요도사이의 섬유근육 매듭** — 두 삼각의 꼭짓점이 만나는 자리",
           star=True, children=[
            _n("모이는 근육", "converging muscles",
               "바깥항문조임근 · 얕은·깊은샅가로근 · 망울해면체근 · 항문올림근 · "
               "바깥요도조임근 일부", star=True, terminal=True),
            _n("episiotomy (응용과제)", "episiotomy",
               "**안쪽곁(median)** 절개는 아물기 좋지만 **샅중심체·항문조임근까지 찢어질** 위험, "
               "**중간가쪽(mediolateral)** 절개는 그 위험을 피한다", star=True, terminal=True)]),
    ]),
},
}
