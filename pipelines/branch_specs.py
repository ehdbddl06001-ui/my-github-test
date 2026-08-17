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
}
