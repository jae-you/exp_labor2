import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="The Invisible Engineer V6.2", layout="wide")

# 2. 스타일 설정 (전체화면, 여백 제거)
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
        /* --- THEME --- */
        :root {
            --bg-color: #1e1e1e;
            --chat-bg: #252526;
            --editor-bg: #1e1e1e;
            --text-color: #d4d4d4;
            --accent-color: #3794ff;
            --user-msg-bg: #0e639c;
            --other-msg-bg: #333333;
        }
        body { margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; background: var(--bg-color); color: var(--text-color); height: 100vh; overflow: hidden; }
        
        /* LAYOUT */
        .container { display: flex; width: 100%; height: 100%; }
        .left-panel { width: 450px; background: var(--chat-bg); border-right: 1px solid #444; display: flex; flex-direction: column; transition: background 0.5s; }
        .right-panel { flex: 1; display: flex; flex-direction: column; background: var(--editor-bg); position: relative; }

        /* INTRO OVERLAY (Start Screen) */
        #intro-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: radial-gradient(circle, #2a2a2a 0%, #111 100%);
            display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 9999;
        }
        .intro-card {
            background: #252526; padding: 40px; border-radius: 12px; border: 1px solid #444; 
            max-width: 500px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .start-btn {
            background: var(--accent-color); color: white; border: none; padding: 15px 40px; 
            font-size: 16px; border-radius: 30px; cursor: pointer; margin-top: 20px; font-weight: bold;
            transition: transform 0.2s;
        }
        .start-btn:hover { transform: scale(1.05); }

        /* CHAT UI */
        .chat-header { padding: 15px; border-bottom: 1px solid #444; font-weight: bold; background: #2d2d2d; display: flex; justify-content: space-between; align-items: center; color: #eee; }
        .status-dot { width: 10px; height: 10px; background: #4ec9b0; border-radius: 50%; display: inline-block; margin-right: 5px; }
        
        .chat-body { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; scroll-behavior: smooth; }
        .msg-row { display: flex; gap: 10px; animation: fadeIn 0.3s ease; }
        .msg-row.me { flex-direction: row-reverse; }
        
        .avatar { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
        
        .bubble { padding: 12px 16px; border-radius: 12px; font-size: 14px; line-height: 1.5; max-width: 280px; position: relative; }
        .bubble.other { background: var(--other-msg-bg); border-top-left-radius: 2px; }
        .bubble.me { background: var(--user-msg-bg); color: white; border-top-right-radius: 2px; }
        .sender { font-size: 11px; color: #888; margin-bottom: 4px; }
        
        /* INTERVIEW MODE STYLES */
        .interview-mode .left-panel { background: #1a1a1a; }
        .interview-mode .chat-header { background: #3d1a1a; border-bottom: 1px solid #ff4b4b; color: white; }
        .profile-card { background: #333; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #9cdcfe; display: none; animation: slideIn 0.5s; }
        .profile-title { font-size: 16px; font-weight: bold; color: white; margin-bottom: 5px; }
        .profile-detail { font-size: 12px; color: #aaa; line-height: 1.4; }

        /* REPLY AREA */
        .reply-area { padding: 15px; border-top: 1px solid #444; background: #2d2d2d; min-height: 80px; }
        .typing-indicator { font-size: 12px; color: #888; margin-bottom: 10px; font-style: italic; display: none; }
        
        .choice-btn {
            display: block; width: 100%; text-align: left; padding: 12px; margin-bottom: 8px;
            background: #3c3c3c; border: 1px solid #444; color: #ddd; border-radius: 8px;
            cursor: pointer; transition: all 0.2s; font-size: 13px;
        }
        .choice-btn:hover { background: #444; border-color: var(--accent-color); }
        .choice-btn strong { color: var(--accent-color); margin-right: 5px; }

        /* IDE UI */
        .ide-header { height: 45px; background: #2d2d2d; border-bottom: 1px solid #444; display: flex; align-items: center; padding: 0 20px; color: #ccc; font-size: 13px; }
        .ide-body { flex: 1; padding: 40px; overflow-y: auto; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        
        .locked-state { text-align: center; color: #666; }
        .locked-icon { font-size: 50px; margin-bottom: 20px; opacity: 0.3; }
        
        /* CODING MISSION */
        .coding-container { width: 100%; max-width: 800px; animation: slideUp 0.5s ease; }
        .mission-card { background: #252526; padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent-color); margin-bottom: 20px; }
        .mission-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; color: white; }
        .task-desc { font-size: 14px; color: #ccc; line-height: 1.6; }
        
        .code-editor { background: #111; padding: 20px; border-radius: 8px; font-family: 'Consolas', monospace; font-size: 14px; border: 1px solid #444; }
        .code-line { margin-bottom: 10px; color: #d4d4d4; display: flex; align-items: center; }
        .input-slot { 
            background: #2d2d2d; border: 1px solid #555; color: var(--accent-color); 
            padding: 5px 10px; border-radius: 4px; font-family: inherit; width: 250px; outline: none; margin-left: 10px;
        }
        .input-slot:focus { border-color: var(--accent-color); background: #333; }
        
        .deploy-btn { 
            background: var(--accent-color); color: white; border: none; padding: 12px 30px; 
            border-radius: 6px; font-size: 14px; cursor: pointer; margin-top: 20px; float: right; 
        }

        /* REPORT SCREEN */
        .report-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 200; padding: 50px; overflow-y: auto; display: none; }
        .stat-card { background: #222; padding: 25px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #333; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
        
        .hidden { display: none !important; }
    </style>
</head>
<body>

    <div id="intro-overlay">
        <div class="intro-card">
            <div style="font-size: 60px; margin-bottom: 20px;">👨‍💻</div>
            <h1 style="color:white; margin:0 0 10px 0;">The Invisible Engineer</h1>
            <p style="color:#aaa; font-size:14px; line-height:1.6;">
                당신은 AI 시스템의 핵심 로직을 설계하는 수석 엔지니어입니다.<br>
                당신의 코드는 시스템의 효율성뿐만 아니라,<br>
                <strong>누군가의 하루</strong>를 결정합니다.
            </p>
            <button class="start-btn" onclick="startGame()">업무 시작하기</button>
        </div>
    </div>

    <div class="container" id="main-container">
        <div class="left-panel" id="left-panel">
            <div class="chat-header" id="chat-header">
                <span id="chat-title">💬 Company Messenger</span>
                <div><span class="status-dot"></span>Online</div>
            </div>
            <div class="chat-body" id="chat-body">
                <div id="profile-card" class="profile-card">
                    <div class="profile-title">👤 인터뷰 대상: 이지은 매니저</div>
                    <div class="profile-detail">
                        • CS 운영팀 7년차 (신입 교육 담당)<br>
                        • 최근 상태: <span style="color:#ff4b4b">⚠️ 고위험군 (Burnout)</span><br>
                        • "AI 도입 후 일이 더 힘들어졌어요..."
                    </div>
                </div>
                </div>
            <div class="reply-area">
                <div id="typing-indicator" class="typing-indicator">상대방 입력 중...</div>
                <div id="choices-container"></div>
            </div>
        </div>

        <div class="right-panel">
            <div class="ide-header"><span>Terminal - zsh</span></div>
            <div class="ide-body" id="ide-body">
                <div class="locked-state">
                    <div class="locked-icon">🔒</div>
                    <h2>대기 중...</h2>
                    <p>메신저에서 업무 협의가 끝나면 에디터가 열립니다.</p>
                </div>
            </div>
        </div>
    </div>

    <div id="report-screen" class="report-overlay">
        <div style="max-width: 800px; margin: 0 auto; background: #222; padding: 40px; border-radius: 12px;">
            <h1>📊 시뮬레이션 결과 리포트</h1>
            <div id="report-content"></div>
            <div style="text-align: center; margin-top:30px;">
                <p style="color:#ccc; margin-bottom:20px;">참여해 주셔서 감사합니다.</p>
                <button class="deploy-btn" style="float:none;" onclick="location.reload()">처음으로 돌아가기</button>
            </div>
        </div>
    </div>

<script>
    // --- PERSONAS ---
    const avatars = {
        ceo: { icon: "👔", color: "#ce9178", name: "최대표" },
        pm: { icon: "📊", color: "#4ec9b0", name: "박팀장" },
        agent: { icon: "🎧", color: "#9cdcfe", name: "이지은 매니저" },
        me: { icon: "👨‍💻", color: "#0e639c", name: "나" }
    };

    // --- SCRIPT DATA ---
    const script = {
        // [STAGE 1]
        intro: {
            msgs: [
                { role: 'ceo', text: "김 수석, 이번 AICC 프로젝트 아주 중요해. 이사회에서 난리야." },
                { role: 'ceo', text: "경쟁사는 상담원 30% 감축했다는데 우린 뭐하냐고 하네. 무조건 **'효율'**과 **'속도'**가 최우선이야." }
            ],
            choices: [
                { label: "수용", text: "알겠습니다. 처리 속도(AHT) 단축을 최우선 목표로 설계하겠습니다.", next: 'task_v1' },
                { label: "우려", text: "대표님, 무조건적인 속도 경쟁은 품질 저하를 부를 수 있습니다.", next: 'intro_arg' }
            ]
        },
        intro_arg: {
            msgs: [ { role: 'ceo', text: "지금 품질 따질 때가 아니야! 일단 숫자를 만들어야 투자를 받는다고. 그냥 시키는 대로 해." } ],
            choices: [ { label: "포기", text: "네... 일단 지표 달성에 집중하겠습니다.", next: 'task_v1' } ]
        },
        
        // [STAGE 2]
        feedback_v1: {
            msgs: [
                { role: 'pm', text: "수석님, V1 지표 확인하셨어요? 속도는 빠른데... **오분류(Error)**가 너무 많아요." },
                { role: 'pm', text: "고객이 '환불'이라고 했는데 AI가 '상품 추천'을 해버려서 민원이 폭주 중입니다. 정확도 좀 높여주세요." }
            ],
            choices: [
                { label: "해결책", text: "문맥 분석 기능을 강화해서 정확도를 높이겠습니다.", next: 'task_v2' }
            ]
        },

        // [STAGE 3: INTERVIEW]
        feedback_v2: {
            mode: 'interview', // Trigger interview UI
            msgs: [
                { role: 'agent', text: "안녕하세요 엔지니어님. 현장 운영을 맡고 있는 이지은입니다. 인터뷰 요청주셔서 왔습니다." },
                { role: 'agent', text: "솔직히 말씀드려도 될까요? 지금 시스템... 저희한테는 **'족쇄'** 같습니다." }
            ],
            choices: [
                { label: "질문", text: "어떤 부분이 가장 힘드신가요? 구체적으로 말씀해주세요.", next: 'interview_deep' },
                { label: "방어", text: "데이터상으로는 효율이 많이 올랐는데요?", next: 'interview_conflict' }
            ]
        },
        interview_deep: {
            msgs: [
                { role: 'agent', text: "AI가 앞에서 고객 말을 자르고 기계적인 답변만 하니까, 제가 전화를 받으면 고객은 이미 머리 끝까지 화가 나 있어요." },
                { role: 'agent', text: "저는 하루 종일 **'죄송합니다, 기계가 실수를 했네요'**라고 사과만 하다가 끝나요. 이게 상담 업무인가요? 욕받이지." },
                { role: 'agent', text: "그리고 0.1초 만에 다음 콜 꽂히는 거... 저희도 사람인데 숨 쉴 틈은 주셔야죠." }
            ],
            choices: [
                { label: "공감/해결", text: "그런 고충이 있는 줄 몰랐습니다. 상담원 보호와 휴식권을 보장하는 기능을 즉시 추가하겠습니다.", next: 'task_v3' }
            ]
        },
        interview_conflict: {
            msgs: [
                { role: 'agent', text: "그 데이터가 사람 갈아넣어서 만든 숫자잖아요! 제 팀원 절반이 이번 달에 그만뒀어요. 시스템이 사람을 쫓아내고 있다고요." }
            ],
            choices: [
                { label: "수용", text: "죄송합니다. 제가 숫자에만 매몰됐었네요. 바로 수정하겠습니다.", next: 'task_v3' }
            ]
        }
    };

    // --- GAME ENGINE ---
    function startGame() {
        document.getElementById('intro-overlay').style.display = 'none';
        playScene('intro');
    }

    function renderMsg(role, text) {
        const chatBody = document.getElementById('chat-body');
        const isMe = role === 'me';
        const sender = avatars[role];
        
        const row = document.createElement('div');
        row.className = `msg-row ${isMe ? 'me' : ''}`;
        row.innerHTML = `
            <div class="avatar" style="background:${sender.color}">${sender.icon}</div>
            <div>
                <div class="sender" style="text-align:${isMe?'right':'left'}">${sender.name}</div>
                <div class="bubble ${isMe ? 'me' : 'other'}">${text}</div>
            </div>
        `;
        chatBody.appendChild(row);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function typeWriter(role, text, callback) {
        const ind = document.getElementById('typing-indicator');
        ind.style.display = 'block';
        ind.innerText = `${avatars[role].name} 입력 중...`;
        
        setTimeout(() => {
            ind.style.display = 'none';
            renderMsg(role, text);
            if(callback) callback();
        }, 1000); 
    }

    function playScene(sceneId) {
        const scene = script[sceneId];
        
        // INTERVIEW MODE TRIGGER
        if (scene.mode === 'interview') {
            document.getElementById('main-container').classList.add('interview-mode');
            document.getElementById('chat-title').innerText = "🎙️ 현장 사용자 인터뷰";
            document.getElementById('profile-card').style.display = 'block';
        }

        let msgIndex = 0;
        function nextMsg() {
            if (msgIndex < scene.msgs.length) {
                const m = scene.msgs[msgIndex++];
                typeWriter(m.role, m.text, nextMsg);
            } else {
                showChoices(scene.choices);
            }
        }
        nextMsg();
    }

    function showChoices(choices) {
        const container = document.getElementById('choices-container');
        container.innerHTML = '';
        choices.forEach(c => {
            const btn = document.createElement('button');
            btn.className = 'choice-btn';
            btn.innerHTML = `<strong>[${c.label}]</strong> ${c.text}`;
            btn.onclick = () => {
                container.innerHTML = '';
                renderMsg('me', c.text);
                if (c.next.startsWith('task_')) {
                    setTimeout(() => startIdeMission(c.next), 800);
                } else {
                    setTimeout(() => playScene(c.next), 800);
                }
            };
            container.appendChild(btn);
        });
    }

    // --- IDE LOGIC ---
    function startIdeMission(taskId) {
        const ideBody = document.getElementById('ide-body');
        let data = {};
        
        if (taskId === 'task_v1') {
            data = { 
                title: "Quest 1: 효율성 극대화", 
                desc: "CEO 지시: 상담원 연결을 최소화하고 처리 속도를 높이십시오.",
                items: [ {l:"Priority", v:"High_Speed"}, {l:"Latency", v:"200ms"}, {l:"Fallback", v:"Block_Call"} ] 
            };
        } else if (taskId === 'task_v2') {
            data = { 
                title: "Quest 2: 정확도 개선", 
                desc: "PM 요청: 오분류를 줄이기 위해 문맥 분석을 강화하십시오.",
                items: [ {l:"Model", v:"Context_Aware_v2"}, {l:"Intent_Check", v:"Deep_Analysis"} ] 
            };
        } else if (taskId === 'task_v3') {
            data = { 
                title: "Quest 3: 지속 가능성 (Human-Centric)", 
                desc: "사용자 피드백: 상담원 보호 및 휴식권 보장 로직을 구현하십시오.",
                items: [ {l:"Protection", v:"Abuse_Shield_On"}, {l:"Input_Filter", v:"Sanitize_Tone"}, {l:"Break_Rule", v:"Dynamic_Rest_3min"} ] 
            };
        }

        ideBody.innerHTML = `
            <div class="coding-container">
                <div class="mission-card">
                    <div style="font-size:18px; font-weight:bold; color:white; margin-bottom:10px;">${data.title}</div>
                    <div class="task-desc">${data.desc}</div>
                </div>
                <div class="code-editor">
                    <div style="color:#6a9955; margin-bottom:15px;"># config.yaml</div>
                    ${data.items.map(i => `
                        <div class="code-line">
                            <span style="color:#9cdcfe; width:120px;">${i.l}:</span> 
                            <input class="input-slot" type="text" value="${i.v}">
                        </div>`).join('')}
                </div>
                <button class="deploy-btn" onclick="deploy('${taskId}')">🚀 코드 배포 (Deploy)</button>
            </div>
        `;
    }

    function deploy(taskId) {
        const ideBody = document.getElementById('ide-body');
        ideBody.innerHTML = `<div class="locked-state"><h2>🚀 Deploying...</h2><p>서버에 변경사항을 적용 중입니다.</p></div>`;
        
        setTimeout(() => {
            ideBody.innerHTML = `<div class="locked-state"><div style="font-size:50px; opacity:0.3">🔒</div><h2>대기 중...</h2><p>메신저 반응을 확인하세요.</p></div>`;
            
            if (taskId === 'task_v1') {
                renderMsg('System', '✅ V1.0 배포 완료. (1주일 경과...)');
                setTimeout(() => playScene('feedback_v1'), 1500);
            } else if (taskId === 'task_v2') {
                renderMsg('System', '✅ V2.0 배포 완료. 현장 인터뷰 연결 중...');
                setTimeout(() => playScene('feedback_v2'), 2000);
            } else {
                document.getElementById('report-screen').style.display = 'block';
                renderReport();
            }
        }, 2000);
    }

    function renderReport() {
        document.getElementById('report-content').innerHTML = `
            <div class="stat-card" style="border-left: 5px solid #ce9178;">
                <h3>Step 1: Efficiency (CEO)</h3>
                <p style="color:#aaa">초기엔 효율성만 추구했습니다. -> <strong>조직 불안정 야기</strong></p>
            </div>
            <div class="stat-card" style="border-left: 5px solid #9cdcfe;">
                <h3>Step 3: Empathy (Agent)</h3>
                <p style="color:#aaa">현장의 목소리를 듣고 시스템을 수정했습니다. -> <strong>지속 가능한 공존 모델 달성</strong></p>
            </div>
            <p style="margin-top:20px; line-height:1.6; color:#ccc; text-align:center;">
                "기술적 결정은 언제나 정치적이고 윤리적인 결과를 낳습니다."
            </p>
        `;
    }

</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
