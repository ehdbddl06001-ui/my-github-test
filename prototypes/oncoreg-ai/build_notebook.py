"""
OncoReg_Colab.ipynb 생성기.

server.py 와 templates/index.html 을 읽어, Colab 에 그대로 업로드하면 되는
'자기완결형' 노트북을 만든다. (노트북이 셀 실행만으로 파일을 다시 써 내려간다)

사용:  python build_notebook.py   ->  OncoReg_Colab.ipynb 생성
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
    # %%writefile 매직은 파이썬 문자열 escape 가 필요 없다(셀 원문을 그대로 파일로 씀).
    header = f"%%writefile {path}\n"
    return code([header] + content.splitlines(keepends=True))


server_src = readfile("server.py")
html_src = readfile(os.path.join("templates", "index.html"))

cells = [
    md("""# OncoReg AI — Gemini 연동 실행 노트북

허가초과 근거 문서 생성 · 임상시험 적격성 검토 프로토타입을 **내 Gemini API 키**로 실제 동작시킨다.

**흐름**: ⓪초기화 → ①설치 → ②파일 기록 → ③Gemini 키 입력 → ④서버 실행(cloudflared URL).

> ⚠️ 문헌/수치/임상시험은 Gemini가 생성한 초안이라 실제 출판물과 다를 수 있습니다. 인용·제출 전 반드시 원문 대조·전문가 검증이 필요합니다.

> 🔴 **다른 앱(TrialMatch)과 안 섞이게** — 이 앱은 전용 폴더(`oncoreg_ai/`), 전용 모듈명
> (`oncoreg_app`), 전용 포트(8000)를 씁니다. 그래도 한 런타임에서 여러 앱을 돌렸다면
> **런타임 → 세션 다시 시작** 후 이 노트북만 위에서부터 실행하는 게 가장 확실합니다.
"""),
    md("## 0) 초기화 — 이전에 돌린 다른 앱의 캐시/포트 정리"),
    code("""# 같은 런타임에서 다른 앱을 돌렸다면, 파이썬이 캐시한 옛 모듈이 그대로 다시 뜨는 걸 막는다.
import sys
for _m in ['server', 'oncoreg_app', 'trialmatch_app']:
    sys.modules.pop(_m, None)
print('모듈 캐시 정리 완료. (포트가 이미 사용 중이면 런타임 다시 시작을 권장)')
"""),
    md("## 1) 패키지 설치"),
    code("!pip -q install google-genai flask flask-cors flask-cloudflared pydantic\n"),
    md("## 2) 백엔드/프론트 파일 기록 (전용 폴더 `oncoreg_ai/`)"),
    code("import os; os.makedirs('oncoreg_ai/templates', exist_ok=True); print('oncoreg_ai/ 준비 완료')\n"),
    writefile_cell("oncoreg_ai/oncoreg_app.py", server_src),
    writefile_cell("oncoreg_ai/templates/index.html", html_src),
    md("""## 3) Gemini API 키 입력

키 발급: <https://aistudio.google.com/app/apikey>  (왼쪽 🔑 '보안 비밀'에 `GEMINI_API_KEY` 저장도 가능)"""),
    code("""import os
key = None
try:
    from google.colab import userdata          # Colab 보안 비밀에서 우선 시도
    key = userdata.get('GEMINI_API_KEY')
except Exception:
    pass
if not key:
    import getpass
    key = getpass.getpass('Gemini API Key 를 붙여넣고 Enter: ')
os.environ['GEMINI_API_KEY'] = key.strip()
os.environ.setdefault('GEMINI_MODEL', 'gemini-2.5-flash')

from google import genai
try:
    _ = genai.Client(api_key=os.environ['GEMINI_API_KEY']).models.list()
    print('✅ Gemini 연결 OK · 모델:', os.environ['GEMINI_MODEL'])
except Exception as e:
    print('⚠️ 키 확인 실패:', e)
"""),
    md("""## 4) 서버 실행 → 공개 URL 받기

출력되는 `https://....trycloudflare.com` 주소를 새 탭에서 열면 이 앱(OncoReg)이 뜬다.
이 셀은 서버라 **계속 실행 상태로 둔다**(중지: ⏹️)."""),
    code("""import sys
sys.path.insert(0, 'oncoreg_ai')          # 전용 폴더에서 import
sys.modules.pop('oncoreg_app', None)      # 캐시된 옛 모듈 제거 후 최신 파일로 로드
from oncoreg_app import create_app
from flask_cloudflared import run_with_cloudflared

app = create_app()
print('>>> 실행 중인 앱: OncoReg AI (oncoreg_app, port 8000)')
run_with_cloudflared(app)
app.run(port=8000)
"""),
    md("""### (대안) cloudflared 가 안 될 때 — Colab 내장 프록시"""),
    code("""import sys, threading
sys.path.insert(0, 'oncoreg_ai')
sys.modules.pop('oncoreg_app', None)
from oncoreg_app import create_app
app = create_app()
threading.Thread(target=lambda: app.run(port=8000, use_reloader=False), daemon=True).start()

from google.colab.output import serve_kernel_port_as_window
serve_kernel_port_as_window(8000)   # 출력된 링크 클릭 -> 새 탭에서 열림
"""),
]

nb = {
    "cells": cells,
    "metadata": {
        "colab": {"provenance": []},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = os.path.join(HERE, "OncoReg_Colab.ipynb")
with open(out, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("wrote", out, "cells:", len(cells))
