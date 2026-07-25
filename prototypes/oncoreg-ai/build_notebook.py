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

**흐름**: ①필요 패키지 설치 → ②백엔드/프론트 파일 기록 → ③Gemini API 키 입력 → ④서버 실행(cloudflared 공개 URL) → 출력된 `https://....trycloudflare.com` 링크를 새 탭에서 열면 끝.

> ⚠️ 문헌/수치/임상시험은 Gemini가 생성한 초안이라 실제 출판물과 다를 수 있습니다. 데모/프로토타입 용도이며, 인용·제출 전 반드시 원문 대조·전문가 검증이 필요합니다.
"""),
    md("## 1) 패키지 설치"),
    code("!pip -q install google-genai flask flask-cors flask-cloudflared pydantic\n"),
    md("## 2) 백엔드(server.py)와 프론트(templates/index.html) 기록"),
    code("import os; os.makedirs('templates', exist_ok=True); print('templates/ 준비 완료')\n"),
    writefile_cell("server.py", server_src),
    writefile_cell("templates/index.html", html_src),
    md("""## 3) Gemini API 키 입력

키 발급: <https://aistudio.google.com/app/apikey>

아래 셀을 실행하면 입력창이 뜬다. (더 안전하게 하려면 Colab 왼쪽 🔑 '보안 비밀'에
`GEMINI_API_KEY` 를 넣어두면 자동으로 읽는다.)"""),
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

# (선택) 모델 변경: gemini-2.5-flash(기본) / gemini-2.0-flash 등
os.environ.setdefault('GEMINI_MODEL', 'gemini-2.5-flash')

# 키가 살아있는지 빠른 확인
from google import genai
try:
    _ = genai.Client(api_key=os.environ['GEMINI_API_KEY']).models.list()
    print('✅ Gemini 연결 OK · 모델:', os.environ['GEMINI_MODEL'])
except Exception as e:
    print('⚠️ 키 확인 실패:', e)
"""),
    md("""## 4) 서버 실행 → 공개 URL 받기

실행하면 잠시 뒤 `https://....trycloudflare.com` 형태의 주소가 출력된다.
**그 주소를 새 탭에서 열면** HTML 화면이 뜨고, '검색' 버튼이 내 Gemini 로 실제 동작한다.

- 이 셀은 서버라서 **계속 실행 상태로 둔다**(멈추면 서버도 꺼짐). 중지하려면 ⏹️.
- cloudflared 가 막히면 아래 '대안: Colab 내장 프록시' 셀을 쓴다."""),
    code("""from server import create_app
from flask_cloudflared import run_with_cloudflared

app = create_app()
run_with_cloudflared(app)      # 공개 URL 을 만들어 콘솔에 출력
app.run(port=8000)             # 이 줄에서 서버가 계속 돈다 (아래 출력의 trycloudflare 주소 사용)
"""),
    md("""### (대안) cloudflared 가 안 될 때 — Colab 내장 프록시

위 셀 대신 아래를 실행한다. 별도 설치 없이 Colab 이 만들어 주는 링크로 접속한다.
(프론트의 fetch 는 상대경로라 이 프록시에서도 그대로 동작한다.)"""),
    code("""import threading
from server import create_app
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
