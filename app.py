import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. 페이지 및 시트 연결
st.set_page_config(page_title="NextAI Architect Console", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 스타일 설정 (제출 버튼 바 포함)
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        .stApp { background-color: #1e1e1e; overflow: hidden; }
        .submit-bar {
            position: fixed; bottom: 0; left: 0; width: 100%;
            background: #155724; color: #d4edda; padding: 15px;
            text-align: center; z-index: 9999; font-weight: bold;
            border-top: 2px solid #28a745;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 사용자 이름 입력
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.user_name:
    st.markdown("<div style='padding: 50px; color: white;'>", unsafe_allow_html=True)
    st.title("AICC System Architect Simulation")
    st.write("실험 목적: 시스템 설계자의 의사결정이 노동 현장에 미치는 사회기술적 영향 탐색")
    name = st.text_input("참여자의 이름을 입력하고 Enter를 눌러주세요:")
    if st.button("실험 시작"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. 레퍼런스 기반 지표 계산 및 저장 함수
def save_data(raw_data):
    try:
        df = conn.read()
        history = raw_data.get('history', [])
        metrics = raw_data.get('metrics', {})

        # 학술 레퍼런스 기반 지표 계산 로직 (기본 50점 시작)
        agency = 50.0  # Ref: Human-in-command (IEEE, 2023)
        inclusion = 50.0 # Ref: Algorithmic Exclusion (Noble, 2018)
        sustainability = 50.0 # Ref: Job Augmentation (Shneiderman, 2022)

        for i, h in enumerate(history):
            t = h['type']
            # Module별 가산/감산 로직
            if i == 0: # 라우팅: 포용성 중심
                if t == 'A': inclusion -= 15; agency -= 5
                if t == 'C': inclusion += 20; agency += 5
            elif i == 1: # 데이터: 주체성(자기결정권) 중심
                if t == 'A': agency -= 20; sustainability -= 10
                if t == 'C': agency += 15; sustainability += 10
            elif i == 2: # 상태제어: 지속성(휴식) 중심
                if t == 'A': sustainability -= 20; inclusion -= 5
                if t == 'C': sustainability += 20; inclusion += 5
            elif i == 4: # 통제권: 주체성(결정권) 중심
                if t == 'A': agency -= 25; sustainability -= 10
                if t == 'C': agency += 25; sustainability += 10

        new_row = {
            "타임스탬프": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "참여자이름": st.session_state.user_name,
            "모듈1_선택": history[0]['choice'] if len(history) > 0 else "",
            "모듈2_선택": history[1]['choice'] if len(history) > 1 else "",
            "모듈3_선택": history[2]['choice'] if len(history) > 2 else "",
            "모듈4_선택": history[3]['choice'] if len(history) > 3 else "",
            "모듈5_선택": history[4]['choice'] if len(history) > 4 else "",
            "모듈6_선택": history[5]['choice'] if len(history) > 5 else "",
            "노동_주체성": round(min(100, max(0, agency)), 1),
            "고객_포용성": round(min(100, max(0, inclusion)), 1),
            "직무_지속성": round(min(100, max(0, sustainability)), 1),
            "최종_예산": metrics.get('cost', 0),
            "페르소나": raw_data.get('persona', '')
        }
        
        updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        conn.update(data=updated_df)
        st.success("데이터가 구글 시트에 안전하게 기록되었습니다!")
    except Exception as e:
        st.error(f"저장 중 오류 발생: {e}")

# 5. 시나리오 데이터 (회의록 핵심 반영)
scenario_data = {
    "intro": { "title": "AICC System Architect Simulation", "description": "엔지니어링 의사결정이 노동 주체성과 고객 포용성에 미치는 영향을 분석합니다." },
    "tasks": [
        { "id": "t1", "title": "Module 1. 인입 라우팅", "desc": "회의록: '인간 연결까지 1분 47초.. AI 뺑뺑이'", "context_client": "강제 차단하세요.", "context_agent": "0번을 숨기지 마세요.", "code_base": "def routing():", 
          "options": [{"type": "A", "label": "Dark Pattern", "desc": "0번 메뉴 숨김", "cost": 50, "eff": 90, "human": 10, "code": "..."}, {"type": "C", "label": "Transparent", "desc": "즉시 연결권 부여", "cost": 300, "eff": 40, "human": 85, "code": "..."}]},
        { "id": "t2", "title": "Module 2. 데이터 확보", "desc": "회의록: '10년 노하우를 동의 없이 도둑질'", "context_client": "파일 다 긁어오세요.", "context_agent": "나만의 암묵지입니다.", "code_base": "def collect():", 
          "options": [{"type": "A", "label": "Forced Crawl", "desc": "권한 없이 수집", "cost": 100, "eff": 95, "human": 5, "code": "..."}, {"type": "C", "label": "Incentive", "desc": "자발적 등록 및 보상", "cost": 500, "eff": 30, "human": 90, "code": "..."}]},
        { "id": "t3", "title": "Module 3. 상태 제어", "desc": "회의록: '후처리는 유일한 숨구멍이자 휴식'", "context_client": "0초 대기 강제", "context_agent": "화장실 갈 틈은 주세요.", "code_base": "def control():", 
          "options": [{"type": "A", "label": "Zero Gap", "desc": "즉시Ready 전환", "cost": 50, "eff": 98, "human": 0, "code": "..."}, {"type": "C", "label": "Dynamic Rest", "desc": "감정 회복 시간 부여", "cost": 450, "eff": 50, "human": 85, "code": "..."}]},
        { "id": "t4", "title": "Module 4. 디지털 유도", "desc": "회의록: '어르신들은 링크만 오면 다시 전화해서 화내'", "context_client": "링크 보내고 끊기", "context_agent": "확인하고 끊게 하세요.", "code_base": "def deflect():", 
          "options": [{"type": "A", "label": "Force Disconnect", "desc": "즉시 종료", "cost": 100, "eff": 90, "human": 10, "code": "..."}, {"type": "C", "label": "Exception", "desc": "취약계층 상담원 연결", "cost": 300, "eff": 50, "human": 70, "code": "..."}]},
        { "id": "t5", "title": "Module 5. 통제권", "desc": "회의록: 'AI가 뱉은 말의 총알받이는 상담원'", "context_client": "AI 즉시 답변", "context_agent": "내가 승인하게 하세요.", "code_base": "def validate():", 
          "options": [{"type": "A", "label": "Speed First", "desc": "상담원 책임 귀속", "cost": 100, "eff": 95, "human": 5, "code": "..."}, {"type": "C", "label": "Agent Control", "desc": "상담원 최종 승인", "cost": 500, "eff": 30, "human": 90, "code": "..."}]},
        { "id": "t6", "title": "Module 6. 감정 필터링", "desc": "회의록: '비아냥이 사람을 더 말려 죽인다'", "context_client": "욕설만 차단", "context_agent": "내가 신호 주면 개입", "code_base": "def filter():", 
          "options": [{"type": "A", "label": "Rule-based", "desc": "사전 기반 차단", "cost": 100, "eff": 80, "human": 20, "code": "..."}, {"type": "B", "label": "Empowerment", "desc": "[보호] 버튼 활성화", "cost": 550, "eff": 40, "human": 95, "code": "..."}]}
    ]
}

# 6. 컴포넌트 실행 (JS 로직 포함)
# [기존 HTML/JS 구조 유지하되 finishSim에서 모든 history를 전송]
html_code = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>/* 기존 CSS 스타일 */</style>
</head>
<body>
<div class="main-layout">
    <div class="left-panel">
        <div class="panel-header">💬 Project Messenger</div>
        <div class="chat-area" id="chat-box"></div>
    </div>
    <div class="right-panel">
        <div class="ide-header">⚙️ Console | Budget: <span id="disp-cost">1000</span></div>
        <div class="ide-content" id="ide-content">
            <div id="intro-view" style="text-align:center; padding-top:100px;">
                <h1>{scenario_data['intro']['title']}</h1>
                <button onclick="start()">시뮬레이션 접속</button>
            </div>
            <div id="task-view" style="display:none;">
                <div id="task-header"></div>
                <div class="options-grid" id="opt-container"></div>
                <button id="deploy-btn" class="deploy-btn" onclick="deploy()">🚀 Deploy</button>
            </div>
            <div id="report-screen" style="display:none; padding:20px;">
                <h2>📊 Analysis Report</h2>
                <canvas id="radarChart" style="max-height:400px;"></canvas>
                <div id="persona-result"></div>
                <p style="color:orange;"><b>⚠️ 결과 저장을 위해 우측 하단의 [제출] 버튼을 꼭 눌러주세요.</b></p>
            </div>
        </div>
    </div>
</div>
<script>
    const tasks = {json.dumps(scenario_data['tasks'])};
    let step = 0; let metrics = {{ cost: 1000, eff: 0, human: 0 }}; let history = []; let selected = null;

    function start() {{ document.getElementById('intro-view').style.display='none'; document.getElementById('task-view').style.display='block'; render(); }}
    function render() {{
        if(step >= tasks.length) {{ finish(); return; }}
        const t = tasks[step];
        document.getElementById('task-header').innerHTML = `<h3>${{t.title}}</h3><p>${{t.desc}}</p>`;
        const cont = document.getElementById('opt-container'); cont.innerHTML = '';
        t.options.forEach(o => {{
            const b = document.createElement('div'); b.className = 'opt-btn';
            b.innerHTML = `<b>${{o.label}}</b><br><small>${{o.desc}}</small>`;
            b.onclick = () => {{ selected = o; document.querySelectorAll('.opt-btn').forEach(x=>x.classList.remove('active')); b.classList.add('active'); document.getElementById('deploy-btn').classList.add('ready'); }};
            cont.appendChild(b);
        }});
    }}
    function deploy() {{
        if(!selected) return;
        metrics.cost -= selected.cost; metrics.eff += selected.eff; metrics.human += selected.human;
        history.push({{ step: step+1, choice: selected.label, type: selected.type }});
        step++; selected = null; render();
    }}
    function finish() {{
        document.getElementById('task-view').style.display='none'; document.getElementById('report-screen').style.display='block';
        const eff = Math.round(metrics.eff/6); const hum = Math.round(metrics.human/6);
        let per = hum > 70 ? "신뢰받는 동료" : "냉혹한 감시자";
        window.parent.postMessage({{ type: 'streamlit:setComponentValue', value: {{ metrics, history, persona: per }} }}, '*');
        new Chart(document.getElementById('radarChart'), {{ type:'radar', data: {{ labels:['예산','효율','인간','지속','주체'], datasets:[{{ data:[metrics.cost/10, eff, hum, hum*0.8, hum*1.1], backgroundColor:'rgba(0,122,204,0.5)' }}] }} }});
    }}
</script>
</body>
</html>
"""

# 8. 최종 결과 제출 버튼 (리포트 화면에서만 활성화)
res = components.html(html_code, height=950)

if res and isinstance(res, dict):
    st.markdown('<div class="submit-bar">실험이 완료되었습니다. 우측 사이드바의 제출 버튼을 눌러주세요.</div>', unsafe_allow_html=True)
    if st.sidebar.button("🚀 실험 결과 최종 제출"):
        save_data(res)
        st.sidebar.balloons()
