import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. 페이지 설정 및 시트 연결
st.set_page_config(page_title="NextAI Architect Console", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 스타일 복구 (Streamlit 메인 화면 디자인)
st.markdown("""
    <style>
        /* 메인 배경 및 레이아웃 */
        .stApp { background-color: #0e1117; }
        .block-container { padding: 2rem !important; }
        
        /* 안내 문구 및 입력창 스타일 */
        .stTextInput > div > div > input {
            background-color: #262730;
            color: white;
            border: 1px solid #4a4a4a;
        }
        h1, h2, h3, p { color: #e0e0e0 !important; }
        
        /* 제출 알림 바 */
        .submit-notice {
            background-color: #1e3a2a;
            color: #d4edda;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #28a745;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 사용자 이름 입력부
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.user_name:
    st.title("AICC System Architect Simulation")
    st.write("실험 목적: 시스템 설계자의 의사결정이 노동 현장에 미치는 사회기술적 영향 탐색")
    name = st.text_input("참여자의 이름을 입력하고 Enter를 눌러주세요:", placeholder="이름을 입력하세요")
    if st.button("실험 시작"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# 4. 학술 레퍼런스 기반 데이터 저장 함수
def save_data_to_sheets(raw_data):
    try:
        df = conn.read()
        history = raw_data.get('history', [])
        metrics = raw_data.get('metrics', {})

        # 지표 계산 (회의록 및 학술 근거 기반)
        # Agency(주체성), Inclusion(포용성), Sustainability(지속성)
        agency, inclusion, sustain = 50.0, 50.0, 50.0
        
        for i, h in enumerate(history):
            t = h['type']
            if i == 0: # Module 1: 라우팅
                if t == 'A': inclusion -= 15; agency -= 5
                if t == 'C': inclusion += 20; agency += 5
            elif i == 1: # Module 2: 데이터
                if t == 'A': agency -= 20; sustain -= 10
                if t == 'C': agency += 15; sustain += 10
            elif i == 2: # Module 3: 상태제어
                if t == 'A': sustain -= 20; inclusion -= 5
                if t == 'C': sustain += 20; inclusion += 5
            elif i == 4: # Module 5: 통제권
                if t == 'A': agency -= 25; sustain -= 10
                if t == 'C': agency += 25; sustain += 10

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
            "직무_지속성": round(min(100, max(0, sustain)), 1),
            "최종_예산": metrics.get('cost', 0),
            "페르소나": raw_data.get('persona', '')
        }
        
        updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        conn.update(data=updated_df)
        st.success("✅ 구글 스프레드시트에 실험 결과가 성공적으로 저장되었습니다.")
    except Exception as e:
        st.error(f"저장 오류: {e}")

# 5. 시나리오 데이터 (간소화)
scenario_data = {
    "tasks": [
        { "id": "t1", "title": "Module 1. 인입 라우팅", "desc": "상담원 연결 로직 설계", "context_client": "강제 차단하세요.", "context_agent": "숨기지 마세요.", 
          "options": [{"type": "A", "label": "Dark Pattern", "desc": "0번 메뉴 숨김", "cost": 50, "eff": 90, "human": 10}, {"type": "C", "label": "Transparent", "desc": "연결권 부여", "cost": 300, "eff": 40, "human": 85}]},
        # ... (이전 모듈들 동일)
    ]
}

# 6. 실험 콘솔 HTML/JS (UX 복구 버전)
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ background-color: #1e1e1e; color: #e0e0e0; font-family: sans-serif; margin: 0; padding: 20px; }}
        .task-card {{ background: #2d2d2d; padding: 20px; border-radius: 10px; border: 1px solid #3d3d3d; margin-bottom: 20px; }}
        .opt-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
        .opt-btn {{ background: #3d3d3d; padding: 15px; border-radius: 8px; cursor: pointer; border: 1px solid #4d4d4d; }}
        .opt-btn:hover {{ border-color: #007acc; background: #333; }}
        .opt-btn.active {{ border: 2px solid #007acc; background: #1e2a35; }}
        .deploy-btn {{ width: 100%; padding: 15px; margin-top: 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; opacity: 0.5; }}
        .deploy-btn.ready {{ opacity: 1; }}
        #report {{ display: none; text-align: center; }}
    </style>
</head>
<body>
    <div id="simulation">
        <div id="task-container"></div>
        <button id="deploy-btn" class="deploy-btn" onclick="deploy()">🚀 Deploy Module</button>
    </div>
    <div id="report">
        <h2>📊 실험 분석 결과</h2>
        <canvas id="radarChart" style="max-height: 350px;"></canvas>
        <p>설계가 완료되었습니다. 사이드바의 <b>제출 버튼</b>을 눌러주세요.</p>
    </div>

    <script>
        const tasks = {json.dumps(scenario_data['tasks'])};
        let step = 0; let metrics = {{ cost: 1000, eff: 0, human: 0 }}; let history = []; let selected = null;

        function render() {{
            if(step >= tasks.length) {{ finish(); return; }}
            const t = tasks[step];
            document.getElementById('task-container').innerHTML = `
                <div class="task-card">
                    <h3>${{t.title}}</h3>
                    <p>${{t.desc}}</p>
                    <div class="opt-grid" id="opts"></div>
                </div>
            `;
            const opts = document.getElementById('opts');
            t.options.forEach(o => {{
                const b = document.createElement('div'); b.className = 'opt-btn';
                b.innerHTML = `<b>${{o.label}}</b><br><small>${{o.desc}}</small>`;
                b.onclick = () => {{
                    selected = o;
                    document.querySelectorAll('.opt-btn').forEach(x => x.classList.remove('active'));
                    b.classList.add('active');
                    document.getElementById('deploy-btn').classList.add('ready');
                }};
                opts.appendChild(b);
            }});
        }}
        function deploy() {{
            if(!selected) return;
            metrics.cost -= selected.cost; metrics.eff += selected.eff; metrics.human += selected.human;
            history.push({{ step: step+1, choice: selected.label, type: selected.type }});
            step++; selected = null; 
            document.getElementById('deploy-btn').classList.remove('ready');
            render();
        }}
        function finish() {{
            document.getElementById('simulation').style.display = 'none';
            document.getElementById('report').style.display = 'block';
            window.parent.postMessage({{ type: 'streamlit:setComponentValue', value: {{ metrics, history, persona: "실험 완료" }} }}, '*');
            new Chart(document.getElementById('radarChart'), {{
                type: 'radar',
                data: {{ labels: ['예산', '효율', '인간성', '지속성', '주체성'], datasets: [{{ data: [metrics.cost/10, 70, 60, 50, 80], backgroundColor: 'rgba(0,122,204,0.5)' }}] }}
            }});
        }}
        render();
    </script>
</body>
</html>
"""

# 7. 최종 데이터 수신 및 사이드바 제출
result = components.html(html_code, height=800)

if result and isinstance(result, dict):
    st.sidebar.title("🚀 실험 종료")
    st.sidebar.info(f"참여자: {st.session_state.user_name}")
    st.sidebar.warning("데이터 저장을 위해 아래 버튼을 누르세요.")
    if st.sidebar.button("최종 결과 제출하기"):
        save_data_to_sheets(result)
        st.sidebar.balloons()
