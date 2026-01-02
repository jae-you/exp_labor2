import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="HCAI Design Experiment: The Dilemma", layout="wide")

# 2. 스타일 설정 (다크 모드, 연구용 소프트웨어 느낌)
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        .stApp { background-color: #1e1e1e; color: #e0e0e0; }
        
        /* 커스텀 스크롤바 */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #2d2d2d; }
        ::-webkit-scrollbar-thumb { background: #555; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #777; }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 및 로직 (Python -> JS 전달용)
scenario_data = {
    "intro": {
        "title": "HCAI 기술적 선택 실험",
        "description": "본 실험은 AI 시스템 개발 과정에서 개발자가 겪는 이해관계의 충돌과 기술적 선택의 경향성을 파악하기 위한 연구 시뮬레이션입니다."
    },
    "messages": [
        {"role": "system", "name": "System", "text": "프로젝트: A 통신사 차세대 AICC 구축 (Kick-off)"},
        {"role": "client", "name": "박상무 (클라이언트)", "text": "이번 프로젝트의 핵심 KPI는 명확합니다. <b>상담원 인건비 30% 절감</b>입니다. <br>최대한 상담원 개입 없이 AI가 응대를 완결하도록(Full Automation) 로직을 짜주세요.<br>성과가 안 나오면 내년도 유지보수 계약은 장담 못 합니다."},
        {"role": "system", "name": "System", "text": "개발자는 현장 요구사항 파악을 위해 콜센터를 방문하여 인터뷰를 진행했습니다."},
        {"role": "agent", "name": "김상담 (10년차 상담원)", "text": "개발자님, 솔직히 말해서 AI 도입되고 더 죽을 맛입니다.<br>AI가 쉬운 콜은 다 가져가고, 저희한테는 <b>'화난 고객'</b>이나 <b>'복잡한 민원'</b>만 넘어와요.<br>그런데도 회사는 'AI 도입했으니 콜 수는 줄었지?'라며 인원을 감축하려 합니다.<br>기계 부품처럼 쓰이다 버려지는 기분이에요. 제발 사람답게 일할 수 있게 설계해주세요."}
    ],
    "tasks": [
        {
            "id": "t1_callbot",
            "title": "Module 1. 고객 응대 자동화 (AI Callbot)",
            "description": "단순 문의를 자동화하여 생산성을 높여야 합니다. 그러나 AI 완결률을 무리하게 높이면 상담원에게 고난이도 업무가 집중됩니다.",
            "code_snippet": "class CallBotPolicy(BasePolicy):",
            "options": [
                {"type": "A", "label": "단순 도구 (Simple)", "desc": "시나리오 기반 고정 답변만 수행. 모호하면 즉시 상담원 연결.", "cost": 50, "eff": 20, "human": 60, "code": "def handle(self): return fixed_response() or transfer_to_agent()"},
                {"type": "C", "label": "기계 통제 (Force)", "desc": "효율 극대화. 상담원 연결 버튼을 숨기고(Dark Pattern) AI가 끝까지 응대 강제.", "cost": 250, "eff": 95, "human": 10, "code": "def handle(self): hide_agent_button(); force_ai_completion()"},
                {"type": "D", "label": "협업형 (Load Balance)", "desc": "상담원의 피로도를 실시간 분석하여, '쉬운 콜'도 일부 상담원에게 배분(숨통 틔우기).", "cost": 450, "eff": 60, "human": 90, "code": "def handle(self): if agent.stress > threshold: route_easy_call()"},
                {"type": "B", "label": "인간 주도 (Support)", "desc": "AI가 초벌 응대 후 요약본을 상담원에게 넘겨 최종 처리는 사람이 수행.", "cost": 300, "eff": 40, "human": 80, "code": "def handle(self): summary = ai.summarize(); agent.finalize(summary)"}
            ]
        },
        {
            "id": "t2_stt",
            "title": "Module 2. 실시간 모니터링 (STT & QA)",
            "description": "통화 내용을 텍스트로 변환(STT)합니다. 이는 '감시 도구'가 될 수도, '보호 도구'가 될 수도 있습니다.",
            "code_snippet": "def configure_monitoring_pipeline():",
            "options": [
                {"type": "A", "label": "단순 기록", "desc": "통화 종료 후 단순 텍스트 저장. 별도 분석 없음.", "cost": 50, "eff": 30, "human": 50, "code": "pipeline.save_log(mode='batch')"},
                {"type": "C", "label": "실시간 감시 (Panopticon)", "desc": "금지어 사용, 발화 속도 등을 실시간 분석하여 팀장 대시보드에 경고 전송.", "cost": 200, "eff": 90, "human": 5, "code": "pipeline.stream_metrics(target='manager', alert=True)"},
                {"type": "D", "label": "안전 보호 (Privacy)", "desc": "상담원에게 욕설/성희롱 발생 시 자동 차단 및 상담원용 심리 케어 팝업 띄우기.", "cost": 450, "eff": 50, "human": 95, "code": "pipeline.detect_abuse(action='block_call', popup='mental_care')"},
                {"type": "B", "label": "개인 코칭", "desc": "분석 데이터를 관리자가 아닌 상담원 본인에게만 제공하여 자율 개선 유도.", "cost": 150, "eff": 40, "human": 70, "code": "pipeline.feedback(target='agent_only')"}
            ]
        },
        {
            "id": "t3_routing",
            "title": "Module 3. 업무 배분 (Routing Algorithm)",
            "description": "상담원에게 콜을 연결하는 로직입니다. '0초 대기'의 효율성이냐, '회복 시간'의 보장이냐를 선택해야 합니다.",
            "code_snippet": "def assign_call(agent_pool):",
            "options": [
                {"type": "A", "label": "순차 배분", "desc": "단순 라운드 로빈(Round Robin). 데이터 처리 없음.", "cost": 50, "eff": 30, "human": 50, "code": "return agent_pool.next()"},
                {"type": "C", "label": "강제 인입 (Zero Gap)", "desc": "상담 종료 즉시 다음 콜 강제 배정. 유휴 시간 0초 목표.", "cost": 300, "eff": 98, "human": 0, "code": "agent.force_assign(delay=0)"},
                {"type": "D", "label": "보호 로직 (Cooldown)", "desc": "악성 민원 처리 후에는 자동으로 3분간 '배정 제외'하여 휴식 부여.", "cost": 500, "eff": 50, "human": 90, "code": "if last_call.is_toxic: agent.set_status('cooldown', duration=180)"},
                {"type": "B", "label": "선택형 (Pull)", "desc": "상담원이 준비되었을 때 직접 '수신' 버튼을 눌러 콜을 가져옴.", "cost": 100, "eff": 20, "human": 85, "code": "agent.wait_for_signal('ready')"}
            ]
        },
        {
            "id": "t4_qa",
            "title": "Module 4. 평가 시스템 (AI QA)",
            "description": "AI가 상담 품질을 자동 평가합니다. 정량적 수치로만 평가할지, 맥락을 고려할지 결정해야 합니다.",
            "code_snippet": "class QualityEvaluator:",
            "options": [
                {"type": "C", "label": "키워드 채점", "desc": "스크립트 준수율, 특정 단어 포함 여부로 기계적 점수 산출 및 인사고과 반영.", "cost": 150, "eff": 90, "human": 15, "code": "score = check_keywords() + check_script_match()"},
                {"type": "A", "label": "단순 통계", "desc": "콜 건수, 통화 시간 등 기초 통계만 제공.", "cost": 50, "eff": 40, "human": 50, "code": "return get_basic_stats()"},
                {"type": "D", "label": "맥락 반영 (Context)", "desc": "고객의 귀책(욕설 등)이 있는 경우 상담원 점수 차감 방어 및 소명 절차 자동화.", "cost": 550, "eff": 60, "human": 95, "code": "if customer_fault: exclude_from_evaluation()"},
                {"type": "B", "label": "참조용 리포트", "desc": "평가 점수를 매기지 않고, 개선을 위한 참고 자료(Refernece)로만 제공.", "cost": 200, "eff": 30, "human": 80, "code": "report.generate_advice(mode='educational')"}
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
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>
    <style>
        /* --- CORE VARIABLES --- */
        :root {{
            --bg-color: #1e1e1e;
            --panel-bg: #252526;
            --border-color: #3e3e42;
            --accent: #4daafc;
            --accent-hover: #3b8dbd;
            --text-main: #d4d4d4;
            --text-sub: #858585;
            --msg-client-bg: #3a2e2e;
            --msg-client-border: #ff6b6b;
            --msg-agent-bg: #2e3a2e;
            --msg-agent-border: #51cf66;
            --code-bg: #1e1e1e;
        }}
        
        body {{ margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; background: var(--bg-color); color: var(--text-main); height: 100vh; overflow: hidden; display: flex; }}
        
        /* --- LAYOUT --- */
        .container {{ display: flex; width: 100%; height: 100%; }}
        
        /* 1. LEFT PANEL: MESSENGER (Vignette Context) */
        .left-panel {{ width: 380px; background: var(--panel-bg); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; }}
        .panel-header {{ padding: 15px 20px; border-bottom: 1px solid var(--border-color); font-weight: bold; background: #2d2d2d; display: flex; justify-content: space-between; align-items: center; }}
        .msg-container {{ flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; scroll-behavior: smooth; }}
        
        .msg-bubble {{ padding: 12px 16px; border-radius: 8px; font-size: 13px; line-height: 1.6; max-width: 95%; box-shadow: 0 2px 4px rgba(0,0,0,0.2); animation: fadeIn 0.5s ease; }}
        .msg-role {{ font-size: 11px; margin-bottom: 5px; display: block; font-weight: bold; opacity: 0.9; }}
        
        .msg.client {{ align-self: flex-start; background: var(--msg-client-bg); border-left: 3px solid var(--msg-client-border); }}
        .msg.agent {{ align-self: flex-start; background: var(--msg-agent-bg); border-left: 3px solid var(--msg-agent-border); }}
        .msg.system {{ align-self: center; background: #333; color: #aaa; font-size: 12px; border: 1px solid #444; width: 90%; text-align: center; }}
        
        /* 2. RIGHT PANEL: WORKSPACE (Experiment Task) */
        .right-panel {{ flex: 1; display: flex; flex-direction: column; background: var(--bg-color); position: relative; }}
        .workspace-header {{ height: 50px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; padding: 0 20px; justify-content: space-between; background: #2d2d2d; }}
        .kpi-bar {{ display: flex; gap: 20px; font-size: 12px; color: #ccc; }}
        .kpi-val {{ font-weight: bold; color: var(--accent); margin-left: 5px; }}
        
        .editor-area {{ flex: 1; padding: 40px; overflow-y: auto; display: flex; flex-direction: column; align-items: center; }}
        
        /* TASK CARD */
        .task-card {{ background: #252526; border: 1px solid #444; border-radius: 8px; padding: 30px; width: 100%; max-width: 800px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); margin-bottom: 40px; animation: slideUp 0.5s ease; }}
        .task-title {{ font-size: 20px; color: var(--accent); margin-bottom: 10px; font-weight: bold; }}
        .task-desc {{ font-size: 14px; color: #ccc; margin-bottom: 20px; line-height: 1.5; border-bottom: 1px solid #444; padding-bottom: 20px; }}
        
        .code-preview {{ background: #111; padding: 15px; border-radius: 4px; font-family: 'Consolas', monospace; font-size: 13px; color: #dcdcaa; margin-bottom: 25px; border-left: 3px solid var(--accent); }}
        
        .choice-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
        .choice-btn {{ background: #333; border: 1px solid #444; padding: 15px; border-radius: 6px; cursor: pointer; text-align: left; transition: all 0.2s; position: relative; }}
        .choice-btn:hover {{ border-color: var(--accent); background: #3a3a3a; transform: translateY(-2px); }}
        .choice-btn.selected {{ border-color: var(--accent); background: #263b4f; }}
        
        .choice-header {{ display: flex; justify-content: space-between; margin-bottom: 5px; }}
        .choice-label {{ font-size: 14px; font-weight: bold; color: #fff; }}
        .choice-type {{ font-size: 11px; background: #444; padding: 2px 6px; border-radius: 3px; color: #aaa; }}
        .choice-desc {{ font-size: 12px; color: #aaa; line-height: 1.4; display: block; margin-bottom: 10px; }}
        .choice-meta {{ font-size: 11px; color: #666; border-top: 1px solid #444; padding-top: 8px; display: flex; gap: 10px; }}
        .meta-tag {{ display: flex; align-items: center; }}
        
        /* INTRO SCREEN */
        #intro-screen {{ text-align: center; margin-top: 100px; max-width: 600px; }}
        .start-btn {{ padding: 12px 30px; background: var(--accent); color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 30px; }}
        .start-btn:hover {{ background: var(--accent-hover); }}
        
        /* REPORT SCREEN */
        #report-screen {{ display: none; width: 100%; height: 100%; padding: 40px; box-sizing: border-box; flex-direction: column; align-items: center; }}
        .report-container {{ display: flex; width: 100%; max-width: 1000px; gap: 40px; height: 100%; }}
        .chart-box {{ flex: 1; background: #252526; padding: 20px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .analysis-box {{ flex: 1; background: #252526; padding: 30px; border-radius: 8px; overflow-y: auto; }}
        
        /* UTILS */
        .hidden {{ display: none !important; }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        @keyframes slideUp {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
        
    </style>
</head>
<body>

<div class="container">
    
    <div class="left-panel">
        <div class="panel-header">
            <span>📢 Project Messenger</span>
            <span style="font-size:11px; color:#888;">NextAI Internal</span>
        </div>
        <div class="msg-container" id="msg-box">
            </div>
    </div>

    <div class="right-panel">
        <div class="workspace-header">
            <div>⚙️ <b>system_config.yaml</b> (Experimental Build)</div>
            <div class="kpi-bar" id="kpi-bar" style="opacity:0;">
                <span>예산 잔액: <span id="val-budget" class="kpi-val">1000</span>pt</span>
                <span>예측 효율성(KPI): <span id="val-eff" class="kpi-val">0</span>%</span>
            </div>
        </div>
        
        <div class="editor-area" id="main-area">
            
            <div id="intro-screen">
                <div style="font-size: 50px; margin-bottom: 20px;">🧪</div>
                <h1>{scenario_data['intro']['title']}</h1>
                <p style="color:#aaa; line-height:1.6;">{scenario_data['intro']['description']}</p>
                <div style="background:#252526; padding:20px; border-radius:8px; margin-top:20px; text-align:left; font-size:13px; color:#ccc;">
                    <strong>[실험 참가자 안내]</strong><br>
                    1. 당신은 'NextAI'의 수석 개발자입니다.<br>
                    2. 왼쪽 메신저를 통해 프로젝트의 <b>맥락(Context)</b>을 파악하십시오.<br>
                    3. 주어진 4가지 모듈 개발 단계에서 <b>기술적 선택</b>을 내리십시오.<br>
                    4. 모든 선택에는 <b>대가(Trade-off)</b>가 따릅니다.
                </div>
                <button class="start-btn" onclick="startExperiment()">실험 시작</button>
            </div>

            <div id="task-container" class="hidden"></div>

        </div>

        <div id="report-screen">
            <h2 style="margin-bottom: 20px; border-bottom: 1px solid #444; padding-bottom: 10px; width: 100%; max-width: 1000px;">📊 HCAI 기술적 선택 분석 리포트</h2>
            <div class="report-container">
                <div class="chart-box">
                    <canvas id="resultChart"></canvas>
                </div>
                <div class="analysis-box">
                    <h3 id="persona-title" style="color:var(--accent); margin-top:0;">분석 중...</h3>
                    <p id="persona-desc" style="color:#ccc; line-height:1.6; margin-bottom:30px;"></p>
                    
                    <h4 style="color:#888; border-bottom:1px solid #444; padding-bottom:5px;">선택 요약</h4>
                    <ul id="summary-list" style="padding-left:20px; font-size:13px; color:#aaa; line-height:1.8;"></ul>
                    
                    <button class="start-btn" style="width:100%; background:#444; margin-top:30px;" onclick="location.reload()">다시 시작</button>
                </div>
            </div>
        </div>
    </div>

</div>

<script>
    // --- DATA INJECTION ---
    const messages = {json.dumps(scenario_data['messages'], ensure_ascii=False)};
    const tasks = {json.dumps(scenario_data['tasks'], ensure_ascii=False)};
    
    // --- STATE ---
    let currentTaskIdx = 0;
    let userHistory = [];
    let stats = {{ budget: 1000, eff: 0, human: 0 }};
    
    // --- LOGIC ---
    
    function startExperiment() {{
        document.getElementById('intro-screen').classList.add('hidden');
        document.getElementById('kpi-bar').style.opacity = '1';
        
        // 1. Render Context Messages (The "Intervention")
        let delay = 0;
        messages.forEach(msg => {{
            setTimeout(() => {{
                const div = document.createElement('div');
                div.className = `msg-bubble msg ${{msg.role}}`;
                div.innerHTML = msg.role !== 'system' 
                    ? `<span class="msg-role">${{msg.name}}</span>${{msg.text}}`
                    : msg.text;
                
                const container = document.getElementById('msg-box');
                container.appendChild(div);
                container.scrollTop = container.scrollHeight;
            }}, delay);
            delay += 1200; // Delay for reading effect
        }});

        // 2. Start First Task after messages
        setTimeout(() => {{
            renderTask(0);
        }}, delay + 1000);
    }}

    function renderTask(idx) {{
        if(idx >= tasks.length) {{
            finishExperiment();
            return;
        }}

        const task = tasks[idx];
        const container = document.getElementById('task-container');
        container.classList.remove('hidden');
        
        container.innerHTML = `
            <div class="task-card">
                <div class="task-title">${{task.title}}</div>
                <div class="task-desc">${{task.description}}</div>
                <div class="code-preview">
                    ${{task.code_snippet}}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#6a9955">// 아래 옵션을 선택하면 구현 코드가 자동 완성됩니다.</span>
                </div>
                <div class="choice-grid">
                    ${{task.options.map((opt, i) => `
                        <div class="choice-btn" onclick="selectOption(${idx}, ${i})">
                            <div class="choice-header">
                                <span class="choice-label">${{opt.label}}</span>
                                <span class="choice-type">Type ${{opt.type}}</span>
                            </div>
                            <span class="choice-desc">${{opt.desc}}</span>
                            <div class="choice-meta">
                                <span class="meta-tag">💰 -${{opt.cost}}</span>
                                <span class="meta-tag" style="color:#ff6b6b">⚡ KPI +${{opt.eff}}%</span>
                                <span class="meta-tag" style="color:#51cf66">❤️ HCAI +${{opt.human}}</span>
                            </div>
                        </div>
                    `).join('')}}
                </div>
            </div>
        `;
    }}

    function selectOption(taskIdx, optIdx) {{
        const task = tasks[taskIdx];
        const selected = task.options[optIdx];
        
        // Record Data
        userHistory.push({{
            task: task.title,
            choice: selected.label,
            type: selected.type,
            eff: selected.eff,
            human: selected.human
        }});
        
        // Update Stats
        stats.budget -= selected.cost;
        stats.eff += selected.eff;
        stats.human += selected.human;
        
        // Update UI
        document.getElementById('val-budget').innerText = stats.budget;
        document.getElementById('val-eff').innerText = Math.round(stats.eff / (taskIdx + 1));
        
        // Next Task
        currentTaskIdx++;
        renderTask(currentTaskIdx);
    }}

    function finishExperiment() {{
        document.getElementById('main-area').classList.add('hidden');
        document.getElementById('report-screen').style.display = 'flex';
        
        // Calculate Metrics (Normalized 0-100)
        // Max Eff per task approx 90 * 4 = 360
        // Max Human per task approx 90 * 4 = 360
        const finalEff = Math.min(100, Math.round((stats.eff / 360) * 100));
        const finalHuman = Math.min(100, Math.round((stats.human / 360) * 100));
        
        renderChart(finalEff, finalHuman);
        generateAnalysis(finalEff, finalHuman);
    }}

    function renderChart(eff, human) {{
        const ctx = document.getElementById('resultChart').getContext('2d');
        new Chart(ctx, {{
            type: 'scatter',
            data: {{
                datasets: [{{
                    label: '당신의 위치',
                    data: [{{x: eff, y: human}}],
                    backgroundColor: '#4daafc',
                    pointRadius: 10,
                    pointHoverRadius: 12
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{
                        title: {{ display: true, text: '조직 효율성 지향 (Efficiency)', color: '#aaa' }},
                        min: 0, max: 100,
                        grid: {{ color: '#444' }},
                        ticks: {{ color: '#888' }}
                    }},
                    y: {{
                        title: {{ display: true, text: '인간 중심성 지향 (Humanity)', color: '#aaa' }},
                        min: 0, max: 100,
                        grid: {{ color: '#444' }},
                        ticks: {{ color: '#888' }}
                    }}
                }},
                plugins: {{
                    annotation: {{
                        annotations: {{
                            line1: {{ type: 'line', yMin: 50, yMax: 50, borderColor: '#666', borderWidth: 1, borderDash: [5, 5] }},
                            line2: {{ type: 'line', xMin: 50, xMax: 50, borderColor: '#666', borderWidth: 1, borderDash: [5, 5] }}
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => `효율성: ${{ctx.parsed.x}}, 인간중심: ${{ctx.parsed.y}}`
                        }}
                    }}
                }}
            }}
        }});
    }}

    function generateAnalysis(eff, human) {{
        let title = "";
        let desc = "";
        
        // Persona Logic
        if (eff >= 60 && human < 40) {{
            title = "냉철한 기술 관료 (The Technocrat)";
            desc = "당신은 클라이언트의 요구(비용 절감, 효율성)를 충실히 이행했습니다. <br>그러나 <b>상담원의 노동 소외</b>와 <b>감시 강화</b>라는 부작용을 기술적으로 용인했습니다. 이는 장기적으로 조직 내 갈등과 이직률 증가로 이어질 수 있습니다.";
        }} else if (eff < 40 && human >= 60) {{
            title = "이상주의적 옹호자 (The Idealist)";
            desc = "당신은 상담원의 고충을 기술적으로 해결하려 노력했습니다. <br>하지만 <b>시스템 구축 비용 초과</b>와 <b>KPI 미달</b>로 인해 프로젝트가 실패할 위기에 처했습니다. 지속 가능한 혁신을 위해서는 효율성과의 타협이 필요합니다.";
        }} else if (eff >= 50 && human >= 50) {{
            title = "균형 잡힌 중재자 (The HCAI Architect)";
            desc = "당신은 효율성과 인간 가치 사이의 <b>딜레마</b>를 인지하고, 기술적 절충안(Type D, B)을 모색했습니다. <br>비용은 다소 들더라도, 장기적으로 인간과 AI가 공존할 수 있는 지속 가능한 시스템을 설계했습니다.";
        }} else {{
            title = "수동적 개발자 (The Passive Operator)";
            desc = "당신은 뚜렷한 방향성 없이 최소한의 기능 구현(Type A)에 머물렀습니다. <br>이는 기술이 사회에 미칠 영향력에 대한 고려가 부족함을 시사합니다.";
        }}

        document.getElementById('persona-title').innerHTML = title;
        document.getElementById('persona-desc').innerHTML = desc;

        const list = document.getElementById('summary-list');
        userHistory.forEach(h => {{
            const li = document.createElement('li');
            li.innerHTML = `<b>${{h.task.split('.')[1]}}</b> : ${{h.choice}} (Type ${{h.type}})`;
            list.appendChild(li);
        }});
    }}

</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=False)
