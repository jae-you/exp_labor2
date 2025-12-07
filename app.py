import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Invisible Engineer V9.1", layout="wide")

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
        /* CORE CSS */
        * { box-sizing: border-box; }
        html, body { margin:0; padding:0; width:100%; height:100vh; background-color:#1e1e1e; font-family:'Pretendard', sans-serif; color:#d4d4d4; overflow:hidden; }
        
        #loader { position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); color:#3794ff; font-weight:bold; }

        .container { display:flex; width:100%; height:100%; }
        .left-panel { width:400px; background:#252526; border-right:1px solid #333; display:flex; flex-direction:column; flex-shrink:0; height:100%; }
        .right-panel { flex:1; display:flex; flex-direction:column; background:#1e1e1e; position:relative; height:100%; }

        /* CHAT UI */
        .chat-header { padding:0 20px; border-bottom:1px solid #333; background:#2d2d2d; font-weight:bold; color:white; display:flex; justify-content:space-between; align-items:center; height:60px; flex-shrink:0; }
        .chat-body { flex:1; padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:12px; scroll-behavior: smooth; min-height:0; }
        
        .msg-row { display:flex; gap:10px; animation:fadeIn 0.3s; }
        .msg-row.me { flex-direction:row-reverse; }
        .avatar { width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:18px; }
        .bubble { padding:10px 14px; border-radius:10px; font-size:13px; line-height:1.5; max-width:260px; box-shadow:0 1px 3px rgba(0,0,0,0.3); }
        .bubble.other { background:#383838; border-top-left-radius:2px; }
        .bubble.me { background:#0e639c; color:white; border-top-right-radius:2px; }
        .sender-name { font-size:11px; color:#888; margin-bottom:2px; }
        
        .choice-area { padding:15px; border-top:1px solid #333; background:#2d2d2d; min-height:140px; display:flex; flex-direction:column; gap:8px; justify-content:center; flex-shrink:0; }
        .choice-btn { 
            background:#3c3c3c; border:1px solid #555; color:#ddd; padding:10px; border-radius:4px; 
            cursor:pointer; text-align:left; transition:0.2s; font-size:12px; width:100%;
        }
        .choice-btn:hover { border-color:#3794ff; background:#444; color:white; }
        .choice-label { color:#3794ff; font-weight:bold; margin-right:5px; }

        /* IDE UI */
        .ide-header { height:60px; background:#1e1e1e; border-bottom:1px solid #333; display:flex; align-items:center; padding:0 30px; color:#858585; font-size:13px; font-family:'Consolas', monospace; flex-shrink:0; }
        .ide-body { flex:1; padding:30px 60px; overflow-y:auto; position:relative; background:#1e1e1e; min-height:0; }

        .mission-box { background:#252526; padding:15px; border-radius:6px; border-left:3px solid #3794ff; margin-bottom:25px; }
        .mission-title { font-size:15px; font-weight:bold; color:white; margin-bottom:5px; }
        .mission-desc { color:#ccc; font-size:13px; line-height:1.5; }

        .config-container { display:flex; flex-direction:column; gap:25px; margin-bottom:50px; }
        .config-item { display: flex; flex-direction: column; border-bottom:1px solid #333; padding-bottom:15px; }
        .section-label { color:#4ec9b0; font-size:13px; font-weight:bold; margin-bottom:8px; font-family:'Consolas', monospace; display:block;}
        
        .chips-area { display:flex; gap:8px; margin-bottom:8px; flex-wrap:wrap; }
        .chip { background:#2d2d2d; padding:6px 12px; border-radius:4px; font-size:12px; cursor:pointer; border:1px solid #444; color:#ccc; font-family:'Pretendard', sans-serif; }
        .chip:hover { border-color:#3794ff; color:white; }

        .editor-wrapper {
            background:#111; border:1px solid #333; border-radius:4px; padding:12px; position:relative;
            font-family:'Pretendard', sans-serif; font-size:14px; line-height:1.5; display:flex; align-items:center;
        }
        .editor-wrapper:focus-within { border-color:#3794ff; }
        .line-num { color:#555; width:20px; text-align:right; margin-right:15px; border-right:1px solid #333; height:100%; font-family:'Consolas', monospace; font-size:12px;}
        .code-input { background:transparent; border:none; color:#d4d4d4; font-family:inherit; font-size:inherit; flex:1; outline:none; width: 100%; }
        .code-input::placeholder { color:#444; font-style:italic; }
        .editor-wrapper.error { border-color:#f48771; animation:shake 0.3s; }

        .deploy-btn { 
            background:#0e639c; color:white; border:none; padding:12px 30px; border-radius:4px; 
            font-size:13px; font-weight:bold; cursor:pointer; float:right; margin-top:20px; font-family:'Consolas', monospace;
        }
        .deploy-btn:hover { background:#1177bb; }

        /* OVERLAYS */
        .overlay { position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); display:flex; justify-content:center; align-items:center; flex-direction:column; z-index:10; }
        #start-screen { position:fixed; top:0; left:0; width:100%; height:100%; background:#1e1e1e; z-index:9999; display:flex; justify-content:center; align-items:center; flex-direction:column; }
        .start-card { background:#252526; padding:40px; border-radius:12px; text-align:center; max-width:600px; border:1px solid #444; box-shadow:0 20px 50px rgba(0,0,0,0.7); }
        
        /* REPORT SCREEN */
        #report-screen { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.98); z-index:100; padding:40px; overflow-y:auto; box-sizing:border-box; }
        .timeline-container { display:flex; gap:20px; justify-content:center; flex-wrap:wrap; padding-bottom:30px; }
        .persona-card { background:#252526; border-radius:12px; width:300px; padding:25px; flex-shrink:0; border:1px solid #444; position:relative; margin:10px; }
        
        /* CEO & DESTINY CARDS */
        .feedback-container { max-width:800px; margin:0 auto 40px auto; display:flex; flex-direction:column; gap:20px; }
        
        .ceo-card { background:#eee; color:#333; padding:25px; border-radius:8px; font-family:'Georgia', serif; }
        .ceo-header { border-bottom:1px solid #ccc; padding-bottom:10px; margin-bottom:15px; font-weight:bold; }
        
        .destiny-card { background:#111; border:1px solid #444; border-left:6px solid; padding:25px; border-radius:8px; display:flex; align-items:center; gap:20px; }
        .destiny-year { font-size:40px; font-weight:bold; color:white; min-width:120px; text-align:center; }
        .destiny-text h3 { margin:0 0 5px 0; font-size:18px; color:white; }
        .destiny-text p { margin:0; color:#aaa; font-size:14px; line-height:1.5; }

        /* STAT BARS */
        .stat-group { margin-bottom:12px; margin-top:12px; }
        .stat-label { font-size:11px; color:#aaa; display:flex; justify-content:space-between; margin-bottom:4px; }
        .stat-track { height:6px; background:#111; border-radius:3px; overflow:hidden; }
        .stat-fill { height:100%; border-radius:3px; transition:width 1s; }
        
        .stage-badge { position:absolute; top:-10px; left:15px; background:#3794ff; color:white; padding:3px 10px; border-radius:15px; font-size:10px; font-weight:bold; }
        
        .evidence-box { 
            background:#1a1a1a; padding:10px; border-radius:4px; margin-top:15px; border:1px solid #333; 
        }
        .evidence-title { font-size:10px; color:#4ec9b0; margin-bottom:5px; font-weight:bold; }
        .evidence-text { font-size:11px; color:#dcdcaa; font-family:'Consolas', monospace; line-height:1.4; }

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
                콜센터 AI 솔루션 설계 시뮬레이션입니다.<br>
                대화를 통해 상황을 파악하고, <strong>3가지 핵심 변수</strong>를 직접 설정하세요.
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
                    
                    <div style="background:#252526; padding:8px; font-size:11px; color:#dcdcaa; margin-bottom:15px; border-radius:4px; border:1px solid #444;">
                        💡 <strong>Tip:</strong> 대괄호 <code>[...]</code>를 지우고 자연어 프롬프트를 완성하세요.
                    </div>

                    <div class="config-section">
                        <label class="section-label">1. AI INTERVENTION (개입/역할)</label>
                        <div class="chips-area" id="c1-chips"></div>
                        <div class="editor-wrapper">
                            <span class="line-num">10</span>
                            <input type="text" class="code-input" id="c1-input" placeholder="Chip 선택 후 값 수정" autocomplete="off">
                        </div>
                    </div>

                    <div class="config-section">
                        <label class="section-label">2. WORKFLOW (업무 배분/속도)</label>
                        <div class="chips-area" id="c2-chips"></div>
                        <div class="editor-wrapper">
                            <span class="line-num">20</span>
                            <input type="text" class="code-input" id="c2-input" placeholder="Chip 선택 후 값 수정" autocomplete="off">
                        </div>
                    </div>

                    <div class="config-section" style="border:none;">
                        <label class="section-label">3. PROTECTION (보호 장치)</label>
                        <div class="chips-area" id="c3-chips"></div>
                        <div class="editor-wrapper">
                            <span class="line-num">30</span>
                            <input type="text" class="code-input" id="c3-input" placeholder="Chip 선택 후 값 수정" autocomplete="off">
                        </div>
                    </div>

                    <div style="color:#f48771; font-size:11px; margin-top:5px; display:none;" id="global-error">
                        ⚠️ 오류: 대괄호 [...]를 지우고 구체적인 값을 입력해야 합니다.
                    </div>
                    <button class="deploy-btn" onclick="validateAndDeploy()">🚀 Apply Changes</button>
                </div>
            </div>
        </div>
    </div>

    <div id="report-screen">
        <div style="max-width:1000px; margin:0 auto;">
            <h1 style="color:white; text-align:center; margin-bottom:40px;">📊 Simulation Final Report</h1>
            
            <div id="feedback-container" class="feedback-container"></div>

            <div id="timeline" class="timeline-container"></div>
            
            <div style="text-align:center; margin-top:30px; border-top:1px solid #333; padding-top:20px;">
                <p style="color:#888; font-size:14px; margin-bottom:20px;">실험이 종료되었습니다.</p>
                <div style="display:flex; justify-content:center; gap:15px;">
                    <button class="deploy-btn" style="float:none; background:#333; border:1px solid #555;" onclick="location.reload()">🔄 다시 하기</button>
                    <button class="deploy-btn" style="float:none;" onclick="window.open('https://forms.google.com/your-survey-url', '_blank')">📝 설문조사 참여하기</button>
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
    let historyData = []; 

    // SCENARIO DATA
    const story = [
        // STAGE 1: CEO
        {
            role: "ceo",
            init: ["김 수석님, 안녕하십니까. 이번 AICC 프로젝트는 아주 중요합니다.", "경쟁사는 비용을 대폭 절감했습니다. 우리도 **'효율성'**과 **'속도'**가 최우선입니다.", "잘 부탁드립니다."],
            branches: [
                { label: "순응", text: "알겠습니다. 효율성을 최우선으로 설계하겠습니다.", reply: "감사합니다. 김 수석님의 전문성을 믿겠습니다. 바로 진행해주십시오.", type: "E" },
                { label: "우려", text: "대표님, 과도한 속도 경쟁은 품질 저하를 초래할 수 있습니다.", reply: "우려하시는 점은 이해합니다만, 지금은 성과를 증명해야 할 시기입니다. 일단 지표 달성에 집중해주십시오.", type: "H" }
            ],
            ide: {
                title: "V1.0 Build (Initial)",
                desc: "CEO 요청: 처리 속도(AHT)와 자동화율을 높이는 설정을 입력하십시오.",
                c1: { chips: [{l:"AI 전담 (자동화)", c:"단순 문의는 AI가 [전담 처리]하고, 해결 안 될 때만 연결하세요."}, {l:"인간 보조", c:"상담원이 주도하고 AI는 [검색]만 보조하세요."}] },
                c2: { chips: [{l:"AI 선처리+0초", c:"AI가 단순건 처리 후, 남은 콜은 [0초] 만에 연결하세요."}, {l:"혼합 배정", c:"단순/복잡 문의를 [혼합]하여 배정하세요."}] },
                c3: { chips: [{l:"기본 필터", c:"욕설 등은 [단순 필터링]만 적용하세요."}, {l:"무차별 연결", c:"보호 조치 없이 [모든 콜]을 연결하세요."}] }
            }
        },
        // STAGE 2: PM
        {
            role: "pm",
            init: ["수석님, V1 배포 후 데이터입니다. 처리량은 늘었지만... 현장 분위기가 심각합니다.", "AI가 쉬운 건 다 가져가고 상담원들에겐 **'악성 민원'**만 몰리고 있어요.", "이대로면 운영이 불가능합니다. 조정이 필요합니다."],
            branches: [
                { label: "수용 (혼합)", text: "업무 강도 조절이 필요하겠군요. 배분 로직을 수정하겠습니다.", reply: "네, 감사합니다. 숨 쉴 구멍은 좀 만들어줘야 할 것 같습니다.", type: "B" },
                { label: "방어 (효율)", text: "효율성 측면에서는 지금이 최적입니다. 사람은 어려운 일을 해야죠.", reply: "틀린 말씀은 아니지만... 사람이 기계 부품은 아니지 않습니까. 다시 재고해주세요.", type: "E" }
            ],
            ide: {
                title: "V2.0 Patch (Optimization)",
                desc: "기획팀 요청: 업무 쏠림 현상을 완화하고 강도를 조절하십시오.",
                c1: { chips: [{l:"코칭 모드", c:"AI가 정답 지시 대신 [해결 팁]을 조언하게 하세요."}, {l:"스크립트 강제", c:"표준화를 위해 [스크립트]를 화면에 고정하세요."}] },
                c2: { chips: [{l:"난이도 믹스", c:"피로도를 고려해 [단순/복잡 문의]를 섞어서 배정하세요."}, {l:"효율 유지", c:"여전히 [단순 문의]는 AI가 100% 처리하세요."}] },
                c3: { chips: [{l:"경고 표시", c:"악성 고객 진입 시 화면에 [붉은색 경고]를 띄우세요."}, {l:"유지", c:"현 상태를 유지하세요."}] }
            }
        },
        // STAGE 3: AGENT
        {
            role: "agent",
            interview: true,
            init: ["(인터뷰룸) 안녕하세요 엔지니어님. 입사 7년차 이지은입니다.", "솔직히 말씀드릴게요. 이 시스템 도입되고 제가 **'앵무새'**가 된 기분이에요.", "AI가 시키는 대로만 읽으니 제 경험은 쓸모가 없어졌고... 하루 종일 욕만 먹다 보니 내가 뭘 하고 있나 싶습니다."],
            branches: [
                { label: "공감/해결", text: "전문성이 무시된다고 느끼셨군요. 권한을 돌려드리고 보호하겠습니다.", reply: "정말요...? 감사합니다. 엔지니어님 덕분에 다시 일할 힘이 생길 것 같아요.", type: "H" },
                { label: "현실적 거절", text: "안타깝지만 표준화된 답변이 회사의 방침입니다.", reply: "그럼 저희는 언제 성장하나요? 평생 기계 뒤치다꺼리만 하라는 건가요...", type: "E" }
            ],
            ide: {
                title: "V3.0 Final (Human-Centric)",
                desc: "현장 피드백: 'Deskilling(탈숙련화)' 방지 및 보호 로직을 적용하십시오.",
                c1: { chips: [{l:"자율성 부여", c:"AI 제안을 수정할 수 있는 [권한]을 부여하세요."}, {l:"통제 유지", c:"AI 프로세스를 따르지 않으면 [경고]를 띄우세요."}] },
                c2: { chips: [{l:"동적 휴식", c:"스트레스 지수 높으면 [3분] 자동 휴식을 주세요."}, {l:"강제 연결", c:"휴식 없이 계속 [연결]하세요."}] },
                c3: { chips: [{l:"적극 방어 (Shield)", c:"[욕설/폭언] 감지 시 AI가 즉시 차단하세요."}, {l:"단순 기록", c:"차단 없이 [기록]만 남기세요."}] }
            }
        }
    ];

    // --- GAME ENGINE ---
    function startGame() {
        document.getElementById('start-screen').style.display = 'none';
        document.getElementById('main-ui').style.opacity = '1';
        playStage(0);
    }

    function playStage(idx) {
        currentStage = idx;
        const s = story[idx];
        
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
            btn.innerHTML = `<strong>[${b.label}]</strong> ${b.text}`;
            btn.onclick = () => {
                area.innerHTML = '';
                addMsg('me', b.text);
                setTimeout(() => {
                    addMsg(story[currentStage].role, b.reply);
                    setTimeout(() => unlockIDE(), 1000);
                }, 800);
            };
            area.appendChild(btn);
        });
    }

    function unlockIDE() {
        document.getElementById('ide-overlay').style.display = 'none';
        document.getElementById('ide-content').classList.remove('hidden');
        
        const data = story[currentStage].ide;
        document.getElementById('mission-title').innerText = data.title;
        document.getElementById('mission-desc').innerText = data.desc;
        
        // *IMPORTANT* Keep previous values (Legacy)
        // Only if empty (first run), we leave them empty. Otherwise keep value.
        // But here we want user to edit. Let's setup chips.
        
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
        let promptSnapshot = [];
        let score = 0; // Stage specific score

        for(let id of inputs) {
            const el = document.getElementById(id);
            const wrapper = el.parentElement;
            const val = el.value.trim();
            
            if (val.includes('[') || val === "") {
                wrapper.classList.add('error');
                valid = false;
            } else {
                wrapper.classList.remove('error');
                promptSnapshot.push(val);
                
                // Simple scoring for demo: check keywords
                if(val.match(/0초|강제|전담|효율|무차별|모든/)) score -= 1;
                if(val.match(/휴식|보호|차단|권한|조언|30초/)) score += 1;
            }
        }

        if (!valid) {
            document.getElementById('global-error').style.display = 'block';
            return;
        }

        // SAVE DATA
        historyData.push({
            stage: currentStage,
            prompts: promptSnapshot,
            score: score
        });

        document.getElementById('ide-content').classList.add('hidden');
        document.getElementById('ide-overlay').style.display = 'flex';
        document.getElementById('ide-overlay').innerHTML = `<h2 style="color:#4ec9b0">🚀 Updating System...</h2>`;
        
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

    // --- REPORT LOGIC ---
    function generateReport() {
        document.getElementById('report-screen').style.display = 'block';
        const timeline = document.getElementById('timeline');
        const feedbackContainer = document.getElementById('feedback-container');
        
        // Total Score
        let totalScore = 0;
        historyData.forEach(h => totalScore += h.score);

        // 1. CEO / DESTINY Feedback
        let ceoTitle, ceoMsg, destinyTitle, destinyDesc, years, color;

        if (totalScore <= -2) { // Efficiency Focused
            ceoTitle = "From: CEO (Subject: 성과는 좋은데...)";
            ceoMsg = "김 수석, 비용 절감은 확실하군. 근데 직원들이 줄줄이 퇴사해서 대체 인력 구하느라 돈이 더 들게 생겼어. 장기적으로 이게 맞는 건가?";
            years = 0.5;
            title = "BAD ENDING: 조기 퇴사 (Burnout)";
            desc = "이지은 매니저는 기계적 업무와 악성 민원에 지쳐 6개월 만에 퇴사했습니다.";
            color = "#f48771";
        } else if (totalScore >= 2) { // Human Focused
            ceoTitle = "From: CEO (Subject: 고민이 많네)";
            ceoMsg = "현장 만족도는 높다는데, 속도가 너무 안 나와. 우리 회사가 자선 단체는 아니잖아? 다음 분기엔 효율성 좀 챙겨주게.";
            years = 12;
            title = "GOOD ENDING: 전문가 성장";
            desc = "이지은 매니저는 AI를 도구로 활용하며 핵심 인재로 성장, 12년 장기 근속했습니다.";
            color = "#4ec9b0";
        } else { // Balanced
            ceoTitle = "From: CEO (Subject: 수고했네)";
            ceoMsg = "비용도 적당히 줄고, 직원 불만도 관리 가능한 수준이군. 균형을 잘 잡았어. 다음 프로젝트도 자네가 맡게.";
            years = 3;
            title = "NORMAL ENDING: 현상 유지";
            desc = "시스템에 적응했지만 큰 비전은 찾지 못했습니다. 3년 후 이직을 고려합니다.";
            color = "#d4d4d4";
        }

        feedbackContainer.innerHTML = `
            <div class="ceo-card">
                <div class="ceo-header">${ceoTitle}</div>
                <div class="email-body">${ceoMsg}</div>
            </div>
            <div class="destiny-card" style="border-left-color:${color}">
                <div class="destiny-year" style="color:${color}">근속 연수: ${years}년</div>
                <div style="font-weight:bold; font-size:18px; color:white; margin-bottom:5px;">${title}</div>
                <div class="destiny-desc">${desc}</div>
            </div>
        `;

        // 2. Timeline Cards
        let html = "";
        const stages = ["Phase 1: Initial", "Phase 2: Optimization", "Phase 3: Final"];
        
        // Initial Stats
        let stats = { mental: 80, physical: 80, skill: 60 };

        historyData.forEach((h, i) => {
            // Apply impact
            let impact = h.score; 
            // Simple Logic: Low score -> bad for human, good for speed
            // High score -> good for human, bad for speed
            
            let changeM = impact * 10;
            let changeP = impact * 10;
            let changeS = impact * 5;

            stats.mental += changeM;
            stats.physical += changeP;
            stats.skill += changeS;
            
            // Clamp
            stats.mental = Math.max(0, Math.min(100, stats.mental));
            stats.physical = Math.max(0, Math.min(100, stats.physical));
            stats.skill = Math.max(0, Math.min(100, stats.skill));

            html += `
                <div class="persona-card">
                    <div class="stage-badge">${stages[i]}</div>
                    
                    <div class="stat-group" style="margin-top:20px;">
                        <div class="stat-label"><span>심리적 안정</span><span class="${changeM>=0?'plus':'minus'}">${Math.round(stats.mental)}%</span></div>
                        <div class="stat-track"><div class="stat-fill" style="width:${stats.mental}%; background:${stats.mental<40?'#f48771':'#4ec9b0'}"></div></div>
                    </div>
                    <div class="stat-group">
                        <div class="stat-label"><span>체력/에너지</span><span class="${changeP>=0?'plus':'minus'}">${Math.round(stats.physical)}%</span></div>
                        <div class="stat-track"><div class="stat-fill" style="width:${stats.physical}%; background:${stats.physical<40?'#f48771':'#4ec9b0'}"></div></div>
                    </div>
                    <div class="stat-group">
                        <div class="stat-label"><span>직무 전문성</span><span class="${changeS>=0?'plus':'minus'}">${Math.round(stats.skill)}%</span></div>
                        <div class="stat-track"><div class="stat-fill" style="width:${stats.skill}%; background:#3794ff"></div></div>
                    </div>

                    <div class="evidence-box">
                        <div class="evidence-title">DEPLOYED LOGS:</div>
                        <div class="evidence-text">> ${h.prompts[0].substring(0,35)}...</div>
                        <div class="evidence-text">> ${h.prompts[1].substring(0,35)}...</div>
                        <div class="evidence-text">> ${h.prompts[2].substring(0,35)}...</div>
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
