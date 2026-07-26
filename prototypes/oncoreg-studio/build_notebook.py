"""OncoReg_Studio_Colab.ipynb 생성기. (OpenAI 연동)
사용:  python build_notebook.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
def readfile(n):
    with open(os.path.join(HERE, n), encoding="utf-8") as f: return f.read()
def code(s): return {"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],
                     "source":s if isinstance(s,list) else s.splitlines(keepends=True)}
def md(s): return {"cell_type":"markdown","metadata":{},
                   "source":s if isinstance(s,list) else s.splitlines(keepends=True)}
def wf(path,content): return code([f"%%writefile {path}\n"]+content.splitlines(keepends=True))

cells=[
 md("""# OncoReg Studio — OpenAI 연동 실행 노트북

자유서술 검색 · 근거수준 가중 랭킹 · 문서 스튜디오(오른쪽 실제 서식 + 왼쪽 근거 삽입).

**흐름**: ⓪초기화 → ①설치 → ②파일 기록 → ③OpenAI 키 입력 → ④서버 실행(cloudflared URL).

> ⚠️ 문헌·수치·지정(긴급승인·희귀의약품)·가이드라인은 AI 생성 초안이라 실제와 다를 수 있습니다. 제출 전 반드시 원문·규제정보 검증이 필요합니다.

> 🔴 다른 앱과 안 섞이게 전용 폴더(`oncoreg_studio/`)·모듈명(`studio_app`)·포트(8020)를 씁니다. 섞이면 런타임 다시 시작 후 이 노트북만 실행하세요."""),
 md("## 0) 초기화"),
 code("""import sys
for _m in ['server','studio_app','oncoreg_app','trialmatch_app']:
    sys.modules.pop(_m, None)
print('모듈 캐시 정리 완료.')
"""),
 md("## 1) 패키지 설치"),
 code("!pip -q install openai flask flask-cors flask-cloudflared\n"),
 md("## 2) 백엔드/프론트 파일 기록 (전용 폴더 `oncoreg_studio/`)"),
 code("import os; os.makedirs('oncoreg_studio/templates', exist_ok=True); print('준비 완료')\n"),
 wf("oncoreg_studio/studio_app.py", readfile("server.py")),
 wf("oncoreg_studio/templates/index.html", readfile(os.path.join("templates","index.html"))),
 md("""## 3) OpenAI API 키 입력 (직접 입력 칸)
키 발급: <https://platform.openai.com/api-keys>  (왼쪽 🔑 보안 비밀에 `OPENAI_API_KEY` 저장도 가능)"""),
 code("""import os
os.environ.setdefault('OPENAI_MODEL', 'gpt-4o-mini')   # 필요시 gpt-4o 등으로 변경
_pre=''
try:
    from google.colab import userdata
    _pre = userdata.get('OPENAI_API_KEY') or ''
except Exception:
    pass

def _verify():
    try:
        from openai import OpenAI
        c=OpenAI(api_key=os.environ.get('OPENAI_API_KEY',''))
        c.chat.completions.create(model=os.environ['OPENAI_MODEL'],
            messages=[{'role':'user','content':'ping'}], max_tokens=1)
        print('✅ OpenAI 연결 OK · 모델:', os.environ['OPENAI_MODEL'])
    except Exception as e:
        print('⚠️ 연결 확인만 실패(키가 맞아도 날 수 있음):', e)
        print('   → 키를 칸에 제대로 넣었다면 4번 서버 실행 셀로 진행해도 됩니다.')

try:
    import ipywidgets as w
    from IPython.display import display
    _key=w.Text(value=_pre, description='API Key', placeholder='sk-... 붙여넣기',
                layout=w.Layout(width='620px'), style={'description_width':'70px'})
    _model=w.Text(value=os.environ['OPENAI_MODEL'], description='Model',
                  layout=w.Layout(width='360px'), style={'description_width':'70px'})
    _btn=w.Button(description='저장하고 확인', button_style='success'); _out=w.Output()
    if _pre: os.environ['OPENAI_API_KEY']=_pre
    def _save(_):
        with _out:
            _out.clear_output()
            os.environ['OPENAI_API_KEY']=_key.value.strip()
            os.environ['OPENAI_MODEL']=_model.value.strip() or 'gpt-4o-mini'
            if not os.environ['OPENAI_API_KEY']: print('⚠️ 키 칸이 비어 있어요.'); return
            print('저장됨. 확인 중…'); _verify()
    _btn.on_click(_save); display(w.VBox([_key, w.HBox([_model,_btn]), _out]))
    print('↑ 칸에 키를 붙여넣고 [저장하고 확인]을 누르세요.')
except Exception:
    os.environ['OPENAI_API_KEY']=input('OpenAI API Key 붙여넣고 Enter: ').strip(); _verify()
"""),
 md("""## 4) 서버 실행 → 공개 URL
출력되는 `https://….trycloudflare.com` 주소를 새 탭에서 열면 스튜디오가 뜹니다. 이 셀은 계속 실행 상태로 둡니다(중지: ⏹️)."""),
 code("""import sys
sys.path.insert(0,'oncoreg_studio'); sys.modules.pop('studio_app',None)
from studio_app import create_app
from flask_cloudflared import run_with_cloudflared
app=create_app(); print('>>> 실행 중인 앱: OncoReg Studio (studio_app, port 8020)')
run_with_cloudflared(app); app.run(port=8020)
"""),
 md("### (대안) cloudflared 가 안 될 때 — Colab 내장 프록시"),
 code("""import sys, threading
sys.path.insert(0,'oncoreg_studio'); sys.modules.pop('studio_app',None)
from studio_app import create_app
app=create_app()
threading.Thread(target=lambda: app.run(port=8020, use_reloader=False), daemon=True).start()
from google.colab.output import serve_kernel_port_as_window
serve_kernel_port_as_window(8020)
"""),
]
nb={"cells":cells,"metadata":{"colab":{"provenance":[]},"kernelspec":{"display_name":"Python 3","name":"python3"},"language_info":{"name":"python"}},"nbformat":4,"nbformat_minor":5}
out=os.path.join(HERE,"OncoReg_Studio_Colab.ipynb")
with open(out,"w",encoding="utf-8") as f: json.dump(nb,f,ensure_ascii=False,indent=1)
print("wrote",out,"cells:",len(cells))
