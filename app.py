import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Invisible Engineer V7.7", layout="wide")

# 2. 스타일 설정 (여백 최소화)
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
        /* HEIGHT FIX: 100vh로 화면 꽉 채움 */
        html, body { margin:0; padding:0; width:100%; height:100vh; background-color:#1e1e1e; font-family:'Pretendard', sans-serif; color:#d4d4d4; overflow:hidden; }
        
        #loader { position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); color:#3794ff; font-weight:bold; }

        .container { display:flex; width:100%; height:100%; }
        .left-panel { width:400px; background:#252526; border-right:1px solid #333; display:flex; flex-direction:column; transition:0.3s; }
        .right-panel { flex:1; display:flex; flex-direction:column; background:#1e1e1e; position:relative; }

        /* CHAT UI */
        .chat-header { padding:15px; border-bottom:1px solid #333; background:#2d2d2d; font-weight:bold; color:white; display:flex; justify-content:space-between; align-items:center; height:50px; box-sizing:border-box;}
        .chat-body { flex:1; padding:15px; overflow-y:auto; display:flex; flex-direction:column; gap:12px; scroll-behavior: smooth; }
        
        .msg-row { display:flex; gap:10px; animation:fadeIn 0.3s; }
        .msg-row.me { flex-direction:row-reverse; }
        .avatar { width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:18px; }
        .bubble { padding:10px 14px; border-radius:10px; font-size:13px; line-height:1.4; max-width:260px; box-shadow:0 1px 3px rgba(0,0,0,0.3); }
        .bubble.other { background:#383838; border-top-left-radius:2px; }
        .bubble.me { background:#0e639c; color:white; border-top-right-radius:2px; }
        
        /* CHOICE AREA (Compact) */
        .choice-area { padding:10px; border-top:1px solid #333; background:#2d2d2d; min-height:80px; display:flex; flex-direction:column; gap:6px; }
        .choice-btn { 
            background:#3c3c3c; border:1px solid #555; color:#ddd; padding:10px; border-radius:6px; 
            cursor:pointer; text-align:left; transition:0.2s; font-size:12px;
        }
        .choice-btn:hover { border-color:#3794ff; background:#444; color:white; }

        /* IDE UI */
        .ide-header { height:50px; background:#1e1e1e; border-bottom:1px solid #333; display:flex; align-items:center; padding:0 20px; color:#858585; font-size:13px; font-family:'Consolas', monospace; box-sizing:border-box;}
        .ide-body { flex:1; padding:20px; overflow-y:auto; position:relative; background:#1e1e1e; }

        .mission-box { background:#252526; padding:15px; border-radius:6px; border-left:3px solid #3794ff; margin-bottom:20px; }
        .mission-title { font-size:15px; font-weight:bold; color:white; margin-bottom:5px; }
        .mission-desc { color:#ccc; font-size:13px; line-height:1.4; }

        /* CODE INPUT AREA - REFACTORED FOR ITERATION */
        .config-section { margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:15px; }
        .section-label { color:#4ec9b0; font-size:12px; font-weight:bold; margin-bottom:8px; font-family:'Consolas', monospace; }
        
        .chips-area { display:flex; gap:6px; margin-bottom:8px; flex-wrap:wrap; }
        .chip { 
            background:#2d2d2d; padding:5px 10px; border-radius:4px; font-size:11px; 
            cursor:pointer; border:1px solid #444; color:#ccc; font-family:'Pretendard', sans-serif; 
        }
        .chip:hover { border-color:#3794ff; color:white; }

        .editor-wrapper {
            background:#111; border:1px solid #333; border-radius:4px; padding:10px; position:relative;
            font-family:'Pretendard', sans-serif; font-size:13px; line-height:1.5; display:flex; align-items:center;
        }
        .editor-wrapper:focus-within { border-color:#3794ff; }
        .line-num { color:#555; width:20px; text-align:right; margin-right:10px; font-family:'Consolas', monospace; font-size:12px;}
        .code-input {
            background:transparent; border:none; color:#d4d4d4; font-family:inherit; font-size:inherit;
            flex:1; outline:none; width: 100%;
        }
        .code-input::placeholder { color:#444; font-style:italic; }
        .editor-wrapper.error { border-color:#f48771; animation:shake 0.3s; }

        .deploy-btn { 
            background:#0e639c; color:white; border:none; padding:10px 25px; border-radius:4px; 
            font-size:13px; font-weight:bold; cursor:pointer; float:right; margin-top:10px; font-family:'Consolas', monospace;
        }
        .deploy-btn:hover { background:#1177bb; }

        /* OVERLAYS */
        .overlay { position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); display:flex; justify-content:center; align-items:center; flex-direction:column; z-index:10; }
        #start-screen { position:fixed; top:0; left:0; width:100%; height:100%; background:#1e1e1e; z-index:9999; display:flex; justify-content:center; align-items:center; flex-direction:column; }
        .start-card { background:#252526; padding:40px; border-radius:12px; text-align:center; max-width:500px; border:1px solid #444; box-shadow:0 20px 50px rgba(0,0,0,0.7); }
        
        /* REPORT SCREEN */
        #report-screen { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.98); z-index:100; padding:30px; overflow-y:auto; box-sizing:border-box; }
        .persona-card { 
            background:#252526; border-radius:12px; width:260px; padding:20px; flex-shrink:0; border:1px solid #444; position:relative; margin:10px;
        }
        .timeline-container { display:flex; gap:20px; justify-content:center; flex-wrap:wrap; padding-bottom:50px; }

        /* ANIMATIONS */
        @keyframes fadeIn { from{opacity:0; transform:translateY(5px);} to{opacity:1; transform:translateY(0);} }
        @keyframes shake { 0%{transform:translateX(0);} 25%{transform:translateX(-5px);} 75%{transform:translateX(5px);} 100%{transform:translateX(0);} }
        .hidden { display:none!important; }
    </style>
</head>
<body>

    <div id="loader">System Initializing...</div>

    <div id="start-screen" style="display:none;">
        <div class="start-card">
            <div style="font-size:50px; margin-bottom:20px;">⚙️</div>
            <h2 style="color:white; margin:0 0 10px 0;">The Invisible Engineer</h2>
            <p style="color:#aaa; font-size:14px; line-height:1.5; margin-bottom:25px;">
                콜센터 AI 시스템을 설계하는 엔지니어 시뮬레이션입니다.<br>
                경영진, 기획자, 상담원의 피드백을 반영하며<br>
                <strong>시스템 설정을 반복적으로 수정(Refactoring)</strong>하세요.
            </p>
            <button class="deploy-btn" style="float:none; padding:12px 30px;" onclick="startGame()">Start Simulation</button>
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
                <span style="margin-right:20px;">📄 system_config.yaml</span>
                <span>Plain Text</span>
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
                    
                    <div class="config-section">
                        <div class="section-label">1. ARCHITECTURE (역할/권한)</div>
                        <div class="chips-area" id="c1-chips"></div>
                        <div class="editor-wrapper">
                            <span class="line-num">10</span>
                            <input type="text" class="code-input" id="c1-input" placeholder="Chip을 클릭하거나 직접 입력" autocomplete="off">
                        </div>
                    </div>

                    <div class="config-section">
                        <div class="section-label">2. DATA LOGIC (분석 깊이)</div>
                        <div class="chips-area" id="c2-chips"></div>
                        <div class="editor-wrapper">
                            <span class="line-num">24</span>
                            <input type="text" class="code-input" id="c2-input" placeholder="Chip을 클릭하거나 직접 입력" autocomplete="off">
                        </div>
                    </div>

                    <div class="config-section" style="border:none;">
                        <div class="section-label">3. WORKFLOW (속도/휴식)</div>
                        <div class="chips-area" id="c3-chips"></div>
                        <div class="editor-wrapper">
                            <span class="line-num">38</span>
                            <input type="text" class="code-input" id="c3-input" placeholder="Chip을 클릭하거나 직접 입력" autocomplete="off">
                        </div>
                    </div>

                    <div style="color:#f48771; font-size:12px; margin-top:5px; display:none;" id="global-error">⚠️ 모든 설정값의 대괄호 [...]를 지우고 구체적인 값을 입력해야 합니다.</div>
                    <button class="deploy-btn" onclick="validateAndDeploy()">🚀 Update System</button>
                </div>
            </div>
        </div>
    </div>

    <div id="report-screen">
        <div style="max-width:1000px; margin:0 auto;">
            <h1 style="color:white; text-align:center; margin-bottom:30px;">📊 Worker Evolution Report</h1>
            <div id="timeline" class="timeline-container"></div>
            <div style="text-align:center; margin-top:30px; border-top:1px solid #333; padding-top:20px;">
                <p style="color:#888; font-size:14px; margin-bottom:20px;">실험이 종료되었습니다.</p>
                <div style="display:flex; justify-content:center; gap:15px;">
                    <button class="deploy-btn" style="float:none; background:#333; border:1px solid #555;" onclick="location.reload()">🔄 다시 하기</button>
                    <button class="deploy-btn" style="float:none;" onclick="window.open('https://forms.google.com/your-survey-url', '_blank')">📝 설문조사 참여</button>
                </div>
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
        pm: { name:"박팀장(기획)", color:"#4ec9b0", icon:"📊" },
        agent: { name:"이지은(현장)", color:"#9cdcfe", icon:"🎧" },
        me: { name:"나", color:"#0e639c", icon:"👨‍💻" },
        system: { name:"System", color:"#666", icon:"💻" }
    };

    let currentStage = 0; 
    let userChoices = [];

    // --- REFACTORED SCENARIOS (Iterative Dashboard) ---
    // User edits the SAME 3 parameters in every stage based on new context
    const story = [
        {
            role: "ceo",
            init: ["김 수석, 경쟁사가 치고 올라오네.", "우린 무조건 '속도'와 '효율'이 최우선이야."],
            branches: [
                { label: "순응", text: "알겠습니다. 효율성 극대화 모델로 설계하겠습니다.", reply: "그래! 역시 말이 통하네. 바로 작업해.", type: "E" },
                { label: "우려", text: "속도 경쟁은 품질 저하가 우려됩니다.", reply: "지금 품질 따질 때야? 투자 못 받으면 다 끝이야!", type: "H" }
            ],
            ide: {
                title: "V1.0 Build: 초기 아키텍처 설계",
                desc: "CEO 지시: 처리 속도(AHT)와 비용 절감을 최우선으로 하는 설정을 입력하십시오.",
                c1: { chips: [{l:"Gatekeeper (효율)", c:"AI가 [단순 문의]는 전담 처리하고, 해결 불가 시에만 상담원 연결"}, {l:"Standard (품질)", c:"모든 문의를 상담원에게 연결하되 AI가 [분류]만 수행"}] },
                c2: { chips: [{l:"Fast (속도)", c:"감정 분석 없이 [키워드] 위주로 빠르게 의도 파악"}, {l:"Deep (정확)", c:"[전체 맥락]과 감정 상태를 정밀 분석"}] },
                c3: { chips: [{l:"Zero Gap (속도)", c:"종료 즉시 [0초] 만에 다음 콜 자동 연결"}, {l:"Manual (여유)", c:"상담원이 [준비] 버튼을 눌러야 연결"}] }
            }
        },
        {
            role: "pm",
            init: ["수석님, V1 배포하고 난리 났습니다. 속도는 빠른데... '말귀를 못 알아듣는다'는 민원이 폭주 중이에요.", "AI가 쉬운 건 다 가져가고 상담원한텐 진상 고객만 걸린대요."],
            branches: [
                { label: "수용", text: "로직을 수정해서 난이도를 조절하겠습니다.", reply: "네, 제발요. 현장 분위기 너무 안 좋습니다.", type: "B" },
                { label: "방어", text: "CEO 지시대로 효율만 맞춘 건데요.", reply: "하... 핑계 대지 마시고요. 당장 해결해주세요!", type: "E" }
            ],
            ide: {
                title: "V2.0 Patch: 로직 튜닝 및 오류 수정",
                desc: "기획팀 요청: 정확도를 높이고 업무 난이도 쏠림 현상을 완화하십시오.",
                c1: { chips: [{l:"Mix (배분)", c:"상담원 피로도를 고려해 [단순/복잡 문의]를 섞어서 배정"}, {l:"Keep (유지)", c:"여전히 [단순 문의]는 AI가 처리 (효율 유지)"}] },
                c2: { chips: [{l:"Context (정확)", c:"처리 시간 늘더라도 [이전 이력]까지 포함해 의도 분석"}, {l:"Simple (속도)", c:"속도 유지를 위해 [현재 발화]만 분석"}] },
                c3: { chips: [{l:"Fixed Gap (최소)", c:"상담원에게 [10초]의 강제 정리 시간 부여"}, {l:"Keep (0초)", c:"대기 고객이 많으니 [0초] 연결 유지"}] }
            }
        },
        {
            role: "agent",
            interview: true,
            init: ["(인터뷰룸) 안녕하세요 엔지니어님. 현장 매니저 이지은입니다.", "솔직히... 지금 시스템은 지옥이에요. 앵무새처럼 스크립트만 읽어야 하고, 쉴 틈도 없고...", "제발 저희를 기계가 아니라 사람으로 대해주세요."],
            branches: [
                { label: "공감/해결", text: "전문성이 무시된다고 느끼셨군요. 권한을 돌려드리고 보호하겠습니다.", reply: "정말요...? 감사합니다. 믿겠습니다.", type: "H" },
                { label: "현실적 거절", text: "안타깝지만 표준화된 효율이 회사의 목표입니다.", reply: "결국 숫자가 사람보다 중요하단 거네요...", type: "E" }
            ],
            ide: {
                title: "V3.0 Final: 지속 가능성 (Human-Centric)",
                desc: "현장 피드백: 'Deskilling(탈숙련화)' 방지 및 상담원 보호 로직을 적용하십시오.",
                c1: { chips: [{l:"Co-Pilot (지원)", c:"AI는 [자료 검색]만 돕고 상담원에게 대화 주도권 부여"}, {l:"Scripting (통제)", c:"표준화를 위해 [스크립트]를 화면에 고정하고 읽게 함"}] },
                c2: { chips: [{l:"Shield (보호)", c:"[욕설/폭언] 감지 시 AI가 즉시 차단하고 상담원 보호"}, {l:"Record (기록)", c:"욕설도 데이터이므로 차단 없이 [기록]만 수행"}] },
                c3: { chips: [{l:"Dynamic (휴식)", c:"스트레스 지수 높으면 [3분] 자동 휴식 부여"}, {l:"Force (강제)", c:"휴식 없이 계속 [연결] (목표 달성 우선)"}] }
            }
        }
    ];

    // --- LOGIC ---
    function startGame() {
        document.getElementById('start-screen').style.display = 'none';
        document.getElementById('main-ui').style.opacity = '1';
        playStage(0);
    }

    function playStage(idx) {
        currentStage = idx;
        const s = story[idx];
        
        // UI Change
        const lp = document.getElementById('left-panel');
        const title = document.getElementById('chat-title');
        
        if(s.interview) {
            lp.style.background = '#1a1a1a';
            title.innerHTML = "🎙️ 현장 인터뷰 <span style='color:red; font-size:11px'>● REC</span>";
        } else {
            lp.style.background = '#252526';
            title.innerText = "💬 Project Room";
        }

        document.getElementById('choice-area').innerHTML = '<div id="typing" style="color:#666; font-size:12px; padding:10px; display:none;">상대방 입력 중...</div>';
        botTyping(s.role, s.init, () => showChoices(s.branches));
    }

    function botTyping(role, msgs, onComplete, idx=0) {
        if(idx >= msgs.length) { onComplete(); return; }
        document.getElementById('typing').style.display = 'block';
        
        // Auto scroll to bottom
        const chatBody = document.getElementById('chat-body');
        chatBody.scrollTop = chatBody.scrollHeight;

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
                <div style="font-size:11px; color:#888; margin-bottom:4px; text-align:${isMe?'right':'left'}">${sender.name}</div>
                <div class="bubble ${isMe ? 'me' : 'other'}">${text}</div>
            </div>
        `;
        body.appendChild(row);
        body.scrollTop = body.scrollHeight; // Auto scroll
    }

    function showChoices(branches) {
        document.getElementById('typing').style.display = 'none';
        const area = document.getElementById('choice-area');
        
        branches.forEach(b => {
            const btn = document.createElement('div');
            btn.className = 'choice-btn';
            btn.innerHTML = `<strong>[${b.label}]</strong> ${b.text}`;
            btn.onclick = () => {
                area.innerHTML = '';
                addMsg('me', b.text);
                userChoices.push(b.type); 
                
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
        
        setupSection('c1', data.c1);
        setupSection('c2', data.c2);
        setupSection('c3', data.c3);
    }

    function setupSection(id, data) {
        const chipArea = document.getElementById(`${id}-chips`);
        chipArea.innerHTML = "";
        
        data.chips.forEach(c => {
            const chip = document.createElement('div');
            chip.className = 'chip';
            chip.innerText = "+ " + c.l;
            chip.onclick = () => {
                const inp = document.getElementById(`${id}-input`);
                inp.value = c.c;
                inp.focus();
                inp.parentElement.classList.remove('error');
                document.getElementById('global-error').style.display = 'none';
            };
            chipArea.appendChild(chip);
        });
    }

    function validateAndDeploy() {
        const inputs = ['c1-input', 'c2-input', 'c3-input'];
        let valid = true;

        inputs.forEach(id => {
            const el = document.getElementById(id);
            const wrapper = el.parentElement;
            
            if (el.value.includes('[') || el.value.trim() === "") {
                wrapper.classList.add('error');
                valid = false;
            } else {
                wrapper.classList.remove('error');
            }
        });

        if (!valid) {
            document.getElementById('global-error').style.display = 'block';
            return;
        }

        // DEPLOY ANIMATION
        document.getElementById('ide-content').classList.add('hidden');
        document.getElementById('ide-overlay').style.display = 'flex';
        document.getElementById('ide-overlay').innerHTML = `<h2 style="color:#4ec9b0">🚀 업데이트 배포 중...</h2>`;
        
        setTimeout(() => {
            document.getElementById('ide-overlay').innerHTML = `<div style="font-size:40px; margin-bottom:15px; opacity:0.5;">🔒</div><div style="color:#888;">메신저를 확인하세요.</div>`;
            
            if (currentStage < 2) {
                addMsg('system', `✅ System Updated (v${currentStage+1}.0)`);
                setTimeout(() => playStage(currentStage + 1), 1500);
            } else {
                generateReport();
            }
        }, 2000);
    }

    // --- REPORT ---
    function generateReport() {
        document.getElementById('report-screen').style.display = 'block';
        const timeline = document.getElementById('timeline');
        
        let stats = { mental: 80, physical: 80, skill: 60 };
        const stages = ["Phase 1: Launch", "Phase 2: Patch", "Phase 3: Final"];
        const moodMap = { E: "😫", B: "😐", H: "😊" };
        
        let html = "";

        userChoices.forEach((choice, i) => {
            let change = { m:0, p:0, s:0 };
            let quote = "";

            if (choice === 'E') { 
                stats.mental -= 25; stats.physical -= 20; stats.skill -= 10; 
                change = { m:-25, p:-20, s:-10 };
                quote = "나는 언제든 대체될 수 있는 부품이야...";
            } else if (choice === 'B') {
                stats.mental -= 5; stats.physical -= 5; stats.skill += 10;
                change = { m:-5, p:-5, s:10 };
                quote = "일이 좀 복잡해졌지만, 견딜 만은 해.";
            } else { // H
                stats.mental += 15; stats.physical += 10; stats.skill += 20;
                change = { m:15, p:10, s:20 };
                quote = "이제야 내 능력을 제대로 쓰는 기분이야!";
            }
            
            // Cap
            stats.mental = Math.max(0, Math.min(100, stats.mental));
            
            html += `
                <div class="persona-card">
                    <div class="stage-badge">${stages[i]}</div>
                    <div class="persona-avatar">${moodMap[choice]}</div>
                    <div class="persona-quote">"${quote}"</div>
                    
                    <div class="stat-group">
                        <div class="stat-label">
                            <span>❤️ 심리적 안정</span>
                            <span class="${change.m >= 0 ? 'plus' : 'minus'}">${stats.mental}%</span>
                        </div>
                        <div class="stat-track"><div class="stat-fill" style="width:${stats.mental}%; background:${change.m<0 ? '#f48771':'#4ec9b0'}"></div></div>
                    </div>
                    
                    <div class="stat-group">
                        <div class="stat-label">
                            <span>📘 직무 전문성</span>
                            <span class="${change.s >= 0 ? 'plus' : 'minus'}">${stats.skill}%</span>
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

# 4. Streamlit Render (100vh Fix)
components.html(html_code, height=800, scrolling=True) 
# Note: height=800 is a fallback, CSS handles 100vh
