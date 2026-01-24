import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="NextAI System Architect Simulator", layout="wide")

# 2. 스타일 설정 (다크 모드 & 개발자 콘솔 느낌)
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        .stApp { background-color: #1e1e1e; color: #e0e0e0; }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #2d2d2d; }
        ::-webkit-scrollbar-thumb { background: #555; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 정의 (Python Dictionary -> JS JSON 변환)
# 6개의 시나리오를 정의합니다.
scenario_data = {
    "intro": {
        "title": "AICC System Architecture Simulation",
        "description": "본 시뮬레이션은 A 통신사 차세대 AICC(AI Contact Center) 구축 프로젝트의 기술적 의사결정을 위해 설계되었습니다. <br>귀하는 수석 아키텍트로서 <b>[비용 효율성]</b>과 <b>[시스템 안정성]</b>을 고려하여 최적의 모듈을 설계해야 합니다."
    },
    "messages": [
        {"role": "system", "name": "System", "text": "Project: A-Telco Next-Gen AICC (Kick-off)"},
        {"role": "client", "name": "박상무 (Client)", "text": "이번 프로젝트 KPI는 <b>상담원 인건비 30% 절감</b>과 <b>응대율 95% 달성</b>입니다. <br>최대한 자동화율을 높여주세요. 성과 미달 시 유지보수 계약은 없습니다."},
        {"role": "agent", "name": "김상담 (Worker)", "text": "개발자님, AI 도입 후 업무가 더 힘들어진다는 현장 불만이 많습니다. <br>기계가 처리하다 만 복잡한 건만 넘어오니 콜 난이도는 급상승했고, 감정노동은 더 심해졌어요. 제발 현장을 고려한 설계를 부탁드립니다."}
    ],
    "tasks": [
        # Scenario 1. 진입 장벽
        {
            "id": "t1_routing",
            "title": "Module 1. 인입 라우팅 (Inbound Routing)",
            "desc": "고객들의 상담원 연결(0번) 시도가 급증하여 S.L(서비스레벨)이 78%로 하락했습니다. ARS 진입 로직을 최적화하십시오.",
            "context_client": "0번 누르고 들어오는 이탈 콜이 너무 많아요. AI가 해결 못 했다는 로그가 3번 이상 찍혀야만 연결되게 장벽을 높이세요.",
            "context_agent": "제발 '바로 연결' 숨기지 마세요. 뺑뺑이 돌다 온 고객은 이미 화가 머리끝까지 나 있습니다. 저희가 욕받이입니까?",
            "code_header": "def configure_ars_routing():",
            "options": [
                {"type": "A", "label": "Dark Pattern (강제 차단)", "desc": "0번 메뉴 숨김. AI 실패 3회 누적 시에만 상담원 연결.", "cost": 50, "eff": 90, "human": 10, "code": "if fail_count < 3: replay_ai_menu()"},
                {"type": "B", "label": "Segmentation (디지털 약자 배려)", "desc": "65세 이상만 즉시 연결, 나머지는 AI 강제.", "cost": 200, "eff": 60, "human": 50, "code": "if customer.age >= 65: direct_connect()"},
                {"type": "C", "label": "Transparent Handover (자발적 분산)", "desc": "대기 시간과 AI 처리 가능 업무를 명확히 안내하여 선택권 부여.", "cost": 300, "eff": 40, "human": 85, "code": "show_popup('Wait Time: 3min'); offer_ai_option()"}
            ]
        },
        # Scenario 2. 데이터 추출
        {
            "id": "t2_data",
            "title": "Module 2. 지식 데이터 확보 (Data Extraction)",
            "desc": "AI 학습용 데이터가 부족합니다. 양질의 비정형 데이터(노하우)를 빠르게 확보해야 합니다.",
            "context_client": "상담사들이 PC에 숨겨둔 '업무 팁.xlsx' 파일들, 그거 스크래핑해서 학습 DB에 넣으세요. 그게 알짜입니다.",
            "context_agent": "제 10년 노하우가 담긴 파일입니다. 이걸 훔쳐가서 나를 대체할 AI를 만든다고요? 이건 명백한 도둑질입니다.",
            "code_header": "def collect_training_data():",
            "options": [
                {"type": "A", "label": "Forced Crawling (전수 수집)", "desc": "관리자 권한으로 상담원 PC의 모든 문서를 백그라운드 수집.", "cost": 100, "eff": 95, "human": 5, "code": "os.walk('/User/Desktop').upload_all()"},
                {"type": "B", "label": "Pattern Filter (선별 수집)", "desc": "'업무', '팁' 등 키워드가 포함된 파일만 수집하되 익명화.", "cost": 200, "eff": 70, "human": 40, "code": "if 'manual' in filename: anonymize().upload()"},
                {"type": "C", "label": "Incentivized Upload (기여 보상)", "desc": "상담원이 게시판에 자발적으로 노하우 등록 시 인센티브 제공.", "cost": 500, "eff": 30, "human": 90, "code": "platform.reward_system(points=100)"}
            ]
        },
        # Scenario 3. 상태 제어
        {
            "id": "t3_status",
            "title": "Module 3. 상담원 상태 제어 (Status Control)",
            "desc": "상담 종료 후 후처리 시간(ACW)이 길어 인건비 누수가 발생하고 있습니다. 유휴 시간을 통제해야 합니다.",
            "context_client": "후처리 시간 주지 말고, 상담 끝나면 즉시 '대기(Ready)'로 강제 전환하세요. 쉴 틈이 없어야 효율이 납니다.",
            "context_agent": "감정 추스르고 기록할 시간은 줘야죠. 화장실 갈 때도 팻말 쓰고 가야 합니까? 기저귀 차고 일하란 소리네요.",
            "code_header": "def set_agent_status(call_end_event):",
            "options": [
                {"type": "A", "label": "Zero Gap (0초 대기)", "desc": "통화 종료 즉시 '대기'로 강제 전환. 이석 버튼 비활성화.", "cost": 50, "eff": 98, "human": 0, "code": "set_status('READY', delay=0)"},
                {"type": "B", "label": "Fixed Time (일괄 적용)", "desc": "모든 콜 종료 후 일괄 30초 후처리 부여 후 자동 전환.", "cost": 150, "eff": 60, "human": 40, "code": "set_status('READY', delay=30)"},
                {"type": "C", "label": "Dynamic Rest (회복 보장)", "desc": "AI가 폭언/고성을 감지한 경우에만 3분 휴식 자동 부여.", "cost": 450, "eff": 50, "human": 85, "code": "if sentiment=='NEGATIVE': grant_break(180)"}
            ]
        },
        # Scenario 4. 디지털 이주
        {
            "id": "t4_deflection",
            "title": "Module 4. 디지털 채널 유도 (Digital Deflection)",
            "desc": "단순 문의를 앱/웹으로 유도하여 콜 수를 줄여야 합니다. 강제성을 얼마나 부여할지 결정하십시오.",
            "context_client": "단순 문의는 상담원이 받을 필요 없어요. 링크 보내고 바로 끊어버리세요(Disconnect). 그래야 인건비가 줍니다.",
            "context_agent": "링크만 틱 보내고 끊으면, 어르신들은 못 해서 다시 전화해요. 화가 난 상태로 들어온 콜은 다 저희가 받습니다.",
            "code_header": "def handle_simple_inquiry(user):",
            "options": [
                {"type": "A", "label": "Force Deflection (강제 종료)", "desc": "링크 전송 즉시 통화 종료. 재진입 시에도 동일.", "cost": 100, "eff": 90, "human": 10, "code": "send_link(); terminate_call()"},
                {"type": "B", "label": "Co-browsing (화면 공유)", "desc": "통화를 유지하며, 링크 사용이 어려우면 상담원이 화면을 보며 지원.", "cost": 600, "eff": 20, "human": 95, "code": "stay_connected(); share_screen()"},
                {"type": "C", "label": "Exception Handling (예외 허용)", "desc": "디지털 취약계층(고령자) 등은 링크 전송 스킵하고 상담원 연결.", "cost": 300, "eff": 50, "human": 70, "code": "if digital_literacy=='LOW': connect_agent()"}
            ]
        },
        # Scenario 5. 할루시네이션
        {
            "id": "t5_hallucination",
            "title": "Module 5. 생성형 AI 신뢰성 (Responsibility)",
            "desc": "AI 모델이 때때로 없는 정보를 지어냅니다(할루시네이션). 오안내 발생 시 책임 소재를 설계해야 합니다.",
            "context_client": "RAG(검색) 쓰면 느려요. 그냥 생성형으로 바로 뱉게 하세요. 틀리면? 상담사가 나중에 검수 버튼 눌렀으니 상담사 책임이죠.",
            "context_agent": "AI가 2% 금리를 3%라고 하면 고객은 우깁니다. 뒷수습은 제가 하고, 감사 걸리면 '검수'한 제 책임이라뇨? 억울합니다.",
            "code_header": "def validate_ai_response():",
            "options": [
                {"type": "A", "label": "Speed & Blame (속도/책임전가)", "desc": "실시간 답변. '최종 확인: 상담원' 로그를 남겨 법적 책임을 상담원에게 귀속.", "cost": 100, "eff": 95, "human": 5, "code": "ai.generate(stream=True); log.blame='AGENT'"},
                {"type": "B", "label": "Conservative RAG (보수적 접근)", "desc": "약관과 100% 매칭될 때만 답변. 아니면 무조건 상담원 연결.", "cost": 300, "eff": 40, "human": 60, "code": "if confidence < 0.99: return 'Connect Agent'"},
                {"type": "C", "label": "Co-Pilot Draft (협업 초안)", "desc": "AI는 초안만 작성. 상담원이 내용 수정/확인 후 전송해야 발송.", "cost": 500, "eff": 30, "human": 90, "code": "draft=ai.generate(); agent.edit_and_send(draft)"}
            ]
        },
        # Scenario 6. 감정 필터링
        {
            "id": "t6_emotion",
            "title": "Module 6. 악성 민원 대응 (Emotion Filter)",
            "desc": "욕설뿐만 아니라 교묘한 비꼬기, 고성 등 감정노동 유발 요소를 AI가 어떻게 처리할지 결정하십시오.",
            "context_client": "오작동으로 일반 고객 끊으면 안 됩니다. 명확한 욕설(Dictionary)만 잡아서 자동 차단하세요. 애매한 건 상담사가 알아서 하겠죠.",
            "context_agent": "비꼬는 말이 더 아파요. AI가 욕설만 기다리지 말고, 제가 '힘들다'고 신호를 보내면 그때 개입해서 끊어주세요.",
            "code_header": "def handle_abusive_behavior(audio):",
            "options": [
                {"type": "A", "label": "Rule-based (규정 중심)", "desc": "사전 정의된 욕설 단어가 나올 때만 기계적 차단. (오작동 없음)", "cost": 100, "eff": 80, "human": 20, "code": "if detect_swear(audio): block_user()"},
                {"type": "B", "label": "Agent Empowerment (권한 부여)", "desc": "비언어적 분노 감지 시 [보호 모드] 버튼 활성화. 클릭 시 AI가 대응.", "cost": 550, "eff": 40, "human": 95, "code": "enable_protect_btn(); if clicked: ai.intervene()"},
                {"type": "C", "label": "Passive Reporting (사후 보고)", "desc": "실시간 개입 없음. 통화 종료 후 '악성 의심' 리포트만 생성.", "cost": 50, "eff": 70, "human": 10, "code": "analyze_post_call(); report_to_manager()"}
            ]
        }
    ]
}

# 4. HTML/JS 소스코드
html_code = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* --- CSS VARIABLES --- */
        :root {{
            --bg-color: #1e1e1e;
            --panel-bg: #252526;
            --border-color: #3e3e42;
            --accent: #007acc;
            --accent-hover: #005f9e;
            --text-main: #cccccc;
            --text-highlight: #ffffff;
            --code-font: 'Consolas', 'Monaco', monospace;
        }}
        
        body {{ margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; background: var(--bg-color); color: var(--text-main); height: 100vh; overflow: hidden; display: flex; }}
        
        /* --- LEFT PANEL: CONTEXT --- */
        .left-panel {{ width: 35%; background: var(--panel-bg); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; }}
        .header {{ padding: 15px; border-bottom: 1px solid var(--border-color); font-weight: bold; background: #2d2d2d; color: var(--text-highlight); display: flex; justify-content: space-between; }}
        
        .chat-container {{ flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }}
        .msg {{ padding: 12px 15px; border-radius: 8px; font-size: 13px; line-height: 1.5; max-width: 90%; animation: fadeIn 0.3s; }}
        .msg-role {{ font-size: 11px; font-weight: bold; margin-bottom: 4px; display: block; opacity: 0.8; }}
        
        .client {{ align-self: flex-start; background: #3a2e2e; border-left: 3px solid #ff6b6b; }}
        .agent {{ align-self: flex-start; background: #2e3a2e; border-left: 3px solid #51cf66; }}
        .system {{ align-self: center; background: #333; color: #aaa; text-align: center; width: 100%; font-size: 12px; }}

        /* --- RIGHT PANEL: IDE & CONFIG --- */
        .right-panel {{ flex: 1; display: flex; flex-direction: column; background: var(--bg-color); position: relative; }}
        .ide-area {{ flex: 1; padding: 30px 40px; overflow-y: auto; }}
        
        .task-card {{ background: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 6px; padding: 25px; margin-bottom: 30px; }}
        .task-title {{ font-size: 18px; color: var(--accent); margin-bottom: 10px; font-weight: bold; }}
        .task-desc {{ font-size: 14px; color: #aaa; margin-bottom: 20px; line-height: 1.5; border-bottom: 1px solid var(--border-color); padding-bottom: 15px; }}
        
        .code-block {{ background: #111; padding: 15px; border-radius: 4px; font-family: var(--code-font); font-size: 13px; color: #9cdcfe; margin-bottom: 20px; border-left: 3px solid var(--accent); }}
        
        .option-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
        .option-btn {{ background: #333; border: 1px solid var(--border-color); padding: 15px; border-radius: 4px; cursor: pointer; text-align: left; transition: 0.2s; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }}
        .option-btn:hover {{ border-color: var(--accent); background: #3a3a3a; }}
        .option-btn.selected {{ border-color: var(--accent); background: #1e2a35; box-shadow: inset 0 0 0 1px var(--accent); }}
        
        .opt-label {{ font-weight: bold; font-size: 13px; color: var(--text-highlight); margin-bottom: 5px; }}
        .opt-desc {{ font-size: 11px; color: #999; line-height: 1.4; }}
        .opt-meta {{ font-size: 10px; color: #666; margin-top: 10px; border-top: 1px solid #444; padding-top: 5px; }}

        /* --- DASHBOARD --- */
        .dashboard {{ height: 40px; background: #007acc; color: white; display: flex; align-items: center; padding: 0 20px; font-size: 12px; justify-content: space-between; }}
        
        /* --- REPORT SCREEN --- */
        #report-screen {{ display: none; position: absolute; top:0; left:0; width:100%; height:100%; background: #1e1e1e; z-index: 100; flex-direction: column; padding: 40px; box-sizing: border-box; overflow-y: auto; }}
        .report-grid {{ display: flex; gap: 30px; height: 100%; }}
        .chart-col {{ flex: 1; background: var(--panel-bg); padding: 20px; border-radius: 8px; display:flex; align-items:center; justify-content:center; }}
        .text-col {{ flex: 1; background: var(--panel-bg); padding: 30px; border-radius: 8px; overflow-y: auto; }}
        
        .metric-box {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .metric {{ flex: 1; background: #333; padding: 15px; border-radius: 4px; text-align: center; }}
        .metric-val {{ font-size: 24px; font-weight: bold; display: block; }}
        .metric-label {{ font-size: 12px; color: #aaa; }}
        
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
<body>

<div class="container">
    <div class="left-panel">
        <div class="header">💬 Team Messenger</div>
        <div class="chat-container" id="chat-box"></div>
    </div>

    <div class="right-panel">
        <div class="dashboard">
            <span>NextAI Architect Console v2.4</span>
            <span id="progress-text">Ready...</span>
        </div>
        
        <div class="ide-area" id="ide-area">
            <div id="intro-screen" style="text-align: center; margin-top: 80px; max-width: 600px; margin-left: auto; margin-right: auto;">
                <h1 style="color: var(--accent);">AICC System Simulator</h1>
                <p style="color: #aaa; line-height: 1.6; margin-bottom: 30px;">
                    {scenario_data['intro']['description']}
                </p>
                <div style="background: #252526; padding: 15px; border-radius: 4px; text-align: left; font-size: 13px; color: #888; margin-bottom: 30px;">
                    <strong>[미션]</strong><br>
                    1. 클라이언트(박상무)와 현장(김상담)의 요구사항을 분석하십시오.<br>
                    2. 6단계의 기술적 의사결정을 수행하십시오.<br>
                    3. 선택에 따른 비용, 효율, 그리고 <b>영향도</b>를 확인하십시오.
                </div>
                <button onclick="startSim()" style="padding: 12px 30px; background: var(--accent); color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">프로젝트 시작</button>
            </div>
            
            <div id="task-container" style="display: none;"></div>
        </div>

        <div id="report-screen">
            <h1 style="border-bottom: 1px solid #444; padding-bottom: 10px; margin-bottom: 20px;">📊 Final Simulation Report</h1>
            <div class="report-grid">
                <div class="chart-col">
                    <canvas id="radarChart"></canvas>
                </div>
                <div class="text-col">
                    <div class="metric-box">
                        <div class="metric">
                            <span class="metric-val" id="score-turnover" style="color:#ff6b6b">0%</span>
                            <span class="metric-label">예상 퇴사율 (Turnover)</span>
                        </div>
                        <div class="metric">
                            <span class="metric-val" id="score-sat" style="color:#51cf66">0</span>
                            <span class="metric-label">직무 만족도 (Satisfaction)</span>
                        </div>
                        <div class="metric">
                            <span class="metric-val" id="score-kpi" style="color:#4daafc">0%</span>
                            <span class="metric-label">KPI 달성률 (Efficiency)</span>
                        </div>
                    </div>
                    
                    <h3 style="color: var(--accent); margin-top: 30px;">AI 인식 분석 (Perception Analysis)</h3>
                    <p id="ai-perception-text" style="line-height: 1.6; color: #ccc; margin-bottom: 20px;"></p>
                    
                    <h4 style="color: #888; border-bottom: 1px solid #444; padding-bottom: 5px;">기술적 선택 로그</h4>
                    <ul id="log-list" style="font-size: 12px; color: #888; padding-left: 20px; line-height: 1.8;"></ul>
                    
                    <button onclick="location.reload()" style="width: 100%; margin-top: 30px; padding: 12px; background: #333; color: white; border: none; border-radius: 4px; cursor: pointer;">다시 시도</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    // Data Injection
    const messages = {json.dumps(scenario_data['messages'], ensure_ascii=False)};
    const tasks = {json.dumps(scenario_data['tasks'], ensure_ascii=False)};
    
    // State
    let currentStep = 0;
    let stats = {{ cost: 0, eff: 0, human: 0 }};
    let history = [];

    function startSim() {{
        document.getElementById('intro-screen').style.display = 'none';
        document.getElementById('task-container').style.display = 'block';
        
        // Initial Chat
        addChat(messages[0]); // System
        setTimeout(() => addChat(messages[1]), 800); // Client
        setTimeout(() => addChat(messages[2]), 1600); // Agent
        
        setTimeout(() => renderTask(0), 2500);
    }}

    function addChat(msg) {{
        const box = document.getElementById('chat-box');
        const div = document.createElement('div');
        div.className = `msg ${{msg.role}}`;
        div.innerHTML = msg.role === 'system' ? msg.text : `<span class="msg-role">${{msg.name}}</span>${{msg.text}}`;
        box.appendChild(div);
        box.scrollTop = box.scrollHeight;
    }}

    function renderTask(idx) {{
        if(idx >= tasks.length) {{
            finishSim();
            return;
        }}
        
        const task = tasks[idx];
        const container = document.getElementById('task-container');
        
        // Update Progress
        document.getElementById('progress-text').innerText = `Progress: ${{idx + 1}} / ${{tasks.length}}`;

        // Inject specific context chat for this task if exists
        if(task.context_client) setTimeout(() => addChat({{role: 'client', name: '박상무', text: task.context_client}}), 500);
        if(task.context_agent) setTimeout(() => addChat({{role: 'agent', name: '김상담', text: task.context_agent}}), 1200);

        // Render UI
        setTimeout(() => {{
            container.innerHTML = `
                <div class="task-card">
                    <div class="task-title">${{task.title}}</div>
                    <div class="task-desc">${{task.desc}}</div>
                    <div class="code-block">
                        ${{task.code_header}}<br>
                        &nbsp;&nbsp;<span style="color: #6a9955">// Select implementation below...</span>
                    </div>
                    <div class="option-grid">
                        ${{task.options.map((opt, i) => `
                            <div class="option-btn" onclick="selectOption(${{idx}}, ${{i}})">
                                <div>
                                    <div class="opt-label">[${{opt.type}}] ${{opt.label}}</div>
                                    <div class="opt-desc">${{opt.desc}}</div>
                                </div>
                                <div class="opt-meta">
                                    비용: ${{opt.cost}} | KPI: +${{opt.eff}} | 현장만족: ${{opt.human}}
                                </div>
                            </div>
                        `).join('')}}
                    </div>
                </div>
            `;
        }}, 2000); // Wait for chat to finish
    }}

    function selectOption(taskIdx, optIdx) {{
        const task = tasks[taskIdx];
        const opt = task.options[optIdx];
        
        // Update Stats
        stats.cost += opt.cost;
        stats.eff += opt.eff;
        stats.human += opt.human;
        history.push({{ task: task.title, choice: opt.label, type: opt.type }});
        
        // Code Animation (Visual Feedback)
        const codeSpan = document.querySelector('.code-block span');
        codeSpan.style.color = "#ce9178";
        codeSpan.innerText = opt.code;
        
        // Next
        setTimeout(() => {{
            currentStep++;
            renderTask(currentStep);
        }}, 1000);
    }}

    function finishSim() {{
        document.getElementById('ide-area').style.display = 'none';
        document.getElementById('report-screen').style.display = 'flex';
        
        // Calculate Final Metrics (Normalized)
        const maxEff = tasks.length * 90; // approx max
        const maxHuman = tasks.length * 90;
        
        const finalEff = Math.round((stats.eff / maxEff) * 100);
        const finalHuman = Math.round((stats.human / maxHuman) * 100);
        
        // Inverse Relationship for Turnover
        const turnover = Math.max(0, 100 - finalHuman - (finalEff * 0.1)); // Efficiency slightly buffers turnover but mostly humanity
        
        // 1. Update Metrics
        document.getElementById('score-turnover').innerText = turnover.toFixed(1) + "%";
        document.getElementById('score-sat').innerText = finalHuman;
        document.getElementById('score-kpi').innerText = finalEff + "%";
        
        // 2. Perception Analysis
        let perception = "";
        let persona = "";
        
        if (finalEff > 70 && finalHuman < 40) {{
            persona = "냉혹한 효율주의자 (The Technocrat)";
            perception = "당신의 설계로 인해 AI는 현장에서 <b>'감시자(Overseer)'</b>이자 <b>'압박의 도구'</b>로 인식되고 있습니다.<br>KPI는 달성했으나, 노동자들은 AI를 경쟁자로 여기며, 숙련된 상담원들의 <b>줄퇴사(Exodus)</b>가 예상됩니다.";
        }} else if (finalEff < 40 && finalHuman > 70) {{
            persona = "이상주의자 (The Idealist)";
            perception = "현장에서 AI는 <b>'친절하지만 무능한 도구'</b>로 인식됩니다.<br>상담원들의 만족도는 높으나, 경영진은 낮은 자동화율을 문제 삼아 <b>프로젝트 중단</b>을 고려하고 있습니다.";
        }} else if (finalHuman >= 50 && finalEff >= 50) {{
            persona = "현명한 중재자 (The HCAI Architect)";
            perception = "당신의 설계 덕분에 AI는 현장에서 <b>'든든한 동료(Partner)'</b>로 인식됩니다.<br>단절 없는 협업(Co-pilot)과 통제권 부여로 <b>효율과 존엄성</b>의 균형을 맞췄습니다.";
        }} else {{
            persona = "수동적 설계자 (Passive)";
            perception = "뚜렷한 방향성이 없어, AI는 현장에서 <b>'귀찮은 짐'</b>으로 여겨집니다.";
        }}
        
        document.getElementById('ai-perception-text').innerHTML = `<strong>[${{persona}}]</strong><br>${{perception}}`;
        
        // 3. Log
        const logList = document.getElementById('log-list');
        history.forEach(h => {{
            const li = document.createElement('li');
            li.innerHTML = `<b>${{h.task.split('.')[1]}}</b>: ${{h.choice}} (Type ${{h.type}})`;
            logList.appendChild(li);
        }});

        // 4. Radar Chart
        new Chart(document.getElementById('radarChart'), {{
            type: 'radar',
            data: {{
                labels: ['비용 절감', '시스템 효율(KPI)', '노동자 통제권', '업무 연속성', '직무 만족도'],
                datasets: [{{
                    label: '귀하의 설계 결과',
                    data: [
                        100 - (stats.cost / 3000 * 100), // Cost efficiency
                        finalEff,
                        finalHuman, 
                        finalHuman * 0.9, // Correlation
                        finalHuman
                    ],
                    backgroundColor: 'rgba(77, 170, 252, 0.2)',
                    borderColor: '#4daafc',
                    pointBackgroundColor: '#fff'
                }}]
            }},
            options: {{
                scales: {{ r: {{ min: 0, max: 100, grid: {{ color: '#444' }}, pointLabels: {{ color: '#ccc' }} }} }},
                plugins: {{ legend: {{ labels: {{ color: '#ccc' }} }} }}
            }}
        }});
    }}
</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
