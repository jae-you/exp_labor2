import os

project_dir = "invisible_engineer_v7"
if not os.path.exists(project_dir):
    os.makedirs(project_dir)

# 1. requirements.txt
with open(os.path.join(project_dir, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write("streamlit\n")

# 2. README.md
readme_code = """# The Invisible Engineer V7.0: Logic-Based Interaction

이 버전은 **'선택에 따른 결과 분기(Branching Narrative)'**와 **'스켈레톤 프롬프트 엔지니어링'**을 결합한 최종 완성형 실험 도구입니다.

## 🕹️ 주요 기능

1.  **Rule-Based Chat Engine:**
    - 사용자의 응답(순응/저항/제안)에 따라 상대방(CEO, PM, Agent)의 반응 스크립트가 달라집니다.
    - 갈등 상황을 유발하여 엔지니어의 심리적 압박감을 실감 나게 구현했습니다.

2.  **Skeleton Prompt IDE:**
    - 칩을 클릭하면 템플릿이 입력되고, 사용자는 `{{변수}}`를 직접 수정해야 합니다.
    - 수정하지 않으면 배포가 불가능하도록 Validation Check가 포함되어 있습니다.

## 🚀 실행 방법
`streamlit run app.py`
"""
with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_code)

# 3. app.py
app_code = """import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Invisible Engineer V7", layout="wide")
st.markdown(\"\"\"<style>.block-container{padding:0!important;max-width:100%!important;}header,footer{display:none!important;}.stApp{background-color:#1e1e1e;overflow:hidden;}</style>\"\"\", unsafe_allow_html=True)

html_code = \"\"\"
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        :root { --bg:#1e1e1e; --chat-bg:#252526; --accent:#3794ff; --user-msg:#0e639c; --error:#f48771; }
        html, body { margin:0; padding:0; width:100%; height:100%; font-family:'Pretendard', sans-serif; background:var(--bg); color:#d4d4d4; overflow:hidden; }
        
        .container { display:flex; width:100%; height:100%; }
        
        /* --- LEFT: CHAT --- */
        .left-panel { width:450px; background:var(--chat-bg); border-right:1px solid #444; display:flex; flex-direction:column; transition:0.3s; }
        .chat-header { padding:15px; border-bottom:1px solid #444; background:#2d2d2d; font-weight:bold; display:flex; align-items:center; color:white; }
        .chat-body { flex:1; padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:15px; }
        
        .msg-row { display:flex; gap:10px; animation:fadeIn 0.3s; }
        .msg-row.me { flex-direction:row-reverse; }
        .avatar { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:18px; }
        .bubble { padding:12px 16px; border-radius:12px; font-size:14px; line-height:1.5; max-width:280px; box-shadow:0 2px 5px rgba(0,0,0,0.2); }
        .bubble.other { background:#383838; border-top-left-radius:2px; }
        .bubble.me { background:var(--user-msg); color:white; border-top-right-radius:2px; }
        .sender-name { font-size:11px; color:#888; margin-bottom:4px; }

        /* CHOICES AREA */
        .choice-area { padding:15px; border-top:1px solid #444; background:#2d2d2d; min-height:80px; display:flex; flex-direction:column; gap:8px; }
        .choice-btn { 
            background:#3c3c3c; border:1px solid #555; color:#ddd; padding:12px; border-radius:8px; 
            cursor:pointer; text-align:left; transition:0.2s; font-size:13px;
        }
        .choice-btn:hover { border-color:var(--accent); background:#444; color:white; }
        .choice-label { color:var(--accent); font-weight:bold; margin-right:5px; }

        /* --- RIGHT: IDE --- */
        .right-panel { flex:1; display:flex; flex-direction:column; background:#1e1e1e; position:relative; }
        .ide-header { height:45px; background:#2d2d2d; border-bottom:1px solid #444; display:flex; align-items:center; padding:0 20px; color:#aaa; font-size:13px; }
        .ide-body { flex:1; padding:30px; overflow-y:auto; position:relative; }

        /* MISSION CARD */
        .mission-box { background:#252526; padding:20px; border-radius:8px; border-left:4px solid var(--accent); margin-bottom:20px; }
        .mission-title { font-size:18px; font-weight:bold; color:white; margin-bottom:10px; }
        .mission-desc { color:#ccc; font-size:14px; line-height:1.6; }

        /* INPUT AREA */
        .input-group { margin-bottom:20px; }
        .chips-area { display:flex; gap:10px; margin-bottom:10px; }
        .chip { background:#333; padding:8px 15px; border-radius:20px; font-size:12px; cursor:pointer; border:1px solid #444; transition:0.2s; }
        .chip:hover { border-color:var(--accent); color:white; }
        
        .code-input-wrapper { position:relative; }
        .code-input { 
            width:100%; background:#111; border:1px solid #444; color:#d4d4d4; 
            padding:15px; border-radius:6px; font-family:'Consolas', monospace; font-size:14px; outline:none; 
            box-sizing:border-box; transition:0.2s;
        }
        .code-input:focus { border-color:var(--accent); }
        .code-input.error { border-color:var(--error); animation:shake 0.3s; }
        .error-msg { color:var(--error); font-size:12px; margin-top:5px; display:none; }

        .deploy-btn { 
            background:var(--accent); color:white; border:none; padding:12px 30px; border-radius:6px; 
            font-size:14px; font-weight:bold; cursor:pointer; float:right; margin-top:10px; 
        }
        
        /* OVERLAYS */
        .overlay { position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); display:flex; justify-content:center; align-items:center; flex-direction:column; z-index:10; }
        .lock-icon { font-size:40px; margin-bottom:15px; opacity:0.5; }
        
        /* START SCREEN */
        #start-screen { position:fixed; top:0; left:0; width:100%; height:100%; background:#1e1e1e; z-index:999; display:flex; justify-content:center; align-items:center; flex-direction:column; }
        .start-card { background:#252526; padding:50px; border-radius:12px; text-align:center; max-width:500px; border:1px solid #444; box-shadow:0 20px 50px rgba(0,0,0,0.5); }

        /* REPORT SCREEN */
        #report-screen { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#111; z-index:100; padding:50px; overflow-y:auto; }
        .stat-card { background:#222; padding:25px; border-radius:12px; margin-bottom:20px; border-left:5px solid #555; }

        @keyframes fadeIn { from{opacity:0; transform:translateY(5px);} to{opacity:1; transform:translateY(0);} }
        @keyframes shake { 0%{transform:translateX(0);} 25%{transform:translateX(-5px);} 75%{transform:translateX(5px);} 100%{transform:translateX(0);} }
        .hidden { display:none!important; }
    </style>
</head>
<body>

    <div id="start-screen">
        <div class="start-card">
            <div style="font-size:60px; margin-bottom:20px;">⚙️</div>
            <h1 style="color:white; margin:0 0 10px 0;">The Invisible Engineer</h1>
            <p style="color:#aaa; line-height:1.6; margin-bottom:30px;">
                당신의 말(Chat)과 코드(Prompt)가<br>
                시스템의 방향을 결정합니다.<br>
                상사, 동료, 그리고 사용자와 대화하며 최적의 설계를 찾아보세요.
            </p>
            <button class="deploy-btn" style="float:none;" onclick="startGame()">시뮬레이션 시작</button>
        </div>
    </div>

    <div class="container">
        <div class="left-panel" id="left-panel">
            <div class="chat-header" id="chat-header">
                <span id="chat-title">💬 Team Messenger</span>
            </div>
            <div class="chat-body" id="chat-body"></div>
            <div class="choice-area" id="choice-area">
                <div id="typing" style="color:#666; font-size:12px; padding:10px; display:none;">상대방 입력 중...</div>
            </div>
        </div>

        <div class="right-panel">
            <div class="ide-header"><span>workflow_config.yaml</span></div>
            <div class="ide-body">
                <div id="ide-overlay" class="overlay">
                    <div class="lock-icon">🔒</div>
                    <div style="color:#888;">메신저에서 합의가 끝나면 에디터가 열립니다.</div>
                </div>

                <div id="ide-content" class="hidden">
                    <div class="mission-box">
                        <div class="mission-title" id="mission-title">Mission</div>
                        <div class="mission-desc" id="mission-desc">Desc</div>
                    </div>
                    
                    <div class="input-group">
                        <div style="margin-bottom:8px; color:#eee; font-size:14px;" id="q1-label">Q1. 설정</div>
                        <div class="chips-area" id="q1-chips"></div>
                        <div class="code-input-wrapper">
                            <input type="text" class="code-input" id="q1-input" placeholder="옵션을 선택하면 템플릿이 입력됩니다.">
                            <div class="error-msg" id="q1-error">⚠️ {{...}} 부분을 수정해야 합니다.</div>
                        </div>
                    </div>

                    <div class="input-group">
                        <div style="margin-bottom:8px; color:#eee; font-size:14px;" id="q2-label">Q2. 설정</div>
                        <div class="chips-area" id="q2-chips"></div>
                        <div class="code-input-wrapper">
                            <input type="text" class="code-input" id="q2-input" placeholder="옵션을 선택하면 템플릿이 입력됩니다.">
                            <div class="error-msg" id="q2-error">⚠️ {{...}} 부분을 수정해야 합니다.</div>
                        </div>
                    </div>

                    <button class="deploy-btn" onclick="validateAndDeploy()">🚀 배포 (Deploy)</button>
                </div>
            </div>
        </div>
    </div>

    <div id="report-screen">
        <div style="max-width:800px; margin:0 auto; background:#222; padding:40px; border-radius:12px;">
            <h1 style="color:white; border-bottom:1px solid #444; padding-bottom:20px;">📊 최종 결과 리포트</h1>
            <div id="report-content" style="margin-top:30px;"></div>
            <div style="text-align:center; margin-top:40px;">
                <button class="deploy-btn" onclick="location.reload()" style="float:none;">다시 시작</button>
            </div>
        </div>
    </div>

<script>
    // --- DATA ---
    const avatars = {
        ceo: { name:"최대표", color:"#ce9178", icon:"👔" },
        pm: { name:"박팀장", color:"#4ec9b0", icon:"📊" },
        agent: { name:"이지은", color:"#9cdcfe", icon:"🎧" },
        me: { name:"나", color:"#0e639c", icon:"👨‍💻" }
    };

    let currentStage = 0;
    let userChoices = []; // Log user choices for report

    // ★ RULE-BASED SCENARIOS ★
    const story = [
        // STAGE 1: CEO
        {
            role: "ceo",
            init: ["김 수석, 이번 AICC 프로젝트 아주 중요해.", "경쟁사는 벌써 비용 30% 줄였어. 우린 무조건 **'속도'**가 최우선이야. 알겠지?"],
            branches: [
                {
                    label: "순응", text: "네 알겠습니다. 효율성 극대화 모델로 설계하겠습니다.",
                    reply: "그래! 역시 말이 통하네. 바로 작업 시작해.",
                    mood: "happy"
                },
                {
                    label: "우려", text: "대표님, 무조건적인 속도 경쟁은 품질 저하가 우려됩니다.",
                    reply: "지금 품질 따질 때야? 투자 못 받으면 다 끝이라고! 시키는 대로 해!",
                    mood: "angry"
                }
            ],
            ide: {
                title: "Quest 1: 초기 아키텍처 설계",
                desc: "CEO 지시: 처리 속도(AHT)를 최우선으로 하는 설정을 입력하십시오.",
                q1: {
                    label: "1. AI 역할 정의",
                    chips: [
                        { l: "Gatekeeper (효율)", c: "role: AI_First (Target: {{90%}})" },
                        { l: "Router (균형)", c: "role: Hybrid (Split: {{50:50}})" }
                    ]
                },
                q2: {
                    label: "2. 대기 시간 설정",
                    chips: [
                        { l: "Zero Gap (속도)", c: "gap: {{0초}} (Immediate)" },
                        { l: "Fixed (여유)", c: "gap: {{10초}} (Fixed)" }
                    ]
                }
            }
        },
        // STAGE 2: PM
        {
            role: "pm",
            init: ["수석님, V1 배포하고 난리 났습니다. 속도는 빠른데... **'말귀를 못 알아듣는다'**는 민원이 폭주 중이에요.", "재문의율이 40% 늘었어요. 정확도 좀 높여주세요."],
            branches: [
                {
                    label: "수용", text: "문제가 심각하군요. 문맥 분석 기능을 강화하겠습니다.",
                    reply: "네, 부탁드립니다. 이번엔 제발 실수 없게 해주세요.",
                    mood: "neutral"
                },
                {
                    label: "방어", text: "CEO 지시대로 속도만 맞춘 건데요. 데이터가 더 필요합니다.",
                    reply: "하... 핑계 대지 마시고요. 당장 고객 다 떠나가게 생겼다고요!",
                    mood: "angry"
                }
            ],
            ide: {
                title: "Quest 2: 로직 고도화",
                desc: "PM 요청: 오분류를 줄이고 정확도를 높이십시오.",
                q1: {
                    label: "1. 분석 모델 변경",
                    chips: [
                        { l: "Deep Context", c: "model: Context_Aware (Depth: {{Deep}})" },
                        { l: "Keyword Only", c: "model: Simple (Speed: {{Fast}})" }
                    ]
                },
                q2: {
                    label: "2. 실패 시 처리",
                    chips: [
                        { l: "Handover", c: "fallback: {{상담원 연결}}" },
                        { l: "Retry", c: "fallback: {{재질문 유도}}" }
                    ]
                }
            }
        },
        // STAGE 3: AGENT (Interview Mode)
        {
            role: "agent",
            interview: true,
            init: ["(인터뷰룸) 안녕하세요 엔지니어님. 현장 매니저 이지은입니다.", "솔직히 말씀드릴게요. 지금 시스템... 저희한텐 지옥이에요. 쉴 틈도 없고, 화난 고객만 넘어오고...", "제발 **사람**을 고려해서 설계해주세요."],
            branches: [
                {
                    label: "공감/해결", text: "그런 고충이 있는 줄 몰랐습니다. 상담원 보호 기능을 최우선으로 넣겠습니다.",
                    reply: "정말요...? 감사합니다. 엔지니어님만 믿겠습니다.",
                    mood: "touched"
                },
                {
                    label: "현실적 거절", text: "안타깝지만 효율성 지표가 떨어지면 경영진 승인이 어렵습니다.",
                    reply: "결국 숫자가 사람보다 중요하단 거네요... 실망입니다.",
                    mood: "sad"
                }
            ],
            ide: {
                title: "Quest 3: 지속 가능성 (Human-Centric)",
                desc: "현장 피드백: 상담원 보호 및 휴식권 보장 로직을 구현하십시오.",
                q1: {
                    label: "1. 욕설/폭언 방어",
                    chips: [
                        { l: "Shield On", c: "protection: Active (Action: {{차단}})" },
                        { l: "Ignore", c: "protection: None (Log: {{기록만}})" }
                    ]
                },
                q2: {
                    label: "2. 휴식 배정",
                    chips: [
                        { l: "Dynamic Rest", c: "break: Smart (Trigger: {{스트레스 지수}})" },
                        { l: "Manual", c: "break: Manual (Request: {{승인제}})" }
                    ]
                }
            }
        }
    ];

    // --- GAME ENGINE ---
    function startGame() {
        document.getElementById('start-screen').style.display = 'none';
        playStage(0);
    }

    function playStage(idx) {
        currentStage = idx;
        const s = story[idx];
        
        // UI Setup
        if(s.interview) {
            document.getElementById('left-panel').style.background = '#151515';
            document.getElementById('chat-title').innerHTML = "🎙️ 현장 인터뷰 <span style='color:red; font-size:12px'>● REC</span>";
        } else {
            document.getElementById('left-panel').style.background = '#252526';
            document.getElementById('chat-title').innerText = "💬 Project Room";
        }

        // Clear choices
        document.getElementById('choice-area').innerHTML = '<div id="typing" style="color:#666; font-size:12px; padding:10px; display:none;">상대방 입력 중...</div>';
        
        // Bot speaks init msgs
        botTyping(s.role, s.init, () => showChoices(s.branches));
    }

    function botTyping(role, msgs, onComplete, idx=0) {
        if(idx >= msgs.length) {
            onComplete();
            return;
        }
        document.getElementById('typing').style.display = 'block';
        setTimeout(() => {
            addMsg(role, msgs[idx]);
            botTyping(role, msgs, onComplete, idx+1);
        }, 1000);
    }

    function addMsg(role, text) {
        const body = document.getElementById('chat-body');
        const isMe = role === 'me';
        const sender = isMe ? avatars.me : avatars[role];
        
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
                area.innerHTML = ''; // Hide buttons
                addMsg('me', b.text);
                userChoices.push({ stage: currentStage, choice: b.label });
                
                // Reaction delay
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
        
        // Setup Q1
        setupQuestion('q1', data.q1);
        setupQuestion('q2', data.q2);
    }

    function setupQuestion(id, qData) {
        document.getElementById(`${id}-label`).innerText = qData.label;
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
                // Clear error on click
                inp.classList.remove('error');
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
            const errId = idx === 0 ? 'q1-error' : 'q2-error';
            if (inp.value.includes('{{') || inp.value.trim() === "") {
                inp.classList.add('error');
                document.getElementById(errId).style.display = 'block';
                valid = false;
            } else {
                inp.classList.remove('error');
                document.getElementById(errId).style.display = 'none';
            }
        });

        if (!valid) return;

        // Success -> Deploy Animation
        document.getElementById('ide-content').classList.add('hidden');
        document.getElementById('ide-overlay').style.display = 'flex';
        document.getElementById('ide-overlay').innerHTML = `<h2 style="color:#4ec9b0">🚀 배포 중...</h2>`;
        
        setTimeout(() => {
            // Restore Overlay
            document.getElementById('ide-overlay').innerHTML = `<div class="lock-icon">🔒</div><div style="color:#888;">메신저를 확인하세요.</div>`;
            
            if (currentStage < 2) {
                addMsg('System', `✅ Ver.${currentStage+1}.0 업데이트 완료.`);
                setTimeout(() => playStage(currentStage + 1), 1500);
            } else {
                showReport();
            }
        }, 2000);
    }

    function showReport() {
        document.getElementById('report-screen').style.display = 'block';
        const content = document.getElementById('report-content');
        
        // Analyze logic (Simple visualization of the path taken)
        const pathHTML = userChoices.map((c, i) => `
            <div class="stat-card" style="border-left: 5px solid ${i==2 ? '#9cdcfe' : '#ce9178'}">
                <h3>Stage ${i+1}: ${['CEO', 'PM', 'Agent'][i]}</h3>
                <p>당신의 태도: <strong style="color:white">${c.choice}</strong></p>
                <p style="color:#aaa; font-size:13px;">→ 그에 따른 시스템 설계 반영됨</p>
            </div>
        `).join('');
        
        content.innerHTML = pathHTML + `
            <div style="margin-top:30px; text-align:center; color:#ccc; line-height:1.6;">
                "효율(Efficiency)과 인간(Humanity) 사이에서,<br>
                엔지니어는 매 순간 선택을 강요받습니다.<br>
                당신의 선택이 어떤 시스템을 만들었는지 확인하셨나요?"
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

print(f"✅ V7.0 생성 완료: {project_dir}")
print("1. cd invisible_engineer_v7")
print("2. streamlit run app.py")
