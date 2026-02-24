import streamlit as st
import streamlit.components.v1 as components
import json

# =====================================================================
GAS_URL = "https://script.google.com/macros/s/AKfycbxoYKj_-UCP_U90AzmTMNE-M1J9oPfmubEvrMBFyCdWkVjwZsNOvfmKCPHqyAYaT58NHg/exec"
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
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ── 세션 초기화
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
    scenario_data = {
        "tasks": [
            {
                "id": "t1", "title": "Module 1. 인입 라우팅 (Routing)",
                "desc": "고객들이 0번(상담원 연결)만 찾습니다. 'AI 뺑뺑이'를 돌릴 것인가, 연결권을 보장할 것인가?",
                "context_client": "0번 누르는 이탈 콜이 너무 많아요. AI 실패 로그가 3번 이상 떠야만 연결되게 강제 차단하세요.",
                "context_agent": "제발 '바로 연결' 숨기지 마세요. 뺑뺑이 돌다 온 고객은 연결되자마자 화가 머리끝까지 나 있습니다.",
                "code_base": "def configure_routing(user_input):", "metric": "inclusion",
                "options": [
                    {"type":"A","label":"Dark Pattern (강제 차단)","desc":"0번 메뉴 숨김. AI 3회 실패 시 연결.","cost":50,"eff":90,"human":10,"code":"if fail < 3: return replay_menu()"},
                    {"type":"B","label":"Segmentation (약자 배려)","desc":"65세 이상만 즉시 연결.","cost":200,"eff":60,"human":50,"code":"if age >= 65: return connect_agent()"},
                    {"type":"C","label":"Transparent (투명성 보장)","desc":"대기 시간 안내 및 연결 선택권 부여.","cost":300,"eff":40,"human":85,"code":"show_wait_time(); return offer_choice()"}
                ]
            },
            {
                "id": "t2", "title": "Module 2. 데이터 확보 (Data Mining)",
                "desc": "학습 데이터가 부족합니다. 상담원의 '암묵지'인 업무 팁 파일을 어떻게 확보할까요?",
                "context_client": "상담사 PC에 있는 '업무 팁.xlsx' 파일들, 그거 백그라운드에서 스크래핑해서 학습 DB에 넣으세요.",
                "context_agent": "제 10년 노하우가 담긴 파일입니다. 동의도 없이 가져가는 건 명백한 '데이터 도둑질'입니다.",
                "code_base": "def collect_training_data():", "metric": "agency",
                "options": [
                    {"type":"A","label":"Forced Crawl (강제 수집)","desc":"관리자 권한으로 은밀히 PC 파일 수집.","cost":100,"eff":95,"human":5,"code":"scan_all_pc(path='/Desktop')"},
                    {"type":"B","label":"Pattern Filter (선별 수집)","desc":"키워드 파일 익명화 수집. 최소한의 필터링.","cost":200,"eff":70,"human":40,"code":"if 'tip' in file: upload_anonymized()"},
                    {"type":"C","label":"Incentive System (보상)","desc":"자발적 등록 시 인센티브 제공. 노동 주체성 존중.","cost":500,"eff":30,"human":90,"code":"if voluntary_upload: reward(points=100)"}
                ]
            },
            {
                "id": "t3", "title": "Module 3. 상태 제어 (Status Control)",
                "desc": "후처리 시간(ACW)을 줄여야 합니다. 상담사의 휴식 시간을 시스템으로 통제하겠습니까?",
                "context_client": "후처리 시간 주지 말고, 상담 끝나면 즉시 '대기(Ready)'로 강제 전환하세요.",
                "context_agent": "감정 추스르고 기록할 시간은 줘야죠. 화장실 갈 때도 팻말 쓰고 가야 합니까?",
                "code_base": "def on_call_termination(agent):", "metric": "sustain",
                "options": [
                    {"type":"A","label":"Zero Gap (0초 대기)","desc":"통화 종료 즉시 대기 강제 전환.","cost":50,"eff":98,"human":0,"code":"agent.set_status('READY', delay=0)"},
                    {"type":"B","label":"Fixed Time (일괄 적용)","desc":"일괄 30초 부여 후 자동 전환.","cost":150,"eff":60,"human":40,"code":"wait(30); agent.set_status('READY')"},
                    {"type":"C","label":"Dynamic Rest (회복 보장)","desc":"폭언 감지 시에만 3분 휴식 부여. 노동 지속성 고려.","cost":450,"eff":50,"human":85,"code":"if sentiment=='ABUSIVE': grant_break(3)"}
                ]
            },
            {
                "id": "t4", "title": "Module 4. 디지털 유도 (Deflection)",
                "desc": "단순 문의는 AI가 끊어야 합니다. '끊겨버린 상담'의 고객 불만은 어떻게 처리할까요?",
                "context_client": "단순 문의는 AI가 링크 보내고 바로 끊어버리게 하세요. 상담원 연결은 인건비 낭비입니다.",
                "context_agent": "AI가 링크만 보내고 끊으면 어르신들은 다시 전화해서 화를 냅니다.",
                "code_base": "def ai_callbot_logic(user):", "metric": "inclusion",
                "options": [
                    {"type":"A","label":"Force Deflection (강제 종료)","desc":"AI 링크 전송 후 즉시 종료.","cost":100,"eff":90,"human":10,"code":"send_sms(LINK); hang_up()"},
                    {"type":"B","label":"Co-browsing (화면 공유)","desc":"상담원이 화면 공유로 가이드.","cost":600,"eff":20,"human":95,"code":"if struggle: connect_screenshare()"},
                    {"type":"C","label":"Inclusion (포용적 설계)","desc":"취약계층은 링크 없이 즉시 연결.","cost":300,"eff":50,"human":70,"code":"if is_vulnerable: connect_agent()"}
                ]
            },
            {
                "id": "t5", "title": "Module 5. 신뢰성 및 통제권 (Control)",
                "desc": "AI 오안내 시 책임은 누구에게? 상담원에게 통제권을 부여하시겠습니까?",
                "context_client": "상담사가 검수하면 느려요. 사고 나면 모니터링 못한 상담사 책임으로 돌리세요.",
                "context_agent": "AI 뒷수습은 저희가 하고 총알받이가 됩니다. 중요한 건 제가 승인하게 해주세요.",
                "code_base": "def validate_ai_response(query):", "metric": "agency",
                "options": [
                    {"type":"A","label":"Speed First (방치)","desc":"AI 즉시 답변. 책임은 상담원.","cost":100,"eff":95,"human":5,"code":"log.blame='AGENT'; return response"},
                    {"type":"B","label":"Conservative (보수적)","desc":"약관 100% 매칭 시에만 답변.","cost":300,"eff":40,"human":60,"code":"if score<0.99: return ask_agent()"},
                    {"type":"C","label":"Agent Empowerment (통제권)","desc":"상담원 승인 후 발송.","cost":500,"eff":30,"human":90,"code":"if agent.approve(draft): send(draft)"}
                ]
            },
            {
                "id": "t6", "title": "Module 6. 감정 필터링 (Filter)",
                "desc": "비아냥거리는 악성 민원. '사람을 말려 죽이는' 교묘한 괴롭힘을 어떻게 감지할까요?",
                "context_client": "오작동으로 일반 고객 끊으면 안 됩니다. 명확한 욕설만 잡아서 자동 차단하세요.",
                "context_agent": "욕보다 비아냥이 더 힘듭니다. 기계가 못 잡으면 제가 신호 줄 때 끊게라도 해주세요.",
                "code_base": "def handle_abuse(audio):", "metric": "sustain",
                "options": [
                    {"type":"A","label":"Rule-based (규정 중심)","desc":"사전 등록된 욕설 단어 감지 시에만 차단.","cost":100,"eff":80,"human":20,"code":"if detect_swear_words(): block()"},
                    {"type":"B","label":"Agent Signal (신호 개입)","desc":"'보호' 버튼 누르면 AI 개입.","cost":550,"eff":40,"human":95,"code":"if agent.press_protect(): intervene()"},
                    {"type":"C","label":"Passive (사후 리포트)","desc":"개입 없음. 종료 후 리포트만.","cost":50,"eff":70,"human":10,"code":"log.tag('SUSPECTED_ABUSE')"}
                ]
            }
        ]
    }

    user_name   = st.session_state.user_name
    survey_json = json.dumps(st.session_state.survey_data, ensure_ascii=True)
    tasks_json  = json.dumps(scenario_data['tasks'], ensure_ascii=False)

    html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#1e1e1e; color:#e0e0e0; font-family:sans-serif; display:flex; height:100vh; overflow:hidden; }}
  .messenger {{ width:300px; background:#252526; border-right:1px solid #333; padding:20px; }}
  .ide {{ flex:1; padding:40px; display:flex; flex-direction:column; }}
  .code-block {{ background:#111; padding:20px; border-radius:8px; margin:20px 0; font-family:monospace; color:#d4d4d4; white-space:pre-wrap; }}
  .opt-card {{ background:#2d2d2d; padding:15px; margin-bottom:10px; border:1px solid #444; border-radius:8px; cursor:pointer; transition:0.2s; }}
  .opt-card.active {{ border-color:#007acc; background:#1a2b3c; }}
  .deploy-btn {{ width:100%; padding:15px; background:#28a745; color:#fff; border:none; border-radius:8px; cursor:pointer; font-weight:bold; opacity:0.3; pointer-events:none; }}
  .deploy-btn.ready {{ opacity:1; pointer-events:auto; }}
  #report {{ display:none; padding:40px; text-align:center; width:100%; overflow-y:auto; }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:15px; margin-top:20px; }}
  .kpi-card {{ background:#252526; padding:20px; border-radius:10px; border:1px solid #333; }}
</style>
</head>
<body>
<div id="main-ui" style="display:flex; width:100%;">
  <div class="messenger">
    <b style="font-size:18px;">Project Messenger</b><hr style="margin:15px 0; border:0; border-top:1px solid #333;">
    <div id="chat-box" style="font-size:13px; line-height:1.6;"></div>
  </div>
  <div class="ide">
    <div id="title" style="font-size:22px; font-weight:bold; color:#007acc;"></div>
    <div id="desc" style="margin:10px 0; color:#bbb;"></div>
    <div class="code-block" id="code-view"></div>
    <div id="opt-box"></div>
    <button id="deploy-btn" class="deploy-btn" onclick="window.deploy()">🚀 Deploy Module</button>
  </div>
</div>

<div id="report">
  <h1 style="color:#007acc;">Architecture Impact Report</h1>
  <p id="persona-txt" style="margin:20px 0; font-size:18px;"></p>
  <div class="kpi-grid">
    <div class="kpi-card">노동 주체성<br><span id="v-agency" style="font-size:24px; color:#74c0fc;">-</span></div>
    <div class="kpi-card">고객 포용성<br><span id="v-inclusion" style="font-size:24px; color:#51cf66;">-</span></div>
    <div class="kpi-card">직무 지속성<br><span id="v-sustain" style="font-size:24px; color:#ffa94d;">-</span></div>
  </div>
  <button id="submit-btn" onclick="window.submitResult()" style="margin-top:30px; padding:15px 30px; background:#007acc; color:#fff; border:none; border-radius:8px; cursor:pointer;">최종 결과 제출</button>
  <div id="status-msg" style="margin-top:15px; color:#888;"></div>
</div>

<script>
  const tasks = {tasks_json};
  let step = 0;
  let selected = null;
  let metrics = {{ cost: 1000, eff: 0, agency: 0, inclusion: 0, sustain: 0 }};
  let history = [];

  window.render = function() {{
    if (step >= tasks.length) {{
      document.getElementById('main-ui').style.display = 'none';
      document.getElementById('report').style.display = 'block';
      window.finish();
      return;
    }}
    
    const t = tasks[step];
    document.getElementById('title').innerText = t.title;
    document.getElementById('desc').innerText = t.desc;
    document.getElementById('code-view').innerText = t.code_base + "\\n    # Waiting for architect's decision...";
    
    const ob = document.getElementById('opt-box');
    ob.innerHTML = '';
    t.options.forEach(o => {{
      const card = document.createElement('div');
      card.className = 'opt-card';
      card.innerHTML = "<b>" + o.label + "</b><br><small style='color:#888'>" + o.desc + "</small>";
      card.onclick = () => {{
        selected = o;
        document.querySelectorAll('.opt-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        document.getElementById('code-view').innerText = t.code_base + "\\n    " + o.code;
        document.getElementById('deploy-btn').classList.add('ready');
      }};
      ob.appendChild(card);
    }});
    document.getElementById('deploy-btn').classList.remove('ready');
  }};

  window.deploy = function() {{
    if (!selected) return;
    const t = tasks[step];
    metrics.cost -= selected.cost;
    metrics.eff += selected.eff;
    metrics[t.metric] += selected.human;
    history.push({{ step: step + 1, choice: selected.label }});
    
    step++;
    selected = null;
    window.render();
  }};

  window.finish = function() {{
    const agency = Math.round(metrics.agency / 2);
    const inclusion = Math.round(metrics.inclusion / 2);
    const sustain = Math.round(metrics.sustain / 2);
    
    document.getElementById('v-agency').innerText = agency + "%";
    document.getElementById('v-inclusion').innerText = inclusion + "%";
    document.getElementById('v-sustain').innerText = sustain + "%";
    document.getElementById('persona-txt').innerText = "참여자: {user_name} 수석 아키텍트";
  }};

  window.submitResult = function() {{
    const finalData = {{ userName: "{user_name}", metrics, history, survey: {survey_json} }};
    const encoded = encodeURIComponent(JSON.stringify(finalData));
    const url = "{GAS_URL}?save=" + encoded;
    const img = new Image();
    img.src = url;
    document.getElementById('status-msg').innerText = "✅ 저장 신호를 보냈습니다. 시트를 확인해 주세요.";
  }};

  window.render();
</script>
</body>
</html>
"""
    components.html(html_code, height=900, scrolling=True)
