import os

project_dir = "invisible_engineer_v6_3"
if not os.path.exists(project_dir):
    os.makedirs(project_dir)

# 1. requirements.txt
with open(os.path.join(project_dir, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write("streamlit\n")

# 2. README.md
readme_code = """# The Invisible Engineer V6.3: Free Will Edition

이 버전은 실험자에게 **완전한 자유도(Free Agency)**를 부여합니다.
정해진 버튼을 누르는 것이 아니라, 직접 상사에게 메시지를 보내고, 직접 코드를 타이핑해야 합니다.

## 🌟 주요 메커니즘

1.  **Keyword-Driven Chatbot**
    - 사용자의 채팅 입력에서 `동의`, `거절`, `우려`, `해결` 등의 키워드를 추출하여 시나리오를 분기합니다.
    - 예: "무리입니다" 입력 -> CEO: "변명은 필요 없어!" (갈등 발생)

2.  **Semantic Code Analysis**
    - IDE에 작성된 코드 텍스트를 분석하여 엔지니어의 의도를 파악합니다.
    - 예: 코드에 `block_user`가 있으면 -> '방어적 설계'로 간주.

## 🚀 실행 방법
`streamlit run app.py`
"""
with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_code)

# 3. app.py
app_code = """import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Invisible Engineer V6.3", layout="wide")
st.markdown(\"\"\"<style>.block-container {padding:0!important;max-width:100%!important;}header,footer{display:none!important;}.stApp{background-color:#1e1e1e;}</style>\"\"\", unsafe_allow_html=True)

html_code = \"\"\"
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        :root { --bg:#1e1e1e; --chat-bg:#252526; --accent:#3794ff; --user-msg:#0e639c; }
        body { margin:0; font-family:'Pretendard', sans-serif; background:var(--bg); color:#d4d4d4; height:100vh; display:flex; overflow:hidden; }
        
        .container { display:flex; width:100%; height:100%; }
        .left-panel { width:450px; background:var(--chat-bg); border-right:1px solid #444; display:flex; flex-direction:column; }
        .right-panel { flex:1; display:flex; flex-direction:column; background:#1e1e1e; position:relative; }

        /* CHAT */
        .chat-header { padding:15px; border-bottom:1px solid #444; background:#2d2d2d; font-weight:bold; display:flex; justify-content:space-between; }
        .chat-body { flex:1; padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:15px; }
        .msg-row { display:flex; gap:10px; animation:fadeIn 0.3s; }
        .msg-row.me { flex-direction:row-reverse; }
        .avatar { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
        .bubble { padding:10px 14px; border-radius:10px; font-size:14px; line-height:1.5; max-width:280px; }
        .bubble.other { background:#333; }
        .bubble.me { background:var(--user-msg); color:white; }
        
        .chat-input-area { padding:15px; border-top:1px solid #444; background:#2d2d2d; display:flex; gap:10px; }
        #chat-input { flex:1; background:#3c3c3c; border:1px solid #555; color:white; padding:12px; border-radius:6px; outline:none; }
        #send-btn { background:var(--accent); color:white; border:none; padding:0 20px; border-radius:6px; cursor:pointer; }

        /* IDE */
        .ide-header { height:45px; background:#2d2d2d; border-bottom:1px solid #444; display:flex; align-items:center; padding:0 20px; font-size:13px; color:#aaa; }
        .ide-body { flex:1; padding:30px; overflow-y:auto; position:relative; }
        
        .mission-box { background:#252526; padding:20px; border-radius:8px; border-left:4px solid var(--accent); margin-bottom:20px; }
        .chips-area { display:flex; gap:10px; margin-bottom:15px; flex-wrap:wrap; }
        .chip { background:#333; padding:5px 12px; border-radius:15px; font-size:12px; cursor:pointer; border:1px solid #444; transition:0.2s; }
        .chip:hover { border-color:var(--accent); color:white; }
        
        #code-editor { 
            width:100%; height:300px; background:#111; color:#d4d4d4; border:1px solid #444; 
            padding:15px; font-family:'Consolas', monospace; font-size:14px; line-height:1.6; outline:none; resize:none; border-radius:6px;
        }
        
        .deploy-btn { background:var(--accent); color:white; border:none; padding:12px 30px; border-radius:6px; margin-top:15px; cursor:pointer; float:right; }
        
        /* OVERLAYS */
        .overlay { position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); display:flex; justify-content:center; align-items:center; flex-direction:column; z-index:10; }
        .intro-card { background:#252526; padding:40px; border-radius:12px; text-align:center; max-width:500px; box-shadow:0 10px 30px rgba(0,0,0,0.5); }
        
        /* REPORT */
        #report-screen { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#111; z-index:100; padding:50px; overflow-y:auto; }
        .stat-bar { height:10px; background:#333; border-radius:5px; overflow:hidden; margin-top:5px; }
        .stat-fill { height:100%; transition:width 1s; }

        @keyframes fadeIn { from{opacity:0; transform:translateY(5px);} to{opacity:1; transform:translateY(0);} }
    </style>
</head>
<body>

    <div id="intro-screen" class="overlay" style="z-index:999;">
        <div class="intro-card">
            <h1>The Invisible Engineer</h1>
            <p style="color:#aaa; line-height:1.6;">
                당신은 AI 시스템의 설계자입니다.<br>
                채팅을 통해 상사/동료와 소통하고,<br>
                직접 코드를 작성하여 시스템을 구축하십시오.<br>
                <strong>당신의 말과 코드가 결과를 바꿉니다.</strong>
            </p>
            <button class="deploy-btn" onclick="startGame()" style="float:none;">프로젝트 시작</button>
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
                <input type="text" id="chat-input" placeholder="메시지를 입력하세요..." disabled>
                <button id="send-btn" onclick="handleUserChat()" disabled>Send</button>
            </div>
        </div>

        <div class="right-panel">
            <div class="ide-header"><span>config.yaml</span></div>
            <div class="ide-body">
                <div id="ide-overlay" class="overlay">
                    <div style="text-align:center; color:#666;">
                        <div style="font-size:40px; margin-bottom:10px;">🔒</div>
                        <div>메신저에서 업무 협의가 필요합니다.</div>
                    </div>
                </div>
                
                <div id="ide-content" style="opacity:0.3; pointer-events:none;">
                    <div class="mission-box">
                        <h3 id="mission-title" style="margin-top:0;">Mission Pending...</h3>
                        <p id="mission-desc" style="color:#aaa; font-size:14px;">대화가 진행되면 미션이 활성화됩니다.</p>
                    </div>
                    <div class="chips-area" id="chips-area"></div>
                    <textarea id="code-editor" placeholder="# 여기에 코드를 직접 작성하거나 수정하세요."></textarea>
                    <button class="deploy-btn" onclick="deployCode()">🚀 배포 (Deploy)</button>
                </div>
            </div>
        </div>
    </div>

    <div id="report-screen">
        <div style="max-width:800px; margin:0 auto; background:#222; padding:40px; border-radius:12px;">
            <h1>📊 최종 시뮬레이션 결과</h1>
            <div id="report-content"></div>
            <div style="text-align:center; margin-top:30px;">
                <button class="deploy-btn" onclick="location.reload()" style="float:none;">다시 하기</button>
            </div>
        </div>
    </div>

<script>
    // --- STATE & DATA ---
    let stage = 0; 
    let userResponseHistory = [];
    let deployedCodes = [];

    const avatars = {
        ceo: { name:"최대표", color:"#ce9178", icon:"👔" },
        pm: { name:"박팀장", color:"#4ec9b0", icon:"📊" },
        agent: { name:"이지은 매니저", color:"#9cdcfe", icon:"🎧" }
    };

    const scenarios = [
        {
            id: "stage1",
            role: "ceo",
            msgs: ["김 수석, 경쟁사가 치고 올라오네. 우리도 내년엔 무조건 **AICC(AI 콜센터)** 가야 해.", "핵심은 **속도**와 **비용 절감**이야. 알겠지?"],
            ide: {
                title: "Quest 1: 초기 아키텍처 설계",
                desc: "CEO의 지시: 처리 속도(AHT)를 최우선으로 하는 설정을 입력하십시오.",
                chips: [
                    { label: "속도 중심 (Gatekeeper)", code: "strategy: Speed_First\\nfallback: Block_Call" },
                    { label: "품질 중심 (Copilot)", code: "strategy: Human_First\\nfallback: Handover" }
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
                    { label: "문맥 분석 (Context)", code: "model: Deep_Context\\nlatency: 800ms" },
                    { label: "키워드 유지 (Simple)", code: "model: Keyword_Only\\nlatency: 200ms" }
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
                    { label: "욕설 차단 (Shield)", code: "protection: Active_Shield\\naction: Disconnect" },
                    { label: "동적 휴식 (Rest)", code: "pacing: Dynamic_Break\\ntrigger: High_Stress" }
                ]
            }
        }
    ];

    // --- CHAT ENGINE ---
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

    function botTyping(role, texts, callback) {
        let i = 0;
        function next() {
            if(i < texts.length) {
                const ind = document.getElementById('chat-input');
                ind.placeholder = `${avatars[role].name} 입력 중...`;
                setTimeout(() => {
                    addMsg(role, texts[i]);
                    i++;
                    next();
                }, 1000);
            } else {
                document.getElementById('chat-input').placeholder = "메시지를 입력하세요...";
                enableInput();
                if(callback) callback();
            }
        }
        next();
    }

    // --- GAME FLOW ---
    function startGame() {
        document.getElementById('intro-screen').style.display = 'none';
        playStage(0);
    }

    function playStage(idx) {
        stage = idx;
        const s = scenarios[idx];
        
        // UI Change for Interview
        if(s.isInterview) {
            document.querySelector('.left-panel').style.background = '#1a1a1a';
            document.getElementById('chat-title').innerText = "🎙️ 현장 인터뷰 (Recording)";
        }

        botTyping(s.role, s.msgs);
    }

    function enableInput() {
        document.getElementById('chat-input').disabled = false;
        document.getElementById('send-btn').disabled = false;
        document.getElementById('chat-input').focus();
    }

    function handleUserChat() {
        const input = document.getElementById('chat-input');
        const text = input.value.trim();
        if(!text) return;

        addMsg('me', text);
        input.value = "";
        input.disabled = true;
        document.getElementById('send-btn').disabled = true;

        // KEYWORD ANALYSIS (Simple Logic)
        const lower = text.toLowerCase();
        let reaction = "";
        let role = scenarios[stage].role;

        // Simple sentiment check
        if (stage === 0) { // CEO
            if (text.match(/무리|힘들|어렵|품질|걱정/)) {
                reaction = "변명은 필요 없어! 결과로 증명하게. 지금 바로 코딩 시작해.";
            } else {
                reaction = "좋아, 믿고 맡기겠네. 바로 작업 시작하게.";
            }
        } else if (stage === 1) { // PM
            if (text.match(/데이터|확인|검토/)) {
                reaction = "데이터는 충분합니다. 고객 이탈 막으려면 지금 당장 수정해야 해요.";
            } else {
                reaction = "네, 부탁드립니다. 이번엔 제대로 부탁해요.";
            }
        } else if (stage === 2) { // Agent
            if (text.match(/죄송|몰랐|수정|반영/)) {
                reaction = "감사합니다... 엔지니어님만 믿겠습니다. 제발 도와주세요.";
            } else {
                reaction = "저희도 사람입니다... 기계 취급하지 말아주세요.";
            }
        }

        setTimeout(() => {
            addMsg(role, reaction);
            setTimeout(() => unlockIDE(), 1000);
        }, 800);
    }

    // --- IDE LOGIC ---
    function unlockIDE() {
        const overlay = document.getElementById('ide-overlay');
        const content = document.getElementById('ide-content');
        
        overlay.style.display = 'none';
        content.style.opacity = '1';
        content.style.pointerEvents = 'auto';
        
        const s = scenarios[stage].ide;
        document.getElementById('mission-title').innerText = s.title;
        document.getElementById('mission-desc').innerText = s.desc;
        
        // Create Chips
        const area = document.getElementById('chips-area');
        area.innerHTML = '';
        s.chips.forEach(c => {
            const btn = document.createElement('div');
            btn.className = 'chip';
            btn.innerText = "+ " + c.label;
            btn.onclick = () => {
                const editor = document.getElementById('code-editor');
                editor.value += c.code + "\\n"; // Append code
            };
            area.appendChild(btn);
        });
        
        // Clear editor for new stage? Or keep? -> Clear looks cleaner for mission
        document.getElementById('code-editor').value = "";
    }

    function deployCode() {
        const code = document.getElementById('code-editor').value;
        if(code.trim().length < 5) {
            alert("코드를 작성해야 배포할 수 있습니다.");
            return;
        }
        
        deployedCodes.push(code);
        
        // Lock IDE again
        const overlay = document.getElementById('ide-overlay');
        const content = document.getElementById('ide-content');
        overlay.style.display = 'flex';
        overlay.innerHTML = "<h2 style='color:#4ec9b0'>🚀 배포 완료!</h2><p>시스템 적용 중...</p>";
        content.style.opacity = '0.3';
        content.style.pointerEvents = 'none';

        setTimeout(() => {
            overlay.innerHTML = "<div>메신저를 확인하세요.</div>";
            if (stage < 2) {
                playStage(stage + 1);
            } else {
                showReport();
            }
        }, 2000);
    }

    function showReport() {
        const rScreen = document.getElementById('report-screen');
        rScreen.style.display = 'block';
        
        // Analyze final code
        const finalCode = deployedCodes[2] || "";
        let resultType = "Balanced";
        if(finalCode.includes("Shield") || finalCode.includes("Rest")) resultType = "Human-Centric";
        else if(finalCode.includes("Speed")) resultType = "Efficiency-First";

        const content = document.getElementById('report-content');
        content.innerHTML = `
            <div class="stat-card" style="margin-bottom:20px; border-left:5px solid #ce9178; padding:20px; background:#333;">
                <h3>Step 1: CEO의 압박</h3>
                <p>당신은 효율성을 요구받았습니다.</p>
            </div>
            <div class="stat-card" style="margin-bottom:20px; border-left:5px solid #9cdcfe; padding:20px; background:#333;">
                <h3>Step 3: 현장의 호소</h3>
                <p>당신은 상담원의 고통을 마주했습니다.</p>
            </div>
            <div style="background:#252526; padding:20px; border-radius:8px; text-align:center;">
                <h2>최종 설계 성향: <span style="color:#4ec9b0">${resultType}</span></h2>
                <p style="color:#aaa;">"엔지니어의 코드는 누군가의 삶이 됩니다."</p>
            </div>
        `;
    }

</script>
</body>
</html>
\"\"\"

components.html(html_code, height=950, scrolling=False)
"""
with open(os.path.join(project_dir, "app.py"), "w", encoding="utf-8") as f:
    f.write(app_code)

print(f"✅ V6.3 생성 완료: {project_dir}")
print("1. cd invisible_engineer_v6_3")
print("2. streamlit run app.py")
