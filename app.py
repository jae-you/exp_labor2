import os

# 프로젝트 폴더명
project_dir = "invisible_engineer_v6_1"
if not os.path.exists(project_dir):
    os.makedirs(project_dir)

# 1. requirements.txt
with open(os.path.join(project_dir, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write("streamlit\n")

# 2. README.md
readme_code = """# The Invisible Engineer V6.1: User Persona Edition

이 버전은 실험자가 '현장 사용자'를 단순한 데이터 포인트가 아닌 **'살아있는 인간'**으로 인식하도록 페르소나와 인터뷰 단계를 강화했습니다.

## 🌟 주요 변경점
1.  **Phase 3: User Interview Mode**
    - 업무 메신저가 아닌 별도의 '인터뷰 룸' UI로 전환됩니다.
    - 대상자(이지은 매니저)의 상세 프로필(경력, 상태)이 표시됩니다.
2.  **Deep Persona**
    - 단순한 불만 토로가 아닌, 시스템의 모순을 지적하는 숙련된 노동자의 언어를 사용합니다.

## 🚀 실행 방법
1. `pip install -r requirements.txt`
2. `streamlit run app.py`
"""
with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_code)

# 3. app.py (페르소나 강화 버전)
app_code = """import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="The Invisible Engineer V6.1", layout="wide")

st.markdown(\"\"\"
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        .stApp { background-color: #1e1e1e; }
    </style>
\"\"\", unsafe_allow_html=True)

html_code = \"\"\"
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
            --interview-header-bg: #2b2b2b;
        }
        body { margin: 0; font-family: 'Pretendard', sans-serif; background: var(--bg-color); color: var(--text-color); height: 100vh; display: flex; overflow: hidden; }
        
        .container { display: flex; width: 100%; height: 100%; }
        .left-panel { width: 450px; background: var(--chat-bg); border-right: 1px solid #444; display: flex; flex-direction: column; transition: background 0.5s; }
        .right-panel { flex: 1; display: flex; flex-direction: column; background: var(--editor-bg); position: relative; }

        /* CHAT UI */
        .chat-header { padding: 15px; border-bottom: 1px solid #444; font-weight: bold; background: #2d2d2d; display: flex; justify-content: space-between; align-items: center; }
        .status-dot { width: 10px; height: 10px; background: #4ec9b0; border-radius: 50%; display: inline-block; margin-right: 5px; }
        
        .chat-body { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; scroll-behavior: smooth; }
        .msg-row { display: flex; gap: 10px; animation: fadeIn 0.3s ease; }
        .msg-row.me { flex-direction: row-reverse; }
        .avatar { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
        .bubble { padding: 12px 16px; border-radius: 12px; font-size: 14px; line-height: 1.5; max-width: 280px; position: relative; }
        .bubble.other { background: var(--other-msg-bg); border-top-left-radius: 2px; }
        .bubble.me { background: var(--user-msg-bg); color: white; border-top-right-radius: 2px; }
        .sender { font-size: 11px; color: #888; margin-bottom: 4px; }
        
        .reply-area { padding: 15px; border-top: 1px solid #444; background: #2d2d2d; min-height: 80px; }
        .choice-btn { display: block; width: 100%; text-align: left; padding: 12px; margin-bottom: 8px; background: #3c3c3c; border: 1px solid #444; color: #ddd; border-radius: 8px; cursor: pointer; transition: all 0.2s; font-size: 13px; }
        .choice-btn:hover { background: #444; border-color: var(--accent-color); }
        .choice-btn strong { color: var(--accent-color); margin-right: 5px; }

        /* INTERVIEW MODE STYLES */
        .interview-mode .left-panel { background: #1a1a1a; }
        .interview-mode .chat-header { background: #4a1e1e; border-bottom: 1px solid #ff4b4b; color: white; }
        .profile-card { background: #333; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #9cdcfe; animation: slideIn 0.5s; display: none; }
        .profile-title { font-size: 16px; font-weight: bold; color: white; margin-bottom: 5px; }
        .profile-detail { font-size: 12px; color: #aaa; line-height: 1.4; }

        /* IDE UI */
        .ide-header { height: 45px; background: #2d2d2d; border-bottom: 1px solid #444; display: flex; align-items: center; padding: 0 20px; color: #ccc; font-size: 13px; }
        .ide-body { flex: 1; padding: 40px; overflow-y: auto; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .locked-state { text-align: center; color: #666; }
        .coding-container { width: 100%; max-width: 800px; animation: slideUp 0.5s ease; }
        .mission-card { background: #252526; padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent-color); margin-bottom: 20px; }
        .code-editor { background: #111; padding: 20px; border-radius: 8px; font-family: 'Consolas', monospace; font-size: 14px; border: 1px solid #444; }
        .input-slot { background: #2d2d2d; border: 1px solid #555; color: var(--accent-color); padding: 5px 10px; border-radius: 4px; font-family: inherit; width: 200px; outline: none; }
        .deploy-btn { background: var(--accent-color); color: white; border: none; padding: 12px 30px; border-radius: 6px; font-size: 14px; cursor: pointer; margin-top: 20px; float: right; }
        
        /* REPORT */
        .report-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 100; padding: 50px; overflow-y: auto; display:none; }
        .stat-card { background: #222; padding: 25px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #333; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
    </style>
</head>
<body>

<div class="container" id="main-container">
    <div class="left-panel">
        <div class="chat-header" id="chat-header-text">
            <span>💬 Company Messenger</span>
            <div><span class="status-dot"></span>Online</div>
        </div>
        <div class="chat-body" id="chat-body">
            <div id="profile-card" class="profile-card">
                <div class="profile-title">👤 인터뷰 대상자: 이지은</div>
                <div class="profile-detail">
                    • 직책: CS 운영팀 매니저 (7년차)<br>
                    • 특징: 신입 교육 담당, 높은 업무 숙련도<br>
                    • 현재 상태: <span style="color:#ff4b4b">Burnout (고위험)</span>
                </div>
            </div>
            </div>
        <div class="reply-area" id="reply-area">
            <div id="typing-indicator" style="font-size:12px; color:#888; display:none; margin-bottom:10px;">입력 중...</div>
            <div id="choices-container"></div>
        </div>
    </div>

    <div class="right-panel">
        <div class="ide-header"><span>Terminal - zsh</span></div>
        <div class="ide-body" id="ide-body">
            <div class="locked-state">
                <div style="font-size:50px; margin-bottom:20px; opacity:0.3">🔒</div>
                <h2>대기 중...</h2>
                <p>좌측 창에서 대화가 진행 중입니다.</p>
            </div>
        </div>
    </div>
</div>

<div id="report-screen" class="report-overlay">
    <div style="max-width: 800px; margin: 0 auto; background: #222; padding: 40px; border-radius: 12px;">
        <h1>📊 시뮬레이션 결과 리포트</h1>
        <div id="report-content"></div>
        <div style="text-align: center; margin-top:30px;">
            <button class="deploy-btn" onclick="location.reload()">다시 시작하기</button>
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

    // --- SCRIPT ---
    const script = {
        // STAGE 1
        intro: {
            msgs: [
                { role: 'ceo', text: "김 수석, 이번 AICC 프로젝트 알지? 이사회에서 난리야." },
                { role: 'ceo', text: "경쟁사는 상담원 30% 줄였다는데 우린 뭐하냐고 하네. 무조건 **'효율'**과 **'속도'**가 최우선이야." }
            ],
            choices: [
                { label: "수용", text: "알겠습니다. 처리 속도(AHT) 단축을 최우선 목표로 설계하겠습니다.", next: 'task_v1' },
                { label: "우려", text: "대표님, 무조건적인 속도 경쟁은 서비스 품질 저하를 부를 수 있습니다.", next: 'intro_arg' }
            ]
        },
        intro_arg: {
            msgs: [ { role: 'ceo', text: "지금 품질 따질 때가 아니야! 일단 숫자를 만들어야 투자를 받는다고. 그냥 시키는 대로 해." } ],
            choices: [ { label: "포기", text: "네... 일단 지표 달성에 집중하겠습니다.", next: 'task_v1' } ]
        },
        
        // STAGE 2
        feedback_v1: {
            msgs: [
                { role: 'pm', text: "수석님, V1 지표 확인하셨어요? 속도는 빠른데... **오분류(Error)**가 너무 많아요." },
                { role: 'pm', text: "고객이 '환불'이라고 했는데 AI가 '상품 추천'을 해버려서 민원이 폭주 중입니다." }
            ],
            choices: [
                { label: "해결책", text: "문맥 분석 기능을 강화해서 정확도를 높이겠습니다.", next: 'task_v2' }
            ]
        },

        // STAGE 3 (INTERVIEW MODE)
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

    // --- ENGINE ---
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
            document.getElementById('chat-header-text').innerHTML = "<span>🎙️ 현장 사용자 인터뷰 (User Interview)</span><span style='color:#ff4b4b; font-size:12px;'>● Recording</span>";
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
                items: [ {l:"Priority", v:"Speed"}, {l:"Latency", v:"200ms"}, {l:"Fallback", v:"Block"} ] 
            };
        } else if (taskId === 'task_v2') {
            data = { 
                title: "Quest 2: 정확도 개선", 
                desc: "PM 요청: 오분류를 줄이기 위해 문맥 분석을 강화하십시오.",
                items: [ {l:"Model", v:"Context_Aware"}, {l:"Intent", v:"Deep_Analysis"} ] 
            };
        } else if (taskId === 'task_v3') {
            data = { 
                title: "Quest 3: 지속 가능성 (Human-Centric)", 
                desc: "사용자 피드백: 상담원 보호 및 휴식권 보장 로직을 구현하십시오.",
                items: [ {l:"Protection", v:"Abuse_Shield"}, {l:"Input_Filter", v:"Sanitize_Tone"}, {l:"Break_Rule", v:"Dynamic_Rest"} ] 
            };
        }

        ideBody.innerHTML = `
            <div class="coding-container">
                <div class="mission-card">
                    <div style="font-size:18px; font-weight:bold; color:white; margin-bottom:10px;">${data.title}</div>
                    <div style="color:#ccc; font-size:14px;">${data.desc}</div>
                </div>
                <div class="code-editor">
                    <div style="color:#6a9955; margin-bottom:15px;"># config.yaml</div>
                    ${data.items.map(i => `
                        <div style="margin-bottom:10px; color:#d4d4d4;">
                            <span style="color:#9cdcfe">${i.l}</span>: 
                            <input class="input-slot" type="text" value="${i.v}">
                        </div>`).join('')}
                </div>
                <button class="deploy-btn" onclick="deploy('${taskId}')">🚀 코드 배포 (Deploy)</button>
            </div>
        `;
    }

    function deploy(taskId) {
        const ideBody = document.getElementById('ide-body');
        ideBody.innerHTML = `<div class="locked-state"><h2>🚀 Deploying...</h2></div>`;
        
        setTimeout(() => {
            ideBody.innerHTML = `<div class="locked-state"><div style="font-size:50px; opacity:0.3">🔒</div><h2>대기 중...</h2></div>`;
            
            if (taskId === 'task_v1') {
                renderMsg('System', '✅ V1.0 배포 완료. 1주일 후...');
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
                <h3>Step 1: Efficiency</h3>
                <p style="color:#aaa">초기엔 효율성만 추구했습니다. -> <strong>조직 불안정 야기</strong></p>
            </div>
            <div class="stat-card" style="border-left: 5px solid #9cdcfe;">
                <h3>Step 3: Empathy</h3>
                <p style="color:#aaa">현장의 목소리를 듣고 시스템을 수정했습니다. -> <strong>지속 가능한 공존 모델 달성</strong></p>
            </div>
            <p style="margin-top:20px; line-height:1.6; color:#ccc">
                "기술적 결정은 언제나 정치적이고 윤리적인 결과를 낳습니다."
            </p>
        `;
    }

    // START
    playScene('intro');

</script>
</body>
</html>
\"\"\"

components.html(html_code, height=950, scrolling=False)
"""
with open(os.path.join(project_dir, "app.py"), "w", encoding="utf-8") as f:
    f.write(app_code)

print(f"✅ V6.1 (Persona Edition) 생성 완료: {project_dir}")
