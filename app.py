import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Invisible Engineer V7.4", layout="wide")

# 2. 스타일 설정
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        #MainMenu { visibility: hidden; }
        .stApp { background-color: #1e1e1e; overflow: hidden; }
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

        /* IDE UI */
        .ide-header { height:45px; background:#1e1e1e; border-bottom:1px solid #333; display:flex; align-items:center; padding:0 20px; color:#858585; font-size:13px; font-family:'Consolas', monospace; }
        .ide-body { flex:1; padding:40px; overflow-y:auto; position:relative; background:#1e1e1e; }

        .mission-box { background:#252526; padding:20px; border-radius:6px; border-left:3px solid #3794ff; margin-bottom:30px; }
        .mission-title { font-size:16px; font-weight:bold; color:white; margin-bottom:8px; }
        .mission-desc { color:#ccc; font-size:14px; line-height:1.5; }

        .input-group { margin-bottom:30px; }
        .input-label { color:#d4d4d4; font-size:13px; margin-bottom:8px; display:flex; justify-content:space-between; }
        
        .chips-area { display:flex; gap:8px; margin-bottom:10px; }
        .chip { 
            background:#2d2d2d; padding:6px 12px; border-radius:4px; font-size:12px; 
            cursor:pointer; border:1px solid #444; color:#ccc; font-family:'Consolas', monospace; 
        }
        .chip:hover { border-color:#3794ff; color:white; }

        .editor-wrapper {
            background:#111; border:1px solid #333; border-radius:4px; padding:15px; position:relative;
            font-family:'Consolas', 'Monaco', monospace; font-size:14px; line-height:1.6; display:flex;
        }
        .editor-wrapper:focus-within { border-color:#3794ff; }
        .line-num { color:#555; display:inline-block; width:20px; user-select:none; margin-right:15px; border-right:1px solid #333; height:100%; text-align:right; padding-right:10px;}
        .code-input {
            background:transparent; border:none; color:#d4d4d4; font-family:inherit; font-size:inherit;
            flex:1; outline:none;
        }
        .code-input::placeholder { color:#444; font-style:italic; }
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
        
        /* --- REPORT SCREEN (PERSONA CARD STYLE) --- */
        #report-screen { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); z-index:100; padding:40px; overflow-y:auto; box-sizing:border-box; }
        
        .timeline-container { display:flex; gap:20px; overflow-x:auto; padding-bottom:20px; justify-content:center; }
        
        .persona-card { 
            background:#252526; border-radius:12px; width:280px; padding:20px; flex-shrink:0; border:1px solid #444; position:relative; 
            transition: transform 0.3s;
        }
        .persona-card:hover { transform: translateY(-5px); border-color:#3794ff; }
        
        .stage-badge { 
            position:absolute; top:-10px; left:20px; background:#3794ff; color:white; 
            padding:4px 12px; border-radius:15px; font-size:11px; font-weight:bold; 
        }
        
        .persona-avatar { font-size:50px; text-align:center; margin:15px 0 10px 0; }
        .persona-quote { font-style:italic; color:#ccc; font-size:13px; text-align:center; margin-bottom:20px; min-height:40px; }
        
        .stat-group { margin-bottom:10px; }
        .stat-label { font-size:11px; color:#888; display:flex; justify-content:space-between; margin-bottom:3px; }
        .stat-track { height:6px; background:#111; border-radius:3px; overflow:hidden; }
        .stat-fill { height:100%; border-radius:3px; transition:width 1s; }
        
        .change-indicator { font-size:10px; font-weight:bold; }
        .plus { color:#4ec9b0; }
        .minus { color:#f48771; }

        @keyframes fadeIn { from{opacity:0; transform:translateY(5px);} to{opacity:1; transform:translateY(0);} }
        @keyframes shake { 0%{transform:translateX(0);} 25%{transform:translateX(-5px);} 75%{transform:translateX(5px);} 100%{transform:translateX(0);} }
        .hidden { display:none!important; }
    </style>
</head>
<body>

    <div id="loader">System Initializing...</div>

    <div id="start-screen" style="display:none;">
        <div class="start-card">
            <div style="font-size:60px; margin-bottom:20px;">⚙️</div>
            <h1 style="color:white; margin:0 0 10px 0;">The Invisible Engineer</h1>
            <p style="color:#aaa; line-height:1.6; margin-bottom:30px;">
                당신의 선택과 코드가 <strong>'한 사람의 인생'</strong>을 결정합니다.<br>
                대화하고, 수정하고, 결과를 목격하세요.
            </p>
            <button class="deploy-btn" style="float:none; padding:15px 40px; font-size:16px;" onclick="startGame()">시뮬레이션 시작</button>
        </div>
    </div>

    <div class="container" id="main-ui" style="opacity:0;">
        <div class="left-panel" id="left-panel">
            <div class="chat-header" id="chat-header">
                <span id="chat-title">💬 Project Room</span>
                <span style="font-size:12px; color:#4ec9b0;">● Online</span>
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
                    <div style="color:#888;">메신저에서 합의가 끝나면 에디터가 열립니다.</div>
                </div>

                <div id="ide-content" class="hidden">
                    <div class="mission-box">
                        <div class="mission-title" id="mission-title">Mission</div>
                        <div class="mission-desc" id="mission-desc">Desc</div>
                    </div>
                    
                    <div style="background:#252526; padding:10px; font-size:12px; color:#dcdcaa; margin-bottom:20px; border-radius:4px; border:1px solid #444;">
                        💡 <strong>Tip:</strong> <code>[값 입력]</code> 부분을 지우고 원하는 숫자를 입력하세요.
                    </div>

                    <div class="input-group">
                        <div class="input-label">
                            <span id="q1-label">Parameter 1</span>
                        </div>
                        <div class="chips-area" id="q1-chips"></div>
                        <div class="editor-wrapper" id="wrap-q1">
                            <span class="line-num">1</span>
                            <input type="text" class="code-input" id="q1-input" placeholder="Chip을 클릭하세요" autocomplete="off">
                        </div>
                        <div class="error-msg" id="q1-error">⚠️ 대괄호 [...]를 지우고 값을 입력해주세요.</div>
                    </div>

                    <div class="input-group">
                        <div class="input-label">
                            <span id="q2-label">Parameter 2</span>
                        </div>
                        <div class="chips-area" id="q2-chips"></div>
                        <div class="editor-wrapper" id="wrap-q2">
                            <span class="line-num">2</span>
                            <input type="text" class="code-input" id="q2-input" placeholder="Chip을 클릭하세요" autocomplete="off">
                        </div>
                        <div class="error-msg" id="q2-error">⚠️ 대괄호 [...]를 지우고 값을 입력해주세요.</div>
                    </div>

                    <button class="deploy-btn" onclick="validateAndDeploy()">🚀 Deploy to Prod</button>
                </div>
            </div>
        </div>
    </div>

    <div id="report-screen">
        <div style="max-width:1000px; margin:0 auto;">
            <h1 style="color:white; text-align:center; margin-bottom:40px;">📊 Worker Evolution Report</h1>
            
            <div id="timeline" class="timeline-container">
                </div>

            <div style="text-align:center; margin-top:40px;">
                <p style="color:#888;">"당신의 기술적 결정이 한 사람의 일상을 이렇게 변화시켰습니다."</p>
                <button class="deploy-btn" style="float:none;" onclick="location.reload()">Restart Experiment</button>
            </div>
        </div>
    </div>

<script>
    window.onload = function() {
        document.getElementById('loader').style.display = 'none';
        document.getElementById('start-screen').style.display = 'flex';
    };

    const avatars = {
        ceo: { name:"최대표", color:"#ce9178", icon:"👔" },
        pm: { name:"박팀장", color:"#4ec9b0", icon:"📊" },
        agent: { name:"이지은", color:"#9cdcfe", icon:"🎧" },
        me: { name:"나", color:"#0e639c", icon:"👨‍💻" },
        system: { name:"System", color:"#666", icon:"💻" }
    };

    let currentStage = 0; 
    let userChoices = []; // Stores choice type: 'E'(Efficiency), 'B'(Balance), 'H'(Human)

    // SCENARIO DATA
    const story = [
        {
            role: "ceo",
            init: ["김 수석, 경쟁사가 치고 올라오네.", "우린 무조건 **'속도'**가 최우선이야. 알겠지?"],
            branches: [
                { label: "순응", text: "알겠습니다. 효율성 극대화 모델로 설계하겠습니다.", reply: "그래! 역시 말이 통하네. 바로 작업해.", type: "E" },
                { label: "우려", text: "속도 경쟁은 품질 저하가 우려됩니다.", reply: "지금 품질 따질 때야? 투자 못 받으면 다 끝이야!", type: "H" }
            ],
            ide: {
                title: "Quest 1: 초기 아키텍처 설계",
                desc: "CEO 지시: 처리 속도(AHT)를 최우선으로 하는 설정을 입력하십시오.",
                q1: { l: "AI 역할 정의", chips: [ {l:"Gatekeeper (효율)", c:"role: AI_First (Goal: [90%])"}, {l:"Router (균형)", c:"role: Hybrid (Split: [50:50])"} ] },
                q2: { l: "대기 시간", chips: [ {l:"Zero Gap (속도)", c:"gap: [0초]"}, {l:"Fixed (여유)", c:"gap: [10초]"} ] }
            }
        },
        {
            role: "pm",
            init: ["수석님, V1 배포하고 난리 났습니다. 속도는 빠른데... **'말귀를 못 알아듣는다'**는 민원이 폭주 중이에요.", "정확도 좀 높여주세요."],
            branches: [
                { label: "수용", text: "문맥 분석 기능을 강화하겠습니다.", reply: "네, 부탁드립니다. 이번엔 실수 없게 해주세요.", type: "B" },
                { label: "방어", text: "CEO 지시대로 속도만 맞춘 건데요.", reply: "하... 핑계 대지 마시고요. 당장 해결해주세요!", type: "E" }
            ],
            ide: {
                title: "Quest 2: 로직 고도화",
                desc: "PM 요청: 오분류를 줄이고 정확도를 높이십시오.",
                q1: { l: "분석 모델", chips: [ {l:"Deep Context", c:"model: Context (Depth: [Deep])"}, {l:"Keyword", c:"model: Simple (Speed: [Fast])"} ] },
                q2: { l: "실패 처리", chips: [ {l:"Handover", c:"fallback: [상담원 연결]"}, {l:"Retry", c:"fallback: [재질문]"} ] }
            }
        },
        {
            role: "agent",
            interview: true,
            init: ["(인터뷰룸) 안녕하세요 엔지니어님. 현장 매니저 이지은입니다.", "솔직히... 지금 시스템은 저희한텐 지옥이에요. 쉴 틈도 없고, 화난 고객만 넘어오고...", "제발 **사람**을 고려해서 설계해주세요."],
            branches: [
                { label: "공감/해결", text: "그런 고충이 있는 줄 몰랐습니다. 보호 기능을 최우선으로 넣겠습니다.", reply: "정말요...? 감사합니다. 믿겠습니다.", type: "H" },
                { label: "현실적 거절", text: "안타깝지만 효율성 지표가 우선입니다.", reply: "결국 숫자가 사람보다 중요하단 거네요...", type: "E" }
            ],
            ide: {
                title: "Quest 3: 지속 가능성 (Human-Centric)",
                desc: "현장 피드백: 상담원 보호 및 휴식권 보장 로직을 구현하십시오.",
                q1: { l: "욕설 방어", chips: [ {l:"Shield On", c:"protection: Active (Action: [차단])"}, {l:"Ignore", c:"protection: None (Log: [기록만])"} ] },
                q2: { l: "휴식 배정", chips: [ {l:"Dynamic", c:"break: Smart (Trigger: [스트레스 지수])"}, {l:"Manual", c:"break: Manual (Request: [승인제])"} ] }
            }
        }
    ];

    // --- GAME LOGIC ---
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
        if(idx >= msgs.length) { onComplete(); return; }
        document.getElementById('typing').style.display = 'block';
        setTimeout(() => {
            addMsg(role, msgs[idx]);
            botTyping(role, msgs, onComplete, idx+1);
        }, 1000);
    }

    function addMsg(role, text) {
        const body = document.getElementById('chat-body');
        const isMe = role === 'me';
        const sender = isMe ? avatars.me : (avatars[role] || avatars.system);
        
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
                area.innerHTML = '';
                addMsg('me', b.text);
                userChoices.push(b.type); // Track User Choice Type
                
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
            
            if (inp.value.includes('[') || inp.value.trim() === "") {
                wrapper.classList.add('error');
                document.getElementById(errId).style.display = 'block';
                valid = false;
            } else {
                wrapper.classList.remove('error');
                document.getElementById(errId).style.display = 'none';
            }
        });

        if (!valid) return;

        document.getElementById('ide-content').classList.add('hidden');
        document.getElementById('ide-overlay').style.display = 'flex';
        document.getElementById('ide-overlay').innerHTML = `<h2 style="color:#4ec9b0">🚀 배포 중...</h2>`;
        
        setTimeout(() => {
            document.getElementById('ide-overlay').innerHTML = `<div style="font-size:40px; margin-bottom:15px; opacity:0.5;">🔒</div><div style="color:#888;">메신저를 확인하세요.</div>`;
            
            if (currentStage < 2) {
                addMsg('system', `✅ Ver.${currentStage+1}.0 Update Complete.`);
                setTimeout(() => playStage(currentStage + 1), 1500);
            } else {
                generateReport();
            }
        }, 2000);
    }

    // --- REPORT LOGIC (WORKER EVOLUTION) ---
    function generateReport() {
        document.getElementById('report-screen').style.display = 'block';
        const timeline = document.getElementById('timeline');
        
        // Initial Stats
        let stats = { mental: 80, physical: 80, skill: 50 };
        
        const stages = ["Stage 1: Launch", "Stage 2: Feedback", "Stage 3: Result"];
        const quotes = [
            ["(기대) 새로운 시스템이라니.. 일이 좀 편해질까?", "(걱정) AI가 들어오면 우린 어떻게 되는 거지?"],
            ["(고통) 말귀 못 알아듣는 AI 때문에 내가 욕을 두 배로 먹어...", "(안도) 오, AI가 제법 똑똑하게 도와주네?"],
            ["(절망) 기계 부품이 된 기분이야. 더는 못 하겠어. (퇴사 결심)", "(성장) 이제야 진짜 '상담'을 하는 기분이야. 전문가가 된 느낌!"]
        ];

        let html = "";

        userChoices.forEach((choice, i) => {
            // Logic: E(Efficiency) -> Stats Down, H(Human) -> Stats Up
            let mood = "😐";
            let quote = "";
            let change = { m:0, p:0, s:0 };

            if (choice === 'E') { 
                stats.mental -= 30; stats.physical -= 30; stats.skill += 5; 
                mood = "😫"; 
                quote = (i === 2) ? quotes[2][0] : quotes[i][0];
                change = { m:-30, p:-30, s:5 };
            } else if (choice === 'B') {
                stats.mental -= 10; stats.physical -= 10; stats.skill += 20;
                mood = "😐";
                quote = "조금 복잡하긴 한데, 적응하면 괜찮을지도...";
                change = { m:-10, p:-10, s:20 };
            } else { // H
                stats.mental += 10; stats.physical += 10; stats.skill += 30;
                mood = "😊";
                quote = (i === 2) ? quotes[2][1] : quotes[i][1];
                change = { m:10, p:10, s:30 };
            }

            // Cap stats
            stats.mental = Math.max(0, Math.min(100, stats.mental));
            
            // Render Card
            html += `
                <div class="persona-card">
                    <div class="stage-badge">${stages[i]}</div>
                    <div class="persona-avatar">${mood}</div>
                    <div class="persona-quote">"${quote}"</div>
                    
                    <div class="stat-group">
                        <div class="stat-label">
                            <span>❤️ 심리적 안정</span>
                            <span class="change-indicator ${change.m >= 0 ? 'plus' : 'minus'}">
                                ${stats.mental}% (${change.m>=0?'+':''}${change.m})
                            </span>
                        </div>
                        <div class="stat-track"><div class="stat-fill" style="width:${stats.mental}%; background:${change.m<0 ? '#f48771':'#4ec9b0'}"></div></div>
                    </div>

                    <div class="stat-group">
                        <div class="stat-label">
                            <span>⚡️ 육체적 여유</span>
                            <span class="change-indicator ${change.p >= 0 ? 'plus' : 'minus'}">
                                ${stats.physical}% (${change.p>=0?'+':''}${change.p})
                            </span>
                        </div>
                        <div class="stat-track"><div class="stat-fill" style="width:${stats.physical}%; background:${change.p<0 ? '#f48771':'#4ec9b0'}"></div></div>
                    </div>

                    <div class="stat-group">
                        <div class="stat-label">
                            <span>📘 직무 전문성</span>
                            <span class="change-indicator plus">
                                ${stats.skill}% (+${change.s})
                            </span>
                        </div>
                        <div class="stat-track"><div class="stat-fill" style="width:${stats.skill}%; background:#3794ff"></div></div>
                    </div>
                </div>
            `;
        });

        timeline.innerHTML = html;
    }

</script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=False)
