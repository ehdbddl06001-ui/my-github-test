"""
TrialMatch_Colab.ipynb 생성기.

server.py 와 templates/index.html 을 읽어, Colab 에 업로드하면 셀 실행만으로
동작하는 자기완결형 노트북을 만든다.

사용:  python build_notebook.py   ->  TrialMatch_Colab.ipynb
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def readfile(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src if isinstance(src, list) else src.splitlines(keepends=True)}


def md(src):
    return {"cell_type": "markdown", "metadata": {},
            "source": src if isinstance(src, list) else src.splitlines(keepends=True)}


def writefile_cell(path, content):
    return code([f"%%writefile {path}\n"] + content.splitlines(keepends=True))


cells = [
    md("""# TrialMatch — 임상시험 연결 검색 (Gemini + ClinicalTrials.gov)

치료 선택지가 소진된 환자가 '자기 상황'을 검색창에 적으면 → **현재 모집 중인 실제 임상시험**을
ClinicalTrials.gov 에서 조회하고, Gemini 가 선정기준과 대조해 적합도를 매겨 연결한다.

**흐름**: ⓪초기화 → ①설치 → ②파일 기록 → ③Gemini 키 입력 → ④서버 실행(cloudflared URL).

> ⚠️ 임상시험 정보는 공개 등록 데이터(모집중)만 조회합니다. 적합도 점수는 Gemini의 참고
> 추정치이며, 최종 참여 적격 여부·연락은 각 실시기관의 절차를 따릅니다. 본 도구는 환자를
> 직접 모집·중개하지 않습니다.

> 🔴 **다른 앱(OncoReg)과 안 섞이게** — 이 앱은 전용 폴더(`trialmatch/`), 전용 모듈명
> (`trialmatch_app`), 전용 포트(8001)를 씁니다. 그래도 한 런타임에서 여러 앱을 돌렸다면
> **런타임 → 세션 다시 시작** 후 이 노트북만 실행하는 게 가장 확실합니다.
"""),
    md("## 0) 초기화 — 이전에 돌린 다른 앱의 캐시/포트 정리"),
    code("""import sys
for _m in ['server', 'oncoreg_app', 'trialmatch_app']:
    sys.modules.pop(_m, None)
print('모듈 캐시 정리 완료. (포트가 이미 사용 중이면 런타임 다시 시작을 권장)')
"""),
    md("## 1) 패키지 설치"),
    code("!pip -q install google-genai flask flask-cors flask-cloudflared pydantic\n"),
    md("## 2) 백엔드/프론트 파일 기록 (전용 폴더 `trialmatch/`)"),
    code("import os; os.makedirs('trialmatch/templates', exist_ok=True); print('trialmatch/ 준비 완료')\n"),
    writefile_cell("trialmatch/trialmatch_app.py", readfile("server.py")),
    writefile_cell("trialmatch/templates/index.html", readfile(os.path.join("templates", "index.html"))),
    md("""## 3) Gemini API 키 입력
키 발급: <https://aistudio.google.com/app/apikey>  (왼쪽 🔑 보안 비밀에 `GEMINI_API_KEY` 저장도 가능)"""),
    code("""import os
key = None
try:
    from google.colab import userdata
    key = userdata.get('GEMINI_API_KEY')
except Exception:
    pass
if not key:
    import getpass
    key = getpass.getpass('Gemini API Key 를 붙여넣고 Enter: ')
os.environ['GEMINI_API_KEY'] = key.strip()
os.environ.setdefault('GEMINI_MODEL', 'gemini-2.5-flash')

# ClinicalTrials.gov 연결 확인 (Colab 은 외부망이 열려 있어 정상 조회됨)
import urllib.request, json
try:
    u = "https://clinicaltrials.gov/api/v2/studies?query.cond=pulmonary%20arterial%20hypertension&filter.overallStatus=RECRUITING&pageSize=1&format=json"
    d = json.loads(urllib.request.urlopen(u, timeout=20).read())
    print('✅ ClinicalTrials.gov 연결 OK · 예시 조회 건수:', len(d.get('studies', [])))
except Exception as e:
    print('⚠️ CT.gov 조회 실패(표본 데이터로 대체됨):', e)
print('모델:', os.environ['GEMINI_MODEL'])
"""),
    md("""## 4) 서버 실행 → 공개 URL

출력되는 `https://….trycloudflare.com` 주소를 **새 탭에서 열면** 이 앱(TrialMatch) 검색창이 뜬다.
이 셀은 서버라 **계속 실행 상태로 둔다**(중지: ⏹️)."""),
    code("""import sys
sys.path.insert(0, 'trialmatch')
sys.modules.pop('trialmatch_app', None)
from trialmatch_app import create_app
from flask_cloudflared import run_with_cloudflared

app = create_app()
print('>>> 실행 중인 앱: TrialMatch (trialmatch_app, port 8001)')
run_with_cloudflared(app)
app.run(port=8001)
"""),
    md("### (대안) cloudflared 가 안 될 때 — Colab 내장 프록시"),
    code("""import sys, threading
sys.path.insert(0, 'trialmatch')
sys.modules.pop('trialmatch_app', None)
from trialmatch_app import create_app
app = create_app()
threading.Thread(target=lambda: app.run(port=8001, use_reloader=False), daemon=True).start()
from google.colab.output import serve_kernel_port_as_window
serve_kernel_port_as_window(8001)
"""),
]

nb = {"cells": cells,
      "metadata": {"colab": {"provenance": []},
                   "kernelspec": {"display_name": "Python 3", "name": "python3"},
                   "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 5}

out = os.path.join(HERE, "TrialMatch_Colab.ipynb")
with open(out, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("wrote", out, "cells:", len(cells))
