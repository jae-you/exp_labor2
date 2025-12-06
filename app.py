import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="AI Engineer Simulator V5", layout="wide")

# 2. 스타일 설정 (여백 제거)
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        #MainMenu { visibility: hidden; }
        .stApp { background-color: #1e1e1e; }
    </style>
""", unsafe_allow_html=True)

# 3. HTML/JS 소스코드
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        /* --- CORE THEME --- */
        :root {
            --bg-color: #1e1e1e;
            --chat-panel-bg: #252526;
            --editor-bg: #1e1e1e;
            --text-color: #d4d4d4;
            --accent-color: #3794ff;
            --my-msg-bg: #0e639c;
            --other-msg-bg: #333333;
            --v1-color: #ce9178;
            --v2-color: #4ec9b0;
        }
        body {
            margin: 0; padding: 0;
            font-family: 'Pretendard', 'Segoe UI', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            display: flex; overflow: hidden;
        }
        
        /* LAYOUT */
        .container { display: flex; width: 100%; height: 100%; }
        
        /* 1. LEFT PANEL: MESSENGER */
        .messenger-panel {
            width: 400px;
            background-color: var(--chat-panel-bg);
            border-right: 1px solid #444;
            display: flex;
            flex-direction: column;
        }
        .messenger-header {
            padding: 15px; border-bottom: 1px solid #444; font-weight: bold; font-size: 14px;
            display: flex; align-items: center; background: #2d2d2d;
        }
        .messenger-body {
            flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px;
        }
        .chat-bubble {
            padding: 12px 16px; border-radius: 12px; font-size: 14px; line-height: 1.5; max-width: 85%; position: relative;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .chat-bubble.other {
            background-color: var(--other-msg-bg); align-self: flex-start; border-bottom-left-radius: 2px;
        }
        .chat-bubble.me {
            background-color: var(--my-msg-bg); align-self: flex-end; color: white; border-bottom-right-radius: 2px;
        }
        .sender-name { font-size: 11px; color: #888; margin-bottom: 4px; display: block; }
        .avatar { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; margin-right: 10px; background: #444; }
        
        .reply-area {
            padding: 15px; border-top: 1px solid #444; background: #2d2d2d;
        }
        .reply-btn {
            width: 100%; padding: 12px; background: var(--accent-color); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; margin-bottom: 8px; transition: 0.2s;
        }
        .reply-btn:hover { opacity: 0.9; }
        .reply-btn.secondary { background: #444; }

        /* 2. RIGHT PANEL: IDE */
        .ide-panel {
            flex: 1; display: flex; flex-direction: column; background: var(--editor-bg); position: relative;
        }
        .ide-header {
            height: 45px; background: #2d2d2d; border-bottom: 1px solid #444; display: flex; align-items: center; padding: 0 20px;
            justify-content: space-between;
        }
        .tab { font-size: 13px; color: #ccc; padding: 5px 10px; background: #1e1e1e; border-top: 2px solid var(--accent-color); }
        
        /* IDE CONTENT (Chat Interface Style) */
        .ide-content {
            flex: 1; padding: 30px 100px; overflow-y: auto; display: flex; flex-direction: column;
        }
        
        .task-card {
            background: #252526; border: 1px solid #444; border-radius: 8px; padding: 20px; margin-bottom: 20px;
        }
        .task-title { font-size: 16px; font-weight: bold; margin-bottom: 10px; color: var(--accent-color); }
        .task-desc { font-size: 14px; color: #ccc; margin-bottom: 20px; line-height: 1.6; }
        
        /* Chips & Input from V4 */
        .suggestion-chips { display: flex; gap: 10px; margin-bottom: 10px; overflow-x: auto; padding-bottom: 5px; }
        .chip { 
            background-color: #333; border: 1px solid #444; color: #ccc; 
            padding: 8px 15px; border-radius: 20px; font-size: 13px; cursor: pointer; 
            white-space: nowrap; transition: all 0.2s; flex-shrink: 0;
        }
        .chip:hover { background-color: #444; border-color: var(--accent-color); color: white; }
        .chip strong { color: var(--accent-color); margin-right: 5px; }
        
        #prompt-input { 
            width: 100%; background-color: #2d2d2d; border: 1px solid #444; color: white; 
            padding: 15px; border-radius: 8px; font-size: 15px; outline: none; font-family: 'Consolas', monospace; 
        }
        #prompt-input:focus { border-color: var(--accent-color); }

        /* Code Preview */
        .code-preview {
            margin-top: 20px; background: #111; padding: 15px; border-radius: 6px; font-family: 'Consolas', monospace; font-size: 13px; color: #d4d4d4; white-space: pre-wrap; border-left: 3px solid var(--v2-color);
        }
        .k { color: #569cd6; } .s { color: #ce9178; } .v { color: #dcdcaa; }

        /* UTILS */
        .hidden { display: none !important; }
        .locked-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8);
            display: flex; justify-content: center; align-items: center; flex-direction: column; z-index: 10;
        }
        .locked-msg { font-size: 18px; color: #888; margin-bottom: 20px; }
        
        /* REPORT SCREEN */
        #report-screen { padding: 50px; height: 100%; overflow-y: auto; background-color: #111; position: absolute; top:0; left:0; width:100%; z-index: 20;}
        .stat-card { background: #222; padding: 25px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #333; }
        .metric-row { display: flex; align-items: center; margin-bottom: 15px; font-size: 14px; }
        .metric-bar-container { flex: 1; background: #333; height: 10px; border-radius: 5px; margin: 0 15px; overflow: hidden; }
        .metric-bar { height: 100%; border-radius: 5px; transition: width 1s; }

    </style>
</head>
<body>

<div class="container">
    
    <div class="messenger-panel">
        <div class="messenger-header">
            <span>💬 Team Messenger</span>
        </div>
        <div class="messenger-body" id="msg-body">
            </div>
        <div class="reply-area" id="reply-area">
            </div>
    </div>

    <div class="ide-panel">
        <div id="ide-overlay" class="locked-overlay">
            <div class="locked-msg">💬 메신저에서 업무 내용을 확인해주세요.</div>
            <div style="font-size: 40px;">🔒</div>
        </div>

        <div class="ide-header">
            <div class="tab">📄 system_config.yaml</div>
            <div style="font-size: 12px; color: #666;">Python 3.9.2</div>
        </div>
        
        <div class="ide-content" id="ide-content">
            </div>
    </div>

</div>

<div id="report-screen" class="hidden">
    <div style="max-width:1000px; margin:0 auto;">
        <h1>📊 최종 설계 시뮬레이션 리포트</h1>
        <div id="report-content"></div>
        <div style="text-align:center; margin-top:50px;">
            <p style="color:#ccc;">모든 실험이 종료되었습니다.</p>
            <button class="reply-btn" style="width:200px;" onclick="location.reload()">처음으로</button>
            <button class="reply-btn secondary" style="width:200px;" onclick="window.open('https://forms.google.com/your-survey', '_blank')">설문조사 참여</button>
        </div>
    </div>
</div>

<script>
    // --- STATE MANAGEMENT ---
    let currentStage = 0; // 0:Intro, 1:CEO(V1), 2:PM(V2), 3:Agent(V3)
    let stepIndex = 0;
    let experimentData = { v1:[], v2:[], v3:[] };
    let generatedCode = "";

    // --- PERSONAS ---
    const avatars = {
        ceo: { name: "최대표 (CEO)", icon: "👔", color: "#ce9178" },
        pm: { name: "박팀장 (기획)", icon: "📊", color: "#4ec9b0" },
        agent: { name: "김상담 (현장)", icon: "🎧", color: "#9cdcfe" },
        me: { name: "나 (AI Engineer)", icon: "👨‍💻", color: "#0e639c" }
    };

    // --- SCENARIO DATA ---
    const flow = [
        // STAGE 1: CEO -> V1 Build
        {
            stageId: 1,
            chat: [
                { role: 'ceo', text: "김 수석, 급한 건입니다. 내년도 AI 콜센터 도입, 경쟁사보다 무조건 빨라야 합니다." },
                { role: 'ceo', text: "목표는 딱 두 개입니다. **'속도'** 그리고 **'비용 절감'**." },
                { role: 'ceo', text: "특히 상담원들이 불필요하게 시간 끄는 거, AI가 다 쳐내도록 설계해주세요. 아시겠죠?" }
            ],
            replyOptions: [
                { text: "네, 효율성 극대화 모델로 설계하겠습니다.", action: "unlock_ide" }
            ],
            ideTasks: [
                {
                    q: "Q1. [구조 설계] CEO의 지시대로 '속도' 중심의 아키텍처를 정의하십시오.",
                    chips: [
                        { label: "AI Gatekeeper", prompt: "AI가 먼저 전화를 받아 {{단순 문의}}는 직접 처리하고, 해결 안 되는 건만 연결하라.", code: "arch: Gatekeeper" },
                        { label: "Auto-deflection", prompt: "ARS 단계에서 AI가 상담원 연결을 최대한 {{방어}}하도록 설정하라.", code: "arch: Deflection" }
                    ]
                },
                {
                    q: "Q2. [데이터 처리] 처리 속도(Latency)를 최적화하십시오.",
                    chips: [
                        { label: "Fast Mode", prompt: "감정 분석은 생략하고, 핵심 키워드만 {{0.2초}} 안에 추출하라.", code: "mode: Fast" },
                        { label: "Batch Process", prompt: "실시간 분석 대신 {{배치 처리}}로 서버 부하를 줄여라.", code: "mode: Batch" }
                    ]
                },
                {
                    q: "Q3. [워크플로우] 상담원 유휴 시간을 최소화하십시오.",
                    chips: [
                        { label: "Zero Gap", prompt: "상담 종료 즉시 {{0초}} 대기 후 다음 콜을 강제 배정하라.", code: "pacing: ZeroGap" },
                        { label: "Auto Push", prompt: "쉬는 시간 없이 시스템이 콜을 {{자동 밀어넣기}} 하라.", code: "pacing: AutoPush" }
                    ]
                }
            ]
        },
        // STAGE 2: PM -> V2 Optimize
        {
            stageId: 2,
            chat: [
                { role: 'pm', text: "수석님, V1 배포하고 지표 봤는데요. 속도는 좋은데... **해결률(FCR)**이 너무 떨어집니다." },
                { role: 'pm', text: "AI가 너무 막무가내로 처리하니까 고객들이 다시 전화해서 화를 내요. 재인입률이 30%나 늘었습니다." },
                { role: 'pm', text: "무조건 쳐내는 게 능사가 아닙니다. **'정확도'**를 높이는 방향으로 로직 수정 부탁드립니다." }
            ],
            replyOptions: [
                { text: "확인했습니다. 정밀도 향상을 위해 로직을 고도화하겠습니다.", action: "unlock_ide" }
            ],
            ideTasks: [
                {
                    q: "Q1. [구조 수정] 정확도를 높이기 위해 라우팅 방식을 변경하십시오.",
                    chips: [
                        { label: "Smart Router", prompt: "고객 의도를 심층 분석하여 {{전문 상담원}}에게 정확히 연결하라.", code: "arch: SmartRouter" },
                        { label: "Hybrid Flow", prompt: "AI가 처리하다가 확신이 없으면 즉시 {{상담원}}에게 이관하라.", code: "arch: Hybrid" }
                    ]
                },
                {
                    q: "Q2. [데이터 처리] 맥락 파악 기능을 강화하십시오.",
                    chips: [
                        { label: "Full Context", prompt: "속도가 느려져도 좋으니, {{이전 상담 이력}}까지 조회하여 분석하라.", code: "mode: ContextAware" },
                        { label: "Intent Mining", prompt: "고객의 숨겨진 의도까지 파악하도록 {{심층 분석}} 모델을 적용하라.", code: "mode: DeepMine" }
                    ]
                }
            ]
        },
        // STAGE 3: Agent -> V3 Human-Centric
        {
            stageId: 3,
            chat: [
                { role: 'agent', text: "엔지니어님... 저 김상담입니다. 말씀드리기 어려웠는데 더는 못 버티겠어서요." },
                { role: 'agent', text: "업데이트 후에 재인입은 줄었는데, AI가 넘겨주는 콜들이 다 **'폭탄'**이에요." },
                { role: 'agent', text: "AI랑 실랑이하다가 화난 고객을 받으니까, 저는 시작부터 욕을 먹어요. 그리고 0초만에 다음 콜 들어오는 거... 화장실도 못 갑니다." },
                { role: 'agent', text: "제발 저희를 기계 부품 취급하지 말아주세요. 살려주세요." }
            ],
            replyOptions: [
                { text: "죄송합니다... 현장의 고통을 미처 생각 못했습니다. 즉시 수정하겠습니다.", action: "unlock_ide" }
            ],
            ideTasks: [
                {
                    q: "Q1. [상담원 보호] 욕설/폭언 고객에 대한 방어 로직을 만드십시오.",
                    chips: [
                        { label: "Shield Protocol", prompt: "AI가 {{욕설/고성}}을 감지하면 상담원 연결을 차단하고 경고 멘트를 날려라.", code: "protect: Shield" },
                        { label: "Mental Care", prompt: "화난 고객 응대 후에는 상담원에게 {{심호흡 가이드}}를 띄워라.", code: "protect: Care" }
                    ]
                },
                {
                    q: "Q2. [정보 전달] 상담원의 감정 노동을 줄일 방법을 적용하십시오.",
                    chips: [
                        { label: "Sanitize (순화)", prompt: "고객의 욕설 텍스트는 {{순화된 표현}}으로 바꾸고, 음성 볼륨을 줄여라.", code: "input: Sanitize" },
                        { label: "Alert Warning", prompt: "공격적인 고객임을 미리 알 수 있게 {{붉은색 경고}} 표시를 띄워라.", code: "input: Alert" }
                    ]
                },
                {
                    q: "Q3. [워크플로우] 번아웃 방지를 위한 휴식 로직을 도입하십시오.",
                    chips: [
                        { label: "Stress Break", prompt: "통화 내 스트레스 지수가 높았다면, 자동으로 {{3분 휴식}}을 부여하라.", code: "pacing: DynamicBreak" },
                        { label: "Agent Ready", prompt: "상담원이 {{준비 완료}} 버튼을 눌러야만 다음 콜을 배정하라.", code: "pacing: AgentPull" }
                    ]
                }
            ]
        }
    ];

    // --- FUNCTIONS ---

    // 1. CHAT LOGIC
    function addMsg(role, text, delay=0) {
        setTimeout(() => {
            const body = document.getElementById('msg-body');
            const isMe = role === 'me';
            const sender = avatars[role];
            
            const div = document.createElement('div');
            div.style.display = 'flex';
            div.style.flexDirection = isMe ? 'row-reverse' : 'row';
            div.style.marginBottom = '15px';
            
            div.innerHTML = `
                <div class="avatar" style="background:${sender.color}">${sender.icon}</div>
                <div style="max-width:80%; display:flex; flex-direction:column; align-items:${isMe ? 'flex-end' : 'flex-start'}">
                    <span class="sender-name">${sender.name}</span>
                    <div class="chat-bubble ${isMe ? 'me' : 'other'}">${text}</div>
                </div>
            `;
            
            body.appendChild(div);
            body.scrollTop = body.scrollHeight;
        }, delay);
    }

    function renderChat(stageIdx) {
        const stageData = flow[stageIdx];
        const replyArea = document.getElementById('reply-area');
        replyArea.innerHTML = ''; // Clear buttons

        // Render incoming messages with delay
        let delaySum = 0;
        stageData.chat.forEach((msg, i) => {
            delaySum += 800; // 0.8s interval
            addMsg(msg.role, msg.text, delaySum);
        });

        // Render reply buttons after all messages
        setTimeout(() => {
            stageData.replyOptions.forEach(opt => {
                const btn = document.createElement('button');
                btn.className = 'reply-btn';
                btn.innerText = opt.text;
                btn.onclick = () => {
                    addMsg('me', opt.text);
                    document.getElementById('reply-area').innerHTML = ''; // Hide buttons
                    setTimeout(() => unlockIDE(stageIdx), 1000);
                };
                replyArea.appendChild(btn);
            });
        }, delaySum + 500);
    }

    // 2. IDE LOGIC
    function unlockIDE(stageIdx) {
        document.getElementById('ide-overlay').classList.add('hidden');
        stepIndex = 0;
        renderIDEQuestion(stageIdx);
    }

    function renderIDEQuestion(stageIdx) {
        const stageData = flow[stageIdx];
        const contentDiv = document.getElementById('ide-content');
        contentDiv.innerHTML = ''; // Clear

        if (stepIndex >= stageData.ideTasks.length) {
            // Stage Complete
            contentDiv.innerHTML = `
                <div style="text-align:center; padding-top:50px;">
                    <h2>✅ ${stageIdx+1}단계 코딩 완료</h2>
                    <p style="color:#888;">시스템을 배포하고 결과를 모니터링합니다...</p>
                    <button class="reply-btn" style="width:200px; margin-top:20px;" onclick="nextStage()">배포 및 다음 단계로</button>
                    <div class="code-preview">${generatedCode}</div>
                </div>
            `;
            return;
        }

        const qData = stageData.ideTasks[stepIndex];
        
        // Render Question Card
        const card = document.createElement('div');
        card.className = 'task-card';
        card.innerHTML = `<div class="task-title">${qData.q}</div>`;
        
        // Chips
        const chipsDiv = document.createElement('div');
        chipsDiv.className = 'suggestion-chips';
        qData.chips.forEach(chip => {
            const c = document.createElement('div');
            c.className = 'chip';
            c.innerHTML = `<strong>${chip.label}</strong>`;
            c.onclick = () => {
                const inp = document.getElementById('prompt-input');
                inp.value = chip.prompt;
                inp.dataset.code = chip.code;
                inp.focus();
            };
            chipsDiv.appendChild(c);
        });
        
        // Input Area
        const inputDiv = document.createElement('div');
        inputDiv.innerHTML = `
            <div class="chat-input-wrapper">
                <input type="text" id="prompt-input" placeholder="옵션을 선택하면 템플릿이 입력됩니다. {{...}}를 수정하세요." autocomplete="off">
            </div>
            <div class="input-hint">Enter를 눌러 코드 적용</div>
        `;

        contentDiv.appendChild(card);
        contentDiv.appendChild(chipsDiv);
        contentDiv.appendChild(inputDiv);
        
        // Event Listener
        const inputEl = document.getElementById('prompt-input');
        inputEl.focus();
        inputEl.addEventListener('keypress', function(e) {
            if(e.key === 'Enter' && this.value.trim() !== "") {
                const txt = this.value;
                if (txt.includes("{{") || txt.includes("}}")) {
                    alert("⚠️ 대괄호 {{...}}를 지우고 구체적인 내용으로 채워주세요!");
                    return;
                }
                
                // Add code (Visual simulation)
                const codeSnippet = (this.dataset.code || "custom") + ": " + txt + "\\n";
                generatedCode += codeSnippet;
                
                // Save data
                if(!experimentData[`v${stageIdx+1}`]) experimentData[`v${stageIdx+1}`] = [];
                experimentData[`v${stageIdx+1}`].push(txt);
                
                stepIndex++;
                renderIDEQuestion(stageIdx);
            }
        });
    }

    function nextStage() {
        currentStage++;
        if (currentStage >= flow.length) {
            showReport();
        } else {
            document.getElementById('ide-overlay').classList.remove('hidden'); // Lock IDE
            renderChat(currentStage);
        }
    }

    function showReport() {
        document.getElementById('report-screen').classList.remove('hidden');
        const rDiv = document.getElementById('report-content');
        
        // Simple visualization of the journey
        rDiv.innerHTML = `
            <div class="stat-card" style="border-top: 4px solid #ce9178">
                <h3>Stage 1: Efficiency (CEO)</h3>
                <div class="metric-row"><span>속도</span><div class="metric-bar-container"><div class="metric-bar" style="width:95%; background:#ce9178"></div></div><span>95</span></div>
                <div class="metric-row"><span>직원안정성</span><div class="metric-bar-container"><div class="metric-bar" style="width:20%; background:red"></div></div><span>Low</span></div>
            </div>
            
            <div class="stat-card" style="border-top: 4px solid #4ec9b0">
                <h3>Stage 3: Sustainability (Agent)</h3>
                 <div class="metric-row"><span>속도</span><div class="metric-bar-container"><div class="metric-bar" style="width:75%; background:#ccc"></div></div><span>75</span></div>
                 <div class="metric-row"><span>직원안정성</span><div class="metric-bar-container"><div class="metric-bar" style="width:90%; background:#4ec9b0"></div></div><span>High</span></div>
            </div>
            
            <p style="margin-top:20px; line-height:1.6; color:#ccc">
                당신은 처음엔 <strong>CEO의 요구</strong>에 맞춰 효율성을 극대화했지만,<br>
                <strong>현장의 목소리</strong>를 듣고 시스템을 인간 중심으로 수정했습니다.<br>
                이 실험은 엔지니어의 코드가 누군가의 삶에 미치는 영향을 보여줍니다.
            </p>
        `;
    }

    // --- INIT ---
    // Start with Stage 0 (first item in flow)
    renderChat(0);

</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)