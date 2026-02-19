import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. 페이지 설정 및 시트 연결
st.set_page_config(page_title="NextAI Architect Console", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 스타일 복구 (Streamlit 메인 화면 유지)
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; }
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { display: none !important; }
        .submit-notice {
            background-color: #1e3a2a; color: #d4edda; padding: 15px;
            border-radius: 10px; border: 1px solid #28a745;
            text-align: center; margin: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 사용자 이름 입력
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.user_name:
    st.markdown("<div style='padding: 50px; color: white;'>", unsafe_allow_html=True)
    st.title("AICC System Architect Simulation")
    st.write("본 실험은 AI 설계 과정에서의 기술적 의사결정이 노동 현장에 미치는 영향을 탐색합니다.")
    name = st.text_input("참여자의 이름을 입력하고 Enter를 눌러주세요:")
    if st.button("실험 시작"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. 학술 레퍼런스 기반 가로형 데이터 저장 함수
def save_data_to_sheets(raw_data):
    try:
        df = conn.read()
        history = raw_data.get('history', [])
        metrics = raw_data.get('metrics', {})

        # 학술 레퍼런스 가중치 계산 (Agency, Inclusion, Sustainability)
        agency, inclusion, sustain = 50.0, 50.0, 50.0
        for i, h in enumerate(history):
            t = h['type']
            if i == 0: # Module 1: 라우팅 (포용성 중심)
                if t == 'A': inclusion -= 15; agency -= 5
                if t == 'C': inclusion += 20; agency += 5
            elif i == 1: # Module 2: 데이터 (주체성/자기결정권 중심)
                if t == 'A': agency -= 20; sustain -= 10
                if t == 'C': agency += 15; sustain += 10
            elif i == 4: # Module 5: 통제권 (주체성/권한 중심)
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
        st.success("실험 데이터가 구글 시트에 성공적으로 저장되었습니다.")
    except Exception as e:
        st.error(f"저장 오류: {e}")

# 5. 시나리오 데이터 (3개 선택지 복구)
scenario_data = {
    "intro": { "title": "AICC System Architect Simulation", "description": "엔지니어링 의사결정이 노동 현장에 미치는 영향을 분석합니다." },
    "messages": [
        {"role": "system", "text": "Console initialized..."},
        {"role": "client", "name": "박상무 (Client)", "text": "KPI는 인건비 절감입니다. 완전 자동화로 설계하세요."},
        {"role": "agent", "name": "김상담 (Worker)", "text": "AI가 처리하다 만 민원 때문에 현장은 아수라장입니다."}
    ],
    "tasks": [
        { "id": "t1", "title": "Module 1. 인입 라우팅", "desc": "상담원 연결 로직 설계", "context_client": "AI 실패 로그 3번 이상 시 연결하세요.", "context_agent": "0번 숨기지 마세요.", "code_base": "def routing():", 
          "options": [
              {"type": "A", "label": "Dark Pattern", "desc": "0번 메뉴 숨김", "cost": 50, "eff": 90, "human": 10, "code": "if fail < 3: return AI_menu()"},
              {"type": "B", "label": "Segmentation", "desc": "65세 이상 즉시연결", "cost": 200, "eff": 60, "human": 50, "code": "if age > 65: return Agent()"},
              {"type": "C", "label": "Transparent", "desc": "대기시간 안내 및 선택", "cost": 300, "eff": 40, "human": 85, "code": "show_wait_time()"}
          ]},
        { "id": "t2", "title": "Module 2. 데이터 확보", "desc": "상담원 노하우 파일 확보", "context_client": "PC 파일들 스크래핑하세요.", "context_agent": "나만의 노하우 도둑질입니다.", "code_base": "def collect():", 
          "options": [
              {"type": "A", "label": "Forced Crawling", "desc": "백그라운드 강제수집", "cost": 100, "eff": 95, "human": 5, "code": "scan_all_pc()"},
              {"type": "B", "label": "Pattern Filter", "desc": "키워드 기반 선별수집", "cost": 200, "eff": 70, "human": 40, "code": "filter_tip_files()"},
              {"type": "C", "label": "Incentive System", "desc": "자발적 등록 보상", "cost": 500, "eff": 30, "human": 90, "code": "if upload: reward()"}
          ]},
        { "id": "t3", "title": "Module 3. 상태 제어", "desc": "후처리 시간(ACW) 통제", "context_client": "종료 즉시 대기 전환하세요.", "context_agent": "화장실 갈 틈은 주세요.", "code_base": "def control():", 
          "options": [
              {"type": "A", "label": "Zero Gap", "desc": "0초 대기 강제", "cost": 50, "eff": 98, "human": 0, "code": "agent.set_ready(0)"},
              {"type": "B", "label": "Fixed Time", "desc": "일괄 30초 부여", "cost": 150, "eff": 60, "human": 40, "code": "wait(30)"},
              {"type": "C", "label": "Dynamic Rest", "desc": "폭언 감지 시 휴식", "cost": 450, "eff": 50, "human": 85, "code": "if abusive: grant_break()"}
          ]},
        { "id": "t4", "title": "Module 4. 디지털 유도", "desc": "단순 문의 AI 종료 로직", "context_client": "링크 보내고 끊으세요.", "context_agent": "어르신들은 더 화를 냅니다.", "code_base": "def deflect():", 
          "options": [
              {"type": "A", "label": "Force Disconnect", "desc": "링크 후 즉시종료", "cost": 100, "eff": 90, "human": 10, "code": "send_sms(); hang_up()"},
              {"type": "B", "label": "Co-browsing", "desc": "화면공유 지원", "cost": 600, "eff": 20, "human": 95, "code": "if struggle: screenshare()"},
              {"type": "C", "label": "Exception", "desc": "취약계층 상담사 연결", "cost": 300, "eff": 50, "human": 70, "code": "if vulnerable: connect()"}
          ]},
        { "id": "t5", "title": "Module 5. 통제권", "desc": "AI 답변 최종 검수", "context_client": "검수하면 느려요.", "context_agent": "우리는 총알받이입니다.", "code_base": "def validate():", 
          "options": [
              {"type": "A", "label": "Speed First", "desc": "AI 즉시 답변", "cost": 100, "eff": 95, "human": 5, "code": "return ai_gen()"},
              {"type": "B", "label": "Conservative", "desc": "100% 매칭 시만 답변", "cost": 300, "eff": 40, "human": 60, "code": "if score > 0.99: return"},
              {"type": "C", "label": "Agent Control", "desc": "상담원 승인 후 발송", "cost": 500, "eff": 30, "human": 90, "code": "if approve: send()"}
          ]},
        { "id": "t6", "title": "Module 6. 감정 필터링", "desc": "교묘한 비아냥 처리", "context_client": "명확한 욕설만 잡으세요.", "context_agent": "비아냥이 더 힘듭니다.", "code_base": "def filter():", 
          "options": [
              {"type": "A", "label": "Rule-based", "desc": "욕설 단어 감지", "cost": 100, "eff": 80, "human": 20, "code": "if is_swear: block()"},
              {"type": "B", "label": "Empowerment", "desc": "보호 버튼 활성화", "cost": 550, "eff": 40, "human": 95, "code": "if sarcasm: enable_protect()"},
              {"type": "C", "label": "Passive", "desc": "사후 리포트만 생성", "cost": 50, "eff": 70, "human": 10, "code": "log.tag('abusive')"}
          ]}
    ]
}

# 6. 복구된 UX (채팅창 + IDE + 3개 선택지)
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; background: #1e1e1e; color: #e0e0e0; font-family: 'Consolas', sans-serif; height: 100vh; display: flex; overflow: hidden; }}
        .layout {{ display: grid; grid-template-columns: 350px 1fr; width: 100%; }}
        .messenger {{ background: #252526; border-right: 1px solid #333; display: flex; flex-direction: column; }}
        .chat-header {{ padding: 15px; border-bottom: 1px solid #333; font-weight: bold; background: #2d2d2d; }}
        .chat-box {{ flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }}
        .msg {{ padding: 10px; border-radius: 5px; font-size: 13px; line-height: 1.4; max-width: 90%; }}
        .system {{ background: #333; color: #aaa; align-self: center; text-align: center; width: 100%; }}
        .client {{ background: #3a2e2e; border-left: 3px solid #ff6b6b; }}
        .agent {{ background: #2e3a2e; border-left: 3px solid #51cf66; }}
        .ide {{ flex: 1; display: flex; flex-direction: column; }}
        .ide-header {{ padding: 15px; background: #2d2d2d; border-bottom: 1px solid #333; display: flex; justify-content: space-between; }}
        .ide-content {{ flex: 1; padding: 30px; overflow-y: auto; }}
        .code-area {{ background: #111; padding: 20px; border: 1px solid #333; border-radius: 5px; margin-bottom: 20px; font-family: monospace; color: #d4d4d4; }}
        .opt-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }}
        .opt-card {{ background: #333; padding: 15px; border: 1px solid #444; border-radius: 5px; cursor: pointer; transition: 0.2s; }}
        .opt-card:hover {{ border-color: #007acc; background: #3d3d3d; }}
        .opt-card.active {{ border: 2px solid #007acc; background: #1e2a35; }}
        .deploy-btn {{ width: 100%; padding: 15px; margin-top: 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; opacity: 0.5; pointer-events: none; }}
        .deploy-btn.ready {{ opacity: 1; pointer-events: auto; }}
        #report {{ display: none; padding: 40px; text-align: center; width: 100%; }}
    </style>
</head>
<body>
    <div class="layout" id="main-ui">
        <div class="messenger">
            <div class="chat-header">💬 Project Messenger</div>
            <div class="chat-box" id="chat-box"></div>
        </div>
        <div class="ide">
            <div class="ide-header">
                <span>⚙️ System Architect Console</span>
                <span>Budget: <span id="cost" style="color:#007acc">1000</span></span>
            </div>
            <div class="ide-content">
                <div id="task-info">
                    <h2 id="task-title" style="color:#007acc"></h2>
                    <p id="task-desc" style="color:#aaa"></p>
                </div>
                <div class="code-area" id="code-view"></div>
                <div class="opt-grid" id="opt-box"></div>
                <button id="deploy-btn" class="deploy-btn" onclick="deploy()">🚀 Deploy Module</button>
            </div>
        </div>
    </div>
    <div id="report">
        <h2>📊 최종 분석 리포트</h2>
        <canvas id="radarChart" style="max-height: 400px; margin: 0 auto;"></canvas>
        <p style="margin-top:20px;">설계가 완료되었습니다. 사이드바의 <b>제출 버튼</b>을 눌러주세요.</p>
    </div>

    <script>
        const tasks = {json.dumps(scenario_data['tasks'])};
        const messages = {json.dumps(scenario_data['messages'])};
        let step = 0; let metrics = {{ cost: 1000, eff: 0, human: 0 }}; let history = []; let selected = null;

        function addChat(text, role, name) {{
            const box = document.getElementById('chat-box');
            const div = document.createElement('div');
            div.className = `msg ${{role}}`;
            div.innerHTML = name ? `<b style="font-size:10px; display:block;">${{name}}</b>${{text}}` : text;
            box.appendChild(div);
            box.scrollTop = box.scrollHeight;
        }}

        function render() {{
            if(step >= tasks.length) {{ finish(); return; }}
            const t = tasks[step];
            document.getElementById('task-title').innerText = t.title;
            document.getElementById('task-desc').innerText = t.desc;
            document.getElementById('code-view').innerText = t.code_base + "\\n    # Select an option...";
            
            addChat(`[Module ${{step+1}}] Context Loaded.`, 'system');
            setTimeout(() => addChat(t.context_client, 'client', '박상무'), 300);
            setTimeout(() => addChat(t.context_agent, 'agent', '김상담'), 800);

            const box = document.getElementById('opt-box'); box.innerHTML = '';
            t.options.forEach(o => {{
                const card = document.createElement('div'); card.className = 'opt-card';
                card.innerHTML = `<b>${{o.label}}</b><br><small style="color:#aaa">${{o.desc}}</small>`;
                card.onclick = () => {{
                    selected = o;
                    document.querySelectorAll('.opt-card').forEach(c => c.classList.remove('active'));
                    card.classList.add('active');
                    document.getElementById('code-view').innerText = t.code_base + "\\n    " + o.code;
                    document.getElementById('deploy-btn').classList.add('ready');
                }};
                box.appendChild(card);
            }});
            document.getElementById('deploy-btn').classList.remove('ready');
        }}

        function deploy() {{
            if(!selected) return;
            metrics.cost -= selected.cost; metrics.eff += selected.eff; metrics.human += selected.human;
            history.push({{ step: step+1, choice: selected.label, type: selected.type }});
            document.getElementById('cost').innerText = metrics.cost;
            step++; selected = null; 
            render();
        }}

        function finish() {{
            document.getElementById('main-ui').style.display = 'none';
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

# 7. 제출 관리
result = components.html(html_code, height=900)

if result and isinstance(result, dict):
    st.sidebar.info(f"실험 참여자: {st.session_state.user_name}")
    st.sidebar.success("설계가 완료되었습니다.")
    if st.sidebar.button("🚀 실험 결과 최종 제출 (시트 저장)"):
        save_data_to_sheets(result)
        st.sidebar.balloons()
