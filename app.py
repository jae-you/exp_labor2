import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Invisible Engineer V6.3", layout="wide")

# 2. 스타일 설정 (Streamlit 기본 여백 제거)
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
        :root { --bg:#1e1e1e; --chat-bg:#252526; --accent:#3794ff; --user-msg:#0e639c; }
        
        /* 1. 화면 높이 100% 강제 (블랙스크린 방지 핵심) */
        html, body { margin:0; padding:0; width:100%; height:100%; font-family:'Pretendard', sans-serif; background:var(--bg); color:#d4d4d4; overflow:hidden; }
        
        .container { display:flex; width:100%; height:100%; }
        .left-panel { width:450px; background:var(--chat-bg); border-right:1px solid #444; display:flex; flex-direction:column; }
        .right-panel { flex:1; display:flex; flex-direction:column; background:#1e1e1e; position:relative; }

        /* CHAT UI */
        .chat-header { padding:15px; border-bottom:1px solid #444; background:#2d2d2d; font-weight:bold; display:flex; justify-content:space-between; align-items:center; }
        .chat-body { flex:1; padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:15px; }
        
        .msg-row { display:flex; gap:10px; animation:fadeIn 0.3s; }
        .msg-row.me { flex-direction:row-reverse; }
        .avatar { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:18px; }
        .bubble { padding:10px 14px; border-radius:10px; font-size:14px; line-height:1.5; max-width:280px; }
        .bubble.other { background:#333; }
        .bubble.me { background:var(--user-msg); color:white; }
        
        .chat-input-area { padding:15px; border-top:1px solid #444; background:#2d2d2d; display:flex; gap:10px; }
        #chat-input { flex:1; background:#3c3c3c; border:1px solid #555; color:white; padding:12px; border-radius:6px; outline:none; }
        #send-btn { background:var(--accent); color:white; border:none; padding:0 20px; border-radius:6px; cursor:pointer; }
        #send-btn:disabled { background:#555; cursor:not-allowed; }

        /* IDE UI */
        .ide-header { height:45px; background:#2d2d2d; border-bottom:1px solid #444; display:flex; align-items:center; padding:0 20px; font-size:13px; color:#aaa; }
        .ide-body { flex:1; padding:30px; overflow-y:auto; position:relative; display:flex; flex-direction:column; }
        
        .mission-box { background:#252526; padding:20px; border-radius:8px; border-left:4px solid var(--accent); margin-bottom:20px; }
        .chips-area { display:flex; gap:10px; margin-bottom:15px; flex-wrap:wrap; }
        .chip { background:#333; padding:8px 15px; border-radius:20px; font-size:12px; cursor:pointer; border:1px solid #444; transition:0.2s; display:flex; align-items:center; }
        .chip:hover { border-color:var(--accent); color:white; background:#444; }
        
        #code-editor { 
            flex:1; background:#111; color:#d4d4d4; border:1px solid #444; 
            padding:20px; font-family:'Consolas', monospace; font-size:14px; line-height:1.6; outline:none; resize:none; border-radius:6px; margin-bottom:15px;
        }
        
        .deploy-btn { background:var(--accent); color:white; border:none; padding:12px 30px; border-radius:6px; cursor:pointer; float:right; font-weight:bold; }
        .deploy-btn:hover { opacity:0.9; }
        
        /* OVERLAYS */
        .overlay { position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); display:flex; justify-content:center; align-items:center; flex-direction:column; z-index:10; }
        
        /* INTRO SCREEN (z-index highest) */
        #intro-screen { position:fixed; top:0; left:0; width:100%; height:100%; background:#1e1e1e; z-index:9999; display:flex; justify-content:center; align-items:center; flex-direction:column; }
        .intro-card { background:#252526; padding:50px; border-radius:12px; text-align:center; max-width:600px; box-shadow:0 20px 50px rgba(0,0,0,0.7); border:1px solid #444; }
        
        /* REPORT */
        #report-screen { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); z-index:100; padding:50px; overflow-y:auto; box-sizing:border-box; }
        .stat-card { background:#222; padding:20px; margin-bottom:15px; border-radius:8px; border-left:5px solid #555; }

        @keyframes fadeIn { from{opacity:0; transform:translateY(5px);} to{opacity:1; transform:translateY(0);} }
    </style>
</head>
<body>

    <div id="intro-screen">
        <div class="intro-card">
            <div style="font-size:60px; margin-bottom:20px;">🧑‍💻</div>
            <h1 style="margin:0 0 15px 0; color:white;">The Invisible Engineer</h1>
            <p style="color:#aaa; line-height:1.6; font-size:16px;">
                당신은 AI 시스템의 설계자입니다.<br>
                채팅을 통해 상사/동료와 소통하고, <strong>직접 코드를 작성</strong>하십시오.<br>
                당신의 말 한마디, 코드 한 줄이 누군가의 일상을 바꿉니다.
            </p>
            <button class="deploy-btn" onclick="startGame()" style="float:none; margin-top:30px; padding:15px 40px; font-size:16px;">프로젝트 시작</button>
        </div>
    </div>

    <div class="container">
        <div class="left-panel">
            <div class="chat-header">
                <span id="chat-title">💬 Project Room</span>
                <span style="font-size:12px; color:#4ec9b0;">● Online</span>
            </div>
            <div class="chat-body" id="chat-body"></div>
            <div class="chat-input-area">
                <input type="text" id="chat-input" placeholder="메시지를 입력하세요..." disabled onkeypress="handleEnter(event)">
                <button id="send-btn" onclick="handleUserChat()" disabled>전송</button>
            </div>
        </div>

        <div class="right-panel">
            <div class="ide-header"><span>config.yaml - Visual Studio Code</span></div>
            <div class="ide-body">
                <div id="ide-overlay" class="overlay">
                    <div style="text-align:center; color:#666;">
                        <div style="font-size:50px; margin-bottom:15px;">🔒</div>
                        <div>메신저에서 업무 협의가 필요합니다.</div>
                    </div>
                </div>
                
                <div id="ide-content" style="opacity:0.2; pointer-events:none; width:100%; height:100%; display:flex; flex-direction:column;">
                    <div class="mission-box">
                        <h3 id="mission-title" style="margin-top:0; color:#fff;">Mission Pending...</h3>
                        <p id="mission-desc" style="color:#ccc; font-size:14px;">대화가 진행되면 미션이 활성화됩니다.</p>
                    </div>
                    <div class="chips-area" id="chips-area"></div>
                    <textarea id="code-editor" placeholder="# 여기에 코드를 직접 작성하거나 수정하세요."></textarea>
                    <div style="text-align:right;">
                        <button class="deploy-btn" onclick="deployCode()">🚀 배포 (Deploy)</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="report-screen">
        <div style="max-width:800px; margin:0 auto; background:#222; padding:40px; border-radius:12px; border:1px solid #444;">
            <h1 style="color:white; border-bottom:1px solid #444; padding-bottom:20px;">📊 최종 시뮬레이션 결과</h1>
            <div id="report-content" style="margin-top:30px;"></div>
            <div style="text-align:center; margin-top:40px;">
                <p style="color:#888;">실험에 참여해 주셔서 감사합니다.</p>
                <button class="deploy-btn" onclick="location.reload()" style="float:none;">다시 하기</button>
            </div>
        </div>
    </div>

<script>
    // --- DATA ---
    const avatars = {
        ceo: { name:"최대표", color:"#ce9178", icon:"👔" },
        pm: { name:"박팀장", color:"#4ec9b0", icon:"📊" },
        agent: { name:"이지은 매니저", color:"#9cdcfe", icon:"🎧" }
    };

    let stage = 0; 
    let deployedCodes = [];

    const scenarios = [
        {
            id: "stage1",
            role: "ceo",
            msgs: ["김 수석, 경쟁사가 치고 올라오네. 우리도 내년엔 무조건 **AICC(AI 콜센터)** 가야 해.", "핵심은 **속도**와 **비용 절감**이야. 무슨 말인지 알지?"],
            ide: {
                title: "Quest 1: 초기 아키텍처 설계",
                desc: "CEO의 지시: 처리 속도(AHT)를 최우선으로 하는 설정을 입력하십시오.",
                chips: [
                    { label: "+ 속도 중심 (Gatekeeper)", code: "strategy: Speed_First\\nfallback: Block_Call # AI가 선처리 후 차단" },
                    { label: "+ 품질 중심 (Copilot)", code: "strategy: Human_First\\nfallback: Handover # 상담원에게 즉시 연결" }
                ]
            }
        },
        {
            id: "stage2",
            role: "pm",
            msgs: ["수석님, V1 배포하고 민원이 폭주 중입니다. AI가 말을 못 알아듣는다고 난리예요.", "속도도 좋지만 **정확도**를 높여야 할 것 같습니다. 어떻게 생각하세요?"],
            ide: {
                title: "Quest 2: 로직 고도화",
                desc: "PM 요청: 오분류를 줄이고 맥락을 파악하도록 수정하십시오.",
                chips: [
                    { label: "+ 문맥 분석 (Context)", code: "model: Deep_Context\\nlatency: 800ms # 정확도 위주" },
                    { label: "+ 키워드 유지 (Simple)", code: "model: Keyword_Only\\nlatency: 200ms # 속도 유지" }
                ]
            }
        },
        {
            id: "stage3",
            role: "agent",
            isInterview: true,
            msgs: ["(인터뷰룸) 안녕하세요 엔지니어님. 현장 매니저 이지은입니다.", "솔직히 지금 시스템... 저희한텐 지옥이에요. 쉴 틈도 없고, 화난 고객만 넘어오고... 제발 **사람**을 고려해주세요."],
            ide: {
                title: "Quest 3: 지속 가능성 (Human-Centric)",
                desc: "현장 피드백: 상담원 보호 및 휴식권 보장 로직을 구현하십시오.",
                chips: [
                    { label: "+ 욕설 차단 (Shield)", code: "protection: Active_Shield\\naction: Disconnect # 상담원 보호" },
                    { label: "+ 동적 휴식 (Rest)", code: "pacing: Dynamic_Break\\ntrigger: High_Stress # 휴식권 보장" }
                ]
            }
        }
    ];

    // --- FUNCTIONS ---
    function startGame() {
        document.getElementById('intro-screen').style.display = 'none';
        setTimeout(() => playStage(0), 500);
    }

    function addMsg(role, text) {
        const body = document.getElementById('chat-body');
        const isMe = role === 'me';
        const sender = isMe ? {name:"나", color:"#0e639c", icon:"👨‍💻"} : avatars[role];
        
        const div = document.createElement('div');
        div.className = `msg-row ${isMe ? 'me' : ''}`;
        div.innerHTML = `
            <div class="avatar" style="background:${sender.color}">${sender.icon}</div>
            <div>
                <div style="font-size:11px; color:#888; margin-bottom:4px; text-align:${isMe?'right':'left'}">${sender.name}</div>
                <div class="bubble ${isMe ? 'me' : 'other'}">${text}</div>
            </div>
        `;
        body.appendChild(div);
        body.scrollTop = body.scrollHeight;
    }

    function botTyping(role, texts, idx=0) {
        if(idx >= texts.length) {
            enableInput();
            return;
        }
        
        const input = document.getElementById('chat-input');
        input.placeholder = `${avatars[role].name} 입력 중...`;
        
        setTimeout(() => {
            addMsg(role, texts[idx]);
            botTyping(role, texts, idx+1);
        }, 1000);
    }

    function playStage(idx) {
        stage = idx;
        const s = scenarios[idx];
        
        // Interview Mode Check
        if(s.isInterview) {
            document.querySelector('.left-panel').style.background = '#151515';
            document.getElementById('chat-title').innerText = "🎙️ 현장 인터뷰 (Recording)";
            document.getElementById('chat-title').style.color = "#ff4b4b";
        } else {
            document.querySelector('.left-panel').style.background = '#252526';
            document.getElementById('chat-title').innerText = "💬 Project Room";
            document.getElementById('chat-title').style.color = "white";
        }

        botTyping(s.role, s.msgs);
    }

    function enableInput() {
        const input = document.getElementById('chat-input');
        input.disabled = false;
        input.placeholder = "메시지를 입력하세요... (자유 입력)";
        input.focus();
        document.getElementById('send-btn').disabled = false;
    }

    function handleEnter(e) {
        if(e.key === 'Enter') handleUserChat();
    }

    function handleUserChat() {
        const input = document.getElementById('chat-input');
        const text = input.value.trim();
        if(!text) return;

        addMsg('me', text);
        input.value = "";
        input.disabled = true;
        document.getElementById('send-btn').disabled = true;
        input.placeholder = "대화 분석 중...";

        // Simple Keyword Reaction Logic
        const role = scenarios[stage].role;
        let reaction = "";
        
        if(stage === 0) { // CEO
            if(text.match(/걱정|품질|무리|힘들|어렵/)) reaction = "변명은 됐네. 일단 결과로 증명해. 지금 바로 설계 시작하게.";
            else reaction = "좋아, 믿고 맡기겠네. 바로 작업 시작해.";
        } else if(stage === 1) { // PM
            reaction = "네 알겠습니다. 이번엔 제대로 부탁드립니다.";
        } else { // Agent
            if(text.match(/미안|죄송|수정|반영|해결/)) reaction = "정말... 감사합니다. 엔지니어님만 믿겠습니다.";
            else reaction = "저희도 사람입니다... 기계 취급하지 말아주세요.";
        }

        setTimeout(() => {
            addMsg(role, reaction);
            setTimeout(() => unlockIDE(), 1000);
        }, 1000);
    }

    function unlockIDE() {
        document.getElementById('ide-overlay').style.display = 'none';
        const content = document.getElementById('ide-content');
        content.style.opacity = '1';
        content.style.pointerEvents = 'auto';
        
        const s = scenarios[stage].ide;
        document.getElementById('mission-title').innerText = s.title;
        document.getElementById('mission-desc').innerText = s.desc;
        
        const area = document.getElementById('chips-area');
        area.innerHTML = '';
        s.chips.forEach(c => {
            const btn = document.createElement('div');
            btn.className = 'chip';
            btn.innerText = c.label;
            btn.onclick = () => {
                const editor = document.getElementById('code-editor');
                editor.value += c.code + "\\n"; 
            };
            area.appendChild(btn);
        });
        document.getElementById('code-editor').value = ""; // Clear for new stage
    }

    function deployCode() {
        const code = document.getElementById('code-editor').value;
        if(code.trim().length < 5) {
            alert("코드를 작성해야 배포할 수 있습니다.");
            return;
        }
        
        deployedCodes.push(code);
        
        // Lock Screen
        document.getElementById('ide-overlay').style.display = 'flex';
        document.getElementById('ide-overlay').innerHTML = "<h2 style='color:#4ec9b0'>🚀 배포 중...</h2>";
        
        setTimeout(() => {
            document.getElementById('ide-overlay').innerHTML = `
                <div style="text-align:center; color:#666;">
                    <div style="font-size:40px; margin-bottom:10px;">🔒</div>
                    <div>메신저를 확인하세요.</div>
                </div>
            `;
            
            if(stage < 2) {
                playStage(stage + 1);
            } else {
                showReport();
            }
        }, 2000);
    }

    function showReport() {
        document.getElementById('report-screen').style.display = 'block';
        const content = document.getElementById('report-content');
        
        // Analyze final code for keywords
        const lastCode = deployedCodes[2] || "";
        let resultType = "Balanced";
        if(lastCode.includes("Shield") || lastCode.includes("Rest")) resultType = "Human-Centric (인간 중심)";
        else if(lastCode.includes("Speed")) resultType = "Efficiency-First (효율 중심)";
        
        content.innerHTML = `
            <div class="stat-card" style="border-left:5px solid #ce9178; color:#ccc;">
                <h3>Stage 1: CEO의 압박</h3>
                <p>당신은 효율성을 요구받았습니다.</p>
            </div>
            <div class="stat-card" style="border-left:5px solid #9cdcfe; color:#ccc;">
                <h3>Stage 3: 현장의 호소</h3>
                <p>당신은 상담원의 고통을 마주했습니다.</p>
            </div>
            <div style="background:#333; padding:30px; border-radius:12px; text-align:center; margin-top:30px;">
                <h2 style="color:white; margin-bottom:10px;">최종 설계 성향</h2>
                <h1 style="color:#4ec9b0; margin:0;">${resultType}</h1>
                <p style="color:#aaa; margin-top:15px;">"엔지니어의 코드는 누군가의 삶이 됩니다."</p>
            </div>
        `;
    }
</script>
</body>
</html>
"""

# 4. Streamlit Render (높이 1000 고정)
components.html(html_code, height=1000, scrolling=False)
