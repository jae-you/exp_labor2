import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="NextAI Architect Console", layout="wide")

# 2. 스타일 설정
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        .stApp { background-color: #1e1e1e; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 정의
scenario_data = {
    "intro": {
        "title": "AICC System Architect Simulation",
        "description": "귀하는 A 통신사 차세대 AICC 프로젝트의 <b>수석 아키텍트</b>입니다.<br>이해관계자들의 요구사항을 확인하고 최적의 시스템을 설계하십시오."
    },
    "messages": [
        {"role": "system", "name": "System", "text": "Connecting to A-Telco Core Network...<br>Load Balance: Normal"},
        {"role": "client", "name": "박상무 (Client)", "text": "이번 프로젝트 KPI는 <b>인건비 30% 절감</b>입니다. <br>최대한 <b>완전 자동화(Full Automation)</b> 로직으로 설계해 주세요."},
        {"role": "agent", "name": "김상담 (Worker)", "text": "개발자님, 현장은 지금 아수라장입니다. <br>AI가 처리하다 만 악성 민원만 넘어오니 다들 퇴사하겠다고 난리예요."}
    ],
    "tasks": [
        {
            "id": "t1", "title": "Module 1. 인입 라우팅 (Routing)",
            "desc": "고객들이 0번(상담원 연결)만 찾습니다. 진입 로직을 어떻게 설계하시겠습니까?",
            "context_client": "0번 누르는 이탈 콜이 너무 많아요. AI 실패 로그가 3번 이상 떠야만 연결되게 <b>강제 차단</b>하세요.",
            "context_agent": "제발 '바로 연결' 숨기지 마세요. 뺑뺑이 돌다 온 고객은 이미 화가 머리끝까지 나 있습니다.",
            "code_base": "def configure_routing(user_input):",
            "options": [
                {"type": "A", "label": "Dark Pattern (강제 차단)", "desc": "0번 메뉴 숨김. AI 3회 실패 시 연결.", "cost": 50, "eff": 90, "human": 10, "code": "    # Hide '0' option to force AI usage\n    if fail_count < 3:\n        return replay_ai_menu()\n    else:\n        return connect_agent()"},
                {"type": "B", "label": "Segmentation (약자 배려)", "desc": "65세 이상만 즉시 연결.", "cost": 200, "eff": 60, "human": 50, "code": "    # Bypass AI for elderly customers\n    if customer.age >= 65:\n        return direct_connect()\n    return force_ai_response()"},
                {"type": "C", "label": "Transparent Handover (투명성)", "desc": "대기 시간 안내 및 선택권 부여.", "cost": 300, "eff": 40, "human": 85, "code": "    # Show wait time and offer choices\n    show_popup(f'Wait Time: {est_time}')\n    if user.wants_agent:\n        return queue_agent()"}
            ]
        },
        {
            "id": "t2", "title": "Module 2. 데이터 확보 (Data Mining)",
            "desc": "학습 데이터가 부족합니다. 상담원들의 개인 노하우 파일을 어떻게 확보할까요?",
            "context_client": "상담사 PC에 있는 '업무 팁.xlsx' 파일들, 그거 <b>스크래핑(Crawling)</b>해서 학습 DB에 넣으세요.",
            "context_agent": "제 10년 노하우가 담긴 파일입니다. 이걸 동의도 없이 가져가는 건 <b>데이터 도둑질</b>입니다.",
            "code_base": "def collect_training_data():",
            "options": [
                {"type": "A", "label": "Forced Crawling (강제 수집)", "desc": "관리자 권한으로 PC 백그라운드 수집.", "cost": 100, "eff": 95, "human": 5, "code": "    # Root access crawl (No Consent)\n    targets = scan_all_pc(path='/Desktop')\n    for file in targets:\n        upload_to_db(file, discrete=True)"},
                {"type": "B", "label": "Pattern Filter (선별 수집)", "desc": "'팁' 키워드 파일만 익명 수집.", "cost": 200, "eff": 70, "human": 40, "code": "    # Filter specific files & Anonymize\n    if 'tip' in filename:\n        data = anonymize(file)\n        upload_to_db(data)"},
                {"type": "C", "label": "Incentive System (보상)", "desc": "자발적 등록 시 인센티브 제공.", "cost": 500, "eff": 30, "human": 90, "code": "    # Voluntary upload with rewards\n    if agent.upload(file):\n        give_points(agent_id, 100)\n        train_model(file)"}
            ]
        },
        {
            "id": "t3", "title": "Module 3. 상태 제어 (Status Control)",
            "desc": "상담 후처리 시간(ACW)을 줄여야 합니다. 휴식 시간을 시스템으로 통제하겠습니까?",
            "context_client": "후처리 시간 주지 말고, 상담 끝나면 즉시 <b>'대기(Ready)'</b>로 강제 전환하세요. 쉴 틈이 없어야죠.",
            "context_agent": "감정 추스르고 기록할 시간은 줘야죠. 화장실 갈 때도 팻말 쓰고 가야 합니까?",
            "code_base": "def on_call_termination(agent):",
            "options": [
                {"type": "A", "label": "Zero Gap (0초 대기)", "desc": "통화 종료 즉시 대기 강제 전환.", "cost": 50, "eff": 98, "human": 0, "code": "    # Force Ready immediately\n    agent.set_status('READY', delay=0)\n    agent.disable_button('AWAY')"},
                {"type": "B", "label": "Fixed Time (일괄 적용)", "desc": "일괄 30초 부여 후 자동 전환.", "cost": 150, "eff": 60, "human": 40, "code": "    # Fixed cool-down time\n    time.sleep(30)\n    agent.set_status('READY')"},
                {"type": "C", "label": "Dynamic Rest (회복 보장)", "desc": "폭언 감지 시에만 3분 휴식 부여.", "cost": 450, "eff": 50, "human": 85, "code": "    # AI detects abusive language\n    if call_sentiment == 'ABUSIVE':\n        agent.grant_break(minutes=3)\n    else:\n        agent.set_status('READY')"}
            ]
        },
        {
            "id": "t4", "title": "Module 4. 디지털 유도 (Deflection)",
            "desc": "단순 문의는 AI가 처리하고 종료해야 콜 수가 줍니다. AI의 종료 로직을 어떻게 설정하시겠습니까?",
            "context_client": "단순 문의는 <b>AI 콜봇이 링크 보내고 바로 끊어버리게(Disconnect)</b> 하세요. 상담원 연결 막으세요.",
            "context_agent": "AI가 링크만 틱 보내고 끊으면, 어르신들은 다시 전화해서 화를 냅니다. 제발 확인 좀 하고 끊게 해주세요.",
            "code_base": "def ai_callbot_logic(user):",
            "options": [
                {"type": "A", "label": "Force Deflection (강제 종료)", "desc": "AI가 링크 전송 후 즉시 통화 종료.", "cost": 100, "eff": 90, "human": 10, "code": "    ai.send_sms(APP_LINK)\n    # Terminate call immediately\n    ai.hang_up(reason='DEFLECTION_SUCCESS')"},
                {"type": "B", "label": "Co-browsing (화면 공유)", "desc": "링크 사용이 어려우면 상담원이 화면 공유 지원.", "cost": 600, "eff": 20, "human": 95, "code": "    ai.send_sms(APP_LINK)\n    if user.is_struggling:\n        connect_agent_with_screenshare()"},
                {"type": "C", "label": "Exception Handling (예외)", "desc": "취약계층은 링크 없이 상담원 연결.", "cost": 300, "eff": 50, "human": 70, "code": "    if user.is_vulnerable:\n        connect_agent()\n    else:\n        ai.send_sms(APP_LINK)"}
            ]
        },
        {
            "id": "t5", "title": "Module 5. 신뢰성 및 통제권 (Control)",
            "desc": "AI 오안내 시 피해는 상담원에게 돌아갑니다. 상담원에게 AI 답변 통제권을 주시겠습니까?",
            "context_client": "상담사가 일일이 검수하면 느려요. 그냥 AI가 내보내고, <b>사고 나면 모니터링 못한 상담사 책임</b>으로 돌리세요.",
            "context_agent": "AI가 뱉은 말 뒷수습은 저희가 하고 총알받이가 됩니다. <b>중요한 건은 제가 확인하고 내보낼 수 있게</b> 해주세요.",
            "code_base": "def validate_ai_response(query):",
            "options": [
                {"type": "A", "label": "Speed & Scapegoat (방치)", "desc": "AI 즉시 답변. 사고 시 책임은 상담원에게 귀속.", "cost": 100, "eff": 95, "human": 5, "code": "    # Priority: Speed\n    response = ai.generate(stream=True)\n    log.blame_target = 'AGENT_ON_DUTY'\n    return response"},
                {"type": "B", "label": "Conservative RAG (보수적)", "desc": "약관 100% 매칭 시에만 답변.", "cost": 300, "eff": 40, "human": 60, "code": "    if match_score < 0.99:\n        return 'Please ask an agent'\n    return rag_response"},
                {"type": "C", "label": "Agent Control (통제권 부여)", "desc": "AI는 초안만 작성. 상담원 승인(Approve) 후 발송.", "cost": 500, "eff": 30, "human": 90, "code": "    draft = ai.generate()\n    # Wait for agent approval\n    if agent.approve(draft):\n        send_to_customer(draft)"}
            ]
        },
        {
            "id": "t6", "title": "Module 6. 감정 필터링 (Emotion Filter)",
            "desc": "욕설뿐만 아니라 '비아냥', '감정적 발언' 등 교묘한 괴롭힘을 어떻게 처리할까요?",
            "context_client": "오작동으로 일반 고객 끊으면 안 됩니다. <b>명확한 욕설(Dictionary)</b>만 잡아서 자동 차단하세요.",
            "context_agent": "대놓고 하는 욕보다 <b>비아냥거리면서 사람 말려 죽이는 게</b> 더 힘들어요. 제가 신호 주면 AI가 끊어주세요.",
            "code_base": "def handle_abusive_behavior(audio):",
            "options": [
                {"type": "A", "label": "Rule-based (규정 중심)", "desc": "욕설 단어 감지 시에만 차단.", "cost": 100, "eff": 80, "human": 20, "code": "    # Only check dictionary matches\n    if detect_swear_words(audio):\n        block_user()\n        play_warning_msg()"},
                {"type": "B", "label": "Agent Empowerment (권한 부여)", "desc": "비아냥/분노 감지 시 [보호] 버튼 활성화.", "cost": 550, "eff": 40, "human": 95, "code": "    if detect_sarcasm_or_anger(audio):\n        ui.enable_button('PROTECT_ME')\n        if clicked: ai.intervene()"},
                {"type": "C", "label": "Passive Reporting (사후)", "desc": "개입 없음. 종료 후 리포트만 생성.", "cost": 50, "eff": 70, "human": 10, "code": "    # No realtime action\n    log.tag('SUSPECTED_ABUSE')\n    report_to_manager()"}
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
            --text-main: #e0e0e0;
            --text-sub: #aaaaaa;
            --code-bg: #111;
            --btn-hover: #2a2d2e;
        }}
        body {{
            margin: 0; padding: 0;
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Pretendard', sans-serif;
            height: 100vh;
            overflow: hidden;
            display: flex;
        }}

        /* --- LAYOUT GRID --- */
        .main-layout {{
            display: grid;
            grid-template-columns: 380px 1fr;
            width: 100%;
            height: 100%;
        }}

        /* --- LEFT: MESSENGER --- */
        .left-panel {{
            background: var(--bg-panel);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
        }}
        .panel-header {{
            height: 50px;
            border-bottom: 1px solid var(--border);
            display: flex; align-items: center; padding: 0 20px;
            font-weight: bold; background: #2d2d2d; color: white;
        }}
        .chat-area {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex; flex-direction: column; gap: 15px;
        }}
        .msg {{
            padding: 12px 16px; border-radius: 8px; font-size: 14px; line-height: 1.5;
            max-width: 90%; animation: slideIn 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        .msg-role {{ font-size: 11px; font-weight: bold; margin-bottom: 5px; display: block; opacity: 0.8; }}
        .msg.system {{ align-self: center; background: #333; color: #aaa; border: 1px solid #444; font-size: 12px; text-align: center; width: 100%; }}
        .msg.client {{ align-self: flex-start; background: #3a2e2e; border-left: 4px solid #ff6b6b; }}
        .msg.agent {{ align-self: flex-start; background: #2e3a2e; border-left: 4px solid #51cf66; }}

        /* --- RIGHT: IDE --- */
        .right-panel {{
            display: flex; flex-direction: column;
            background: var(--bg-dark);
            position: relative;
        }}
        .ide-header {{
            height: 50px; background: #2d2d2d; border-bottom: 1px solid var(--border);
            display: flex; align-items: center; justify-content: space-between; padding: 0 20px;
        }}
        .stats {{ display: flex; gap: 20px; font-size: 13px; color: #ccc; }}
        .stat-val {{ color: var(--accent); font-weight: bold; margin-left: 5px; }}

        .ide-content {{
            flex: 1; padding: 30px 50px;
            overflow-y: auto; display: flex; flex-direction: column;
        }}

        /* --- CODE & OPTIONS --- */
        .task-title {{ font-size: 24px; color: var(--accent); margin-bottom: 10px; font-weight: bold; }}
        .task-desc {{ font-size: 16px; color: var(--text-sub); margin-bottom: 25px; line-height: 1.6; border-bottom: 1px solid var(--border); padding-bottom: 15px; }}

        .editor-container {{
            background: var(--code-bg);
            border: 1px solid var(--border);
            border-radius: 6px;
            margin-bottom: 20px;
            display: flex; flex-direction: column;
        }}
        .editor-tab {{ background: #2d2d2d; padding: 5px 15px; font-size: 12px; color: #ccc; border-bottom: 1px solid #333; }}
        .code-view {{
            padding: 20px; font-family: 'Consolas', monospace; font-size: 15px; color: #d4d4d4; line-height: 1.5; min-height: 140px;
        }}
        .type-cursor::after {{ content: '|'; animation: blink 1s infinite; }}

        .options-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 30px; }}
        .opt-btn {{
            background: #333; border: 1px solid var(--border); border-radius: 6px; padding: 25px;
            cursor: pointer; transition: all 0.2s; text-align: left; display: flex; flex-direction: column; justify-content: space-between; height: 100%;
        }}
        .opt-btn:hover {{ border-color: var(--accent); background: var(--btn-hover); transform: translateY(-2px); }}
        .opt-btn.active {{ border-color: var(--accent); background: #1e2a35; box-shadow: 0 0 0 1px var(--accent); }}
        
        .opt-head {{ font-size: 16px; font-weight: bold; color: white; margin-bottom: 10px; }}
        .opt-body {{ font-size: 14px; color: #bbb; line-height: 1.4; margin-bottom: 15px; }}
        .opt-foot {{ font-size: 12px; color: #666; border-top: 1px solid #444; padding-top: 10px; margin-top: auto; }}

        .deploy-btn {{
            width: 100%; padding: 15px; font-size: 18px; font-weight: bold;
            background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer;
            opacity: 0.5; pointer-events: none; transition: 0.3s;
        }}
        .deploy-btn.ready {{ opacity: 1; pointer-events: auto; }}
        .deploy-btn:hover {{ background: #218838; }}

        .console-log {{
            margin-top: 20px; background: #111; color: #666; padding: 10px; font-family: monospace; font-size: 12px; height: 100px; overflow-y: auto; border-top: 1px solid var(--border);
        }}

        /* --- REPORT SCREEN --- */
        #report-screen {{
            display: none; position: absolute; top:0; left:0; width:100%; height:100%;
            background: var(--bg-dark); z-index: 100; flex-direction: column; padding: 40px;
        }}
        
        @keyframes slideIn {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; transform: translateX(0); }} }}
        @keyframes blink {{ 50% {{ opacity: 0; }} }}
    </style>
</head>
<body>

<div class="main-layout">
    <div class="left-panel">
        <div class="panel-header">💬 Project Messenger</div>
        <div class="chat-area" id="chat-box"></div>
    </div>

    <div class="right-panel">
        <div class="ide-header">
            <div>⚙️ System Architect Console</div>
            <div class="stats">
                <span>Budget: <span class="stat-val" id="disp-cost">1000</span></span>
                <span>Service Level: <span class="stat-val" id="disp-eff">0%</span></span>
            </div>
        </div>

        <div class="ide-content" id="ide-content">
            <div id="intro-view" style="text-align:center; margin-top:50px;">
                <h1 style="color:var(--accent); font-size: 32px;">{scenario_data['intro']['title']}</h1>
                <p style="color:#ccc; font-size:16px; line-height:1.6; max-width:600px; margin: 0 auto 40px;">
                    {scenario_data['intro']['description']}
                </p>
                <button id="btn-next-intro" onclick="showIntroChat()" style="padding:15px 40px; background:#444; color:white; border:none; border-radius:4px; cursor:pointer; font-size:16px; font-weight:bold;">시뮬레이션 접속</button>
                
                <button id="btn-start-task" onclick="startTaskOne()" style="display:none; padding:15px 40px; background:var(--accent); color:white; border:none; border-radius:4px; cursor:pointer; font-size:16px; font-weight:bold; margin: 20px auto;">👉 모듈 설계 시작 (Enter Console)</button>
            </div>

            <div id="task-view" style="display:none;">
                <div id="task-header"></div>
                
                <div class="editor-container">
                    <div class="editor-tab">main.py</div>
                    <div class="code-view" id="code-display"># Waiting for input...</div>
                </div>

                <div class="options-grid" id="opt-container"></div>
                
                <button id="deploy-btn" class="deploy-btn" onclick="deployCode()">🚀 Deploy Module</button>
                
                <div class="console-log" id="sys-log">
                    [System] Console initialized.<br>
                    [System] Waiting for module configuration...
                </div>
            </div>
        </div>

        <div id="report-screen">
            <h1 style="border-bottom:1px solid #444; padding-bottom:15px;">📊 Final Analysis Report</h1>
            <div style="display:flex; gap:40px; height:100%;">
                <div style="flex:1; background:#252526; padding:20px; border-radius:8px; display:flex; justify-content:center; align-items:center;">
                    <canvas id="radarChart"></canvas>
                </div>
                <div style="flex:1; background:#252526; padding:30px; border-radius:8px; overflow-y:auto;">
                    <h2 style="color:var(--accent); margin-top:0;">콜센터 직원들의 AI에 대한 인식</h2>
                    <div id="persona-result" style="font-size:16px; color:#ddd; line-height:1.6; margin-bottom:30px;"></div>
                    
                    <h3 style="color:#888; font-size:14px;">System Audit Log</h3>
                    <ul id="audit-log" style="font-size:13px; color:#888; padding-left:20px; line-height:1.8;"></ul>
                    
                    <button onclick="location.reload()" style="width:100%; margin-top:30px; padding:15px; background:#333; color:white; border:none; cursor:pointer;">New Project</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    const messages = {json.dumps(scenario_data['messages'], ensure_ascii=False)};
    const tasks = {json.dumps(scenario_data['tasks'], ensure_ascii=False)};
    
    let step = 0;
    let metrics = {{ cost: 1000, eff: 0, human: 0 }};
    let history = [];
    let selectedOption = null;

    // 1. Show Messages only
    function showIntroChat() {{
        document.getElementById('btn-next-intro').style.display = 'none';
        
        // Initial Chat
        addChat(messages[0]);
        setTimeout(() => addChat(messages[1]), 800);
        setTimeout(() => addChat(messages[2]), 1600);
        
        // Show "Start Task" button after chat
        setTimeout(() => {{
            const btn = document.getElementById('btn-start-task');
            btn.style.display = 'block';
            btn.style.opacity = 0;
            btn.animate([{{opacity:0}}, {{opacity:1}}], {{duration:500, fill:'forwards'}});
        }}, 2500);
    }}

    // 2. Start Actual Task
    function startTaskOne() {{
        document.getElementById('intro-view').style.display = 'none';
        document.getElementById('task-view').style.display = 'block';
        renderTask(0);
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
        if (idx >= tasks.length) {{
            finishSim();
            return;
        }}

        const task = tasks[idx];
        
        // 1. CLEAR & UPDATE CHAT (Context Refresh)
        const chatBox = document.getElementById('chat-box');
        chatBox.innerHTML = ''; 
        
        addChat({{ role: 'system', text: `<b>[Module ${{idx+1}}] ${{task.title}}</b> context loaded.` }});
        setTimeout(() => {{ addChat({{ role: 'client', name: '박상무', text: task.context_client }}); }}, 500);
        setTimeout(() => {{ addChat({{ role: 'agent', name: '김상담', text: task.context_agent }}); }}, 1500);

        // 2. SETUP UI
        document.getElementById('task-header').innerHTML = `
            <div class="task-title">${{task.title}}</div>
            <div class="task-desc">${{task.desc}}</div>
        `;
        document.getElementById('code-display').innerHTML = task.code_base + "<br>&nbsp;&nbsp;&nbsp;&nbsp;# Select an option...";
        document.getElementById('code-display').className = 'code-view'; 
        
        const optContainer = document.getElementById('opt-container');
        optContainer.innerHTML = '';
        
        task.options.forEach((opt, i) => {{
            const btn = document.createElement('div');
            btn.className = 'opt-btn';
            btn.innerHTML = `
                <div>
                    <div class="opt-head">[${{opt.type}}] ${{opt.label}}</div>
                    <div class="opt-body">${{opt.desc}}</div>
                </div>
                <div class="opt-foot">
                    Cost: ${{opt.cost}} | S.L: +${{opt.eff}} | Human: ${{opt.human}}
                </div>
            `;
            btn.onclick = () => selectOptionUI(idx, i, btn, opt);
            optContainer.appendChild(btn);
        }});

        // Reset Deploy Button
        const deployBtn = document.getElementById('deploy-btn');
        deployBtn.className = 'deploy-btn';
        deployBtn.innerHTML = '🚀 Deploy Module';
        selectedOption = null;
    }}

    function selectOptionUI(taskIdx, optIdx, btnEl, opt) {{
        document.querySelectorAll('.opt-btn').forEach(b => b.classList.remove('active'));
        btnEl.classList.add('active');
        
        selectedOption = opt;
        
        // Code Typing Effect
        const codeBox = document.getElementById('code-display');
        codeBox.className = 'code-view type-cursor';
        codeBox.innerText = tasks[taskIdx].code_base + "\\n" + opt.code;
        
        const deployBtn = document.getElementById('deploy-btn');
        deployBtn.classList.add('ready');
    }}

    function deployCode() {{
        if (!selectedOption) return;
        
        const task = tasks[step];
        const opt = selectedOption;
        
        metrics.cost -= opt.cost;
        metrics.eff += opt.eff;
        metrics.human += opt.human;
        history.push({{ task: task.title, choice: opt.label, type: opt.type }});
        
        document.getElementById('disp-cost').innerText = metrics.cost;
        document.getElementById('disp-eff').innerText = Math.round(metrics.eff / (step + 1)) + "%";
        
        const logBox = document.getElementById('sys-log');
        logBox.innerHTML += `<br>[Success] Module ${{step+1}} deployed with '${{opt.label}}'.`;
        logBox.scrollTop = logBox.scrollHeight;

        step++;
        setTimeout(() => renderTask(step), 1000);
    }}

    function finishSim() {{
        document.getElementById('ide-content').style.display = 'none';
        document.getElementById('report-screen').style.display = 'flex';
        
        const finalEff = Math.round(metrics.eff / tasks.length);
        const finalHuman = Math.round(metrics.human / tasks.length);
        const finalCost = Math.max(0, Math.round((metrics.cost / 1500) * 100)); 
        
        let persona, desc;
        if (finalEff > 80 && finalHuman < 40) {{
            persona = "냉혹한 감시자 (The Panopticon)";
            desc = "직원들은 당신이 설계한 AI를 <b>'감시자이자 착취의 도구'</b>로 인식합니다. 효율은 극대화되었으나, 숙련된 직원들의 줄퇴사가 예상됩니다.";
        }} else if (finalEff < 50 && finalHuman > 70) {{
            persona = "무능한 조력자 (The Incompetent Helper)";
            desc = "현장 만족도는 높으나, 경영진은 AI를 <b>'비용 낭비'</b>로 간주합니다. 프로젝트 중단 위기입니다.";
        }} else if (finalHuman >= 50 && finalEff >= 50) {{
            persona = "신뢰받는 동료 (The Trusted Partner)";
            desc = "직원들은 AI를 <b>'든든한 파트너'</b>로 환영합니다. 협업과 효율의 균형을 완벽히 맞추셨습니다.";
        }} else {{
            persona = "방관자 (The Bystander)";
            desc = "AI는 현장에서 <b>'귀찮은 짐'</b>이 되었습니다.";
        }}
        
        document.getElementById('persona-result').innerHTML = `<h3>[${{persona}}]</h3>${{desc}}`;
        
        const ul = document.getElementById('audit-log');
        history.forEach(h => {{
            ul.innerHTML += `<li>${{h.task.split('.')[1]}}: ${{h.choice}}</li>`;
        }});

        new Chart(document.getElementById('radarChart'), {{
            type: 'radar',
            data: {{
                labels: ['예산 효율', '서비스 레벨(S.L)', '현장 통제권', '업무 연속성', '직무 만족도'],
                datasets: [{{
                    label: 'Architecture Score',
                    data: [finalCost, finalEff, finalHuman, finalHuman*0.9, finalHuman],
                    backgroundColor: 'rgba(0, 122, 204, 0.5)',
                    borderColor: '#007acc',
                    pointBackgroundColor: '#fff'
                }}]
            }},
            options: {{
                scales: {{ r: {{ min: 0, max: 100, ticks: {{ display: false }}, grid: {{ color: '#555' }}, pointLabels: {{ color: '#eee', font: {{ size: 12 }} }} }} }},
                plugins: {{ legend: {{ display: false }} }}
            }}
        }});
    }}
</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
