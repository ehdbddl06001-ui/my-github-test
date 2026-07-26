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
 code("!pip -q install google-genai openai flask flask-cors flask-cloudflared\n"),
 md("## 2) 백엔드/프론트 파일 기록 (전용 폴더 `oncoreg_studio/`)"),
 code("import os; os.makedirs('oncoreg_studio/templates', exist_ok=True); print('준비 완료')\n"),
 wf("oncoreg_studio/studio_app.py", readfile("server.py")),
 wf("oncoreg_studio/templates/index.html", readfile(os.path.join("templates","index.html"))),
 md("""## 3) API 키 입력 (Gemini 또는 OpenAI · 직접 입력 칸)
- Gemini 키: <https://aistudio.google.com/app/apikey>  ·  OpenAI 키: <https://platform.openai.com/api-keys>
- 공급자를 고르고 키를 붙여넣으세요. (보안 비밀 `GEMINI_API_KEY`/`OPENAI_API_KEY` 가 있으면 자동으로 채워집니다)"""),
 code("""import os
_pre_g=_pre_o=''
try:
    from google.colab import userdata
    _pre_g=userdata.get('GEMINI_API_KEY') or ''
    _pre_o=userdata.get('OPENAI_API_KEY') or ''
except Exception:
    pass

def _verify():
    prov=os.environ.get('LLM_PROVIDER','gemini')
    try:
        if prov=='gemini':
            from google import genai
            genai.Client(api_key=os.environ.get('GEMINI_API_KEY','')).models.generate_content(
                model=os.environ.get('GEMINI_MODEL','gemini-2.5-flash'), contents='ping')
            print('✅ Gemini 연결 OK · 모델:', os.environ.get('GEMINI_MODEL'))
        else:
            from openai import OpenAI
            OpenAI(api_key=os.environ.get('OPENAI_API_KEY','')).chat.completions.create(
                model=os.environ.get('OPENAI_MODEL','gpt-4o-mini'),
                messages=[{'role':'user','content':'ping'}], max_tokens=1)
            print('✅ OpenAI 연결 OK · 모델:', os.environ.get('OPENAI_MODEL'))
    except Exception as e:
        print('⚠️ 연결 확인만 실패(키가 맞아도 날 수 있음):', e)
        print('   → 키를 칸에 제대로 넣었다면 4번 서버 실행 셀로 진행해도 됩니다.')

try:
    import ipywidgets as w
    from IPython.display import display
    _prov=w.Dropdown(options=[('Gemini','gemini'),('OpenAI','openai')], value='gemini',
                     description='공급자', style={'description_width':'70px'})
    _key=w.Text(value=_pre_g, description='API Key', placeholder='키 붙여넣기',
                layout=w.Layout(width='620px'), style={'description_width':'70px'})
    _model=w.Text(value='gemini-2.5-flash', description='Model',
                  layout=w.Layout(width='360px'), style={'description_width':'70px'})
    _btn=w.Button(description='저장하고 확인', button_style='success'); _out=w.Output()
    def _on_prov(ch):
        if ch['new']=='gemini': _key.value=_pre_g; _model.value='gemini-2.5-flash'
        else: _key.value=_pre_o; _model.value='gpt-4o-mini'
    _prov.observe(_on_prov, names='value')
    def _save(_):
        with _out:
            _out.clear_output()
            prov=_prov.value; os.environ['LLM_PROVIDER']=prov
            k=_key.value.strip()
            if not k: print('⚠️ 키 칸이 비어 있어요.'); return
            if prov=='gemini':
                os.environ['GEMINI_API_KEY']=k; os.environ['GEMINI_MODEL']=_model.value.strip() or 'gemini-2.5-flash'
            else:
                os.environ['OPENAI_API_KEY']=k; os.environ['OPENAI_MODEL']=_model.value.strip() or 'gpt-4o-mini'
            print('저장됨('+prov+'). 확인 중…'); _verify()
    _btn.on_click(_save); display(w.VBox([_prov, _key, w.HBox([_model,_btn]), _out]))
    print('↑ 공급자 선택 → 키 붙여넣고 [저장하고 확인].')
except Exception:
    os.environ['LLM_PROVIDER']='gemini'
    os.environ['GEMINI_API_KEY']=input('Gemini API Key 붙여넣고 Enter: ').strip()
    os.environ.setdefault('GEMINI_MODEL','gemini-2.5-flash'); _verify()
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
