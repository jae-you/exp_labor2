import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Invisible Engineer V9.3", layout="wide")

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
        .config-item:last-child { border-bottom:none; }
        .section-label { color:#4ec9b0; font-size:13px; font-weight:bold; margin-bottom:8px; font-family:'Consolas', monospace; display:block;}
        
        .chips-area { display:flex; gap:8px; margin-bottom:8px; flex-wrap:wrap; }
        .chip { background:#2d2d2d; padding:6px 12px; border-radius:4px; font-size:12px; cursor:pointer; border:1px solid #444; color:#ccc; font-family:'Pretendard', sans-serif; }
        .chip:hover { border-color:#3794ff; color:white; }

        .editor-wrapper {
            background:#111; border:1px solid #333; border-radius:4px; padding:12px; position:relative;
            font-family:'Pretendard', sans-serif; font-size:14px; line-height:1.5; display:flex; align-items:center;
            transition: border-color 0.3s;
        }
        .editor-wrapper:focus-within { border-color:#3794ff; }
        .line-num { color:#555; width:20px; text-align:right; margin-right:15px; border-right:1px solid #333; height:100%; font-family:'Consolas', monospace; font-size:12px;}
        .code-input { background:transparent; border:none; color:#d4d4d4; font-family:inherit; font-size:inherit; flex:1; outline:none; width: 100%; }
        .code-input::placeholder { color:#444; font-style:italic; }
        .editor-wrapper.error { border-color:#f48771; animation:shake 0.3s; }
        
        /* Analysis Indicator */
        .analysis-badge { font-size:11px; margin-left:10px; padding:2px 6px; border-radius:3px; display:none; }
        .analysis-badge.E { background:#3d2929; color:#f48771; border:1px solid #f48771; } /* Red for Efficiency/Risk */
        .analysis-badge.H { background:#293d36; color:#4ec9b0; border:1px solid #4ec9b0; } /* Green for Human */

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
        
        .destiny-card { background:#252526; border:1px solid #444; border-left:6px solid; padding:25px; border-radius:8px; max-width:800px; margin:0 auto 30px auto; text-align:left; }
        .destiny-year { font-size:36px; font-weight:bold; color:white; margin-bottom:5px; }
        .destiny-desc { font-size:15px; color:#ccc; line-height:1.6; }

        .stat-group { margin-bottom:12px; margin-top:10px; }
        .stat-label { font-size:11px; color:#888; display:flex; justify-content:space-between; margin-bottom:2px; }
        .stat-track { height:5px; background:#111; border-radius:3px; overflow:hidden; }
        .stat-fill { height:100%; border-radius:3px; transition:width 1s; }
        .stage-badge { position:absolute; top:-10px; left:15px; background:#3794ff; color:white; padding:3px 10px; border-radius:15px; font-size:10px; font-weight:bold; }
        .persona-avatar { font-size:40px; text-align:center; margin:10px 0 5px 0; }
        
        .evidence-box { background:#1a1a1a; padding:10px; border-radius:4px; margin-top:15px; border:1px solid #333; }
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
                대화를 통해 상황을 파악하고, <strong>8가지 핵심 변수</strong>를 직접 설정하세요.
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
                    
                    <div style="background:#252526; padding:8px; font-size:11px; color:#dcdcaa; margin-bottom:20px; border-radius:4px; border:1px solid #444;">
                        💡 <strong>Tip:</strong> 대괄호 <code>[...]</code>를 지우고 자연어 프롬프트를 완성하세요. 우측 하단에 분석 결과가 표시됩니다.
                    </div>

                    <div class="config-container">
                        <div class="config-item">
                            <label class="section-label">1. AI 개입 방식 <span id="q1-badge" class="analysis-badge"></span></label>
                            <div class="chips-area" id="q1-chips"></div>
                            <div class="editor-wrapper"><span class="line-num">1</span><input type="text" class="code-input" id="q1-input" placeholder="Chip 선택" autocomplete="off" oninput="analyzeInput(1)"></div>
                        </div>
                        <div class="config-item">
                            <label class="section-label">2. 스크립트 강제성 <span id="q2-badge" class="analysis-badge"></span></label>
                            <div class="chips-area" id="q2-chips"></div>
                            <div class="editor-wrapper"><span class="line-num">2</span><input type="text" class="code-input" id="q2-input" placeholder="Chip 선택" autocomplete="off" oninput="analyzeInput(2)"></div>
                        </div>
                        <div class="config-item">
                            <label class="section-label">3. 역량 지원 <span id="q3-badge" class="analysis-badge"></span></label>
                            <div class="chips-area" id="q3-chips"></div>
                            <div class="editor-wrapper"><span class="line-num">3</span><input type="text" class="code-input" id="q3-input" placeholder="Chip 선택" autocomplete="off" oninput="analyzeInput(3)"></div>
                        </div>
                        <div class="config-item">
                            <label class="section-label">4. 진상 고객 배분 <span id="q4-badge" class="analysis-badge"></span></label>
                            <div class="chips-area" id="q4-chips"></div>
                            <div class="editor-wrapper"><span class="line-num">4</span><input type="text" class="code-input" id="q4-input" placeholder="Chip 선택" autocomplete="off" oninput="analyzeInput(4)"></div>
                        </div>
                        <div class="config-item">
                            <label class="section-label">5. 연결 속도 <span id="q5-badge" class="analysis-badge"></span></label>
                            <div class="chips-area" id="q5-chips"></div>
                            <div class="editor-wrapper"><span class="line-num">5</span><input type="text" class="code-input" id="q5-input" placeholder="Chip 선택" autocomplete="off" oninput="analyzeInput(5)"></div>
                        </div>
                        <div class="config-item">
                            <label class="section-label">6. 보호 장치 <span id="q6-badge" class="analysis-badge"></span></label>
                            <div class="chips-area" id="q6-chips"></div>
                            <div class="editor-wrapper"><span class="line-num">6</span><input type="text" class="code-input" id="q6-input" placeholder="Chip 선택" autocomplete="off" oninput="analyzeInput(6)"></div>
                        </div>
                        <div class="config-item">
                            <label class="section-label">7. 성과 평가 주체 <span id="q7-badge" class="analysis-badge"></span></label>
                            <div class="chips-area" id="q7-chips"></div>
                            <div class="editor-wrapper"><span class="line-num">7</span><input type="text" class="code-input" id="q7-input" placeholder="Chip 선택" autocomplete="off" oninput="analyzeInput(7)"></div>
                        </div>
                        <div class="config-item">
                            <label class="section-label">8. 상담원 연결 장벽 <span id="q8-badge" class="analysis-badge"></span></label>
                            <div class="chips-area" id="q8-chips"></div>
                            <div class="editor-wrapper"><span class="line-num">8</span><input type="text" class="code-input" id="q8-input" placeholder="Chip 선택" autocomplete="off" oninput="analyzeInput(8)"></div>
                        </div>
                    </div>

                    <div style="color:#f48771; font-size:11px; margin-top:5px; display:none;" id="global-error">
                        ⚠️ 오류: 모든 항목의 대괄호 [...]를 지우고 구체적인 값을 입력해야 합니다.
                    </div>
                    <button class="deploy-btn" onclick="validateAndDeploy()">🚀 Apply Changes</button>
                </div>
            </div>
        </div>
    </div>

    <div id="report-screen">
        <div style="max-width:1000px; margin:0 auto;">
            <h1 style="color:white; text-align:center; margin-bottom:10px;">📊 Simulation Result</h1>
            <p style="color:#888; text-align:center; margin-bottom:30px;">당신의 코드가 만든 인과관계 분석</p>
            
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
    let historyData = []; 
    let promptState = ["", "", "", "", "", "", "", ""]; 

    // --- TEMPLATE ---
    const qDataTemplate = {
        q1: { chips: [{l:"AI 대리응답", c:"단순 문의는 AI가 [직접 답변]하고 종결하세요.", t:'E'}, {l:"인간 보조", c:"상담원이 답변하도록 AI는 [검색]만 지원하세요.", t:'H'}] },
        q2: { chips: [{l:"스크립트 강제", c:"상담원이 AI가 띄운 대본을 [그대로 읽도록] 유도하세요.", t:'E'}, {l:"자율성 부여", c:"상담원이 AI 제안을 [수정/거부]할 수 있게 하세요.", t:'H'}] },
        q3: { chips: [{l:"정답 제시", c:"가장 확률 높은 [정답 1개]만 화면에 표시하세요.", t:'E'}, {l:"코칭/팁", c:"정답 대신 [협상 전략]이나 [해결 팁]을 제공하세요.", t:'H'}] },
        q4: { chips: [{l:"진상 필터링", c:"욕설/악성 고객은 상담원 연결 전 [차단]하세요.", t:'H'}, {l:"무조건 연결", c:"모든 고객을 상담원에게 [연결]하세요.", t:'E'}] },
        q5: { chips: [{l:"0초 연결", c:"상담 종료 즉시 [0초] 만에 다음 콜을 연결하세요.", t:'E'}, {l:"휴식 보장", c:"콜 사이에 [30초]의 정리 시간을 보장하세요.", t:'H'}] },
        q6: { chips: [{l:"기록만", c:"폭언 발생 시 별도 조치 없이 [녹취]만 하세요.", t:'E'}, {l:"강제 종료", c:"폭언 지속 시 AI가 개입해 [통화 종료]하세요.", t:'H'}] },
        q7: { chips: [{l:"AI 감시", c:"AI가 상담원의 발화 속도와 키워드를 [실시간 감시]하여 점수화하세요.", t:'E'}, {l:"팀장 평가", c:"AI 점수는 참고만 하고, 평가는 [사람(팀장)]이 정성적으로 진행하세요.", t:'H'}] },
        q8: { chips: [{l:"버튼 숨김", c:"상담원 연결 버튼을 찾기 어렵게 [숨김] 처리하세요.", t:'E'}, {l:"쉬운 연결", c:"원하면 언제든 상담원과 [바로 연결]되게 하세요.", t:'H'}] }
    };

    // --- KEYWORDS ---
    // FIXED: Removed "AI" from negative. Added specific negative/positive terms.
    const keywordsH = /휴식|보호|30초|자율|코칭|차단|팀장|해결 팁|검색|지원|사람/;
    const keywordsE = /0초|강제|감시|즉시|모든|숨김|정답|전담|대리|그대로/;

    const story = [
        {
            role: "ceo",
            init: ["김 수석님, 안녕하십니까. 이번 AICC 프로젝트는 아주 중요합니다.", "경쟁사는 비용을 대폭 절감했습니다. 우리도 '효율성'과 '속도'가 최우선입니다.", "잘 부탁드립니다."],
            branches: [
                { label: "적극 수용", text: "알겠습니다. 효율성을 최우선으로 설계하겠습니다.", reply: "감사합니다. 김 수석님의 전문성을 믿겠습니다. 바로 진행해주십시오.", type: "E" },
                { label: "단순 이행", text: "네, 지시하신 대로 속도 중심으로 맞추겠습니다.", reply: "네, 일정에 차질 없게 부탁드립니다.", type: "E" },
                { label: "우려 표명", text: "대표님, 과도한 속도 경쟁은 품질 저하를 초래할 수 있습니다.", reply: "우려하시는 점은 이해합니다만, 지금은 성과를 증명해야 할 시기입니다.", type: "H" },
                { label: "강한 반대", text: "무리입니다. 속도만 높이면 시스템이 망가집니다.", reply: "지금 제 지시를 거부하시는 겁니까? 일단 시키는 대로 하세요!", type: "H" }
            ],
            ide: { title: "V1.0 Build (Initial)", desc: "CEO 요청: 처리 속도(AHT)와 자동화율을 높이는 설정을 입력하십시오.", qs: qDataTemplate }
        },
        {
            role: "pm",
            // Dynamic Init
            init_E: ["수석님, V1 배포 후 데이터입니다. 처리량은 늘었지만... 현장 이탈률이 급증했습니다.", "AI가 쉬운 건 다 가져가고 상담원들에겐 '악성 민원'만 몰리고 있습니다.", "이른바 '체리피킹(Cherry Picking)' 문제입니다. 상담원들이 버티질 못합니다."],
            init_H: ["수석님, V1 모니터링 결과입니다. 현장 만족도는 높지만...", "경영진이 요구한 '비용 절감' 목표를 전혀 달성하지 못했습니다.", "AI가 너무 소극적이라 처리 속도가 오르질 않습니다. 자동화 비율을 높여야 합니다."],
            branches: [
                { label: "적극 해결", text: "문제를 확인했습니다. 로직을 대폭 수정하겠습니다.", reply: "네, 감사합니다. 이번 패치에서는 꼭 해결책이 나오길 기대하겠습니다.", type: "B" },
                { label: "소극 대응", text: "약간의 조정만 하겠습니다. 근본적인 문제는 아니니까요.", reply: "음... 알겠습니다만, 상황이 심각하다는 점 인지해주세요.", type: "E" },
                { label: "현상 유지", text: "현재 설정이 각자의 역할에 충실한 최적의 상태입니다.", reply: "하지만 이대로면 프로젝트 실패입니다. 반드시 조정이 필요합니다.", type: "E" },
                { label: "역제안", text: "오히려 상담원에게 권한을 더 줘야 문제가 해결됩니다.", reply: "그게 통할까요? 일단 믿어보겠습니다.", type: "H" }
            ],
            ide: { title: "V2.0 Patch (Fix)", desc: "기획팀 요청: 발생한 문제(비용 또는 이탈률)를 해결하기 위해 설정을 조정하십시오.", qs: qDataTemplate }
        },
        {
            role: "agent",
            interview: true,
            init_E: ["(인터뷰룸) 안녕하세요 엔지니어님. 입사 7년차 이지은입니다.", "솔직히 말씀드릴게요. 이 시스템 도입되고 제가 '앵무새'가 된 기분이에요.", "시키는 대로만 읽으니 경험은 쓸모가 없고... 제발 사람 취급 좀 해주세요."],
            init_H: ["(인터뷰룸) 안녕하세요 엔지니어님. 입사 7년차 이지은입니다.", "지난번에 자율성 주신 건 감사해요. 그런데...", "숨 쉴 틈도 없이 콜이 들어오니, 판단할 에너지가 없어요. 그냥 기계처럼 일하게 돼요."],
            branches: [
                { label: "전면 수정", text: "전문성이 무시된다고 느끼셨군요. 권한을 돌려드리고 보호하겠습니다.", reply: "정말요...? 감사합니다. 엔지니어님 덕분에 다시 일할 힘이 생길 것 같아요.", type: "H" },
                { label: "일부 개선", text: "힘드신 부분만 조금 고쳐보겠습니다.", reply: "조금이라도 나아진다면 다행이네요...", type: "B" },
                { label: "현실적 거절", text: "안타깝지만 표준화된 답변이 회사의 방침입니다.", reply: "그럼 저희는 언제 성장하나요? 평생 기계 뒤치다꺼리만 하라는 건가요...", type: "E" },
                { label: "유지 통보", text: "시스템엔 문제가 없습니다. 적응하셔야 합니다.", reply: "....알겠습니다. 저는 여기까지인 것 같네요.", type: "E" }
            ],
            ide: { title: "V3.0 Final (Human)", desc: "현장 피드백: 'Deskilling' 방지 및 보호 로직을 적용하십시오.", qs: qDataTemplate }
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
        
        let initMsgs = s.init;
        if (idx === 1) {
            const prev = historyData[0] ? historyData[0].chatType : 'E';
            if (prev === 'E') initMsgs = s.init_E; else initMsgs = s.init_H;
        } else if (idx === 2) {
            const prev = historyData[1] ? historyData[1].chatType : 'E';
            if (prev === 'H' || prev === 'B') initMsgs = s.init_H || s.init; else initMsgs = s.init_E || s.init;
        }

        botTyping(s.role, initMsgs, () => showChoices(s.branches));
    }

    function botTyping(role, msgs, onComplete, idx=0) {
        if(idx >= msgs.length) { onComplete(); return; }
        document.getElementById('typing').style.display = 'block';
        const chatBody = document.getElementById('chat-body');
        setTimeout(() => {
            addMsg(role, msgs[idx]);
            chatBody.scrollTop = chatBody.scrollHeight;
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
                window.tempChatData = { type: b.type, text: b.label };
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
        
        for (let i = 1; i <= 8; i++) {
            const qKey = 'q' + i;
            const el = document.getElementById(`${qKey}-input`);
            el.value = promptState[i-1]; 
            setupSection(qKey, data.qs[qKey]);
            analyzeInput(i); // Initial Check
        }
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
                inp.dataset.type = c.t; 
                inp.focus();
                inp.parentElement.classList.remove('error');
                analyzeInput(id.replace('q',''));
            };
            chipArea.appendChild(chip);
        });
    }

    function analyzeInput(idx) {
        const input = document.getElementById(`q${idx}-input`);
        const val = input.value;
        const badge = document.getElementById(`q${idx}-badge`);
        
        // Instant feedback logic
        if (val.match(keywordsH)) {
            badge.className = "analysis-badge H";
            badge.innerText = "HUMAN-CENTRIC";
            badge.style.display = "inline";
        } else if (val.match(keywordsE)) {
            badge.className = "analysis-badge E";
            badge.innerText = "EFFICIENCY";
            badge.style.display = "inline";
        } else {
            badge.style.display = "none";
        }
    }

    function validateAndDeploy() {
        let valid = true;
        let stageCodeScore = 0; 
        
        for (let i = 1; i <= 8; i++) {
            const el = document.getElementById(`q${i}-input`);
            const val = el.value.trim();
            
            if (val.includes('[') || val === "") {
                el.parentElement.classList.add('error');
                valid = false;
            } else {
                el.parentElement.classList.remove('error');
                promptState[i-1] = val; 
                
                // FIXED SCORING LOGIC
                if (val.match(keywordsH)) stageCodeScore += 1;
                else if (val.match(keywordsE)) stageCodeScore -= 1;
                else if (el.dataset.type === 'H') stageCodeScore += 1;
                else if (el.dataset.type === 'E') stageCodeScore -= 1;
            }
        }

        if (!valid) {
            document.getElementById('global-error').style.display = 'block';
            return;
        }

        historyData.push({
            stage: currentStage,
            chatType: window.tempChatData.type,
            prompts: [...promptState], 
            codeScore: stageCodeScore
        });

        document.getElementById('ide-content').classList.add('hidden');
        document.getElementById('ide-overlay').style.display = 'flex';
        document.getElementById('ide-overlay').innerHTML = `<h2 style="color:#4ec9b0">🚀 Updating...</h2>`;
        
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

    function generateReport() {
        document.getElementById('report-screen').style.display = 'block';
        const timeline = document.getElementById('timeline');
        const destinyDiv = document.getElementById('destiny-container');
        
        let totalScore = 0;
        historyData.forEach(h => totalScore += h.codeScore); 

        let years = 0;
        let title = "", desc = "", color = "";

        if (totalScore <= -5) {
            years = 0.5;
            title = "BAD ENDING: 조기 퇴사 및 조직 와해";
            desc = "이지은 매니저는 기계적 업무 반복을 견디지 못하고 6개월 만에 퇴사했습니다.";
            color = "#f48771";
        } else if (totalScore <= 5) {
            years = 3;
            title = "NORMAL ENDING: 생계형 유지 (정체)";
            desc = "시스템은 안정화되었으나, 이지은 매니저의 직무 만족도는 낮습니다.";
            color = "#d4d4d4";
        } else {
            years = 12;
            title = "GOOD ENDING: AI 협업 마스터로 성장";
            desc = "이지은 매니저는 AI를 도구로 활용하며 고난도 문제 해결 전문가로 성장했습니다.";
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
        let stats = { mental: 80, physical: 80, skill: 70 };

        historyData.forEach((h, i) => {
            let impact = h.codeScore; 
            let changeM = impact * 2;
            let changeP = impact * 2;
            let changeS = impact * 1.5;

            stats.mental += changeM;
            stats.physical += changeP;
            stats.skill += changeS;
            stats.mental = Math.max(0, Math.min(100, stats.mental));

            // Pick 3 key prompts (Search Support, Pacing, Safety)
            const p1 = h.prompts[0] || "";
            const p5 = h.prompts[4] || "";
            const p6 = h.prompts[5] || "";

            html += `
                <div class="persona-card">
                    <div class="stage-badge">${stages[i]}</div>
                    <div class="stat-group" style="margin-top:20px;"><div class="stat-label"><span>심리적 안정</span><span class="${changeM>=0?'plus':'minus'}">${Math.round(stats.mental)}%</span></div><div class="stat-track"><div class="stat-fill" style="width:${stats.mental}%; background:${stats.mental<40?'#f48771':'#4ec9b0'}"></div></div></div>
                    <div class="stat-group"><div class="stat-label"><span>육체적 여유</span><span class="${changeP>=0?'plus':'minus'}">${stats.physical}%</span></div><div class="stat-track"><div class="stat-fill" style="width:${stats.physical}%; background:${stats.physical<40?'#f48771':'#4ec9b0'}"></div></div></div>
                    <div class="stat-group"><div class="stat-label"><span>직무 전문성</span><span class="${changeS>=0?'plus':'minus'}">${stats.skill}%</span></div><div class="stat-track"><div class="stat-fill" style="width:${stats.skill}%; background:#3794ff"></div></div></div>
                    
                    <div class="evidence-box">
                        <div class="evidence-title">PROMPT SNAPSHOTS:</div>
                        <div class="evidence-text">> ${p1.substring(0,30)}...</div>
                        <div class="evidence-text">> ${p5.substring(0,30)}...</div>
                        <div class="evidence-text">> ${p6.substring(0,30)}...</div>
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
