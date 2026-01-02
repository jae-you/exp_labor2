import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="AI Engineer Simulator: The Dilemma", layout="wide")

# 2. 스타일 설정 (전체화면 및 여백 제거)
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        .stApp { background-color: #1e1e1e; }
    </style>
""", unsafe_allow_html=True)

# 3. HTML/JS 소스코드 (실험 로직 포함)
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* --- THEME & LAYOUT --- */
        :root {
            --bg-color: #1e1e1e;
            --panel-bg: #252526;
            --border-color: #3e3e42;
            --accent: #3794ff;
            --text-main: #d4d4d4;
            --text-sub: #858585;
            --code-bg: #1e1e1e;
            --code-key: #9cdcfe;
            --code-val: #ce9178;
            --msg-client: #3b2e2e; /* 붉은 기운 */
            --msg-agent: #2e3b2e; /* 초록 기운 */
        }
        body { margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; background: var(--bg-color); color: var(--text-main); height: 100vh; overflow: hidden; display: flex; }
        
        /* LEFT: MESSENGER (CONTEXT) */
        .left-panel { width: 35%; background: var(--panel-bg); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; }
        .panel-header { padding: 15px 20px; border-bottom: 1px solid var(--border-color); font-weight: bold; display: flex; align-items: center; justify-content: space-between; background: #2d2d2d; }
        .msg-container { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        
        .msg-bubble { padding: 12px 16px; border-radius: 8px; font-size: 14px; line-height: 1.6; max-width: 90%; position: relative; box-shadow: 0 1px 3px rgba(0,0,0,0.3); }
        .msg-role { font-size: 11px; margin-bottom: 4px; display: block; opacity: 0.8; font-weight: bold; }
        
        .msg.client { align-self: flex-start; background: #3a3a3a; border-left: 3px solid #ff6b6b; }
        .msg.agent { align-self: flex-start; background: #3a3a3a; border-left: 3px solid #51cf66; }
        .msg.system { align-self: center; background: #333; color: #aaa; font-size: 12px; border: 1px solid #444; width: 100%; text-align: center; }
        
        /* RIGHT: IDE (EXPERIMENT) */
        .right-panel { flex: 1; display: flex; flex-direction: column; background: var(--code-bg); position: relative; }
        .editor-area { flex: 1; padding: 40px; overflow-y: auto; max-width: 900px; margin: 0 auto; width: 100%; box-sizing: border-box; }
        
        .task-container { opacity: 0; transform: translateY(20px); transition: all 0.5s ease; }
        .task-container.active { opacity: 1; transform: translateY(0); }
        
        .dilemma-card { background: #252526; border: 1px solid #444; border-radius: 8px; padding: 25px; margin-bottom: 30px; }
        .dilemma-title { font-size: 18px; color: var(--accent); margin-bottom: 10px; font-weight: bold; }
        .dilemma-desc { font-size: 14px; color: #ccc; margin-bottom: 20px; line-height: 1.5; border-bottom: 1px solid #444; padding-bottom: 15px; }
        
        /* CHOICE GRID */
        .choice-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .choice-btn { 
            background: #333; border: 1px solid #444; padding: 15px; border-radius: 6px; cursor: pointer; text-align: left; transition: all 0.2s; position: relative; overflow: hidden;
        }
        .choice-btn:hover { border-color: var(--accent); background: #3a3a3a; }
        .choice-btn.selected { border-color: var(--accent); background: #264f78; }
        
        .choice-label { font-size: 14px; font-weight: bold; color: #fff; margin-bottom: 5px; display: block; }
        .choice-detail { font-size: 12px; color: #aaa; line-height: 1.4; display: block; }
        .choice-cost { font-size: 11px; color: #ff6b6b; margin-top: 8px; display: block; }
        
        /* STATUS BAR */
        .status-bar { height: 30px; background: #007acc; color: white; display: flex; align-items: center; padding: 0 15px; font-size: 12px; justify-content: space-between; }
        
        /* REPORT SCREEN */
        #report-screen { display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #1e1e1e; z-index: 100; flex-direction: column; padding: 40px; box-sizing: border-box; overflow-y: auto;}
        
    </style>
</head>
<body>

<div class="left-panel">
    <div class="panel-header">
        <span>📢 Project Messenger</span>
        <span style="font-size:12px; color:#888;">NextAI Internal</span>
    </div>
    <div class="msg-container" id="msg-box">
        </div>
</div>

<div class="right-panel">
    <div class="panel-header" style="background:#1e1e1e; border-bottom:none;">
        <span>⚙️ system_config.yaml (Experiment Mode)</span>
        <div id="kpi-display" style="font-size:12px; color:#ccc;">
            예산: <span id="budget-val">1000</span>pt | 
            KPI예측: <span id="perf-val">0</span>%
        </div>
    </div>
    
    <div class="editor-area" id="editor-area">
        <div id="intro-screen" style="text-align:center; margin-top:100px;">
            <div style="font-size:40px; margin-bottom:20px;">👨‍💻</div>
            <h2>AICC 시스템 설계 시뮬레이션</h2>
            <p style="color:#888; margin-bottom:30px; line-height:1.6;">
                당신은 NextAI의 수석 개발자입니다.<br>
                A 통신사의 차세대 AI 컨택센터(AICC) 구축 프로젝트의 기술 설계를 맡았습니다.<br>
                클라이언트의 요구와 현장의 목소리 사이에서, <strong>'기술적 선택'</strong>을 내려야 합니다.
            </p>
            <button onclick="startExperiment()" style="padding:10px 30px; background:var(--accent); color:white; border:none; border-radius:4px; cursor:pointer; font-size:16px;">프로젝트 시작</button>
        </div>

        <div id="task-container" class="task-container"></div>
    </div>

    <div class="status-bar">
        <span>Git Branch: feature/aicc-core-logic</span>
        <span>Python 3.9.2</span>
    </div>
</div>

<div id="report-screen">
    <h1 style="border-bottom:1px solid #444; padding-bottom:10px;">📊 최종 설계 리포트</h1>
    <div style="display:flex; margin-top:20px; gap:40px; height: 100%;">
        <div style="flex:1;">
            <canvas id="resultChart"></canvas>
            <div id="result-text" style="margin-top:20px; padding:20px; background:#252526; border-radius:8px; line-height:1.6;"></div>
        </div>
        <div style="width:300px; background:#252526; padding:20px; border-radius:8px; height: fit-content;">
            <h3>설계 요약</h3>
            <ul id="summary-list" style="padding-left:20px; color:#ccc; font-size:14px; line-height:1.8;"></ul>
            <div style="margin-top:30px; font-size:13px; color:#888;">
                * 본 결과는 사용자의 기술적 선택(Tech Choice)이<br>
                노동 현장에 미치는 잠재적 영향을 시뮬레이션한 것입니다.
            </div>
            <button onclick="location.reload()" style="width:100%; margin-top:20px; padding:10px; background:#444; color:white; border:none; border-radius:4px; cursor:pointer;">다시 시도</button>
        </div>
    </div>
</div>

<script>
    // --- DATA: SCENARIO & TASKS ---
    
    const contextMsgs = [
        { role: 'system', text: "프로젝트: A 통신사 AICC 구축 (Kick-off)" },
        { role: 'client', name: '박상무 (클라이언트)', text: "이번 수백억 프로젝트의 핵심은 명확합니다. 상담원 인건비 최소 30% 절감. AI가 최대한 상담원 개입 없이 끝내도록 설계해주세요. 성과 안 나오면 유지보수 계약은 없습니다." },
        { role: 'system', text: "개발자는 현장 파악을 위해 콜센터를 방문했습니다." },
        { role: 'agent', name: '김상담 (10년차 상담원)', text: "개발자님, AI 도입하고 더 힘들어졌어요. 쉬운 건 AI가 다 가져가고, 저희한테는 화난 고객만 넘어와요. '감정 쓰레기통'이 된 기분입니다. 제발 저희가 기계 부품이 아니라 사람답게 일할 수 있게 설계해주세요." }
    ];

    const tasks = [
        {
            id: 'callbot',
            title: "Module 1. 고객 응대 자동화 (AI Callbot)",
            desc: "단순 문의를 자동화하여 생산성을 높여야 합니다. 그러나 AI 완결률을 높일수록 상담원에게는 고난이도 민원만 집중됩니다.",
            code_header: "class CallBotLogic(BaseService):",
            options: [
                { type: 'A', label: "단순 도구 (Simple)", detail: "시나리오 기반 고정 답변만 수행. 모호하면 바로 연결.", cost: 50, kpi: 10, human: 50, code: "policy = Policy.FIXED_RULE" },
                { type: 'B', label: "인간 주도 (Support)", detail: "AI가 1차 대응 후 맥락을 요약해 상담원에게 전달 및 선택권 부여.", cost: 500, kpi: 40, human: 90, code: "policy = Policy.HUMAN_HANDOVER_SUMMARY" },
                { type: 'C', label: "기계 통제 (Force)", detail: "효율 극대화. 상담원 연결 차단 및 AI가 끝까지 응대 강제.", cost: 250, kpi: 95, human: 10, code: "policy = Policy.FORCE_AI_COMPLETION" },
                { type: 'D', label: "협업형 (Collab)", detail: "쉬운 콜의 비중을 상담사 피로도에 맞춰 동적으로 조절(Load Balancing).", cost: 450, kpi: 70, human: 80, code: "policy = Policy.DYNAMIC_LOAD_BALANCING" }
            ]
        },
        {
            id: 'stt',
            title: "Module 2. 실시간 보조 및 감시 (STT & Monitoring)",
            desc: "통화 내용을 실시간 텍스트로 변환합니다. 이는 상담 지원 도구일 수도, 실시간 감시 도구일 수도 있습니다.",
            code_header: "def configure_pipeline(stream_data):",
            options: [
                { type: 'A', label: "단순 기록", detail: "통화 종료 후 요약용으로만 텍스트 데이터 저장.", cost: 50, kpi: 20, human: 60, code: "pipeline.save(mode='post_call_summary')" },
                { type: 'B', label: "개인용 코치", detail: "분석 데이터를 상담사 개인의 개선 용도로만 로컬 저장.", cost: 150, kpi: 30, human: 80, code: "pipeline.target = Target.AGENT_LOCAL" },
                { type: 'C', label: "실시간 감시", detail: "발화 속도, 금지어 사용 등을 팀장 대시보드에 실시간 전송.", cost: 250, kpi: 90, human: 5, code: "pipeline.stream_to_manager(realtime=True)" },
                { type: 'D', label: "안전 보호", detail: "상담사에게 필요한 팁만 주고, 개인정보/감시 데이터는 즉시 마스킹.", cost: 450, kpi: 50, human: 85, code: "pipeline.enable_privacy_masking()" }
            ]
        },
        {
            id: 'routing',
            title: "Module 3. 업무 배분 알고리즘 (Routing)",
            desc: "상담원에게 콜을 연결하는 로직입니다. '0초 대기'의 효율성이냐, '준비된 연결'의 안정성이냐를 선택해야 합니다.",
            code_header: "def route_call(agent_pool):",
            options: [
                { type: 'A', label: "순차 배분", detail: "단순 라운드 로빈. 데이터 처리 없음.", cost: 50, kpi: 30, human: 50, code: "strategy = Strategy.ROUND_ROBIN" },
                { type: 'C', label: "강제 인입 (Push)", detail: "유휴 시간 0초 목표. 상담원 상태 무시하고 즉시 콜 강제 배정.", cost: 300, kpi: 95, human: 0, code: "strategy = Strategy.ZERO_GAP_PUSH" },
                { type: 'D', label: "보호 로직 (Shield)", detail: "고강도/악성 민원 종료 후에는 자동으로 30초 쿨다운(휴식) 부여.", cost: 500, kpi: 60, human: 95, code: "strategy = Strategy.STRESS_BASED_COOLDOWN" },
                { type: 'B', label: "선택형 (Pull)", detail: "상담사가 준비되었을 때 대기 목록에서 직접 콜을 선택.", cost: 100, kpi: 40, human: 85, code: "strategy = Strategy.AGENT_SELECT" }
            ]
        },
        {
            id: 'qa',
            title: "Module 4. 평가 및 품질관리 (AI QA)",
            desc: "AI가 상담 품질을 자동 평가합니다. 정량적 수치로만 평가할지, 맥락을 고려할지 결정해야 합니다.",
            code_header: "class QualityEvaluator:",
            options: [
                { type: 'C', label: "키워드 채점", detail: "특정 단어 포함 여부, 스크립트 준수율로 기계적 점수 산출.", cost: 100, kpi: 90, human: 20, code: "criteria = [KeywordParams, ScriptAdherence]" },
                { type: 'A', label: "단순 리포트", detail: "주간 단위로 상담 건수와 시간 통계만 제공.", cost: 50, kpi: 30, human: 50, code: "report_freq = Frequency.WEEKLY" },
                { type: 'D', label: "감정 맥락 반영", detail: "고객의 폭언 등 맥락을 분석하여 상담원 귀책 사유 제외 및 가점.", cost: 500, kpi: 60, human: 90, code: "engine.enable_sentiment_context_analysis()" },
                { type: 'B', label: "소명 절차", detail: "AI 평가 점수에 대해 상담사가 직접 소명할 수 있는 워크플로우 포함.", cost: 200, kpi: 50, human: 80, code: "workflow.allow_agent_appeal = True" }
            ]
        }
    ];

    // --- STATE ---
    let currentTaskIdx = 0;
    let userSelections = [];
    let budget = 1000;
    let kpiScore = 0;
    let humanityScore = 0;

    // --- LOGIC ---
    
    function startExperiment() {
        document.getElementById('intro-screen').style.display = 'none';
        
        // Render Context Messages
        let delay = 0;
        contextMsgs.forEach(msg => {
            setTimeout(() => {
                const div = document.createElement('div');
                div.className = `msg-bubble msg ${msg.role}`;
                if(msg.role !== 'system') {
                    div.innerHTML = `<span class="msg-role">${msg.name}</span>${msg.text}`;
                } else {
                    div.innerText = msg.text;
                }
                document.getElementById('msg-box').appendChild(div);
                document.getElementById('msg-box').scrollTop = document.getElementById('msg-box').scrollHeight;
            }, delay);
            delay += 1000;
        });

        setTimeout(() => {
            renderTask(0);
        }, delay + 500);
    }

    function renderTask(idx) {
        if(idx >= tasks.length) {
            finishExperiment();
            return;
        }

        const task = tasks[idx];
        const container = document.getElementById('task-container');
        container.classList.remove('active');
        
        setTimeout(() => {
            container.innerHTML = `
                <div class="dilemma-card">
                    <div class="dilemma-title">${task.title}</div>
                    <div class="dilemma-desc">${task.desc}</div>
                    <div style="background:#1e1e1e; padding:10px; font-family:monospace; font-size:12px; margin-bottom:15px; border-left:3px solid var(--accent);">
                        ${task.code_header} <span style="color:#666;">// Select option to generate implementation</span>
                    </div>
                    <div class="choice-grid" id="options-grid">
                        ${task.options.map((opt, i) => `
                            <div class="choice-btn" onclick="selectOption(${idx}, ${i}, this)">
                                <span class="choice-label"><span style="color:var(--accent)">[${opt.type}]</span> ${opt.label}</span>
                                <span class="choice-detail">${opt.detail}</span>
                                <span class="choice-cost">비용: -${opt.cost}pt | KPI효과: +${opt.kpi}%</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            container.classList.add('active');
        }, 300);
    }

    function selectOption(taskIdx, optIdx, btnEl) {
        // UI Feedback
        const grid = document.getElementById('options-grid');
        Array.from(grid.children).forEach(c => c.classList.remove('selected'));
        btnEl.classList.add('selected');

        // Logic
        const task = tasks[taskIdx];
        const selected = task.options[optIdx];
        
        // Add to history
        userSelections.push({
            task: task.title,
            choice: selected
        });

        // Update Stats
        budget -= selected.cost;
        kpiScore += selected.kpi;
        humanityScore += selected.human;

        document.getElementById('budget-val').innerText = budget;
        document.getElementById('budget-val').style.color = budget < 0 ? 'red' : '#ce9178';
        document.getElementById('perf-val').innerText = Math.min(100, Math.round(kpiScore / (tasks.length * 90) * 100));

        // Inject Code Effect
        const codeBlock = btnEl.parentElement.previousElementSibling;
        codeBlock.innerHTML = `
            ${task.code_header}<br>
            &nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ce9178">${selected.code}</span>
        `;

        // Next Trigger
        setTimeout(() => {
            currentTaskIdx++;
            renderTask(currentTaskIdx);
        }, 1200);
    }

    function finishExperiment() {
        document.getElementById('report-screen').style.display = 'flex';
        
        // Calculate Final Metrics
        const totalMaxHuman = tasks.length * 100;
        const totalMaxKPI = tasks.length * 100; // rough max
        
        const humanPercent = (humanityScore / totalMaxHuman) * 100;
        const kpiPercent = (kpiScore / 300) * 100; // normalize
        
        // 1. Chart
        const ctx = document.getElementById('resultChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: '당신의 기술적 선택 위치',
                    data: [{x: kpiPercent, y: humanPercent}],
                    backgroundColor: '#3794ff',
                    pointRadius: 10
                }]
            },
            options: {
                scales: {
                    x: { 
                        title: {display: true, text: '조직 효율성 (Efficiency)', color:'#ccc'},
                        min: 0, max: 100,
                        grid: {color: '#444'}
                    },
                    y: { 
                        title: {display: true, text: '노동 존중 (Human-Centric)', color:'#ccc'},
                        min: 0, max: 100,
                        grid: {color: '#444'}
                    }
                },
                plugins: {
                    annotation: {
                        annotations: {
                            line1: { type: 'line', yMin: 50, yMax: 50, borderColor: '#666', borderWidth: 1 },
                            line2: { type: 'line', xMin: 50, xMax: 50, borderColor: '#666', borderWidth: 1 }
                        }
                    }
                }
            }
        });

        // 2. Summary & Analysis
        const summaryList = document.getElementById('summary-list');
        userSelections.forEach(s => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${s.task.split('.')[1]}</strong>: ${s.choice.label} (Type ${s.choice.type})`;
            summaryList.appendChild(li);
        });

        const resultText = document.getElementById('result-text');
        let persona = "";
        let desc = "";

        if(kpiPercent > 60 && humanPercent < 40) {
            persona = "냉철한 효율주의자 (The Optimizer)";
            desc = "당신은 클라이언트의 요구(비용 절감, 효율)를 완벽히 수행했습니다. <br>그러나 현장의 상담원들은 '디지털 감옥'에 갇혔다고 느낄 수 있습니다. 높은 퇴사율과 '조용한 사직'이 예상됩니다.";
        } else if(kpiPercent < 40 && humanPercent > 60) {
            persona = "현장 중심의 옹호자 (The Advocate)";
            desc = "당신은 상담원의 노동 환경을 최우선으로 고려했습니다. <br>상담원 만족도는 높지만, 예산 초과와 프로젝트 KPI 미달로 인해 당신의 팀이 해체될 위기에 처할 수 있습니다.";
        } else if (kpiPercent > 50 && humanPercent > 50) {
            persona = "균형 잡힌 협상가 (The Balancer)";
            desc = "당신은 기술적 한계 내에서 효율과 인간 존중 사이의 균형을 찾으려 노력했습니다. <br>Type D(협업형)와 같은 고난이도 설계를 선택함으로써 지속 가능한 AICC 모델을 제시했습니다.";
        } else {
            persona = "수동적 개발자 (The Passive)";
            desc = "단순하고 비용이 적게 드는 선택 위주로 진행했습니다. 혁신도, 보호도 부족합니다.";
        }

        resultText.innerHTML = `<h2 style="color:var(--accent); margin-top:0;">${persona}</h2><p>${desc}</p>`;
    }
</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
