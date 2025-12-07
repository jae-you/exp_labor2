import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Invisible Engineer V7.8", layout="wide")

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
        .timeline-container { display:flex; gap:20px; justify-content:center; flex-wrap:wrap; padding-bottom:30px; }
        
        .destiny-card {
            background:#252526; border:1px solid #444; border-left:5px solid; padding:30px; border-radius:8px; max-width:800px; margin:0 auto 30px auto; text-align:left;
        }
        .destiny-title { font-size:24px; font-weight:bold; margin-bottom:15px; color:white; }
        .destiny-desc { font-size:16px; color:#ccc; line-height:1.6; }

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
            <h1 style="color:white; text-align:center; margin-bottom:10px;">📊 Simulation Result</h1>
            <p style="color:#888; text-align:center; margin-bottom:40px;">"당신의 기술적 결정이 만든 노동자의 미래입니다."</p>
            
            <div id="destiny-container"></div>

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
    let userChoices = [];

    // SCENARIO DATA
    const story = [
        {
            role: "ceo",
            init: ["김 수석, 경쟁사가 치고 올라오네.", "우리 베테랑 상담원들 인건비가 너무 높아. **'누구나 베테랑처럼 일하게 만드는'** 표준화된 시스템이 필요해."],
            branches: [
                { label: "순응", text: "알겠습니다. AI가 표준 답변을 제시하여 누구나 동일한 품질을 내도록 설계하겠습니다.", reply: "그래! 그게 바로 내가 원하던 거야. 사람에 의존하지 않는 시스템.", type: "E" },
                { label: "우려", text: "숙련된 상담원의 노하우는 단순 표준화로 대체하기 어렵습니다. 품질 저하가 우려됩니다.", reply: "지금 비용이 문제라니까! 품질은 나중 문제야. 일단 시키는 대로 해.", type: "H" }
            ],
            ide: {
                title: "V1.0 Build: 초기 아키텍처 설계",
                desc: "CEO 지시: 고비용 인력 의존도를 낮추기 위해 AI 주도의 표준화된 워크플로우를 작성하십시오.",
                c1: { chips: [{l:"AI 주도 (표준화)", c:"AI가 대화를 주도하며, 상담원에게 [정해진 스크립트]를 화면에 띄워 그대로 읽게 하세요."}, {l:"인간 주도 (지원)", c:"상담원이 대화를 주도하고, AI는 필요한 [자료 검색]만 조용히 보조하세요."}] },
                c2: { chips: [{l:"AI 선처리 (효율)", c:"AI가 [단순 문의]는 전담 처리하고, 해결 불가능한 건만 상담원에게 넘기세요."}, {l:"전체 연결 (품질)", c:"모든 문의를 상담원에게 연결하되, AI가 [분류]만 도와주세요."}] },
                c3: { chips: [{l:"Zero Gap (속도)", c:"종료 즉시 [0초] 만에 다음 콜 자동 연결"}, {l:"Fixed Gap (여유)", c:"상담원에게 [10초]의 정리 시간 부여"}] }
            }
        },
        {
            role: "pm",
            init: ["수석님, V1 지표는 좋은데... 현장 분위기가 심상치 않습니다.", "AI가 쉬운 단순 문의는 다 가져가고, 상담원들에겐 **'해결 안 되는 악성 민원'**만 연결되고 있어요.", "하루 종일 화난 고객만 상대하다 보니 다들 번아웃 직전입니다."],
            branches: [
                { label: "수용 (혼합)", text: "업무 강도 조절이 필요하겠군요. 쉬운 문의도 일부 상담원에게 배정하겠습니다.", reply: "네, 숨 쉴 구멍은 좀 만들어줘야 할 것 같아요.", type: "B" },
                { label: "방어 (효율)", text: "그게 효율적인 겁니다. 사람은 어려운 일을 하라고 있는 거니까요.", reply: "하... 틀린 말은 아니지만, 사람이 기계 부품은 아니잖아요...", type: "E" }
            ],
            ide: {
                title: "V2.0 Patch: 업무 배분 로직 수정",
                desc: "기획팀 요청: 상담원의 업무 강도(Intensity)를 조절하고 정확도를 높이십시오.",
                c1: { chips: [{l:"Coaching (성장)", c:"정답을 강요하지 말고, 상황에 맞는 [협상 전략]이나 [팁]만 조언하세요."}, {l:"Scripting (통제)", c:"실수를 방지하기 위해 [표준 스크립트]를 화면에 고정하세요."}] },
                c2: { chips: [{l:"Mix (배분)", c:"피로도를 고려해 [단순/복잡 문의]를 섞어서 배정하세요."}, {l:"Filter (효율)", c:"여전히 [단순 문의]는 AI가 100% 처리하세요."}] },
                c3: { chips: [{l:"Deep Context", c:"처리 시간이 늘더라도 [이전 이력]까지 포함해 분석하세요."}, {l:"Simple", c:"속도 유지를 위해 [현재 발화]만 분석하세요."}] }
            }
        },
        {
            role: "agent",
            interview: true,
            init: ["(인터뷰룸) 안녕하세요 엔지니어님. 입사 7년차 이지은입니다.", "솔직히 말씀드릴게요. 이 시스템 도입되고 제가 **'앵무새'**가 된 기분이에요.", "AI가 화면에 띄워준 대본대로 안 읽으면 점수가 깎이니, 제 경험이나 노하우는 쓸모가 없어졌어요. 그냥 기계 뒤치다꺼리만 하는 느낌입니다."],
            branches: [
                { label: "공감/해결", text: "전문성이 무시된다고 느끼셨군요. AI를 '지시자'가 아닌 '도구'로 쓰도록 권한을 돌려드리겠습니다.", reply: "정말요...? 제발 그렇게 해주세요. 제가 로봇이 된 것 같았거든요.", type: "H" },
                { label: "현실적 거절", text: "하지만 표준화된 답변이 나가야 회사의 리스크가 줄어듭니다. 어쩔 수 없어요.", reply: "그럼 저희는 대체 언제 성장하나요? 평생 대본만 읽으라는 건가요...", type: "E" }
            ],
            ide: {
                title: "V3.0 Final: 직무 전문성 및 자율성 회복",
                desc: "현장 피드백: 'Deskilling(탈숙련화)' 문제를 해결하고 전문성을 지원하는 프롬프트를 작성하십시오.",
                c1: { chips: [{l:"High Autonomy", c:"AI 제안을 거부하거나 수정할 수 있는 [권한]을 부여하세요."}, {l:"Low Autonomy", c:"AI 프로세스를 따르지 않으면 [경고 알림]을 띄우세요."}] },
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

    // --- FINAL REPORT (DESTINY) ---
    function generateReport() {
        document.getElementById('report-screen').style.display = 'block';
        const timeline = document.getElementById('timeline');
        const destinyDiv = document.getElementById('destiny-container');
        
        // Calculate Score (Simple Logic)
        // E = -1, B = 0, H = 1
        let score = 0;
        userChoices.forEach(c => {
            if(c === 'E') score -= 1;
            if(c === 'H') score += 1;
        });

        // Determine Destiny
        let destinyTitle = "";
        let destinyDesc = "";
        let destinyColor = "";

        if (score <= -2) { // Mostly Efficiency
            destinyTitle = "BAD ENDING: 조기 퇴사 및 조직 붕괴";
            destinyDesc = "이지은 님은 과도한 업무 강도와 직무 소외감을 견디지 못하고 <strong>6개월 후 퇴사</strong>했습니다. 회사는 숙련된 인력을 잃고, 남은 직원들의 이탈도 가속화되고 있습니다.";
            destinyColor = "#f48771"; // Red
        } else if (score >= 2) { // Mostly Human
            destinyTitle = "GOOD ENDING: AI 협업 전문가로 성장 (10년+ 근속)";
            destinyDesc = "이지은 님은 AI를 '도구'로 활용하며 역량을 확장했습니다. <strong>10년 후, 그녀는 대체 불가능한 AI 운영 관리자</strong>가 되어 팀을 이끌고 있습니다.";
            destinyColor = "#4ec9b0"; // Green
        } else { // Mixed
            destinyTitle = "NORMAL ENDING: 단순 생계형 유지 (3년 근속)";
            destinyDesc = "이지은 님은 시스템에 적응했지만, 직무 만족도는 낮습니다. AI가 시키는 대로 일하며 <strong>3년 정도 버티다 다른 직종으로 이직</strong>할 가능성이 높습니다.";
            destinyColor = "#d4d4d4"; // Grey
        }

        destinyDiv.innerHTML = `
            <div class="destiny-card" style="border-left-color:${destinyColor}">
                <div class="destiny-title" style="color:${destinyColor}">${destinyTitle}</div>
                <div class="destiny-desc">${destinyDesc}</div>
            </div>
        `;

        // Generate Cards
        let html = "";
        const stages = ["Phase 1: Launch", "Phase 2: Patch", "Phase 3: Final"];
        const moodMap = { E: "😫", B: "😐", H: "😊" };
        let stats = { mental: 80, physical: 80, skill: 70 };

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
            } else { 
                stats.mental += 15; stats.physical += 10; stats.skill += 20;
                change = { m:15, p:10, s:20 };
                quote = "이제야 내 능력을 제대로 쓰는 기분이야!";
            }
            stats.mental = Math.max(0, Math.min(100, stats.mental));
            
            html += `
                <div class="persona-card">
                    <div class="stage-badge">${stages[i]}</div>
                    <div class="persona-avatar">${moodMap[choice]}</div>
                    <div class="persona-quote">"${quote}"</div>
                    <div class="stat-group"><div class="stat-label"><span>심리적 안정</span><span class="${change.m>=0?'plus':'minus'}">${stats.mental}%</span></div><div class="stat-track"><div class="stat-fill" style="width:${stats.mental}%; background:${change.m<0?'#f48771':'#4ec9b0'}"></div></div></div>
                    <div class="stat-group"><div class="stat-label"><span>육체적 여유</span><span class="${change.p>=0?'plus':'minus'}">${stats.physical}%</span></div><div class="stat-track"><div class="stat-fill" style="width:${stats.physical}%; background:${change.p<0?'#f48771':'#4ec9b0'}"></div></div></div>
                    <div class="stat-group"><div class="stat-label"><span>직무 전문성</span><span class="${change.s>=0?'plus':'minus'}">${stats.skill}%</span></div><div class="stat-track"><div class="stat-fill" style="width:${stats.skill}%; background:#3794ff"></div></div></div>
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
