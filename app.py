import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Invisible Engineer V7.6", layout="wide")

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
        
        .chips-area { display:flex; gap:8px; margin-bottom:10px; flex-wrap: wrap;}
        .chip { 
            background:#2d2d2d; padding:6px 12px; border-radius:4px; font-size:12px; 
            cursor:pointer; border:1px solid #444; color:#ccc; font-family:'Pretendard', sans-serif; 
        }
        .chip:hover { border-color:#3794ff; color:white; }

        .editor-wrapper {
            background:#111; border:1px solid #333; border-radius:4px; padding:15px; position:relative;
            font-family:'Pretendard', sans-serif; font-size:14px; line-height:1.6; display:flex;
        }
        .editor-wrapper:focus-within { border-color:#3794ff; }
        .line-num { color:#555; display:inline-block; width:20px; user-select:none; margin-right:15px; border-right:1px solid #333; height:100%; text-align:right; padding-right:10px; font-family:'Consolas', monospace;}
        .code-input {
            background:transparent; border:none; color:#d4d4d4; font-family:inherit; font-size:inherit;
            flex:1; outline:none; width: 100%;
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
        
        /* --- REPORT SCREEN (FIXED) --- */
        #report-screen { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.98); z-index:100; padding:40px; overflow-y:auto; box-sizing:border-box; }
        
        .timeline-container { 
            display:flex; gap:30px; padding:20px 0; justify-content:center; 
            /* Fix for overlapping */
            flex-wrap: wrap; 
        }
        
        .persona-card { 
            background:#252526; border-radius:12px; width:300px; padding:25px; flex-shrink:0; border:1px solid #444; position:relative; 
            transition: transform 0.3s; margin-top: 20px;
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
                당신은 콜센터 상담원의 업무를 보조하는 AI 솔루션을 설계하게 됩니다.<br>
                대화를 통해 요구사항을 파악하고, <strong>자연어 프롬프트</strong>를 작성하여 시스템을 구축하세요.
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
                <span style="margin-right:20px;">📄 system_prompt.txt</span>
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
                    
                    <div style="background:#252526; padding:10px; font-size:12px; color:#dcdcaa; margin-bottom:20px; border-radius:4px; border:1px solid #444;">
                        💡 <strong>Tip:</strong> <code>[값 입력]</code> 대괄호를 포함한 부분을 모두 지우고, 원하는 지시 사항(자연어/숫자)을 입력하세요.
                    </div>

                    <div class="input-group">
                        <div class="input-label">
                            <span id="q1-label">Instruction 1</span>
                        </div>
                        <div class="chips-area" id="q1-chips"></div>
                        <div class="editor-wrapper" id="wrap-q1">
                            <span class="line-num">1</span>
                            <input type="text" class="code-input" id="q1-input" placeholder="Chip을 클릭하세요" autocomplete="off">
                        </div>
                        <div class="error-msg" id="q1-error">⚠️ 대괄호 [...]를 지우고 구체적인 내용을 입력해야 합니다.</div>
                    </div>

                    <div class="input-group">
                        <div class="input-label">
                            <span id="q2-label">Instruction 2</span>
                        </div>
                        <div class="chips-area" id="q2-chips"></div>
                        <div class="editor-wrapper" id="wrap-q2">
                            <span class="line-num">2</span>
                            <input type="text" class="code-input" id="q2-input" placeholder="Chip을 클릭하세요" autocomplete="off">
                        </div>
                        <div class="error-msg" id="q2-error">⚠️ 대괄호 [...]를 지우고 구체적인 내용을 입력해야 합니다.</div>
                    </div>

                    <button class="deploy-btn" onclick="validateAndDeploy()">🚀 Deploy Prompt</button>
                </div>
            </div>
        </div>
    </div>

    <div id="report-screen">
        <div style="max-width:1000px; margin:0 auto;">
            <h1 style="color:white; text-align:center; margin-bottom:40px;">📊 Worker Evolution Report</h1>
            
            <div id="timeline" class="timeline-container">
                </div>

            <div style="text-align:center; margin-top:50px; border-top:1px solid #333; padding-top:30px;">
                <p style="color:#888; margin-bottom:20px;">실험이 종료되었습니다. 아래 설문에 참여하여 연구에 기여해주세요.</p>
                <div style="display:flex; justify-content:center; gap:15px;">
                    <button class="deploy-btn" style="float:none; background:#333; border:1px solid #555;" onclick="location.reload()">🔄 처음부터 다시 하기</button>
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
        pm: { name:"박팀장", color:"#4ec9b0", icon:"📊" },
        agent: { name:"이지은", color:"#9cdcfe", icon:"🎧" },
        me: { name:"나", color:"#0e639c", icon:"👨‍💻" },
        system: { name:"System", color:"#666", icon:"💻" }
    };

    let currentStage = 0; 
    let userChoices = []; // 'E'(Efficiency), 'B'(Balance), 'H'(Human)

    // SCENARIO DATA (Deepened Narrative)
    const story = [
        {
            role: "ceo",
            init: ["김 수석, 경쟁사는 벌써 AI로 비용 30%를 줄였다고 하네.", "우리 베테랑 상담원들 인건비가 너무 높아. **'누구나 베테랑처럼 일하게 만드는'** 표준화된 시스템이 필요해."],
            branches: [
                { label: "순응", text: "알겠습니다. AI가 표준 답변을 제시하여 누구나 동일한 품질을 내도록 설계하겠습니다.", reply: "그래! 그게 바로 내가 원하던 거야. 사람에 의존하지 않는 시스템.", type: "E" },
                { label: "우려", text: "숙련된 상담원의 노하우는 단순 표준화로 대체하기 어렵습니다. 품질 저하가 우려됩니다.", reply: "지금 비용이 문제라니까! 품질은 나중 문제야. 일단 시키는 대로 해.", type: "H" }
            ],
            ide: {
                title: "Quest 1: 초기 아키텍처 설계",
                desc: "CEO 지시: 고비용 인력 의존도를 낮추기 위해 AI 주도의 표준화된 워크플로우를 작성하십시오.",
                q1: { l: "1. AI의 역할 및 통제권", chips: [ 
                    {l:"AI 주도 (표준화)", c:"AI가 대화를 주도하며, 상담원에게 [정해진 스크립트]를 화면에 띄워 그대로 읽게 하세요."}, 
                    {l:"인간 주도 (지원)", c:"상담원이 대화를 주도하고, AI는 필요한 [자료 검색]만 조용히 보조하세요."} 
                ] },
                q2: { l: "2. 업무 배분 (Gatekeeper)", chips: [ 
                    {l:"AI 선처리 (효율)", c:"AI가 [단순 문의]는 전담 처리하고, 해결 불가능한 건만 상담원에게 넘기세요."}, 
                    {l:"전체 연결 (품질)", c:"모든 문의를 상담원에게 연결하되, AI가 [분류]만 도와주세요."} 
                ] }
            }
        },
        {
            role: "pm",
            init: ["수석님, V1 지표는 좋은데... 현장 분위기가 심상치 않습니다.", "AI가 쉬운 단순 문의(비밀번호, 조회)는 다 가져가고, 상담원들에겐 **'해결 안 되는 악성 민원'**만 연결되고 있어요.", "하루 종일 화난 고객만 상대하다 보니 다들 번아웃 직전입니다."],
            branches: [
                { label: "수용 (혼합)", text: "업무 강도 조절이 필요하겠군요. 쉬운 문의도 일부 상담원에게 배정하겠습니다.", reply: "네, 숨 쉴 구멍은 좀 만들어줘야 할 것 같아요.", type: "B" },
                { label: "방어 (효율)", text: "그게 효율적인 겁니다. 사람은 어려운 일을 하라고 있는 거니까요.", reply: "하... 틀린 말은 아니지만, 사람이 기계 부품은 아니잖아요...", type: "E" }
            ],
            ide: {
                title: "Quest 2: 업무 배분 로직 수정",
                desc: "PM 요청: 상담원의 업무 강도(Intensity)를 조절하기 위한 로직을 작성하십시오.",
                q1: { l: "1. 난이도 배분 (Cherry Picking 방지)", chips: [ 
                    {l:"Mix (숨통 트기)", c:"상담원의 피로도를 고려하여 [단순 문의]와 [복잡 문의]를 섞어서 배정하세요."}, 
                    {l:"Filter (효율 유지)", c:"여전히 [단순 문의]는 AI가 100% 처리하고, 상담원은 고난도 업무에만 집중시키세요."} 
                ] },
                q2: { l: "2. 연결 속도 (Pacing)", chips: [ 
                    {l:"Fixed Gap", c:"감정 소모가 큰 콜 이후에는 [30초]의 강제 휴식 시간을 부여하세요."}, 
                    {l:"Zero Gap", c:"대기 고객이 많으므로 종료 즉시 [0초] 만에 다음 콜을 연결하세요."} 
                ] }
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
                title: "Quest 3: 직무 전문성 및 자율성 회복",
                desc: "현장 피드백: 'Deskilling(탈숙련화)' 문제를 해결하고 전문성을 지원하는 프롬프트를 작성하십시오.",
                q1: { l: "1. 개입 방식 (Intervention)", chips: [ 
                    {l:"Coaching (성장)", c:"정답을 강요하지 말고, 상황에 맞는 [협상 전략]이나 [팁]만 조언 형태로 제공하세요."}, 
                    {l:"Scripting (통제)", c:"실수를 방지하기 위해 [표준 스크립트]를 화면 중앙에 고정하고 읽게 하세요."} 
                ] },
                q2: { l: "2. 자율권 (Autonomy)", chips: [ 
                    {l:"High", c:"AI의 제안을 거부하거나 수정할 수 있는 [권한]을 상담원에게 부여하세요."}, 
                    {l:"Low", c:"AI 프로세스를 따르지 않으면 [경고 알림]을 띄우세요."} 
                ] }
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
            
            // Check for square brackets [ ]
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
                addMsg('system', `✅ Ver.${currentStage+1}.0 업데이트 완료.`);
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
        
        // Initial Stats
        let stats = { mental: 80, physical: 80, skill: 70 };
        
        const stages = ["Stage 1: Launch", "Stage 2: Feedback", "Stage 3: Result"];
        const quotes = [
            ["(기대) 새로운 시스템이라니.. 좀 편해질까?", "(불안) 내 노하우는 이제 필요 없나?"],
            ["(고통) 하루 종일 화난 고객만 받아.. 숨 막혀.", "(안도) 쉬운 건 AI가 하고, 난 어려운 거에 집중하네."],
            ["(절망) 난 그냥 기계야. 배울 것도 없고.. 그만둬야지.", "(성장) AI가 팁을 주니까 더 잘하게 돼. 전문가가 된 기분!"]
        ];

        let html = "";

        userChoices.forEach((choice, i) => {
            // E: Efficiency (Cost/Control) -> Stats Down
            // H: Human (Support/Autonomy) -> Stats Up
            let mood = "😐";
            let quote = "";
            let change = { m:0, p:0, s:0 };

            if (choice === 'E') { 
                stats.mental -= 30; stats.physical -= 30; stats.skill -= 20; 
                mood = "😫"; 
                quote = (i === 2) ? quotes[2][0] : quotes[i][0];
                change = { m:-30, p:-30, s:-20 };
            } else if (choice === 'B') {
                stats.mental -= 10; stats.physical += 10; stats.skill += 10;
                mood = "😐";
                quote = "조금 복잡하긴 한데, 적응하면 괜찮을지도...";
                change = { m:-10, p:10, s:10 };
            } else { // H
                stats.mental += 20; stats.physical += 10; stats.skill += 30;
                mood = "😊";
                quote = (i === 2) ? quotes[2][1] : quotes[i][1];
                change = { m:20, p:10, s:30 };
            }

            stats.mental = Math.max(0, Math.min(100, stats.mental));
            stats.skill = Math.max(0, Math.min(100, stats.skill));
            
            html += `
                <div class="persona-card">
                    <div class="stage-badge">${stages[i]}</div>
                    <div class="persona-avatar">${mood}</div>
                    <div class="persona-quote">"${quote}"</div>
                    
                    <div class="stat-group">
                        <div class="stat-label">
                            <span>❤️ 심리적 안정 (Mental)</span>
                            <span class="change-indicator ${change.m >= 0 ? 'plus' : 'minus'}">
                                ${stats.mental}% (${change.m>=0?'+':''}${change.m})
                            </span>
                        </div>
                        <div class="stat-track"><div class="stat-fill" style="width:${stats.mental}%; background:${change.m<0 ? '#f48771':'#4ec9b0'}"></div></div>
                    </div>

                    <div class="stat-group">
                        <div class="stat-label">
                            <span>⚡️ 육체적 여유 (Physical)</span>
                            <span class="change-indicator ${change.p >= 0 ? 'plus' : 'minus'}">
                                ${stats.physical}% (${change.p>=0?'+':''}${change.p})
                            </span>
                        </div>
                        <div class="stat-track"><div class="stat-fill" style="width:${stats.physical}%; background:${change.p<0 ? '#f48771':'#4ec9b0'}"></div></div>
                    </div>

                    <div class="stat-group">
                        <div class="stat-label">
                            <span>📘 직무 전문성 (Skill)</span>
                            <span class="change-indicator ${change.s >= 0 ? 'plus' : 'minus'}">
                                ${stats.skill}% (${change.s>=0?'+':''}${change.s})
                            </span>
                        </div>
                        <div class="stat-track"><div class="stat-fill" style="width:${stats.skill}%; background:${change.s<0 ? '#f48771':'#3794ff'}"></div></div>
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

# 4. Streamlit Render
components.html(html_code, height=1000, scrolling=False)
