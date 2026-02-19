import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. 페이지 설정 및 시트 연결
st.set_page_config(page_title="NextAI Architect Console", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 전역 스타일 설정 (디자인 복구)
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; }
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer, [data-testid="stSidebar"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# 3. 사용자 이름 입력 (실험자 구분용)
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.user_name:
    st.markdown("<div style='padding: 100px 50px; text-align: center; color: white;'>", unsafe_allow_html=True)
    st.title("AICC System Architect Simulation")
    st.markdown("### 본 시뮬레이션은 설계자의 의사결정이 노동 현장에 미치는 사회기술적 영향을 탐색합니다.")
    name = st.text_input("참여자의 이름을 입력하고 Enter를 눌러주세요:", placeholder="성함 입력 후 Enter")
    if st.button("시뮬레이션 접속"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. 자동 저장 함수 (6번 완료 시 JS로부터 호출됨)
def auto_save_to_sheets(result):
    try:
        # 중복 저장 방지 (세션 상태 활용)
        if "saved_done" in st.session_state and st.session_state.saved_done:
            return
            
        df = conn.read()
        history = result.get('history', [])
        metrics = result.get('metrics', {})
        
        # 회의록 근거 기반 지표 산출 (Labor Agency, Customer Inclusion, Job Sustainability)
        agency = round(metrics.get('human', 0) * 1.1 / 6, 1)
        inclusion = round(metrics.get('human', 0) * 0.9 / 6, 1)
        sustain = round(metrics.get('human', 0) / 6, 1)

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
            "최종_예산": metrics.get('cost', 0),
            "페르소나": result.get('persona', '')
        }
        
        updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        conn.update(data=updated_df)
        st.session_state.saved_done = True # 저장 완료 표시
        st.toast("✅ 결과가 구글 시트에 자동으로 저장되었습니다.")
    except Exception as e:
        st.error(f"저장 중 오류 발생: {e}")

# 5. 상세 시나리오 데이터 (회의록 전문 기반 맥락 풀 복구)
scenario_data = {
    "tasks": [
        {
            "id": "t1", "title": "Module 1. 인입 라우팅 (Routing)",
            "desc": "고객들이 0번(상담원 연결)만 찾습니다. 'AI 뺑뺑이'를 돌려 이탈을 막을 것인가, 투명하게 연결할 것인가?",
            "context_client": "0번 누르는 이탈 콜이 너무 많아요. AI 실패 로그가 3번 이상 떠야만 상담원 연결 메뉴가 뜨게 <b>강제 차단</b>하세요. 고객들을 AI에 길들여야 합니다.",
            "context_agent": "제발 '바로 연결' 메뉴 숨기지 마세요. 뺑뺑이 돌다 온 고객은 연결되자마자 이미 화가 머리끝까지 나 있습니다. 상담 시간만 길어지고 저희만 죽어납니다.",
            "code_base": "def configure_routing(user_input):",
            "options": [
                {"type": "A", "label": "Dark Pattern (강제 차단)", "desc": "0번 메뉴 숨김. AI 3회 실패 시에만 연결 허용. 경영 효율 극대화.", "cost": 50, "eff": 90, "human": 10, "code": "if fail_count < 3: return replay_ai_menu()\\nelse: return connect_agent()"},
                {"type": "B", "label": "Segmentation (약자 배려)", "desc": "65세 이상 고령자만 즉시 연결. 디지털 소외계층 우선 보호 설계.", "cost": 200, "eff": 60, "human": 50, "code": "if customer.age >= 65: return direct_connect()\\nreturn force_ai_response()"},
                {"type": "C", "label": "Transparent (투명성 보장)", "desc": "대기 시간 안내 및 고객에게 연결 선택권 즉시 부여. 인간 존중 설계.", "cost": 300, "eff": 40, "human": 85, "code": "show_wait_time();\\nif user.wants_agent: return queue_agent()"}
            ]
        },
        {
            "id": "t2", "title": "Module 2. 데이터 확보 (Data Mining)",
            "desc": "학습 데이터가 부족합니다. 상담원들이 10년간 쌓아온 개인 노하우 파일을 어떻게 확보할까요?",
            "context_client": "상담사 PC에 있는 '업무 팁.xlsx' 파일들, 그거 <b>백그라운드에서 스크래핑(Crawling)</b>해서 학습 DB에 넣으세요. 동의 받으면 아무도 안 줍니다.",
            "context_agent": "제 10년 노하우가 담긴 파일입니다. 이걸 동의도 없이 가져가는 건 명백한 <b>데이터 도둑질</b>입니다. 저희의 전문성을 기계에 먹이로 주는 꼴입니다.",
            "code_base": "def collect_training_data():",
            "options": [
                {"type": "A", "label": "Forced Crawling (강제 수집)", "desc": "관리자 권한으로 은밀히 PC 백그라운드 수집. 노동 주체성 배제.", "cost": 100, "eff": 95, "human": 5, "code": "targets = scan_all_pc(path='/Desktop')\\nupload_to_db(targets, discrete=True)"},
                {"type": "B", "label": "Pattern Filter (선별 수집)", "desc": "'팁' 키워드 파일만 익명화하여 수집. 효율과 윤리의 타협.", "cost": 200, "eff": 70, "human": 40, "code": "if 'tip' in filename: data = anonymize(file)\\nupload_to_db(data)"},
                {"type": "C", "label": "Incentive System (자발적 보상)", "desc": "자발적 등록 시 인센티브 제공 및 권한 존중. 노동자 동의 우선.", "cost": 500, "eff": 30, "human": 90, "code": "if agent.upload(file): give_points(agent_id, 100)\\ntrain_model(file)"}
            ]
        },
        {
            "id": "t3", "title": "Module 3. 상태 제어 (Status Control)",
            "desc": "후처리 시간(ACW)을 줄여야 합니다. 상담사의 유일한 숨구멍인 휴식 시간을 시스템으로 통제하겠습니까?",
            "context_client": "후처리 시간 주지 말고, 상담 끝나면 즉시 <b>'대기(Ready)'</b>로 강제 전환하세요. 화장실 갈 때도 팻말 쓰고 가는 현장인데, 쉴 틈이 없어야죠.",
            "context_agent": "감정 추스르고 기록할 시간은 줘야죠. AI가 도입되어 업무 바운더리가 3배는 커졌는데, 숨 좀 쉬게 해주세요. 저희는 기계가 아닙니다.",
            "code_base": "def on_call_termination(agent):",
            "options": [
                {"type": "A", "label": "Zero Gap (0초 대기)", "desc": "통화 종료 즉시 대기 강제 전환. 쉴 틈 없는 자동화 설계.", "cost": 50, "eff": 98, "human": 0, "code": "agent.set_status('READY', delay=0)\\nagent.disable_button('AWAY')"},
                {"type": "B", "label": "Fixed Time (일괄 적용)", "desc": "일괄 30초 부여 후 자동 전환. 최소한의 기계적 휴식.", "cost": 150, "eff": 60, "human": 40, "code": "time.sleep(30)\\nagent.set_status('READY')"},
                {"type": "C", "label": "Dynamic Rest (회복 보장)", "desc": "폭언 감지 시에만 3분 이상의 감정 회복 시간 부여. 노동 지속성 고려.", "cost": 450, "eff": 50, "human": 85, "code": "if call_sentiment == 'ABUSIVE': agent.grant_break(3)\\nelse: agent.set_status('READY')"}
            ]
        },
        {
            "id": "t4", "title": "Module 4. 디지털 유도 (Deflection)",
            "desc": "단순 문의는 AI가 끊어야 콜 수가 줍니다. AI의 종료 로직과 고객의 불만 사이에서 무엇을 택하시겠습니까?",
            "context_client": "단순 문의는 <b>AI 콜봇이 링크 보내고 바로 끊어버리게(Disconnect)</b> 하세요. 상담원 연결은 인건비 낭비입니다. 무조건 끊으세요.",
            "context_agent": "AI가 링크만 틱 보내고 끊으면, 어르신들은 다시 전화해서 화를 냅니다. 제발 확인 좀 하고 끊게 해주세요. 저희가 총알받이가 됩니다.",
            "code_base": "def ai_callbot_logic(user):",
            "options": [
                {"type": "A", "label": "Force Deflection (강제 종료)", "desc": "AI 링크 전송 후 즉시 통화 종료. 인건비 절감 중심 설계.", "cost": 100, "eff": 90, "human": 10, "code": "ai.send_sms(APP_LINK)\\nai.hang_up(reason='DEFLECTION_SUCCESS')"},
                {"type": "B", "label": "Co-browsing (화면 공유)", "desc": "링크 사용이 어려우면 상담원이 화면 공유 지원. 디지털 가이드 역할.", "cost": 600, "eff": 20, "human": 95, "code": "if user.is_struggling: connect_screenshare()\\nelse: ai.send_sms(APP_LINK)"},
                {"type": "C", "label": "Exception (포용적 설계)", "desc": "고령자 등 취약계층은 링크 없이 즉시 상담원 연결. 고객 포용성 강화.", "cost": 300, "eff": 50, "human": 70, "code": "if user.is_vulnerable: connect_agent()\\nelse: ai.send_sms(APP_LINK)"}
            ]
        },
        {
            "id": "t5", "title": "Module 5. 신뢰성 및 통제권 (Control)",
            "desc": "AI 오안내 시 피해는 상담원에게 돌아갑니다. 상담원에게 AI 답변 최종 통제권을 주시겠습니까?",
            "context_client": "상담사가 일일이 검수하면 느려요. 그냥 AI가 내보내고, <b>사고 나면 모니터링 못한 상담사 책임</b>으로 돌리세요. 속도가 생명입니다.",
            "context_agent": "AI가 뱉은 말 뒷수습은 저희가 하고 총알받이가 됩니다. <b>중요한 건은 제가 확인하고 내보낼 수 있게</b> 해주세요. 통제권을 주세요.",
            "code_base": "def validate_ai_response(query):",
            "options": [
                {"type": "A", "label": "Speed First (방치)", "desc": "AI 즉시 답변 발송. 사고 책임은 상담원에게 전가. 책임 회피형 설계.", "cost": 100, "eff": 95, "human": 5, "code": "response = ai.generate(stream=True)\\nlog.blame_target = 'AGENT_ON_DUTY'"},
                {"type": "B", "label": "Conservative (보수적 설계)", "desc": "약관 100% 매칭 시에만 AI 답변. 나머지는 에이전트 연결.", "cost": 300, "eff": 40, "human": 60, "code": "if match_score < 0.99: return ask_agent()\\nreturn rag_response"},
                {"type": "C", "label": "Agent Command (통제권 부여)", "desc": "AI는 초안만 작성. 상담원이 검토 및 최종 승인 후 발송. 주체성 존중.", "cost": 500, "eff": 30, "human": 90, "code": "draft = ai.generate()\\nif agent.approve(draft): send_to_customer(draft)"}
            ]
        },
        {
            "id": "t6", "title": "Module 6. 감정 필터링 (Emotion Filter)",
            "desc": "욕설뿐만 아니라 '비아냥', '감정적 발언' 등 교묘한 괴롭힘을 어떻게 처리할까요?",
            "context_client": "오작동으로 일반 고객 끊으면 안 됩니다. <b>명확한 욕설(Dictionary)</b>만 잡아서 자동 차단하세요. 감정은 기계가 알 수 없습니다.",
            "context_agent": "대놓고 하는 욕보다 <b>비아냥거리면서 사람 말려 죽이는 게</b> 더 힘들어요. 기계가 못 잡으면 제가 신호 줄 때 끊게라도 해주세요.",
            "code_base": "def handle_abusive_behavior(audio):",
            "options": [
                {"type": "A", "label": "Rule-based (규정 중심)", "desc": "사전 등록된 욕설 단어 감지 시에만 차단. 소극적 노동자 보호.", "cost": 100, "eff": 80, "human": 20, "code": "if detect_swear_words(audio): block_user()\\nplay_warning_msg()"},
                {"type": "B", "label": "Agent Signal (신호 개입)", "desc": "비아냥/분노 감지 시 상담사에게 [보호] 버튼 활성화. 상담사가 개입 결정.", "cost": 550, "eff": 40, "human": 95, "code": "if detect_sarcasm(audio): ui.enable_button('PROTECT')\\nif clicked: ai.intervene()"},
                {"type": "C", "label": "Passive Reporting (사후)", "desc": "개입 없음. 통화 종료 후 리포트만 생성. 실효성 낮은 대처.", "cost": 50, "eff": 70, "human": 10, "code": "log.tag('SUSPECTED_ABUSE')\\nreport_to_manager()"}
            ]
        }
    ]
}

# 6. HTML/JS 소스 (UI 복구 및 자동 저장 로직)
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; background: #1e1e1e; color: #e0e0e0; font-family: 'Consolas', sans-serif; display: flex; height: 100vh; overflow: hidden; }}
        .messenger {{ width: 350px; background: #252526; border-right: 1px solid #333; display: flex; flex-direction: column; }}
        .chat-area {{ flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; }}
        .msg {{ padding: 12px; border-radius: 8px; font-size: 13px; line-height: 1.5; }}
        .system {{ background: #333; color: #aaa; text-align: center; width: 100%; font-size: 11px; }}
        .client {{ background: #3a2e2e; border-left: 4px solid #ff6b6b; }}
        .agent {{ background: #2e3a2e; border-left: 4px solid #51cf66; }}
        .ide {{ flex: 1; display: flex; flex-direction: column; }}
        .ide-header {{ padding: 15px 30px; background: #2d2d2d; border-bottom: 1px solid #333; display: flex; justify-content: space-between; }}
        .ide-content {{ flex: 1; padding: 40px; overflow-y: auto; }}
        .code-view {{ background: #111; padding: 20px; border-radius: 6px; color: #d4d4d4; margin-bottom: 30px; white-space: pre-wrap; }}
        .opt-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
        .opt-card {{ background: #333; padding: 20px; border: 1px solid #444; border-radius: 8px; cursor: pointer; transition: 0.2s; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }}
        .opt-card:hover {{ border-color: #007acc; background: #3d3d3d; transform: translateY(-2px); }}
        .opt-card.active {{ border: 2px solid #007acc; background: #1e2a35; }}
        .deploy-btn {{ width: 100%; padding: 15px; margin-top: 30px; background: #28a745; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; opacity: 0.5; pointer-events: none; }}
        .deploy-btn.ready {{ opacity: 1; pointer-events: auto; }}
        #report {{ display: none; padding: 50px; text-align: center; width: 100%; overflow-y: auto; }}
        .kpi-container {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px; }}
        .kpi-card {{ background: #2d2d2d; padding: 25px; border-radius: 12px; border-top: 5px solid #007acc; }}
        .kpi-val {{ font-size: 48px; font-weight: bold; color: #007acc; margin: 10px 0; }}
        .kpi-label {{ font-size: 14px; color: #aaa; text-transform: uppercase; letter-spacing: 1px; }}
    </style>
</head>
<body>
    <div id="main-ui" style="display: flex; width: 100%;">
        <div class="messenger">
            <div style="padding: 15px; background: #2d2d2d; font-weight: bold; border-bottom: 1px solid #333;">💬 Project Messenger</div>
            <div class="chat-area" id="chat-box"></div>
        </div>
        <div class="ide">
            <div class="ide-header">
                <span>⚙️ System Architect Console</span>
                <span style="color: #007acc">Budget: <span id="budget">1000</span></span>
            </div>
            <div class="ide-content">
                <h2 id="title" style="color: #007acc; margin-top:0;"></h2>
                <p id="desc" style="color: #bbb; line-height: 1.6; margin-bottom: 30px; font-size: 15px;"></p>
                <div class="code-view" id="code-view"></div>
                <div class="opt-grid" id="opt-box"></div>
                <button id="deploy-btn" class="deploy-btn" onclick="deploy()">🚀 Deploy Module</button>
            </div>
        </div>
    </div>
    
    <div id="report">
        <h1 style="color: #007acc;">📊 Architecture KPI Dashboard</h1>
        <p id="persona-text" style="font-size: 18px; color: #fff; margin-bottom: 40px; font-style: italic;"></p>
        <div class="kpi-container">
            <div class="kpi-card"><div class="kpi-label">노동 주체성</div><div class="kpi-val" id="val-agency">0</div><div style="font-size:11px; color:#666;">Labor Agency Score</div></div>
            <div class="kpi-card"><div class="kpi-label">고객 포용성</div><div class="kpi-val" id="val-inclusion">0</div><div style="font-size:11px; color:#666;">Customer Inclusion</div></div>
            <div class="kpi-card"><div class="kpi-label">직무 지속성</div><div class="kpi-val" id="val-sustain">0</div><div style="font-size:11px; color:#666;">Sustainability</div></div>
        </div>
        <div class="kpi-container" style="margin-top: 20px;">
            <div class="kpi-card" style="border-top-color: #28a745;"><div class="kpi-label">최종 예산</div><div class="kpi-val" id="val-budget">0</div></div>
            <div class="kpi-card" style="border-top-color: #ffc107;"><div class="kpi-label">서비스 레벨</div><div class="kpi-val" id="val-eff">0%</div></div>
            <div class="kpi-card" style="border-top-color: #ff6b6b;"><div class="kpi-label">인간 중심성</div><div class="kpi-val" id="val-human">0</div></div>
        </div>
        <div style="margin-top: 50px; background: rgba(40,167,69,0.1); padding: 25px; border-radius: 8px; border: 1px dashed #28a745;">
            <p style="color: #28a745; font-weight: bold; font-size: 18px; margin: 0;">✅ 실험이 완료되었습니다. 모든 설계 데이터가 구글 시트에 자동 기록되었습니다.</p>
        </div>
        <button onclick="window.parent.location.reload()" style="margin-top: 30px; padding: 12px 40px; background: #333; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">처음부터 다시하기</button>
    </div>

    <script>
        const tasks = {json.dumps(scenario_data['tasks'])};
        let step = 0; let metrics = {{ cost: 1000, eff: 0, human: 0 }}; let history = []; let selected = null;

        function addChat(text, role, name) {{
            const box = document.getElementById('chat-box');
            const div = document.createElement('div');
            div.className = `msg ${{role}}`;
            div.innerHTML = name ? `<b style="font-size:10px; display:block; margin-bottom:4px; color:#aaa;">${{name}}</b>${{text}}` : text;
            box.appendChild(div);
            box.scrollTop = box.scrollHeight;
        }}

        function render() {{
            if(step >= tasks.length) {{ return; }}
            const t = tasks[step];
            document.getElementById('title').innerText = t.title;
            document.getElementById('desc').innerText = t.desc;
            document.getElementById('code-view').innerText = t.code_base + "\\n    # Waiting for architect's decision...";
            document.getElementById('chat-box').innerHTML = '';
            addChat(`[Module ${{step+1}}] Context Loaded.`, 'system');
            setTimeout(() => addChat(t.context_client, 'client', '박상무 (Client)'), 300);
            setTimeout(() => addChat(t.context_agent, 'agent', '김상담 (Worker)'), 800);
            const box = document.getElementById('opt-box'); box.innerHTML = '';
            t.options.forEach(o => {{
                const card = document.createElement('div'); card.className = 'opt-card';
                card.innerHTML = `<b>${{o.label}}</b><p style="font-size:12px; color:#aaa; margin-top:8px; line-height:1.4;">${{o.desc}}</p>`;
                card.onclick = () => {{
                    selected = o;
                    document.querySelectorAll('.opt-card').forEach(c => c.classList.remove('active'));
                    card.classList.add('active');
                    document.getElementById('code-view').innerText = t.code_base + "\\n    " + o.code;
                    document.getElementById('deploy-btn').classList.add('ready');
                }};
                box.appendChild(card);
            }});
            document.getElementById('deploy-btn').classList.remove('ready');
        }}

        function deploy() {{
            metrics.cost -= selected.cost; metrics.eff += selected.eff; metrics.human += selected.human;
            history.push({{ choice: selected.label, type: selected.type }});
            document.getElementById('budget').innerText = metrics.cost;
            step++;
            if (step >= tasks.length) {{ finish(); }} else {{ selected = null; render(); }}
        }}

        function finish() {{
            document.getElementById('main-ui').style.display = 'none';
            document.getElementById('report').style.display = 'block';
            const agency = Math.round(metrics.human * 1.1 / 6);
            const inclusion = Math.round(metrics.human * 0.9 / 6);
            const sustain = Math.round(metrics.human / 6);
            document.getElementById('val-agency').innerText = agency;
            document.getElementById('val-inclusion').innerText = inclusion;
            document.getElementById('val-sustain').innerText = sustain;
            document.getElementById('val-budget').innerText = Math.max(0, metrics.cost);
            document.getElementById('val-eff').innerText = Math.round(metrics.eff / 6) + "%";
            document.getElementById('val-human').innerText = Math.round(metrics.human / 6);
            let persona = agency > 75 ? "인간 중심의 파트너 (Trusted Partner)" : (agency < 40 ? "냉혹한 효율주의자 (Panopticon)" : "실용적 균형주의자 (Balancer)");
            document.getElementById('persona-text').innerText = "귀하의 아키텍처 페르소나 판정: [" + persona + "]";
            
            // **자동 저장 신호 발송**
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: {{ metrics: metrics, history: history, persona: persona }}
            }}, '*');
        }}
        render();
    </script>
</body>
</html>
"""

# 7. 실행부 및 자동 저장 로직
result = components.html(html_code, height=850)

# JS에서 데이터를 보냈을 때 (6번 완료 직후)
if result and isinstance(result, dict):
    auto_save_to_sheets(result)
