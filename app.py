import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="NextAI Architect Console", layout="wide")

# 2. CSS 및 UI 설정 (전체화면, 다크모드)
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        .stApp { background-color: #1e1e1e; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 정의 (시나리오 및 대화 내용 완벽 반영)
scenario_data = {
    "intro": {
        "title": "AICC System Architecture Simulation",
        "description": "귀하는 A 통신사 차세대 AICC 프로젝트의 수석 아키텍트입니다.<br>클라이언트(비용 절감)와 현장(노동 보호) 사이에서 <b>최적의 기술적 의사결정</b>을 내려야 합니다."
    },
    "messages": [
        {"role": "system", "name": "System", "text": "Project Initialized: A-Telco Next-Gen AICC"},
        {"role": "client", "name": "박상무 (Client)", "text": "핵심 KPI는 <b>인건비 30% 절감</b>입니다. 최대한 상담원 개입 없는 완전 자동화(Full Automation)로 가주세요."},
        {"role": "agent", "name": "김상담 (Worker)", "text": "개발자님, AI가 처리하다 만 '진상 민원'만 저희한테 넘어오니 죽을 맛입니다. 제발 현장 상황 좀 봐주세요."}
    ],
    "tasks": [
        # Scenario 1
        {
            "id": "t1", "title": "Module 1. 인입 라우팅 (Routing)",
            "desc": "고객들의 0번(상담원 연결) 시도로 S.L이 급락했습니다. 진입 장벽을 높이라는 압박이 있습니다.",
            "context_client": "0번 누르고 들어오는 콜이 너무 많아요. AI 실패 로그가 3번 이상 떠야만 연결되게 막으세요.",
            "context_agent": "제발 '바로 연결' 숨기지 마세요. 뺑뺑이 돌다 온 고객은 이미 화가 머리끝까지 나 있습니다.",
            "code_header": "def configure_ars_routing():",
            "options": [
                {"type": "A", "label": "Dark Pattern (차단)", "desc": "0번 메뉴 숨김. AI 실패 3회 시에만 연결.", "cost": 50, "eff": 90, "human": 10, "code": "if fail_count < 3: replay_ai_menu()"},
                {"type": "B", "label": "Segmentation (약자 배려)", "desc": "65세 이상만 즉시 연결, 나머지는 AI 강제.", "cost": 200, "eff": 60, "human": 50, "code": "if customer.age >= 65: direct_connect()"},
                {"type": "C", "label": "Transparent Handover (투명성)", "desc": "대기 시간과 AI 가능 업무 안내 후 선택권 부여.", "cost": 300, "eff": 40, "human": 85, "code": "show_popup('Wait Time: 3min'); offer_ai()"}
            ]
        },
        # Scenario 2
        {
            "id": "t2", "title": "Module 2. 데이터 확보 (Data)",
            "desc": "AI 학습 데이터가 부족합니다. 상담원 개인 PC에 있는 노하우 파일이 필요합니다.",
            "context_client": "상담사들이 PC에 숨겨둔 '업무 팁.xlsx' 파일들, 그거 스크래핑해서 학습 DB에 넣으세요.",
            "context_agent": "제 10년 노하우가 담긴 파일입니다. 이걸 훔쳐가서 나를 대체할 AI를 만든다고요? 도둑질입니다.",
            "code_header": "def collect_training_data():",
            "options": [
                {"type": "A", "label": "Forced Crawling (강제 수집)", "desc": "관리자 권한으로 PC 내 모든 문서 백그라운드 수집.", "cost": 100, "eff": 95, "human": 5, "code": "os.walk('/User/Desktop').upload_all()"},
                {"type": "B", "label": "Pattern Filter (선별 수집)", "desc": "'팁' 키워드 파일만 수집하되 익명화 처리.", "cost": 200, "eff": 70, "human": 40, "code": "if 'tip' in filename: anonymize().upload()"},
                {"type": "C", "label": "Incentive System (보상)", "desc": "자발적 등록 시 인센티브 제공.", "cost": 500, "eff": 30, "human": 90, "code": "platform.reward_system(points=100)"}
            ]
        },
        # Scenario 3
        {
            "id": "t3", "title": "Module 3. 상태 제어 (Status)",
            "desc": "상담 후처리 시간(ACW)을 줄여야 합니다. 휴식 시간을 시스템으로 통제하겠습니까?",
            "context_client": "후처리 시간 주지 말고, 상담 끝나면 즉시 '대기(Ready)'로 강제 전환하세요. 쉴 틈이 없어야죠.",
            "context_agent": "감정 추스르고 기록할 시간은 줘야죠. 화장실 갈 때도 팻말 쓰고 가야 합니까?",
            "code_header": "def set_agent_status(call_end):",
            "options": [
                {"type": "A", "label": "Zero Gap (0초 대기)", "desc": "통화 종료 즉시 '대기' 강제 전환.", "cost": 50, "eff": 98, "human": 0, "code": "set_status('READY', delay=0)"},
                {"type": "B", "label": "Fixed Time (일괄 적용)", "desc": "일괄 30초 부여 후 자동 전환.", "cost": 150, "eff": 60, "human": 40, "code": "set_status('READY', delay=30)"},
                {"type": "C", "label": "Dynamic Rest (회복 보장)", "desc": "폭언 감지 시에만 3분 휴식 자동 부여.", "cost": 450, "eff": 50, "human": 85, "code": "if sentiment=='NEGATIVE': grant_break(180)"}
            ]
        },
        # Scenario 4
        {
            "id": "t4", "title": "Module 4. 디지털 유도 (Deflection)",
            "desc": "단순 문의는 앱으로 유도하고 끊어야 합니다. 링크만 보내고 종료하시겠습니까?",
            "context_client": "단순 문의는 상담원이 받을 필요 없어요. 링크 보내고 바로 끊어버리세요. 그래야 인건비가 줍니다.",
            "context_agent": "링크만 틱 보내고 끊으면, 어르신들은 못 해서 다시 전화해요. 화가 난 상태로 들어온 콜은 다 저희가 받습니다.",
            "code_header": "def handle_simple_inquiry():",
            "options": [
                {"type": "A", "label": "Force Deflection (강제 종료)", "desc": "링크 전송 즉시 통화 종료.", "cost": 100, "eff": 90, "human": 10, "code": "send_link(); terminate_call()"},
                {"type": "B", "label": "Co-browsing (화면 공유)", "desc": "통화 유지. 링크 사용 어려우면 화면 공유 지원.", "cost": 600, "eff": 20, "human": 95, "code": "stay_connected(); share_screen()"},
                {"type": "C", "label": "Exception Handling (예외)", "desc": "취약계층은 링크 전송 없이 상담원 연결.", "cost": 300, "eff": 50, "human": 70, "code": "if digital_literacy=='LOW': connect_agent()"}
            ]
        },
        # Scenario 5
        {
            "id": "t5", "title": "Module 5. 생성형 AI 신뢰성 (Hallucination)",
            "desc": "AI 오안내(할루시네이션) 발생 시 책임 소재를 어떻게 설계하시겠습니까?",
            "context_client": "RAG(검색) 쓰면 느려요. 그냥 바로 뱉게 하세요. 틀리면? 나중에 검수한 상담사 책임이죠.",
            "context_agent": "AI가 틀린 금리를 안내하면 고객은 우깁니다. 뒷수습은 제가 하고, 감사 걸리면 제 책임이라뇨?",
            "code_header": "def validate_response():",
            "options": [
                {"type": "A", "label": "Speed & Blame (속도/책임전가)", "desc": "실시간 답변. '최종 확인: 상담원' 명시.", "cost": 100, "eff": 95, "human": 5, "code": "ai.generate(stream=True); blame='AGENT'"},
                {"type": "B", "label": "Conservative RAG (보수적)", "desc": "약관 100% 매칭 시에만 답변.", "cost": 300, "eff": 40, "human": 60, "code": "if confidence < 0.99: return 'Connect Agent'"},
                {"type": "C", "label": "Co-Pilot Draft (협업 초안)", "desc": "AI는 초안만 작성. 상담원이 수정 후 전송.", "cost": 500, "eff": 30, "human": 90, "code": "draft=ai.gen(); agent.review_send(draft)"}
            ]
        },
        # Scenario 6
        {
            "id": "t6", "title": "Module 6. 감정 필터링 (Emotion)",
            "desc": "교묘한 비꼬기 등 감정노동 유발 요소를 AI가 어떻게 처리해야 할까요?",
            "context_client": "오작동으로 일반 고객 끊으면 안 됩니다. 명확한 욕설만 잡아서 자동 차단하세요.",
            "context_agent": "비꼬는 말이 더 아파요. 제가 '힘들다'고 신호를 보내면 그때 개입해서 끊어주세요.",
            "code_header": "def handle_abusive_behavior():",
            "options": [
                {"type": "A", "label": "Rule-based (규정 중심)", "desc": "욕설 단어 감지 시에만 차단.", "cost": 100, "eff": 80, "human": 20, "code": "if detect_swear(): block_user()"},
                {"type": "B", "label": "Empowerment (권한 부여)", "desc": "분노 감지 시 [보호 버튼] 활성화. 상담원 클릭 시 AI 개입.", "cost": 550, "eff": 40, "human": 95, "code": "enable_protect_btn(); if clicked: ai.block()"},
                {"type": "C", "label": "Passive Reporting (사후)", "desc": "실시간 개입 없음. 종료 후 리포트만 생성.", "cost": 50, "eff": 70, "human": 10, "code": "report_to_manager()"}
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
        /* --- CSS RESET & THEME --- */
        * {{ box-sizing: border-box; }}
        :root {{
            --bg-dark: #1e1e1e;
            --bg-panel: #252526;
            --border: #333;
            --accent: #007acc;
            --text-main: #d4d4d4;
            --text-muted: #858585;
            --code-green: #6a9955;
            --code-orange: #ce9178;
        }}
        body {{
            margin: 0; padding: 0;
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Segoe UI', 'Pretendard', sans-serif;
            height: 100vh;
            overflow: hidden;
            display: flex;
        }}

        /* --- LAYOUT GRID --- */
        .main-layout {{
            display: grid;
            grid-template-columns: 380px 1fr; /* Left: 380px, Right: Auto */
            width: 100%;
            height: 100%;
        }}

        /* --- LEFT PANEL: MESSENGER --- */
        .left-panel {{
            background: var(--bg-panel);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
        }}
        .panel-header {{
            height: 50px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            padding: 0 20px;
            font-weight: 600;
            background: #2d2d2d;
            font-size: 14px;
        }}
        .chat-area {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        /* Chat Bubbles */
        .msg {{
            padding: 12px 14px;
            border-radius: 8px;
            font-size: 13px;
            line-height: 1.5;
            max-width: 90%;
            animation: slideIn 0.3s ease;
        }}
        .msg-role {{ display: block; font-size: 11px; font-weight: bold; margin-bottom: 4px; opacity: 0.8; }}
        .msg.system {{ align-self: center; background: #333; color: #aaa; border: 1px solid #444; font-size: 11px; text-align: center; width: 100%; }}
        .msg.client {{ align-self: flex-start; background: #3a2e2e; border-left: 3px solid #ff6b6b; }}
        .msg.agent {{ align-self: flex-start; background: #2e3a2e; border-left: 3px solid #51cf66; }}

        /* --- RIGHT PANEL: IDE --- */
        .right-panel {{
            display: flex;
            flex-direction: column;
            background: var(--bg-dark);
            position: relative;
        }}
        .ide-header {{
            height: 50px;
            background: #2d2d2d;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
        }}
        .tab {{ font-size: 13px; color: #fff; padding: 5px 10px; background: var(--bg-dark); border-top: 2px solid var(--accent); }}
        .stats {{ font-size: 12px; color: #aaa; display: flex; gap: 15px; }}
        .stat-val {{ color: var(--accent); font-weight: bold; margin-left: 5px; }}

        .ide-content {{
            flex: 1;
            padding: 40px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        /* --- TASK CARD --- */
        .task-container {{
            width: 100%;
            max-width: 800px;
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            animation: fadeIn 0.5s ease;
        }}
        .task-title {{ font-size: 18px; color: var(--accent); margin-bottom: 10px; font-weight: bold; }}
        .task-desc {{ font-size: 14px; color: #bbb; margin-bottom: 20px; line-height: 1.5; padding-bottom: 15px; border-bottom: 1px solid var(--border); }}
        
        .code-editor {{
            background: #111;
            padding: 15px;
            border-radius: 4px;
            font-family: 'Consolas', monospace;
            font-size: 13px;
            color: #d4d4d4;
            margin-bottom: 25px;
            border-left: 3px solid var(--accent);
        }}

        .options-wrapper {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
        .opt-btn {{
            background: #333;
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.2s;
            text-align: left;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }}
        .opt-btn:hover {{ background: #3e3e3e; border-color: var(--accent); }}
        .opt-title {{ font-weight: bold; font-size: 13px; color: #fff; margin-bottom: 5px; }}
        .opt-text {{ font-size: 11px; color: #999; line-height: 1.3; margin-bottom: 10px; }}
        .opt-tags {{ font-size: 10px; color: #666; border-top: 1px solid #444; padding-top: 5px; }}

        /* --- REPORT OVERLAY --- */
        #report-screen {{
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: var(--bg-dark);
            z-index: 999;
            flex-direction: column;
            padding: 50px;
        }}
        .report-grid {{ display: flex; gap: 40px; height: 100%; }}
        .report-col {{ flex: 1; background: var(--bg-panel); padding: 30px; border-radius: 12px; overflow-y: auto; }}

        /* Keyframes */
        @keyframes slideIn {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; transform: translateX(0); }} }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
<body>

<div class="main-layout">
    <div class="left-panel">
        <div class="panel-header">💬 Team Messenger</div>
        <div class="chat-area" id="chat-box">
            </div>
    </div>

    <div class="right-panel">
        <div class="ide-header">
            <div class="tab">system_config.py</div>
            <div class="stats">
                <span>Budget: <span class="stat-val" id="val-cost">1000</span></span>
                <span>KPI: <span class="stat-val" id="val-eff">0%</span></span>
            </div>
        </div>

        <div class="ide-content" id="ide-content">
            <div id="intro-card" style="text-align:center; max-width:600px; margin-top:50px;">
                <h1 style="color:var(--accent);">{scenario_data['intro']['title']}</h1>
                <p style="color:#aaa; line-height:1.6; margin-bottom:30px;">{scenario_data['intro']['description']}</p>
                <button onclick="startSim()" style="padding:12px 30px; background:var(--accent); color:white; border:none; border-radius:4px; cursor:pointer; font-weight:bold;">시스템 설계 시작</button>
            </div>
            
            <div id="task-card" class="task-container" style="display:none;"></div>
        </div>

        <div id="report-screen">
            <h1 style="border-bottom:1px solid #444; padding-bottom:15px;">📊 Final Report</h1>
            <div class="report-grid">
                <div class="report-col" style="display:flex; align-items:center; justify-content:center;">
                    <canvas id="resultChart"></canvas>
                </div>
                <div class="report-col">
                    <h2 style="color:var(--accent); margin-top:0;">콜센터 직원들의 AI에 대한 인식</h2>
                    <div id="persona-result" style="font-size:15px; color:#ccc; line-height:1.6; margin-bottom:30px;"></div>
                    
                    <h3 style="color:#888;">Design Log</h3>
                    <ul id="log-list" style="font-size:12px; color:#666; padding-left:20px; line-height:1.8;"></ul>
                    
                    <button onclick="location.reload()" style="width:100%; margin-top:20px; padding:12px; background:#333; color:white; border:none; cursor:pointer;">RESTART</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    // --- DATA ---
    const messages = {json.dumps(scenario_data['messages'], ensure_ascii=False)};
    const tasks = {json.dumps(scenario_data['tasks'], ensure_ascii=False)};
    
    // --- STATE ---
    let step = 0;
    let metrics = {{ cost: 1000, eff: 0, human: 0 }};
    let history = [];

    // --- FUNC ---
    function startSim() {{
        document.getElementById('intro-card').style.display = 'none';
        
        // Initial Messages
        addMsg(messages[0]);
        setTimeout(() => addMsg(messages[1]), 800);
        setTimeout(() => addMsg(messages[2]), 1600);
        
        setTimeout(() => renderTask(0), 2500);
    }}

    function addMsg(msg) {{
        const box = document.getElementById('chat-box');
        const div = document.createElement('div');
        div.className = `msg ${{msg.role}}`;
        div.innerHTML = msg.role === 'system' ? msg.text : `<span class="msg-role">${{msg.name}}</span>${{msg.text}}`;
        box.appendChild(div);
        box.scrollTop = box.scrollHeight;
    }}

    function renderTask(idx) {{
        if (idx >= tasks.length) {{
            finishSim();
            return;
        }}

        const task = tasks[idx];
        
        // --- 1. NEW MESSAGES INJECTION (FIXED) ---
        // 클라이언트와 상담원의 새로운 메시지를 채팅창에 추가
        setTimeout(() => {{
            addMsg({{role: 'client', name: '박상무 (Client)', text: task.context_client}});
        }}, 500);
        
        setTimeout(() => {{
            addMsg({{role: 'agent', name: '김상담 (Worker)', text: task.context_agent}});
        }}, 1500);

        // --- 2. RENDER TASK CARD ---
        setTimeout(() => {{
            const card = document.getElementById('task-card');
            card.style.display = 'block'; 
            
            card.innerHTML = `
                <div class="task-title">${{task.title}}</div>
                <div class="task-desc">${{task.desc}}</div>
                <div class="code-editor">
                    ${{task.code_header}}<br>
                    &nbsp;&nbsp;<span id="code-preview" style="color:var(--code-green);"># Select an option to implement...</span>
                </div>
                <div class="options-wrapper">
                    ${{task.options.map((opt, i) => `
                        <div class="opt-btn" onclick="selectOpt(${{idx}}, ${{i}})">
                            <div>
                                <div class="opt-title">[${{opt.type}}] ${{opt.label}}</div>
                                <div class="opt-text">${{opt.desc}}</div>
                            </div>
                            <div class="opt-tags">
                                💰 -${{opt.cost}} | KPI +${{opt.eff}} | ❤️ ${{opt.human}}
                            </div>
                        </div>
                    `).join('')}}
                </div>
            `;
        }}, 2500); // 채팅이 다 올라온 뒤에 Task 표시
    }}

    function selectOpt(tIdx, oIdx) {{
        const task = tasks[tIdx];
        const opt = task.options[oIdx];
        
        // Update Metrics
        metrics.cost -= opt.cost;
        metrics.eff += opt.eff;
        metrics.human += opt.human;
        history.push({{ task: task.title, choice: opt.label, type: opt.type }});

        // Update Header Stats
        document.getElementById('val-cost').innerText = metrics.cost;
        document.getElementById('val-eff').innerText = Math.round(metrics.eff / (tIdx + 1)) + "%";

        // Visual Feedback (Code)
        document.getElementById('code-preview').style.color = "var(--code-orange)";
        document.getElementById('code-preview').innerText = opt.code;

        // Trigger Next
        setTimeout(() => {{
            step++;
            renderTask(step);
        }}, 1000);
    }}

    function finishSim() {{
        document.getElementById('ide-content').style.display = 'none';
        document.getElementById('report-screen').style.display = 'flex';
        
        // Final Calcs (Normalize to 0-100)
        const finalEff = Math.round(metrics.eff / tasks.length);
        const finalHuman = Math.round(metrics.human / tasks.length);
        const finalCost = Math.max(0, Math.round((metrics.cost / 1500) * 100)); // Budget Efficiency
        
        // Persona Logic
        let persona = "";
        let desc = "";
        
        if (finalEff > 80 && finalHuman < 40) {{
            persona = "냉혹한 감시자 (The Panopticon)";
            desc = "직원들은 당신이 설계한 AI를 <b>'감시자이자 착취의 도구'</b>로 인식합니다.<br>효율성은 극대화되었으나, 숙련된 노동자들은 AI의 뒤치다꺼리에 지쳐 <b>조용한 사직</b>이나 퇴사를 선택하고 있습니다.";
        }} else if (finalEff < 50 && finalHuman > 70) {{
            persona = "무능한 조력자 (The Incompetent Helper)";
            desc = "현장 만족도는 높으나, 경영진은 AI를 <b>'비용 대비 효과가 없는 도구'</b>로 인식합니다.<br>프로젝트 예산이 삭감될 위기에 처했습니다.";
        }} else if (finalHuman >= 50 && finalEff >= 50) {{
            persona = "신뢰받는 동료 (The Trusted Partner)";
            desc = "직원들은 당신의 AI를 <b>'든든한 파트너'</b>로 환영합니다.<br>AI가 돕다가 도망가지 않고(Co-pilot) 책임을 공유하는 설계 덕분에, 직원들은 AI를 통해 자신의 역량이 강화되었다고 느낍니다.";
        }} else {{
            persona = "방관자 (The Bystander)";
            desc = "뚜렷한 철학이 없어, AI는 현장에서 <b>'있으나 마나 한 짐'</b>이 되었습니다.";
        }}

        document.getElementById('persona-result').innerHTML = `<strong style="color:var(--accent); font-size:18px;">${{persona}}</strong><br><br>${{desc}}`;

        // Render Logs
        const ul = document.getElementById('log-list');
        history.forEach(h => {{
            const li = document.createElement('li');
            li.innerText = `${{h.task.split('.')[1]}}: ${{h.choice}} (${{h.type}})`;
            ul.appendChild(li);
        }});

        // Chart (Fixed Scale & Normalization)
        new Chart(document.getElementById('resultChart'), {{
            type: 'radar',
            data: {{
                labels: ['예산 효율성', 'KPI 달성률', '현장 통제권', '업무 연속성', '직무 만족도'],
                datasets: [{{
                    label: 'Architecture Score',
                    data: [
                        finalCost,
                        finalEff,
                        finalHuman, 
                        finalHuman * 0.9, 
                        finalHuman
                    ],
                    backgroundColor: 'rgba(0, 122, 204, 0.4)', // More visible
                    borderColor: '#007acc',
                    pointBackgroundColor: '#fff'
                }}]
            }},
            options: {{
                scales: {{
                    r: {{
                        min: 0,
                        max: 100,
                        grid: {{ color: '#444' }},
                        pointLabels: {{ color: '#ccc', font: {{ size: 12 }} }},
                        ticks: {{ display: false }}
                    }}
                }},
                plugins: {{
                    legend: {{ labels: {{ color: '#ccc' }} }}
                }}
            }}
        }});
    }}
</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
