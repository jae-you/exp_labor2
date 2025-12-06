import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Invisible Engineer V7.2", layout="wide")

# 2. 스타일 설정
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
        /* HEIGHT FIX */
        html, body { margin:0; padding:0; width:100%; height:1000px; background-color:#1e1e1e; font-family:'Pretendard', sans-serif; color:#d4d4d4; overflow:hidden; }
        
        #loader { position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); color:#3794ff; font-weight:bold; }

        /* LAYOUT */
        .container { display:flex; width:100%; height:100%; }
        .left-panel { width:450px; background:#252526; border-right:1px solid #333; display:flex; flex-direction:column; transition:0.3s; }
        .right-panel { flex:1; display:flex; flex-direction:column; background:#1e1e1e; position:relative; }

        /* CHAT UI */
        .chat-header { padding:15px; border-bottom:1px solid #333; background:#2d2d2d; font-weight:bold; color:white; display:flex; justify-content:space-between; align-items:center; }
        .chat-body { flex:1; padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:15px; }
        
        .msg-row { display:flex; gap:10px; animation:fadeIn 0.3s; }
        .msg-row.me { flex-direction:row-reverse; }
        .avatar { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:20px; }
        .bubble { padding:12px 16px; border-radius:12px; font-size:14px; line-height:1.5; max-width:280px; box-shadow:0 2px 5px rgba(0,0,0,0.2); }
        .bubble.other { background:#383838; border-top-left-radius:2px; }
        .bubble.me { background:#0e639c; color:white; border-top-right-radius:2px; }
        
        /* CHOICE AREA */
        .choice-area { padding:15px; border-top:1px solid #333; background:#2d2d2d; min-height:100px; display:flex; flex-direction:column; gap:8px; }
        .choice-btn { 
            background:#3c3c3c; border:1px solid #555; color:#ddd; padding:12px; border-radius:6px; 
            cursor:pointer; text-align:left; transition:0.2s; font-size:13px;
        }
        .choice-btn:hover { border-color:#3794ff; background:#444; color:white; }
        .choice-label { color:#3794ff; font-weight:bold; margin-right:5px; }

        /* --- IDE UI (Cursor Style) --- */
        .ide-header { height:45px; background:#1e1e1e; border-bottom:1px solid #333; display:flex; align-items:center; padding:0 20px; color:#858585; font-size:13px; font-family:'Consolas', monospace; }
        .ide-body { flex:1; padding:40px; overflow-y:auto; position:relative; background:#1e1e1e; }

        .mission-box { background:#252526; padding:20px; border-radius:6px; border-left:3px solid #3794ff; margin-bottom:30px; }
        .mission-title { font-size:16px; font-weight:bold; color:white; margin-bottom:8px; }
        .mission-desc { color:#ccc; font-size:14px; line-height:1.5; }

        /* CODE INPUT AREA */
        .input-group { margin-bottom:30px; }
        .input-label { color:#d4d4d4; font-size:13px; margin-bottom:8px; display:flex; justify-content:space-between; }
        .code-guide { color:#4ec9b0; font-size:11px; cursor:help; }
        
        .chips-area { display:flex; gap:8px; margin-bottom:10px; }
        .chip { 
            background:#2d2d2d; padding:6px 12px; border-radius:4px; font-size:12px; 
            cursor:pointer; border:1px solid #444; color:#ccc; font-family:'Consolas', monospace; 
        }
        .chip:hover { border-color:#3794ff; color:white; }

        /* Real Editor Style Input */
        .editor-wrapper {
            background:#111; border:1px solid #333; border-radius:4px; padding:15px; position:relative;
            font-family:'Consolas', 'Monaco', monospace; font-size:14px; line-height:1.6;
        }
        .editor-wrapper:focus-within { border-color:#3794ff; }
        .line-num { color:#555; display:inline-block; width:20px; user-select:none; margin-right:10px; border-right:1px solid #333; }
        .code-input {
            background:transparent; border:none; color:#d4d4d4; font-family:inherit; font-size:inherit;
            width:calc(100% - 40px); outline:none;
        }
        .code-input::placeholder { color:#444; }
        .highlight-bracket { color: #f48771; font-weight:bold; }

        /* Error Shake */
        .editor-wrapper.error { border-color:#f48771; animation:shake 0.3s; }
        .error-msg { color:#f48771; font-size:12px; margin-top:5px; display:none; padding-left:5px; }

        .deploy-btn { 
            background:#0e639c; color:white; border:none; padding:10px 25px; border-radius:4px; 
            font-size:13px; font-weight:bold; cursor:pointer; float:right; margin-top:10px; font-family:'Consolas', monospace;
        }
        .deploy-btn:hover { background:#1177bb; }

        /* OVERLAYS */
        .overlay { position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); display:flex; justify-content:center; align-items:center; flex-direction:column; z-index:10; }
        #start-screen { position:fixed; top:0; left:0; width:100%; height:100%; background:#1e1e1e; z-index:9999; display:flex; justify-content:center; align-items:center; flex-direction:column; }
        .start-card { background:#252526; padding:50px; border-radius:12px; text-align:center; max-width:600px; border:1px solid #444; box-shadow:0 20px 50px rgba(0,0,0,0.7); }
        
        #report-screen { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); z-index:100; padding:50px; overflow-y:auto; }
        .stat-card { background:#222; padding:20px; margin-bottom:15px; border-radius:8px; border-left:5px solid #555; }

        @keyframes fadeIn { from{opacity:0; transform:translateY(5px);} to{opacity:1; transform:translateY(0);} }
        @keyframes shake { 0%{transform:translateX(0);} 25%{transform:translateX(-5px);} 75%{transform:translateX(5px);} 100%{transform:translateX(0);} }
        .hidden { display:none!important; }
    </style>
</head>
<body>

    <div id="loader">Loading Environment...</div>

    <div id="start-screen" style="display:none;">
        <div class="start-card">
            <div style="font-size:60px; margin-bottom:20px;">⚙️</div>
            <h1 style="color:white; margin:0 0 10px 0;">The Invisible Engineer</h1>
            <p style="color:#aaa; line-height:1.6; margin-bottom:30px;">
                "엔지니어의 코드는 누군가의 삶이 됩니다."<br>
                채팅을 통해 소통하고, <strong>직접 값을 수정하여</strong> 시스템을 설계하세요.
            </p>
            <button class="deploy-btn" style="float:none; padding:15px 40px; font-size:16px;" onclick="startGame()">Start Simulation</button>
        </div>
    </div>

    <div class="container" id="main-ui" style="opacity:0;">
        <div class="left-panel" id="left-panel">
            <div class="chat-header" id="chat-header">
                <span id="chat-title">💬 Project Room</span>
            </div>
            <div class="chat-body" id="chat-body"></div>
            <div class="choice-area" id="choice-area">
                <div id="typing" style="color:#666; font-size:12px; padding:10px; display:none;">입력 중...</div>
            </div>
        </div>

        <div class="right-panel">
            <div class="ide-header">
                <span style="margin-right:20px;">📄 config.yaml</span>
                <span>python 3.9</span>
            </div>
            <div class="ide-body">
                <div id="ide-overlay" class="overlay">
                    <div style="font-size:40px; margin-bottom:15px; opacity:0.5;">🔒</div>
                    <div style="color:#888;">메신저에서 합의가 완료되면 활성화됩니다.</div>
                </div>

                <div id="ide-content" class="hidden">
                    <div class="mission-box">
                        <div class="mission-title" id="mission-title">Mission</div>
                        <div class="mission-desc" id="mission-desc">Desc</div>
                    </div>
                    
                    <div class="input-group">
                        <div style="background:#252526; padding:10px; font-size:12px; color:#4ec9b0; margin-bottom:15px; border-radius:4px;">
                            💡 <strong>TIP:</strong> <code>{{...}}</code> 괄호와 내용을 지우고, 구체적인 숫자나 단어로 채워넣으세요.
                        </div>
                    </div>

                    <div class="input-group">
                        <div class="input-label">
                            <span id="q1-label">Parameter 1</span>
                        </div>
                        <div class="chips-area" id="q1-chips"></div>
                        <div class="editor-wrapper" id="wrap-q1">
                            <span class="line-num">1</span>
                            <input type="text" class="code-input" id="q1-input" placeholder="옵션을 선택하세요" autocomplete="off">
                        </div>
                        <div class="error-msg" id="q1-error">⚠️ 괄호 {{...}}를 지우고 값을 입력해야 합니다.</div>
                    </div>

                    <div class="input-group">
                        <div class="input-label">
                            <span id="q2-label">Parameter 2</span>
                        </div>
                        <div class="chips-area" id="q2-chips"></div>
                        <div class="editor-wrapper" id="wrap-q2">
                            <span class="line-num">2</span>
                            <input type="text" class="code-input" id="q2-input" placeholder="옵션을 선택하세요" autocomplete="off">
                        </div>
                        <div class="error-msg" id="q2-error">⚠️ 괄호 {{...}}를 지우고 값을 입력해야 합니다.</div>
                    </div>

                    <button class="deploy-btn" onclick="validateAndDeploy()">🚀 Deploy to Prod</button>
                </div>
            </div>
        </div>
    </div>

    <div id="report-screen">
        <div style="max-width:800px; margin:0 auto; background:#252526; padding:40px; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.5);">
            <h1 style="color:white; border-bottom:1px solid #444; padding-bottom:20px;">📊 Simulation Report</h1>
            <div id="report-content" style="margin-top:30px;"></div>
            <div style="text-align:center; margin-top:40px;">
                <button class="deploy-btn" style="float:none;" onclick="location.reload()">Restart</button>
            </div>
        </div>
    </div>

<script>
    // --- LOAD SAFETY ---
    window.onload = function() {
        document.getElementById('loader').style.display = 'none';
        document.getElementById('start-screen').style.display = 'flex';
    };

    // --- DATA ---
    const avatars = {
        ceo: { name:"최대표", color:"#ce9178", icon:"👔" },
        pm: { name:"박팀장", color:"#4ec9b0", icon:"📊" },
        agent: { name:"이지은", color:"#9cdcfe", icon:"🎧" },
        me: { name:"나", color:"#0e639c", icon:"👨‍💻" }
    };

    let currentStage = 0; // 0:CEO, 1:PM, 2:Agent
    let userChoices = [];

    const story = [
        // STAGE 0: CEO (Efficiency)
        {
            role: "ceo",
            init: ["김 수석, 이번 AICC 프로젝트 아주 중요해.", "경쟁사는 벌써 비용 30% 줄였어. 우린 무조건 **'속도'**가 최우선이야."],
            branches: [
                { label: "순응", text: "알겠습니다. 효율성 극대화 모델로 설계하겠습니다.", reply: "그래! 역시 말이 통하네. 바로 작업 시작해.", mood: "happy" },
                { label: "우려", text: "대표님, 무조건적인 속도 경쟁은 품질 저하가 우려됩니다.", reply: "지금 품질 따질 때야? 투자 못 받으면 다 끝이라고! 시키는 대로 해!", mood: "angry" }
            ],
            ide: {
                title: "Mission 1: 초기 아키텍처 설계",
                desc: "CEO 지시: 처리 속도(AHT)를 최우선으로 하는 설정을 입력하십시오.",
                q1: { l: "AI 역할 정의", chips: [ {l:"Gatekeeper", c:"role: AI_First (Goal: {{90%}})"}, {l:"Router", c:"role: Hybrid (Split: {{50:50}})"} ] },
                q2: { l: "대기 시간", chips: [ {l:"Zero Gap", c:"gap: {{0초}} (Immediate)"}, {l:"Fixed", c:"gap: {{10초}} (Fixed)"} ] }
            }
        },
        // STAGE 1: PM (Accuracy)
        {
            role: "pm",
            init: ["수석님, V1 배포하고 난리 났습니다. 속도는 빠른데... **'말귀를 못 알아듣는다'**는 민원이 폭주 중이에요.", "재문의율이 40% 늘었어요. 정확도 좀 높여주세요."],
            branches: [
                { label: "수용", text: "문제가 심각하군요. 문맥 분석 기능을 강화하겠습니다.", reply: "네, 부탁드립니다. 이번엔 제발 실수 없게 해주세요.", mood: "neutral" },
                { label: "방어", text: "CEO 지시대로 속도만 맞춘 건데요. 데이터가 더 필요합니다.", reply: "하... 핑계 대지 마시고요. 당장 고객 다 떠나가게 생겼다고요!", mood: "angry" }
            ],
            ide: {
                title: "Mission 2: 로직 고도화",
                desc: "PM 요청: 오분류를 줄이고 정확도를 높이십시오.",
                q1: { l: "분석 모델", chips: [ {l:"Deep Context", c:"model: Context (Depth: {{Deep}})"}, {l:"Keyword", c:"model: Simple (Speed: {{Fast}})"} ] },
                q2: { l: "실패 처리", chips: [ {l:"Handover", c:"fallback: {{상담원 연결}}"}, {l:"Retry", c:"fallback: {{재질문}}"} ] }
            }
        },
        // STAGE 2: AGENT (Humanity)
        {
            role: "agent",
            interview: true,
            init: ["(인터뷰룸) 안녕하세요 엔지니어님. 현장 매니저 이지은입니다.", "솔직히 말씀드릴게요. 지금 시스템... 저희한텐 지옥이에요. 쉴 틈도 없고, 화난 고객만 넘어오고...", "제발 **사람**을 고려해서 설계해주세요."],
            branches: [
                { label: "공감/해결", text: "그런 고충이 있는 줄 몰랐습니다. 상담원 보호 기능을 최우선으로 넣겠습니다.", reply: "정말요...? 감사합니다. 엔지니어님만 믿겠습니다.", mood: "touched" },
                { label: "현실적 거절", text: "안타깝지만 효율성 지표가 떨어지면 경영진 승인이 어렵습니다.", reply: "결국 숫자가 사람보다 중요하단 거네요... 실망입니다.", mood: "sad" }
            ],
            ide: {
                title: "Mission 3: 지속 가능성 (Human-Centric)",
                desc: "현장 피드백: 상담원 보호 및 휴식권 보장 로직을 구현하십시오.",
                q1: { l: "욕설 방어", chips: [ {l:"Shield On", c:"protection: Active (Action: {{차단}})"}, {l:"Ignore", c:"protection: None (Log: {{기록만}})"} ] },
                q2: { l: "휴식 배정", chips: [ {l:"Dynamic", c:"break: Smart (Trigger: {{스트레스 지수}})"}, {l:"Manual", c:"break: Manual (Request: {{승인제}})"} ] }
            }
        }
    ];

    // --- ENGINE ---
    function startGame() {
        document.getElementById('start-screen').style.display = 'none';
        document.getElementById('main-ui').style.opacity = '1';
        playStage(0);
    }

    function playStage(idx) {
        currentStage = idx;
        const s = story[idx];
        
        if(s.interview) {
            document.getElementById('left-panel').style.background = '#151515';
            document.getElementById('chat-title').innerHTML = "🎙️ 현장 인터뷰 <span style='color:red; font-size:12px'>● REC</span>";
        } else {
            document.getElementById('left-panel').style.background = '#252526';
            document.getElementById('chat-title').innerText = "💬 Project Room";
        }

        document.getElementById('choice-area').innerHTML = '<div id="typing" style="color:#666; font-size:12px; padding:10px; display:none;">상대방 입력 중...</div>';
        
        botTyping(s.role, s.init, () => showChoices(s.branches));
    }

    function botTyping(role, msgs, onComplete, idx=0) {
        if(idx >= msgs.length) {
            onComplete();
            return;
        }
        document.getElementById('typing').style.display = 'block';
        setTimeout(() => {
            addMsg(role, msgs[idx]);
            botTyping(role, msgs, onComplete, idx+1);
        }, 1000);
    }

    function addMsg(role, text) {
        const body = document.getElementById('chat-body');
        const isMe = role === 'me';
        const sender = isMe ? avatars.me : avatars[role];
        
        const row = document.createElement('div');
        row.className = `msg-row ${isMe ? 'me' : ''}`;
        row.innerHTML = `
            <div class="avatar" style="background:${sender.color}">${sender.icon}</div>
            <div>
                <div class="sender-name" style="text-align:${isMe?'right':'left'}">${sender.name}</div>
                <div class="bubble ${isMe ? 'me' : 'other'}">${text}</div>
            </div>
        `;
        body.appendChild(row);
        body.scrollTop = body.scrollHeight;
    }

    function showChoices(branches) {
        document.getElementById('typing').style.display = 'none';
        const area = document.getElementById('choice-area');
        
        branches.forEach(b => {
            const btn = document.createElement('div');
            btn.className = 'choice-btn';
            btn.innerHTML = `<span class="choice-label">[${b.label}]</span> ${b.text}`;
            btn.onclick = () => {
                area.innerHTML = ''; // Hide buttons
                addMsg('me', b.text);
                userChoices.push({ stage: currentStage, choice: b.label });
                
                setTimeout(() => {
                    addMsg(story[currentStage].role, b.reply);
                    setTimeout(() => unlockIDE(), 1000);
                }, 800);
            };
            area.appendChild(btn);
        });
    }

    // --- IDE LOGIC ---
    function unlockIDE() {
        document.getElementById('ide-overlay').style.display = 'none';
        document.getElementById('ide-content').classList.remove('hidden');
        
        const data = story[currentStage].ide;
        document.getElementById('mission-title').innerText = data.title;
        document.getElementById('mission-desc').innerText = data.desc;
        
        setupQuestion('q1', data.q1);
        setupQuestion('q2', data.q2);
    }

    function setupQuestion(id, qData) {
        document.getElementById(`${id}-label`).innerText = qData.l;
        document.getElementById(`${id}-input`).value = "";
        const chipArea = document.getElementById(`${id}-chips`);
        chipArea.innerHTML = "";
        
        qData.chips.forEach(c => {
            const chip = document.createElement('div');
            chip.className = 'chip';
            chip.innerText = c.l;
            chip.onclick = () => {
                const inp = document.getElementById(`${id}-input`);
                inp.value = c.c;
                inp.focus();
                inp.parentElement.classList.remove('error');
                document.getElementById(`${id}-error`).style.display = 'none';
            };
            chipArea.appendChild(chip);
        });
    }

    function validateAndDeploy() {
        const i1 = document.getElementById('q1-input');
        const i2 = document.getElementById('q2-input');
        let valid = true;

        [i1, i2].forEach((inp, idx) => {
            const wrapper = inp.parentElement;
            const errId = idx === 0 ? 'q1-error' : 'q2-error';
            
            if (inp.value.includes('{{') || inp.value.trim() === "") {
                wrapper.classList.add('error');
                document.getElementById(errId).style.display = 'block';
                valid = false;
            } else {
                wrapper.classList.remove('error');
                document.getElementById(errId).style.display = 'none';
            }
        });

        if (!valid) return;

        // ANIMATE DEPLOY
        document.getElementById('ide-content').classList.add('hidden');
        document.getElementById('ide-overlay').style.display = 'flex';
        document.getElementById('ide-overlay').innerHTML = `<h2 style="color:#4ec9b0">🚀 Deploying...</h2><p>Applying changes to server...</p>`;
        
        setTimeout(() => {
            document.getElementById('ide-overlay').innerHTML = `<div style="font-size:40px; margin-bottom:15px; opacity:0.5;">🔒</div><div style="color:#888;">메신저를 확인하세요.</div>`;
            
            if (currentStage < 2) {
                addMsg('System', `✅ Ver.${currentStage+1}.0 Update Complete.`);
                setTimeout(() => playStage(currentStage + 1), 1500);
            } else {
                showReport();
            }
        }, 2000);
    }

    function showReport() {
        document.getElementById('report-screen').style.display = 'block';
        const content = document.getElementById('report-content');
        
        const pathHTML = userChoices.map((c, i) => `
            <div class="stat-card" style="border-left: 5px solid ${i==2 ? '#9cdcfe' : '#ce9178'}">
                <h3>Stage ${i+1}: ${['CEO', 'PM', 'Agent'][i]}</h3>
                <p>당신의 태도: <strong style="color:white">${c.choice}</strong></p>
                <p style="color:#aaa; font-size:13px;">→ 그에 따른 시스템 설계 반영됨</p>
            </div>
        `).join('');
        
        content.innerHTML = pathHTML + `
            <div style="margin-top:30px; text-align:center; color:#ccc; line-height:1.6;">
                "효율(Efficiency)과 인간(Humanity) 사이에서,<br>
                엔지니어는 매 순간 선택을 강요받습니다."
            </div>
        `;
    }

</script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=False)
