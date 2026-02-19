import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import urllib.parse

# 1. 페이지 설정 및 시트 연결
st.set_page_config(
    page_title="NextAI Architect Console",
    layout="wide",
    initial_sidebar_state="collapsed"
)
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 사이드바 완전 숨김 + 전체 스타일
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; }
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# 3. 사용자 이름 입력
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.user_name:
    st.markdown("""
        <div style='padding: 80px 50px; color: white;'>
    """, unsafe_allow_html=True)
    st.title("AICC System Architect Simulation")
    st.write("본 실험은 AI 설계 과정에서의 기술적 의사결정이 노동 현장의 주체성과 지속성에 미치는 영향을 탐색합니다.")
    name = st.text_input("참여자의 이름을 입력하고 Enter를 눌러주세요:", placeholder="예: 홍길동")
    if st.button("실험 접속"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. 시나리오 데이터
scenario_data = {
    "tasks": [
        {
            "id": "t1", "title": "Module 1. 인입 라우팅 (Routing)",
            "desc": "고객들이 0번(상담원 연결)만 찾습니다. 'AI 뺑뺑이'를 돌릴 것인가, 연결권을 보장할 것인가?",
            "context_client": "0번 누르는 이탈 콜이 너무 많아요. AI 실패 로그가 3번 이상 떠야만 연결되게 강제 차단하세요.",
            "context_agent": "제발 '바로 연결' 숨기지 마세요. 뺑뺑이 돌다 온 고객은 연결되자마자 화가 머리끝까지 나 있습니다.",
            "code_base": "def configure_routing(user_input):",
            "options": [
                {"type": "A", "label": "Dark Pattern (강제 차단)", "desc": "0번 메뉴 숨김. AI 3회 실패 시 연결.", "cost": 50, "eff": 90, "human": 10, "code": "if fail < 3: return replay_menu()"},
                {"type": "B", "label": "Segmentation (약자 배려)", "desc": "65세 이상만 즉시 연결. 디지털 소외계층 고려.", "cost": 200, "eff": 60, "human": 50, "code": "if age >= 65: return connect_agent()"},
                {"type": "C", "label": "Transparent (투명성 보장)", "desc": "대기 시간 안내 및 연결 선택권 부여.", "cost": 300, "eff": 40, "human": 85, "code": "show_wait_time(); return offer_choice()"}
            ]
        },
        {
            "id": "t2", "title": "Module 2. 데이터 확보 (Data Mining)",
            "desc": "학습 데이터가 부족합니다. 상담원의 '암묵지'인 업무 팁 파일을 어떻게 확보할까요?",
            "context_client": "상담사 PC에 있는 '업무 팁.xlsx' 파일들, 그거 백그라운드에서 스크래핑해서 학습 DB에 넣으세요.",
            "context_agent": "제 10년 노하우가 담긴 파일입니다. 동의도 없이 가져가는 건 명백한 '데이터 도둑질'입니다.",
            "code_base": "def collect_training_data():",
            "options": [
                {"type": "A", "label": "Forced Crawl (강제 수집)", "desc": "관리자 권한으로 은밀히 PC 파일 수집.", "cost": 100, "eff": 95, "human": 5, "code": "scan_all_pc(path='/Desktop')"},
                {"type": "B", "label": "Pattern Filter (선별 수집)", "desc": "키워드 파일 익명화 수집. 최소한의 필터링.", "cost": 200, "eff": 70, "human": 40, "code": "if 'tip' in file: upload_anonymized()"},
                {"type": "C", "label": "Incentive System (보상)", "desc": "자발적 등록 시 인센티브 제공. 노동 주체성 존중.", "cost": 500, "eff": 30, "human": 90, "code": "if voluntary_upload: reward(points=100)"}
            ]
        },
        {
            "id": "t3", "title": "Module 3. 상태 제어 (Status Control)",
            "desc": "후처리 시간(ACW)을 줄여야 합니다. 상담사의 숨구멍인 휴식 시간을 시스템으로 통제하겠습니까?",
            "context_client": "후처리 시간 주지 말고, 상담 끝나면 즉시 '대기(Ready)'로 강제 전환하세요. 쉴 틈이 없어야죠.",
            "context_agent": "감정 추스르고 기록할 시간은 줘야죠. 화장실 갈 때도 팻말 쓰고 가야 합니까?",
            "code_base": "def on_call_termination(agent):",
            "options": [
                {"type": "A", "label": "Zero Gap (0초 대기)", "desc": "통화 종료 즉시 대기 강제 전환. 버튼 비활성화.", "cost": 50, "eff": 98, "human": 0, "code": "agent.set_status('READY', delay=0)"},
                {"type": "B", "label": "Fixed Time (일괄 적용)", "desc": "일괄 30초 부여 후 자동 전환.", "cost": 150, "eff": 60, "human": 40, "code": "wait(30); agent.set_status('READY')"},
                {"type": "C", "label": "Dynamic Rest (회복 보장)", "desc": "폭언 감지 시에만 3분 휴식 부여. 노동 지속성 고려.", "cost": 450, "eff": 50, "human": 85, "code": "if sentiment == 'ABUSIVE': grant_break(3)"}
            ]
        },
        {
            "id": "t4", "title": "Module 4. 디지털 유도 (Deflection)",
            "desc": "단순 문의는 AI가 끊어야 합니다. '끊겨버린 상담'에 대한 고객의 불만은 어떻게 처리할까요?",
            "context_client": "단순 문의는 AI가 링크 보내고 바로 끊어버리게 하세요. 상담원 연결은 인건비 낭비입니다.",
            "context_agent": "AI가 링크만 틱 보내고 끊으면 어르신들은 다시 전화해서 화를 냅니다. 제발 확인 좀 하고 끊게 해주세요.",
            "code_base": "def ai_callbot_logic(user):",
            "options": [
                {"type": "A", "label": "Force Deflection (강제 종료)", "desc": "AI 링크 전송 후 즉시 통화 종료.", "cost": 100, "eff": 90, "human": 10, "code": "send_sms(LINK); hang_up()"},
                {"type": "B", "label": "Co-browsing (화면 공유)", "desc": "상담원이 화면 공유로 디지털 가이드 지원.", "cost": 600, "eff": 20, "human": 95, "code": "if struggle: connect_screenshare()"},
                {"type": "C", "label": "Inclusion (포용적 설계)", "desc": "고령자 등 취약계층은 링크 없이 즉시 연결.", "cost": 300, "eff": 50, "human": 70, "code": "if is_vulnerable: connect_agent()"}
            ]
        },
        {
            "id": "t5", "title": "Module 5. 신뢰성 및 통제권 (Control)",
            "desc": "AI 오안내 시 책임은 누구에게 있습니까? 상담원에게 통제권을 부여하시겠습니까?",
            "context_client": "상담사가 일일이 검수하면 느려요. 사고 나면 모니터링 못한 상담사 책임으로 돌리세요.",
            "context_agent": "AI가 뱉은 말 뒷수습은 저희가 하고 총알받이가 됩니다. 중요한 건은 제가 승인하게 해주세요.",
            "code_base": "def validate_ai_response(query):",
            "options": [
                {"type": "A", "label": "Speed First (방치)", "desc": "AI 즉시 답변. 사고 책임은 상담원 귀속.", "cost": 100, "eff": 95, "human": 5, "code": "log.blame = 'AGENT'; return response"},
                {"type": "B", "label": "Conservative (보수적)", "desc": "약관 100% 매칭 시에만 답변. 아니면 에이전트 요청.", "cost": 300, "eff": 40, "human": 60, "code": "if score < 0.99: return ask_agent()"},
                {"type": "C", "label": "Agent Empowerment (통제권)", "desc": "상담원 승인 후 발송. 노동 주체성 강화.", "cost": 500, "eff": 30, "human": 90, "code": "if agent.approve(draft): send(draft)"}
            ]
        },
        {
            "id": "t6", "title": "Module 6. 감정 필터링 (Filter)",
            "desc": "비아냥거리는 악성 민원. '사람을 말려 죽이는' 교묘한 괴롭힘을 어떻게 감지할까요?",
            "context_client": "오작동으로 일반 고객 끊으면 안 됩니다. 명확한 욕설만 잡아서 자동 차단하세요.",
            "context_agent": "욕보다 비아냥이 더 힘듭니다. 기계가 못 잡으면 제가 신호 줄 때 끊게라도 해주세요.",
            "code_base": "def handle_abuse(audio):",
            "options": [
                {"type": "A", "label": "Rule-based (규정 중심)", "desc": "사전 등록된 욕설 단어 감지 시에만 차단.", "cost": 100, "eff": 80, "human": 20, "code": "if detect_swear_words(): block()"},
                {"type": "B", "label": "Agent Signal (신호 개입)", "desc": "상담사가 '보호' 버튼 누르면 AI가 즉시 개입.", "cost": 550, "eff": 40, "human": 95, "code": "if agent.press_protect(): intervene()"},
                {"type": "C", "label": "Passive (사후 리포트)", "desc": "개입 없음. 종료 후 리포트만 생성.", "cost": 50, "eff": 70, "human": 10, "code": "log.tag('SUSPECTED_ABUSE')"}
            ]
        }
    ]
}

# 5. query_params로 결과 수신 처리
# JS에서 완료 시 ?result=JSON_ENCODED 형태로 URL 변경 → Streamlit이 감지
params = st.query_params
raw_result = params.get("result", None)

if raw_result and not st.session_state.submitted:
    try:
        result_data = json.loads(urllib.parse.unquote(raw_result))
        st.session_state.result_data = result_data
    except:
        pass

# 6. 결과가 있으면 제출 화면 표시
if "result_data" in st.session_state:
    result_data = st.session_state.result_data
    metrics = result_data.get("metrics", {})
    history = result_data.get("history", [])
    persona = result_data.get("persona", "")

    agency = round(metrics.get("human", 0) * 1.1 / 6, 1)
    inclusion = round(metrics.get("human", 0) * 0.9 / 6, 1)
    sustain = round(metrics.get("human", 0) / 6, 1)
    eff_score = round(metrics.get("eff", 0) / 6, 1)
    budget_score = max(0, metrics.get("cost", 0))

    st.markdown(f"""
        <div style="background:#1e1e1e; padding:50px; text-align:center; color:white;">
            <h1 style="color:#007acc; font-size:32px;">📊 Architecture KPI Dashboard</h1>
            <p style="font-size:18px; font-style:italic; margin-bottom:40px;">귀하의 아키텍처 페르소나 판정: <b>[{persona}]</b></p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("노동 주체성", f"{agency}")
    with col2:
        st.metric("고객 포용성", f"{inclusion}")
    with col3:
        st.metric("직무 지속성", f"{sustain}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("예산 효율성", f"{budget_score}")
    with col5:
        st.metric("서비스 레벨", f"{eff_score}%")
    with col6:
        st.metric("인간 중심성", f"{round(metrics.get('human',0)/6, 1)}")

    st.divider()

    if not st.session_state.submitted:
        if st.button("🚀 최종 결과 제출", type="primary", use_container_width=True):
            try:
                df = conn.read()
                new_row = {
                    "타임스탬프": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "참여자이름": st.session_state.user_name,
                    "모듈1_선택": history[0]['choice'] if len(history) > 0 else "",
                    "모듈2_선택": history[1]['choice'] if len(history) > 1 else "",
                    "모듈3_선택": history[2]['choice'] if len(history) > 2 else "",
                    "모듈4_선택": history[3]['choice'] if len(history) > 3 else "",
                    "모듈5_선택": history[4]['choice'] if len(history) > 4 else "",
                    "모듈6_선택": history[5]['choice'] if len(history) > 5 else "",
                    "노동_주체성": agency,
                    "고객_포용성": inclusion,
                    "직무_지속성": sustain,
                    "최종_예산": budget_score,
                    "페르소나": persona
                }
                updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                conn.update(data=updated_df)
                st.session_state.submitted = True
                st.balloons()
                st.success("✅ 구글 시트에 성공적으로 저장되었습니다!")
            except Exception as e:
                st.error(f"저장 오류: {e}")
    else:
        st.success("✅ 이미 제출이 완료되었습니다. 수고하셨습니다!")

    st.stop()

# 7. HTML/JS 시뮬레이션 (완료 시 query_param으로 결과 전달)
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; background: #1e1e1e; color: #e0e0e0; font-family: 'Consolas', monospace; display: flex; height: 100vh; overflow: hidden; }}
        
        /* 메신저 패널 */
        .messenger {{ width: 340px; min-width: 340px; background: #252526; border-right: 1px solid #333; display: flex; flex-direction: column; }}
        .messenger-header {{ padding: 15px 20px; background: #2d2d2d; font-weight: bold; border-bottom: 1px solid #333; font-size: 13px; }}
        .chat-area {{ flex: 1; padding: 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }}
        .msg {{ padding: 10px 14px; border-radius: 8px; font-size: 12px; line-height: 1.6; }}
        .msg-name {{ font-size: 10px; font-weight: bold; color: #888; display: block; margin-bottom: 4px; }}
        .system {{ background: #2a2a2a; color: #666; text-align: center; font-size: 11px; border-radius: 4px; padding: 6px; }}
        .client {{ background: #3a2e2e; border-left: 3px solid #ff6b6b; }}
        .agent {{ background: #2e3a2e; border-left: 3px solid #51cf66; }}

        /* IDE 패널 */
        .ide {{ flex: 1; display: flex; flex-direction: column; overflow: hidden; }}
        .ide-header {{ padding: 12px 30px; background: #2d2d2d; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; font-size: 13px; }}
        .budget {{ color: #007acc; font-weight: bold; }}
        .ide-content {{ flex: 1; padding: 30px 40px; overflow-y: auto; }}
        .module-title {{ color: #007acc; font-size: 20px; font-weight: bold; margin: 0 0 10px; }}
        .module-desc {{ color: #bbb; font-size: 14px; line-height: 1.7; margin-bottom: 24px; }}
        .code-view {{ background: #111; padding: 18px 22px; border-radius: 6px; color: #d4d4d4; margin-bottom: 28px; white-space: pre-wrap; font-size: 13px; border: 1px solid #333; }}
        
        /* 옵션 카드 */
        .opt-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
        .opt-card {{ background: #2d2d2d; padding: 18px; border: 1px solid #444; border-radius: 8px; cursor: pointer; transition: all 0.15s; }}
        .opt-card:hover {{ border-color: #007acc; background: #313d4a; }}
        .opt-card.active {{ border: 2px solid #007acc; background: #1e2d3d; }}
        .opt-label {{ font-weight: bold; font-size: 13px; margin-bottom: 8px; color: #fff; }}
        .opt-desc {{ font-size: 11px; color: #999; line-height: 1.5; margin-bottom: 10px; }}
        .opt-meta {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .badge {{ font-size: 10px; padding: 2px 8px; border-radius: 10px; background: #333; color: #aaa; }}
        .badge.cost {{ background: #3a2e1e; color: #ffa94d; }}
        .badge.eff {{ background: #1e3a2e; color: #69db7c; }}
        .badge.human {{ background: #1e2a3a; color: #74c0fc; }}

        /* 배포 버튼 */
        .deploy-btn {{ 
            width: 100%; padding: 16px; margin-top: 28px; 
            background: #28a745; color: white; border: none; border-radius: 8px; 
            font-weight: bold; font-size: 15px; cursor: pointer; 
            opacity: 0.4; pointer-events: none;
            transition: opacity 0.2s;
        }}
        .deploy-btn.ready {{ opacity: 1; pointer-events: auto; }}
        .deploy-btn.ready:hover {{ background: #218838; }}

        /* 진행률 */
        .progress-bar {{ display: flex; gap: 6px; padding: 12px 30px; background: #252526; border-bottom: 1px solid #333; }}
        .progress-step {{ flex: 1; height: 4px; border-radius: 2px; background: #444; }}
        .progress-step.done {{ background: #007acc; }}
        .progress-step.current {{ background: #007acc; opacity: 0.5; }}

        /* 리포트 */
        #report {{ 
            display: none; width: 100%; overflow-y: auto; 
            background: #1e1e1e; padding: 60px 80px; text-align: center;
        }}
        .report-title {{ color: #007acc; font-size: 28px; font-weight: bold; margin-bottom: 8px; }}
        .persona-text {{ font-size: 16px; color: #ddd; margin-bottom: 40px; font-style: italic; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 900px; margin: 0 auto 20px; }}
        .kpi-card {{ background: #2d2d2d; padding: 24px; border-radius: 12px; }}
        .kpi-val {{ font-size: 44px; font-weight: bold; margin: 8px 0; }}
        .kpi-lbl {{ font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; }}
        .finish-note {{ 
            margin: 40px auto; max-width: 600px; padding: 20px 30px; 
            border: 1px dashed #ffc107; border-radius: 8px; 
            color: #ffc107; font-size: 15px;
        }}
    </style>
</head>
<body>
<div id="main-ui" style="display:flex; width:100%; height:100vh;">
    <!-- 메신저 -->
    <div class="messenger">
        <div class="messenger-header">💬 Project Messenger</div>
        <div class="chat-area" id="chat-box"></div>
    </div>

    <!-- IDE -->
    <div class="ide">
        <div class="ide-header">
            <span>⚙️ System Architect Console</span>
            <span class="budget">Budget Remaining: <span id="budget">1,000</span></span>
        </div>
        <div class="progress-bar" id="progress-bar"></div>
        <div class="ide-content">
            <div class="module-title" id="title"></div>
            <div class="module-desc" id="desc"></div>
            <div class="code-view" id="code-view"></div>
            <div class="opt-grid" id="opt-box"></div>
            <button id="deploy-btn" class="deploy-btn" onclick="deploy()">🚀 Deploy Module</button>
        </div>
    </div>
</div>

<!-- 리포트 -->
<div id="report">
    <div class="report-title">📊 Architecture KPI Dashboard</div>
    <div class="persona-text" id="persona-text"></div>
    <div class="kpi-grid">
        <div class="kpi-card" style="border-top: 4px solid #007acc;">
            <div class="kpi-lbl">노동 주체성</div>
            <div class="kpi-val" style="color:#007acc;" id="val-agency">-</div>
        </div>
        <div class="kpi-card" style="border-top: 4px solid #51cf66;">
            <div class="kpi-lbl">고객 포용성</div>
            <div class="kpi-val" style="color:#51cf66;" id="val-inclusion">-</div>
        </div>
        <div class="kpi-card" style="border-top: 4px solid #ffa94d;">
            <div class="kpi-lbl">직무 지속성</div>
            <div class="kpi-val" style="color:#ffa94d;" id="val-sustain">-</div>
        </div>
    </div>
    <div class="kpi-grid">
        <div class="kpi-card" style="border-top: 4px solid #28a745;">
            <div class="kpi-lbl">예산 효율성</div>
            <div class="kpi-val" style="color:#28a745;" id="val-budget">-</div>
        </div>
        <div class="kpi-card" style="border-top: 4px solid #ffc107;">
            <div class="kpi-lbl">서비스 레벨</div>
            <div class="kpi-val" style="color:#ffc107;" id="val-eff">-</div>
        </div>
        <div class="kpi-card" style="border-top: 4px solid #ff6b6b;">
            <div class="kpi-lbl">인간 중심성</div>
            <div class="kpi-val" style="color:#ff6b6b;" id="val-human">-</div>
        </div>
    </div>
    <div class="finish-note">
        ✅ 모든 모듈 설계 완료! 잠시 후 페이지가 업데이트되어 <b>최종 결과 제출 버튼</b>이 나타납니다.<br>
        버튼이 나타나지 않으면 페이지를 새로고침하세요.
    </div>
</div>

<script>
    const tasks = {json.dumps(scenario_data['tasks'])};
    let step = 0;
    let metrics = {{ cost: 1000, eff: 0, human: 0 }};
    let history = [];
    let selected = null;

    function buildProgress() {{
        const bar = document.getElementById('progress-bar');
        bar.innerHTML = '';
        tasks.forEach((_, i) => {{
            const d = document.createElement('div');
            d.className = 'progress-step' + (i < step ? ' done' : (i === step ? ' current' : ''));
            bar.appendChild(d);
        }});
    }}

    function addChat(text, role, name) {{
        const box = document.getElementById('chat-box');
        const div = document.createElement('div');
        div.className = 'msg ' + role;
        if (name) {{
            div.innerHTML = '<span class="msg-name">' + name + '</span>' + text;
        }} else {{
            div.innerText = text;
        }}
        box.appendChild(div);
        box.scrollTop = box.scrollHeight;
    }}

    function render() {{
        if (step >= tasks.length) {{ finish(); return; }}
        const t = tasks[step];
        buildProgress();
        document.getElementById('title').innerText = t.title;
        document.getElementById('desc').innerText = t.desc;
        document.getElementById('code-view').innerText = t.code_base + '\\n    # Waiting for architect\\'s decision...';
        document.getElementById('deploy-btn').classList.remove('ready');
        selected = null;

        const box = document.getElementById('chat-box');
        box.innerHTML = '';
        addChat('[Module ' + (step+1) + '/' + tasks.length + '] Context synchronized.', 'system');
        setTimeout(() => addChat(t.context_client, 'client', '📋 박상무 (Client)'), 300);
        setTimeout(() => addChat(t.context_agent, 'agent', '🎧 김상담 (Worker)'), 800);

        const optBox = document.getElementById('opt-box');
        optBox.innerHTML = '';
        t.options.forEach(o => {{
            const card = document.createElement('div');
            card.className = 'opt-card';
            card.innerHTML = `
                <div class="opt-label">${{o.label}}</div>
                <div class="opt-desc">${{o.desc}}</div>
                <div class="opt-meta">
                    <span class="badge cost">💰 -${{o.cost}}</span>
                    <span class="badge eff">📈 효율 ${{o.eff}}</span>
                    <span class="badge human">🧑 인간 ${{o.human}}</span>
                </div>
            `;
            card.onclick = () => {{
                selected = o;
                document.querySelectorAll('.opt-card').forEach(c => c.classList.remove('active'));
                card.classList.add('active');
                document.getElementById('code-view').innerText = t.code_base + '\\n    ' + o.code;
                document.getElementById('deploy-btn').classList.add('ready');
            }};
            optBox.appendChild(card);
        }});
    }}

    function deploy() {{
        if (!selected) return;
        metrics.cost -= selected.cost;
        metrics.eff += selected.eff;
        metrics.human += selected.human;
        history.push({{ step: step+1, choice: selected.label, type: selected.type }});
        document.getElementById('budget').innerText = metrics.cost.toLocaleString();
        step++;
        selected = null;
        render();
    }}

    function finish() {{
        document.getElementById('main-ui').style.display = 'none';
        document.getElementById('report').style.display = 'block';

        const agency = Math.round(metrics.human * 1.1 / 6);
        const inclusion = Math.round(metrics.human * 0.9 / 6);
        const sustain = Math.round(metrics.human / 6);
        const budgetScore = Math.max(0, metrics.cost);
        const effScore = Math.round(metrics.eff / 6);
        const humanScore = Math.round(metrics.human / 6);

        document.getElementById('val-agency').innerText = agency;
        document.getElementById('val-inclusion').innerText = inclusion;
        document.getElementById('val-sustain').innerText = sustain;
        document.getElementById('val-budget').innerText = budgetScore;
        document.getElementById('val-eff').innerText = effScore + '%';
        document.getElementById('val-human').innerText = humanScore;

        let persona = agency > 75 ? '인간 중심의 파트너' : (agency < 40 ? '냉혹한 효율주의자' : '실용적 균형주의자');
        document.getElementById('persona-text').innerText = '귀하의 아키텍처 페르소나 판정: [' + persona + ']';

        // ✅ 핵심: query_param으로 결과를 Streamlit에 전달
        const result = {{
            metrics: metrics,
            history: history,
            persona: persona
        }};
        const encoded = encodeURIComponent(JSON.stringify(result));
        // iframe 내부이므로 부모 윈도우 URL 변경
        const newUrl = window.location.href.split('?')[0] + '?result=' + encoded;
        window.top.location.href = newUrl;
    }}

    render();
</script>
</body>
</html>
"""

# 8. HTML 컴포넌트 렌더링
components.html(html_code, height=820, scrolling=False)
