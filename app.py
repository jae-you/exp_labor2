import streamlit as st
import streamlit.components.v1 as components
import json

# =====================================================================
GAS_URL = "https://script.google.com/macros/s/AKfycbyEB0gBk4KjbhH-18lRGSGG8yE3v0KHiCv90KZDDEvFtmcp7cTO3sDszG66l7fUW4GlTg/exec"
# =====================================================================

st.set_page_config(
    page_title="NextAI Architect Console",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* ── 기본 레이아웃 ── */
    .stApp { background-color: #1e1e1e; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header, footer { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    div[data-testid="stVerticalBlock"] { gap: 0 !important; }

    /* ── 설문 페이지 전용 ── */
    html, body, [class*="css"], .stApp, * {
        font-family: 'Noto Sans KR', sans-serif !important;
    }

    /* 질문 레이블 */
    div[data-testid="stRadio"] > label,
    div[data-testid="stNumberInput"] > label,
    div[data-testid="stTextInput"] > label {
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #e0e0e0 !important;
        line-height: 1.6 !important;
        margin-bottom: 8px !important;
    }

    /* 라디오 옵션 카드 */
    div[data-testid="stRadio"] > div > label {
        background: #252526 !important;
        border: 1px solid #2e2e2e !important;
        border-radius: 8px !important;
        padding: 11px 16px !important;
        color: #ccc !important;
        width: 100% !important;
    }

    /* 인풋 박스 */
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {
        background: #252526 !important;
        border: 1px solid #2e2e2e !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
    }

    .stop-box {
        background: #2a1a1a; border-left: 3px solid #ff6b6b;
        border-radius: 0 8px 8px 0; padding: 14px 18px;
        font-size: 13px; color: #ff6b6b;
    }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "scenario"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "survey_data" not in st.session_state:
    st.session_state.survey_data = {}

# PAGE 1 : 시나리오 안내
if st.session_state.page == "scenario":
    components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { background: #1e1e1e; color: #e0e0e0; font-family: sans-serif; display: flex; justify-content: center; padding: 40px; }
  .wrap { max-width: 800px; width: 100%; }
  h1 { font-size: 24px; color: #fff; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0; }
  .card { background: #252526; padding: 15px; border-radius: 8px; border: 1px solid #333; }
  .next-btn { width: 100%; padding: 15px; background: #007acc; color: #fff; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
</style>
</head>
<body>
<div class="wrap">
  <h1>실험 시나리오 안내</h1>
  <div class="grid">
    <div class="card"><b>역할</b><br>기술 리드 엔지니어</div>
    <div class="card"><b>회사</b><br>중견 IT 기업</div>
    <div class="card"><b>클라이언트</b><br>은행 위탁 콜센터</div>
    <div class="card"><b>엔드유저</b><br>숙련된 상담사</div>
  </div>
  <button class="next-btn" id="go-btn">사전 설문 시작 →</button>
</div>
<script>
  document.getElementById('go-btn').onclick = function() {
    window.parent.postMessage({ type: 'GO_SURVEY' }, '*');
  };
</script>
</body>
</html>
""", height=500)

    st.markdown('<div style="padding: 0 60px;">', unsafe_allow_html=True)
    if st.button("▶ 다음 단계로 이동", type="primary", use_container_width=True):
        st.session_state.page = "survey"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# PAGE 2 : 사전 설문
elif st.session_state.page == "survey":
    st.title("사전 설문조사")
    survey = {}
    q1 = st.radio("Q1. 성별", ["① 남성", "② 여성"], index=None)
    q2 = st.number_input("Q2. 출생연도", min_value=1950, max_value=2005, value=None)
    q3 = st.radio("Q3. 경력", ["① 3년 미만", "② 3년~5년", "③ 5년~7년", "④ 7년~10년", "⑤ 10년 이상"], index=None)
    
    if q3 in ["① 3년 미만", "⑤ 10년 이상"]:
        st.error("참여 대상이 아닙니다.")
        st.stop()

    user_name_input = st.text_input("성함 (데이터 식별용)")

    if st.button("실험 시작 →", type="primary", use_container_width=True):
        if q1 and q2 and q3 and user_name_input:
            st.session_state.survey_data = {"성별": q1, "연도": q2, "경력": q3}
            st.session_state.user_name = user_name_input
            st.session_state.page = "sim"
            st.rerun()

# PAGE 3 : 시뮬레이션
elif st.session_state.page == "sim":
    # (scenario_data 생략 - 기존 데이터 유지)
    scenario_data = {
        "tasks": [
            { "id": "t1", "title": "Module 1. 인입 라우팅", "desc": "라우팅 로직 설계", "context_client": "강제 차단하세요.", "context_agent": "숨기지 마세요.", "code_base": "def routing():", "metric": "inclusion", "options": [{"type":"A","label":"A안","desc":"설명A","cost":50,"eff":90,"human":10,"code":"#codeA"},{"type":"C","label":"C안","desc":"설명C","cost":300,"eff":40,"human":85,"code":"#codeC"}] },
            { "id": "t2", "title": "Module 2. 데이터 확보", "desc": "데이터 마이닝", "context_client": "다 긁어오세요.", "context_agent": "도둑질입니다.", "code_base": "def collect():", "metric": "agency", "options": [{"type":"A","label":"A안","desc":"설명A","cost":100,"eff":95,"human":5,"code":"#codeA"},{"type":"C","label":"C안","desc":"설명C","cost":500,"eff":30,"human":90,"code":"#codeC"}] }
        ] # 예시를 위해 2개만 넣었으나 실제로는 6개 다 넣으시면 됩니다.
    }

    survey_json = json.dumps(st.session_state.survey_data)
    tasks_json = json.dumps(scenario_data['tasks'], ensure_ascii=False)

    html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ background:#1e1e1e; color:#e0e0e0; font-family:sans-serif; margin:0; display:flex; height:100vh; }}
  .messenger {{ width:300px; background:#252526; border-right:1px solid #333; padding:20px; }}
  .ide {{ flex:1; padding:40px; display:flex; flex-direction:column; }}
  .code-block {{ background:#111; padding:20px; border-radius:8px; margin:20px 0; font-family:monospace; }}
  .opt-card {{ background:#2d2d2d; padding:15px; margin-bottom:10px; border:1px solid #444; border-radius:8px; cursor:pointer; }}
  .opt-card.active {{ border-color:#007acc; background:#1a2b3c; }}
  .deploy-btn {{ width:100%; padding:20px; background:#28a745; color:#fff; border:none; border-radius:8px; cursor:pointer; font-weight:bold; opacity:0.3; }}
  .deploy-btn.ready {{ opacity:1; }}
  #report {{ display:none; padding:40px; text-align:center; width:100%; }}
</style>
</head>
<body>
<div id="main-ui" style="display:flex; width:100%;">
  <div class="messenger">
    <b>Messenger</b><hr>
    <div id="chat-box"></div>
  </div>
  <div class="ide">
    <div id="title" style="font-size:20px; font-weight:bold; color:#007acc;"></div>
    <div id="desc" style="margin:10px 0;"></div>
    <div class="code-block" id="code-view"></div>
    <div id="opt-box"></div>
    <button id="deploy-btn" class="deploy-btn">🚀 Deploy Module</button>
  </div>
</div>
<div id="report">
  <h1>Architecture Impact Report</h1>
  <div id="persona-txt"></div>
  <button id="submit-btn" style="padding:15px 30px; background:#007acc; color:#fff; border:none; border-radius:8px; margin-top:20px;">최종 결과 제출</button>
</div>

<script>
  const tasks = {tasks_json};
  let step = 0;
  let selected = null;
  let metrics = {{ cost: 1000, eff: 0, agency: 0, inclusion: 0, sustain: 0 }};
  let history = [];

  const deployBtn = document.getElementById('deploy-btn');
  const submitBtn = document.getElementById('submit-btn');

  function render() {{
    if (step >= tasks.length) {{
      document.getElementById('main-ui').style.display = 'none';
      document.getElementById('report').style.display = 'block';
      document.getElementById('persona-txt').innerText = "분석 완료: 참여자 " + "{st.session_state.user_name}";
      return;
    }}
    
    const t = tasks[step];
    document.getElementById('title').innerText = t.title;
    document.getElementById('desc').innerText = t.desc;
    document.getElementById('code-view').innerText = t.code_base;
    
    const ob = document.getElementById('opt-box');
    ob.innerHTML = '';
    t.options.forEach(o => {{
      const card = document.createElement('div');
      card.className = 'opt-card';
      card.innerHTML = "<b>" + o.label + "</b><br>" + o.desc;
      card.onclick = () => {{
        selected = o;
        document.querySelectorAll('.opt-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        document.getElementById('code-view').innerText = t.code_base + "\\n  " + o.code;
        deployBtn.classList.add('ready');
      }};
      ob.appendChild(card);
    }});
    deployBtn.classList.remove('ready');
  }}

  deployBtn.onclick = () => {{
    if (!selected) return;
    metrics.cost -= selected.cost;
    metrics.eff += selected.eff;
    metrics[tasks[step].metric] += selected.human;
    history.push({{ step: step + 1, choice: selected.label }});
    
    step++;
    selected = null;
    render();
  }};

  submitBtn.onclick = () => {{
    const finalData = {{ userName: "{st.session_state.user_name}", metrics, history }};
    const encoded = encodeURIComponent(JSON.stringify(finalData));
    const img = new Image();
    img.src = "{GAS_URL}?save=" + encoded;
    alert("저장 신호를 보냈습니다.");
  }};

  render();
</script>
</body>
</html>
"""
    components.html(html_code, height=900, scrolling=True)
