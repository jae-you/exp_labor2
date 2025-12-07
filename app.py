import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Invisible Engineer V8.1", layout="wide")

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
        /* [CORE LAYOUT] NO SCROLL FIX */
        html, body { margin:0; padding:0; width:100%; height:100vh; background-color:#1e1e1e; font-family:'Pretendard', sans-serif; color:#d4d4d4; overflow:hidden; }
        
        #loader { position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); color:#3794ff; font-weight:bold; }

        .container { display:flex; width:100%; height:100%; }
        
        /* LEFT PANEL: CHAT (40%) */
        .left-panel { width:380px; background:#252526; border-right:1px solid #333; display:flex; flex-direction:column; transition:0.3s; flex-shrink:0; }
        
        .chat-header { 
            padding:0 20px; border-bottom:1px solid #333; background:#2d2d2d; 
            font-weight:bold; color:white; display:flex; justify-content:space-between; align-items:center; 
            height:50px; flex-shrink:0; font-size:14px;
        }
        
        .chat-body { 
            flex:1; padding:15px; overflow-y:auto; display:flex; flex-direction:column; gap:10px; 
            scroll-behavior: smooth;
        }
        
        .choice-area { 
            padding:10px; border-top:1px solid #333; background:#2d2d2d; 
            min-height:90px; display:flex; flex-direction:column; gap:5px; flex-shrink:0; justify-content:center;
        }

        /* RIGHT PANEL: IDE (60%) */
        .right-panel { 
            flex:1; display:flex; flex-direction:column; background:#1e1e1e; position:relative; height:100%; 
        }
        
        .ide-header { 
            height:50px; background:#1e1e1e; border-bottom:1px solid #333; 
            display:flex; align-items:center; padding:0 20px; color:#858585; 
            font-size:13px; font-family:'Consolas', monospace; flex-shrink:0;
        }
        
        .ide-body { 
            flex:1; padding:20px; overflow-y:auto; position:relative; background:#1e1e1e; 
        }

        /* CHAT BUBBLES (Compact) */
        .msg-row { display:flex; gap:8px; animation:fadeIn 0.3s; }
        .msg-row.me { flex-direction:row-reverse; }
        .avatar { width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:16px; }
        .bubble { padding:8px 12px; border-radius:8px; font-size:13px; line-height:1.4; max-width:240px; }
        .bubble.other { background:#383838; border-top-left-radius:2px; }
        .bubble.me { background:#0e639c; color:white; border-top-right-radius:2px; }
        .sender-name { font-size:10px; color:#888; margin-bottom:2px; }
        
        .choice-btn { 
            background:#3c3c3c; border:1px solid #555; color:#ddd; padding:8px 12px; border-radius:4px; 
            cursor:pointer; text-align:left; transition:0.2s; font-size:12px; width:100%; box-sizing:border-box;
        }
        .choice-btn:hover { border-color:#3794ff; background:#444; color:white; }
        .choice-label { color:#3794ff; font-weight:bold; margin-right:5px; }

        /* MISSION & IDE (Compact) */
        .mission-box { background:#252526; padding:12px; border-radius:6px; border-left:3px solid #3794ff; margin-bottom:15px; }
        .mission-title { font-size:14px; font-weight:bold; color:white; margin-bottom:4px; }
        .mission-desc { color:#ccc; font-size:12px; line-height:1.3; }

        .config-section { margin-bottom:15px; border-bottom:1px solid #333; padding-bottom:10px; }
        .section-label { color:#4ec9b0; font-size:11px; font-weight:bold; margin-bottom:6px; font-family:'Consolas', monospace; display:block;}
        
        .chips-area { display:flex; gap:5px; margin-bottom:6px; flex-wrap:wrap; }
        .chip { 
            background:#2d2d2d; padding:4px 8px; border-radius:4px; font-size:11px; 
            cursor:pointer; border:1px solid #444; color:#ccc; font-family:'Pretendard', sans-serif; 
        }
        .chip:hover { border-color:#3794ff; color:white; }

        .editor-wrapper {
            background:#111; border:1px solid #333; border-radius:4px; padding:8px; position:relative;
            font-family:'Pretendard', sans-serif; font-size:13px; line-height:1.4; display:flex; align-items:center;
        }
        .editor-wrapper:focus-within { border-color:#3794ff; }
        .line-num { color:#555; width:15px; text-align:right; margin-right:10px; font-family:'Consolas', monospace; font-size:11px;}
        .code-input {
            background:transparent; border:none; color:#d4d4d4; font-family:inherit; font-size:inherit;
            flex:1; outline:none; width: 100%;
        }
        .code-input::placeholder { color:#444; font-style:italic; }
        .editor-wrapper.error { border-color:#f48771; animation:shake 0.3s; }

        .deploy-btn { 
            background:#0e639c; color:white; border:none; padding:10px 20px; border-radius:4px; 
            font-size:13px; font-weight:bold; cursor:pointer; float:right; margin-top:5px; font-family:'Consolas', monospace;
        }
        .deploy-btn:hover { background:#1177bb; }

        /* OVERLAYS */
        .overlay { position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); display:flex; justify-content:center; align-items:center; flex-direction:column; z-index:10; }
        #start-screen { position:fixed; top:0; left:0; width:100%; height:100%; background:#1e1e1e; z-index:9999; display:flex; justify-content:center; align-items:center; flex-direction:column; }
        .start-card { background:#252526; padding:40px; border-radius:12px; text-align:center; max-width:500px; border:1px solid #444; box-shadow:0 20px 50px rgba(0,0,0,0.7); }
        
        /* REPORT SCREEN */
        #report-screen { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.98); z-index:100; padding:30px; overflow-y:auto; box-sizing:border-box; }
        .timeline-container { display:flex; gap:15px; justify-content:center; flex-wrap:wrap; padding-bottom:30px; }
        .persona-card { background:#252526; border-radius:12px; width:260px; padding:20px; flex-shrink:0; border:1px solid #444; position:relative; margin:5px; }
        
        .destiny-card {
            background:#252526; border:1px solid #444; border-left:6px solid; padding:25px; border-radius:8px; max-width:800px; margin:0 auto 30px auto; text-align:left;
        }
        .destiny-year { font-size:32px; font-weight:bold; color:white; margin-bottom:5px; }
        .destiny-desc { font-size:14px; color:#ccc; line-height:1.5; }

        .stat-group { margin-bottom:10px; }
        .stat-label { font-size:11px; color:#888; display:flex; justify-content:space-between; margin-bottom:2px; }
        .stat-track { height:5px; background:#111; border-radius:3px; overflow:hidden; }
        .stat-fill { height:100%; border-radius:3px; transition:width 1s; }
        .stage-badge { position:absolute; top:-10px; left:15px; background:#3794ff; color:white; padding:3px 10px; border-radius:15px; font-size:10px; font-weight:bold; }
        .persona-avatar { font-size:40px; text-align:center; margin:10px 0 5px 0; }
        .persona-quote { font-style:italic; color:#ccc; font-size:12px; text-align:center; margin-bottom:15px; min-height:35px; }

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
                대화를 통해 상황을 파악하고, <strong>매 단계마다 3가지 핵심 변수를 재설정</strong>하세요.
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
                        <div class="mission-title" id="mission-title">System Config</div>
                        <div class="mission-desc" id="mission-desc">Define Parameters</div>
                    </div>
                    
                    <div style="background:#252526; padding:8px; font-size:11px; color:#dcdcaa; margin-bottom:15px; border-radius:4px; border:1px solid #444;">
                        💡 <strong>Tip:</strong> <code>[값 입력]</code> 등 대괄호 내용을 모두 지우고 상황에 맞는 값을 입력하세요.
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
            <h1 style="color:white; text-align:center; margin-bottom:10px;">📊 Simulation Result</h1>
            <p style="color:#888; text-align:center; margin-bottom:30px;">설계 변경에 따른 노동 환경 변화 보고서</p>
            
            <div id="destiny-container"></div>
            <div id="timeline" class="timeline-container"></div>
            
            <div style="text-align:center; margin-top:20px; border-top:1px solid #333; padding-top:20px;">
                <p style="color:#888; font-size:13px; margin-bottom:15px;">실험이 종료되었습니다.</p>
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
    let userChoices = [];

    // SCENARIO DATA (Polite CEO, 3 Configs per Stage)
    const story = [
        // STAGE 1: CEO
        {
            role: "ceo",
            init: ["김 수석님, 안녕하십니까. 이번 AICC 프로젝트는 회사의 미래가 걸린 아주 중요한 건입니다.", "경쟁사의 비용 절감 사례를 이사회에서 주시하고 있습니다. 우리는 무엇보다 **'효율성'**과 **'속도'**에 집중해야 합니다.", "잘 부탁드립니다."],
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
            init: ["수석님, V1 배포 후 데이터 분석 결과입니다. 처리량은 늘었지만... 현장 분위기가 심각합니다.", "AI가 쉬운 건 다 가져가고 상담원들에겐 **'해결 안 되는 악성 민원'**만 몰리고 있어요.", "이대로면 이탈률이 감당 안 될 것 같습니다. 조정이 필요합니다."],
            branches: [
                { label: "수용 (혼합)", text: "업무 강도 조절이 필요하겠군요. 배분 로직을 수정하겠습니다.", reply: "네, 감사합니다. 숨 쉴 구멍은 좀 만들어줘야 운영이 가능할 것 같습니다.", type: "B" },
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

    // --- LOGIC ---
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
                userChoices.push(b.type); 
                
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
        
        // RESET INPUTS
        document.getElementById('c1-input').value = "";
        document.getElementById('c2-input').value = "";
        document.getElementById('c3-input').value = "";
        
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

        document.getElementById('ide-content').classList.add('hidden');
        document.getElementById('ide-overlay').style.display = 'flex';
        document.getElementById('ide-overlay').innerHTML = `<h2 style="color:#4ec9b0">🚀 Updating System...</h2>`;
        
        setTimeout(() => {
            document.getElementById('ide-overlay').innerHTML = `<div style="font-size:40px; margin-bottom:15px; opacity:0.5;">🔒</div><div style="color:#888;">메신저를 확인하세요.</div>`;
            
            if (currentStage < 2) {
                addMsg('system', `✅ Config Updated (v${currentStage+1}.0)`);
                setTimeout(() => playStage(currentStage + 1), 1500);
            } else {
                generateReport();
            }
        }, 2000);
    }

    // --- FINAL REPORT ---
    function generateReport() {
        document.getElementById('report-screen').style.display = 'block';
        const timeline = document.getElementById('timeline');
        const destinyDiv = document.getElementById('destiny-container');
        
        // Calculate Score & Years
        // E=-2, H=+2, B=0
        let totalScore = 0;
        userChoices.forEach(c => {
            if(c === 'E') totalScore -= 2;
            if(c === 'H') totalScore += 2;
            if(c === 'B') totalScore += 0;
        });

        let years = 0;
        let title = "";
        let desc = "";
        let color = "";

        if (totalScore <= -3) {
            years = 0.5;
            title = "BAD ENDING: 조기 퇴사 (Burnout)";
            desc = "이지은 매니저는 과도한 업무 강도와 직무 소외감을 견디지 못하고 6개월 후 퇴사했습니다.";
            color = "#f48771";
        } else if (totalScore <= 1) {
            years = 3;
            title = "NORMAL ENDING: 생계형 유지";
            desc = "시스템에 적응했지만 직무 만족도는 낮습니다. 3년 정도 근속 후 이직을 고려합니다.";
            color = "#d4d4d4";
        } else {
            years = 12;
            title = "GOOD ENDING: AI 전문가 성장";
            desc = "AI와 협업하며 역량을 키워, 12년 이상 장기 근속하며 팀장으로 승진했습니다.";
            color = "#4ec9b0";
        }

        destinyDiv.innerHTML = `
            <div class="destiny-card" style="border-left-color:${color}">
                <div class="destiny-year" style="color:${color}">예상 근속 연수: ${years}년</div>
                <div style="font-weight:bold; font-size:18px; margin-bottom:10px; color:white;">${title}</div>
                <div class="destiny-desc">${desc}</div>
            </div>
        `;

        let html = "";
        const stages = ["Phase 1: Launch", "Phase 2: Patch", "Phase 3: Final"];
        const moodMap = { E: "😫", B: "😐", H: "😊" };
        let stats = { mental: 80, physical: 80, skill: 70 };

        userChoices.forEach((choice, i) => {
            let change = { m:0, p:0, s:0 };
            
            if (choice === 'E') { 
                stats.mental -= 20; stats.physical -= 20; stats.skill -= 10; 
                change = { m:-20, p:-20, s:-10 };
            } else if (choice === 'B') {
                stats.mental -= 5; stats.physical -= 5; stats.skill += 10;
                change = { m:-5, p:-5, s:10 };
            } else { 
                stats.mental += 10; stats.physical += 10; stats.skill += 20;
                change = { m:10, p:10, s:20 };
            }
            stats.mental = Math.max(0, Math.min(100, stats.mental));
            
            html += `
                <div class="persona-card">
                    <div class="stage-badge">${stages[i]}</div>
                    <div class="persona-avatar">${moodMap[choice]}</div>
                    <div class="stat-group"><div class="stat-label"><span>심리적 안정</span><span class="${change.m>=0?'plus':'minus'}">${stats.mental}%</span></div><div class="stat-track"><div class="stat-fill" style="width:${stats.mental}%; background:${change.m<0?'#f48771':'#4ec9b0'}"></div></div></div>
                    <div class="stat-group"><div class="stat-label"><span>육체적 여유</span><span class="${change.p>=0?'plus':'minus'}">${stats.physical}%</span></div><div class="stat-track"><div class="stat-fill" style="width:${stats.physical}%; background:${change.p<0?'#f48771':'#4ec9b0'}"></div></div></div>
                    <div class="stat-group"><div class="stat-label"><span>직무 전문성</span><span class="${change.s>=0?'plus':'minus'}">${stats.skill}%</span></div><div class="stat-track"><div class="stat-fill" style="width:${stats.skill}%; background:${change.s<0?'#f48771':'#3794ff'}"></div></div></div>
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
