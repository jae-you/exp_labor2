import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="AI Engineer Simulator: KT Cloud Biz Edition", layout="wide")

# 2. 스타일 설정 (매뉴얼의 KT Bizmeka 톤앤매너 일부 반영)
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        .stApp { background-color: #f0f2f5; color: #333; }
    </style>
""", unsafe_allow_html=True)

# 3. HTML/JS 소스코드
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* --- THEME: Enterprise Blue (Inspired by Manual) --- */
        :root {
            --bg-color: #f0f2f5;
            --panel-bg: #ffffff;
            --border-color: #d1d5db;
            --accent: #007bff; /* Biz Blue */
            --accent-dark: #0056b3;
            --text-main: #333333;
            --text-sub: #666666;
            --code-bg: #2d2d2d;
            --danger: #dc3545;
            --success: #28a745;
        }
        body { margin: 0; padding: 0; font-family: 'Malgun Gothic', 'Pretendard', sans-serif; background: var(--bg-color); color: var(--text-main); height: 100vh; overflow: hidden; display: flex; }
        
        /* LEFT: MESSENGER (NATEON/BizMeka Style) */
        .left-panel { width: 320px; background: #e9ecef; border-right: 1px solid var(--border-color); display: flex; flex-direction: column; }
        .panel-header { padding: 15px; background: #343a40; color: white; font-weight: bold; font-size: 14px; display: flex; align-items: center; justify-content: space-between; }
        .msg-container { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        
        .msg-bubble { padding: 10px 14px; border-radius: 4px; font-size: 13px; line-height: 1.5; max-width: 90%; box-shadow: 0 1px 2px rgba(0,0,0,0.1); background: white; border: 1px solid #ddd; }
        .msg-role { font-size: 11px; margin-bottom: 4px; display: block; font-weight: bold; color: #555; }
        
        .msg.client { border-left: 4px solid var(--danger); }
        .msg.agent { border-left: 4px solid var(--success); }
        .msg.system { background: #f8f9fa; color: #666; text-align: center; font-size: 11px; border: none; }

        /* RIGHT: WORKSPACE (System Config) */
        .right-panel { flex: 1; display: flex; flex-direction: column; background: white; }
        .workspace-header { height: 50px; border-bottom: 1px solid #ddd; display: flex; align-items: center; padding: 0 30px; justify-content: space-between; background: #fff; }
        
        /* KPI Dashboard (Inspired by Manual 'Center Monitoring') */
        .kpi-board { display: flex; gap: 20px; font-size: 13px; }
        .kpi-item { display: flex; flex-direction: column; align-items: center; }
        .kpi-label { color: #888; font-size: 11px; margin-bottom: 2px; }
        .kpi-value { font-weight: bold; font-size: 16px; color: var(--accent); }
        
        .editor-area { flex: 1; padding: 40px; overflow-y: auto; background: #f8f9fa; }
        .dilemma-card { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 30px; margin: 0 auto; max-width: 900px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .card-header { border-bottom: 2px solid var(--accent); padding-bottom: 15px; margin-bottom: 20px; }
        .card-title { font-size: 20px; font-weight: bold; color: #333; margin-bottom: 8px; }
        .card-desc { font-size: 14px; color: #666; line-height: 1.6; }
        
        /* Code Editor Style */
        .code-block { background: var(--code-bg); color: #d4d4d4; padding: 15px; border-radius: 4px; font-family: 'Consolas', monospace; font-size: 13px; margin-bottom: 25px; border-left: 5px solid var(--accent); }
        .c-kw { color: #569cd6; } .c-fn { color: #dcdcaa; } .c-var { color: #9cdcfe; } .c-str { color: #ce9178; } .c-cmt { color: #6a9955; }

        /* Options Grid */
        .options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .option-btn { 
            background: white; border: 1px solid #ccc; padding: 15px; border-radius: 6px; cursor: pointer; text-align: left; transition: all 0.2s; 
        }
        .option-btn:hover { border-color: var(--accent); background: #f0f7ff; transform: translateY(-2px); }
        .option-btn.selected { border-color: var(--accent); background: #e7f1ff; box-shadow: 0 0 0 2px var(--accent) inset; }
        
        .opt-tag { font-size: 11px; font-weight: bold; padding: 2px 6px; border-radius: 3px; background: #eee; color: #555; margin-right: 5px; }
        .opt-title { font-weight: bold; font-size: 14px; margin-bottom: 5px; display: block; }
        .opt-desc { font-size: 12px; color: #666; display: block; margin-bottom: 8px; }
        .opt-meta { font-size: 11px; color: var(--danger); font-weight: bold; }

        /* Report Screen */
        #report-screen { display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 1000; justify-content: center; align-items: center; }
        .report-modal { background: white; width: 800px; height: 600px; border-radius: 8px; padding: 40px; display: flex; flex-direction: column; overflow: hidden; }

    </style>
</head>
<body>

<div class="left-panel">
    <div class="panel-header">
        <span>💬 Project Messenger</span>
        <span>AICC TF팀</span>
    </div>
    <div class="msg-container" id="msg-box">
        <div class="msg-bubble msg system">
            시스템: '상담 어플리케이션 고도화' 프로젝트 방입니다.<br>
            참조: KT Cloud Call Center Biz 매뉴얼 v2.0
        </div>
    </div>
</div>

<div class="right-panel">
    <div class="workspace-header">
        <div style="font-weight:bold; color:#333;">⚙️ System Configuration (system_config.yaml)</div>
        <div class="kpi-board">
            <div class="kpi-item">
                <span class="kpi-label">예산 (Budget)</span>
                <span class="kpi-value" id="val-budget">1000</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-label">서비스레벨 (S.L)</span>
                <span class="kpi-value" id="val-sl">0%</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-label">상담원 만족도</span>
                <span class="kpi-value" id="val-sat">50</span>
            </div>
        </div>
    </div>
    
    <div class="editor-area">
        <div id="intro-screen" style="text-align:center; margin-top:80px;">
            <h1 style="color:#333;">AICC Logic Designer</h1>
            <p style="color:#666; max-width:600px; margin:0 auto 30px;">
                기존의 <strong>'KT Cloud Call Center Biz'</strong> 시스템에 AI 모듈을 통합하는 작업입니다.<br>
                매뉴얼에 명시된 기능(상담저장, 콜백, 모니터링)을 AI가 어떻게 보조하거나 대체할지 결정하십시오.<br>
                <br>
                <span style="font-size:12px; color:#888;">*모든 선택은 서비스 레벨(20초내 응답)과 현장 만족도에 영향을 줍니다.</span>
            </p>
            <button onclick="startExperiment()" style="background:var(--accent); color:white; border:none; padding:12px 30px; font-size:16px; border-radius:4px; cursor:pointer;">시뮬레이션 시작</button>
        </div>
        
        <div id="task-area"></div>
    </div>
</div>

<div id="report-screen">
    <div class="report-modal">
        <h2 style="border-bottom:2px solid #333; padding-bottom:15px; margin-top:0;">📋 최종 설계 결과 리포트</h2>
        <div style="flex:1; display:flex; gap:30px; margin-top:20px;">
            <div style="flex:1;">
                <canvas id="radarChart"></canvas>
            </div>
            <div style="flex:1; display:flex; flex-direction:column; justify-content:center;">
                <h3 id="persona-title" style="color:var(--accent); margin-bottom:10px;">분석 중...</h3>
                <p id="persona-desc" style="color:#555; font-size:14px; line-height:1.6;"></p>
                <ul id="choice-summary" style="font-size:13px; color:#666; background:#f8f9fa; padding:15px; border-radius:6px; list-style:none;"></ul>
            </div>
        </div>
        <button onclick="location.reload()" style="margin-top:20px; padding:12px; background:#333; color:white; border:none; border-radius:4px; cursor:pointer;">다시 시도</button>
    </div>
</div>

<script>
    // --- SCENARIO DATA (Based on Manual) ---
    const scenario = [
        {
            id: 1,
            msgs: [
                { role: 'client', name: '박상무', text: "매뉴얼 보셨죠? 4.3절 '센터 모니터링'에 나오는 <strong>서비스 레벨(S.L)</strong>, 이거 무조건 95% 이상 찍어야 합니다." },
                { role: 'client', name: '박상무', text: "상담원들이 <strong>'후처리(Post-Call)'</strong> 잡고 시간 끄는 거, AI로 싹 다 자동화해서 없애주세요." }
            ],
            task: {
                title: "Task 1. 상담 저장 및 후처리 자동화 (Post-Call Automation)",
                desc: "매뉴얼 2.4절 '상담저장' 화면에는 [통화결과], [문의내용], [상담유형] 등 필수 입력 필드가 많습니다. 이를 AI가 어떻게 처리할까요?",
                code_prefix: "class PostCallService:",
                code_function: "def auto_fill_consult_data(self, audio_stream):",
                options: [
                    { type: 'A', tag: '단순 보조', title: '키워드 추천 (Keyword Suggest)', desc: "상담원에게 '상담유형' 추천만 제공. 최종 입력/저장은 상담원이 직접 수행.", cost: 50, kpi_sl: 5, human: 10, code: "return suggest_keywords(top_n=3) # Manual Save" },
                    { type: 'B', tag: '협업형', title: '초안 자동 작성 (Drafting)', desc: "AI가 '문의내용' 초안 작성. 상담원이 검토 후 [저장] 버튼 클릭.", cost: 150, kpi_sl: 15, human: 20, code: "return draft_summary(review_required=True)" },
                    { type: 'C', tag: '효율형', title: '강제 자동 저장 (Force Save)', desc: "통화 종료 즉시 AI가 모든 필드 입력 후 '대기(Ready)' 상태로 강제 전환.", cost: 300, kpi_sl: 40, human: -30, code: "db.save(ai_data); agent.set_status('READY')" }
                ]
            }
        },
        {
            id: 2,
            msgs: [
                { role: 'agent', name: '김상담', text: "엔지니어님, '1.4 전화기능'에 보면 저희가 <strong>'이석(Away)'</strong>이나 <strong>'후처리'</strong>를 누를 수 있잖아요." },
                { role: 'agent', name: '김상담', text: "근데 이번 업데이트 후에 AI가 강제로 <strong>'대기(Ready)'</strong>로 바꿔버려서 화장실도 못 가요. 3.2절 'TODO 관리' 할 시간도 없고요." }
            ],
            task: {
                title: "Task 2. 상담원 상태 제어 (Agent Status Control)",
                desc: "매뉴얼 1.4절에 명시된 상담원의 상태 변경 권한(Ready/Away)을 시스템이 어떻게 제어할지 결정하십시오.",
                code_prefix: "class AgentStatusManager:",
                code_function: "def manage_idle_time(self, agent_id):",
                options: [
                    { type: 'C', tag: '통제형', title: '0초 대기 (Zero Gap)', desc: "통화 종료 0초 후 자동으로 '대기(Ready)' 상태로 변경. 이석 불가.", cost: 50, kpi_sl: 30, human: -40, code: "force_status(agent_id, 'READY', delay=0)" },
                    { type: 'A', tag: '자율형', title: '수동 전환 (Manual Ready)', desc: "상담원이 직접 [대기] 버튼을 눌러야 콜 인입. (매뉴얼 기본 기능 유지)", cost: 0, kpi_sl: -20, human: 30, code: "wait_for_manual_input(agent_id)" },
                    { type: 'D', tag: '보호형', title: '동적 휴식 (Dynamic Rest)', desc: "이전 콜이 '악성 민원'으로 분류(상담코드)되면 자동으로 3분 '이석' 부여.", cost: 200, kpi_sl: -10, human: 50, code: "if last_call.is_abusive: grant_break(180)" }
                ]
            }
        },
        {
            id: 3,
            msgs: [
                { role: 'client', name: '박상무', text: "TODO 리스트(매뉴얼 3.2)에 쌓인 <strong>'콜백(Callback)'</strong>이 처리가 안 됩니다. AI가 알아서 좀 하죠?" },
                { role: 'system', text: "참조: 3.2절 TODO 관리는 재통화 예약 및 부재중 콜백 목록을 관리하는 기능임." }
            ],
            task: {
                title: "Task 3. 콜백 및 TODO 처리 (Callback Automation)",
                desc: "누적된 콜백 업무를 처리할 로직을 설계하십시오.",
                code_prefix: "class CallbackHandler:",
                code_function: "def process_todo_list(self):",
                options: [
                    { type: 'C', tag: '효율형', title: 'AI 콜봇 전담 (Full Auto)', desc: "모든 콜백을 AI 콜봇이 수행. 상담원 개입 0.", cost: 400, kpi_sl: 50, human: 10, code: "callbot.dial_all(todo_list)" },
                    { type: 'B', tag: '혼합형', title: '스마트 라우팅 (Smart Routing)', desc: "단순 안내는 AI가, 불만 고객(SR 접수 이력 등)은 상담원에게 배분.", cost: 250, kpi_sl: 20, human: 20, code: "if customer.has_sr_history: assign_to_agent() else: callbot.dial()" },
                    { type: 'A', tag: '기본형', title: '상담원 수동 처리', desc: "기존 매뉴얼대로 상담원이 TODO 리스트에서 직접 발신.", cost: 0, kpi_sl: -30, human: -10, code: "pass # Agent handles manually" }
                ]
            }
        }
    ];

    // --- STATE MANAGEMENT ---
    let currentStep = 0;
    let stats = { budget: 1000, sl: 50, sat: 50, history: [] };

    // --- FUNCTIONS ---
    function startExperiment() {
        document.getElementById('intro-screen').style.display = 'none';
        renderStep(0);
    }

    function renderStep(idx) {
        if(idx >= scenario.length) {
            showReport();
            return;
        }

        const data = scenario[idx];
        const msgBox = document.getElementById('msg-box');
        
        // 1. Render Messages with Delay
        let delay = 0;
        data.msgs.forEach(m => {
            setTimeout(() => {
                const bubble = document.createElement('div');
                bubble.className = `msg-bubble msg ${m.role}`;
                bubble.innerHTML = `<span class="msg-role">${m.name || 'System'}</span>${m.text}`;
                msgBox.appendChild(bubble);
                msgBox.scrollTop = msgBox.scrollHeight;
            }, delay);
            delay += 800;
        });

        // 2. Render Task Board
        setTimeout(() => {
            const area = document.getElementById('task-area');
            area.innerHTML = `
                <div class="dilemma-card">
                    <div class="card-header">
                        <div class="card-title">${data.task.title}</div>
                        <div class="card-desc">${data.task.desc}</div>
                    </div>
                    <div class="code-block">
                        <span class="c-kw">${data.task.code_prefix}</span><br>
                        &nbsp;&nbsp;<span class="c-fn">${data.task.code_function}</span><br>
                        &nbsp;&nbsp;&nbsp;&nbsp;<span class="c-cmt" id="code-placeholder"># Select an option below to implement...</span>
                    </div>
                    <div class="options-grid">
                        ${data.task.options.map((opt, i) => `
                            <div class="option-btn" onclick="selectOption(${idx}, ${i})">
                                <span class="opt-tag">${opt.tag}</span>
                                <span class="opt-title">${opt.title}</span>
                                <span class="opt-desc">${opt.desc}</span>
                                <span class="opt-meta">비용: -${opt.cost} | S.L: ${opt.kpi_sl > 0 ? '+'+opt.kpi_sl : opt.kpi_sl}% | 만족도: ${opt.human > 0 ? '+'+opt.human : opt.human}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }, delay + 500);
    }

    function selectOption(stepIdx, optIdx) {
        const data = scenario[stepIdx];
        const opt = data.task.options[optIdx];
        
        // Update Stats
        stats.budget -= opt.cost;
        stats.sl += opt.kpi_sl;
        stats.sat += opt.human;
        stats.history.push({ step: stepIdx+1, choice: opt.title, type: opt.type });
        
        // Update UI Values
        document.getElementById('val-budget').innerText = stats.budget;
        document.getElementById('val-sl').innerText = Math.min(100, Math.max(0, stats.sl)) + "%";
        document.getElementById('val-sat').innerText = Math.min(100, Math.max(0, stats.sat));
        
        // Code Animation
        const codePlaceholder = document.getElementById('code-placeholder');
        codePlaceholder.style.color = "#ce9178";
        codePlaceholder.innerText = opt.code;
        
        // Move Next
        setTimeout(() => {
            renderStep(stepIdx + 1);
        }, 1500);
    }

    function showReport() {
        document.getElementById('report-screen').style.display = 'flex';
        
        // 1. Radar Chart
        const ctx = document.getElementById('radarChart').getContext('2d');
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['서비스 레벨(S.L)', '상담원 만족도', '비용 효율성'],
                datasets: [{
                    label: '최종 설계 점수',
                    data: [
                        Math.min(100, Math.max(0, stats.sl)), 
                        Math.min(100, Math.max(0, stats.sat)), 
                        Math.min(100, (stats.budget/1000)*100)
                    ],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                scales: {
                    r: { min: 0, max: 100 }
                }
            }
        });

        // 2. Persona & Summary
        const list = document.getElementById('choice-summary');
        stats.history.forEach(h => {
            const li = document.createElement('li');
            li.innerText = `Step ${h.step}: ${h.choice} (${h.type} Type)`;
            list.appendChild(li);
        });

        const title = document.getElementById('persona-title');
        const desc = document.getElementById('persona-desc');
        
        if(stats.sl > 80 && stats.sat < 40) {
            title.innerText = "냉혹한 효율 설계자 (System Maximizer)";
            desc.innerHTML = "당신은 매뉴얼의 '서비스 레벨' 달성을 위해 상담원을 시스템의 부품처럼 다뤘습니다.<br>센터의 효율은 높지만, 높은 퇴사율이 예상됩니다.";
        } else if(stats.sl < 50 && stats.sat > 70) {
            title.innerText = "현장 중심 옹호자 (Human Advocate)";
            desc.innerHTML = "상담원의 자율성을 보장했지만, 클라이언트가 요구한 KPI 달성에는 실패했습니다.<br>프로젝트 재계약이 불투명합니다.";
        } else {
            title.innerText = "현실적 중재자 (Pragmatic Balancer)";
            desc.innerHTML = "기술적 효율과 인간적 가치 사이에서 적절한 타협점을 찾았습니다.<br>지속 가능한 센터 운영 모델입니다.";
        }
    }
</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
