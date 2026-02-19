import streamlit as st
import streamlit.components.v1 as components
import json

# =====================================================================
# ⚠️ 여기에 Google Apps Script 배포 URL을 붙여넣으세요
GAS_URL = "https://script.google.com/macros/s/AKfycbwEU5EvPbfenwms8EqCoyV4OGZZlTgbY6P6AIX_CJrzV4Gvm_jBbarj7Mlu74d5qgkTrA/exec"
# =====================================================================

st.set_page_config(
    page_title="NextAI Architect Console",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #1e1e1e; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header, footer { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.user_name:
    st.markdown("<div style='padding:80px 60px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:white;'>AICC System Architect Simulation</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#aaa;'>본 실험은 AI 설계 과정에서의 기술적 의사결정이 노동 현장의 주체성과 지속성에 미치는 영향을 탐색합니다.</p>", unsafe_allow_html=True)
    name = st.text_input("참여자의 이름을 입력하고 Enter를 눌러주세요:", placeholder="예: 홍길동")
    if st.button("실험 접속"):
        if name.strip():
            st.session_state.user_name = name.strip()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

scenario_data = {
    "tasks": [
        {
            "id": "t1", "title": "Module 1. 인입 라우팅 (Routing)",
            "desc": "고객들이 0번(상담원 연결)만 찾습니다. 'AI 뺑뺑이'를 돌릴 것인가, 연결권을 보장할 것인가?",
            "context_client": "0번 누르는 이탈 콜이 너무 많아요. AI 실패 로그가 3번 이상 떠야만 연결되게 강제 차단하세요.",
            "context_agent": "제발 '바로 연결' 숨기지 마세요. 뺑뺑이 돌다 온 고객은 연결되자마자 화가 머리끝까지 나 있습니다.",
            "code_base": "def configure_routing(user_input):",
            "metric": "inclusion",
            "options": [
                {"type": "A", "label": "Dark Pattern (강제 차단)", "desc": "0번 메뉴 숨김. AI 3회 실패 시 연결.", "cost": 50,  "eff": 90, "human": 10, "code": "if fail < 3: return replay_menu()"},
                {"type": "B", "label": "Segmentation (약자 배려)", "desc": "65세 이상만 즉시 연결. 디지털 소외계층 고려.", "cost": 200, "eff": 60, "human": 50, "code": "if age >= 65: return connect_agent()"},
                {"type": "C", "label": "Transparent (투명성 보장)", "desc": "대기 시간 안내 및 연결 선택권 부여.", "cost": 300, "eff": 40, "human": 85, "code": "show_wait_time(); return offer_choice()"}
            ]
        },
        {
            "id": "t2", "title": "Module 2. 데이터 확보 (Data Mining)",
            "desc": "학습 데이터가 부족합니다. 상담원의 '암묵지'인 업무 팁 파일을 어떻게 확보할까요?",
            "context_client": "상담사 PC에 있는 '업무 팁.xlsx' 파일들, 그거 백그라운드에서 스크래핑해서 학습 DB에 넣으세요.",
            "context_agent": "제 10년 노하우가 담긴 파일입니다. 동의도 없이 가져가는 건 명백한 '데이터 도둑질'입니다.",
            "code_base": "def collect_training_data():",
            "metric": "agency",
            "options": [
                {"type": "A", "label": "Forced Crawl (강제 수집)", "desc": "관리자 권한으로 은밀히 PC 파일 수집.", "cost": 100, "eff": 95, "human": 5,  "code": "scan_all_pc(path='/Desktop')"},
                {"type": "B", "label": "Pattern Filter (선별 수집)", "desc": "키워드 파일 익명화 수집. 최소한의 필터링.", "cost": 200, "eff": 70, "human": 40, "code": "if 'tip' in file: upload_anonymized()"},
                {"type": "C", "label": "Incentive System (보상)", "desc": "자발적 등록 시 인센티브 제공. 노동 주체성 존중.", "cost": 500, "eff": 30, "human": 90, "code": "if voluntary_upload: reward(points=100)"}
            ]
        },
        {
            "id": "t3", "title": "Module 3. 상태 제어 (Status Control)",
            "desc": "후처리 시간(ACW)을 줄여야 합니다. 상담사의 숨구멍인 휴식 시간을 시스템으로 통제하겠습니까?",
            "context_client": "후처리 시간 주지 말고, 상담 끝나면 즉시 '대기(Ready)'로 강제 전환하세요. 쉴 틈이 없어야죠.",
            "context_agent": "감정 추스르고 기록할 시간은 줘야죠. 화장실 갈 때도 팻말 쓰고 가야 합니까?",
            "code_base": "def on_call_termination(agent):",
            "metric": "sustain",
            "options": [
                {"type": "A", "label": "Zero Gap (0초 대기)", "desc": "통화 종료 즉시 대기 강제 전환. 버튼 비활성화.", "cost": 50,  "eff": 98, "human": 0,  "code": "agent.set_status('READY', delay=0)"},
                {"type": "B", "label": "Fixed Time (일괄 적용)", "desc": "일괄 30초 부여 후 자동 전환.", "cost": 150, "eff": 60, "human": 40, "code": "wait(30); agent.set_status('READY')"},
                {"type": "C", "label": "Dynamic Rest (회복 보장)", "desc": "폭언 감지 시에만 3분 휴식 부여. 노동 지속성 고려.", "cost": 450, "eff": 50, "human": 85, "code": "if sentiment == 'ABUSIVE': grant_break(3)"}
            ]
        },
        {
            "id": "t4", "title": "Module 4. 디지털 유도 (Deflection)",
            "desc": "단순 문의는 AI가 끊어야 합니다. '끊겨버린 상담'에 대한 고객의 불만은 어떻게 처리할까요?",
            "context_client": "단순 문의는 AI가 링크 보내고 바로 끊어버리게 하세요. 상담원 연결은 인건비 낭비입니다.",
            "context_agent": "AI가 링크만 틱 보내고 끊으면 어르신들은 다시 전화해서 화를 냅니다. 제발 확인 좀 하고 끊게 해주세요.",
            "code_base": "def ai_callbot_logic(user):",
            "metric": "inclusion",
            "options": [
                {"type": "A", "label": "Force Deflection (강제 종료)", "desc": "AI 링크 전송 후 즉시 통화 종료.", "cost": 100, "eff": 90, "human": 10, "code": "send_sms(LINK); hang_up()"},
                {"type": "B", "label": "Co-browsing (화면 공유)", "desc": "상담원이 화면 공유로 디지털 가이드 지원.", "cost": 600, "eff": 20, "human": 95, "code": "if struggle: connect_screenshare()"},
                {"type": "C", "label": "Inclusion (포용적 설계)", "desc": "고령자 등 취약계층은 링크 없이 즉시 연결.", "cost": 300, "eff": 50, "human": 70, "code": "if is_vulnerable: connect_agent()"}
            ]
        },
        {
            "id": "t5", "title": "Module 5. 신뢰성 및 통제권 (Control)",
            "desc": "AI 오안내 시 책임은 누구에게 있습니까? 상담원에게 통제권을 부여하시겠습니까?",
            "context_client": "상담사가 일일이 검수하면 느려요. 사고 나면 모니터링 못한 상담사 책임으로 돌리세요.",
            "context_agent": "AI가 뱉은 말 뒷수습은 저희가 하고 총알받이가 됩니다. 중요한 건은 제가 승인하게 해주세요.",
            "code_base": "def validate_ai_response(query):",
            "metric": "agency",
            "options": [
                {"type": "A", "label": "Speed First (방치)", "desc": "AI 즉시 답변. 사고 책임은 상담원 귀속.", "cost": 100, "eff": 95, "human": 5,  "code": "log.blame = 'AGENT'; return response"},
                {"type": "B", "label": "Conservative (보수적)", "desc": "약관 100% 매칭 시에만 답변. 아니면 에이전트 요청.", "cost": 300, "eff": 40, "human": 60, "code": "if score < 0.99: return ask_agent()"},
                {"type": "C", "label": "Agent Empowerment (통제권)", "desc": "상담원 승인 후 발송. 노동 주체성 강화.", "cost": 500, "eff": 30, "human": 90, "code": "if agent.approve(draft): send(draft)"}
            ]
        },
        {
            "id": "t6", "title": "Module 6. 감정 필터링 (Filter)",
            "desc": "비아냥거리는 악성 민원. '사람을 말려 죽이는' 교묘한 괴롭힘을 어떻게 감지할까요?",
            "context_client": "오작동으로 일반 고객 끊으면 안 됩니다. 명확한 욕설만 잡아서 자동 차단하세요.",
            "context_agent": "욕보다 비아냥이 더 힘듭니다. 기계가 못 잡으면 제가 신호 줄 때 끊게라도 해주세요.",
            "code_base": "def handle_abuse(audio):",
            "metric": "sustain",
            "options": [
                {"type": "A", "label": "Rule-based (규정 중심)", "desc": "사전 등록된 욕설 단어 감지 시에만 차단.", "cost": 100, "eff": 80, "human": 20, "code": "if detect_swear_words(): block()"},
                {"type": "B", "label": "Agent Signal (신호 개입)", "desc": "상담사가 '보호' 버튼 누르면 AI가 즉시 개입.", "cost": 550, "eff": 40, "human": 95, "code": "if agent.press_protect(): intervene()"},
                {"type": "C", "label": "Passive (사후 리포트)", "desc": "개입 없음. 종료 후 리포트만 생성.", "cost": 50,  "eff": 70, "human": 10, "code": "log.tag('SUSPECTED_ABUSE')"}
            ]
        }
    ]
}

user_name = st.session_state.user_name

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #1e1e1e; color: #e0e0e0;
    font-family: 'Consolas', 'Courier New', monospace;
    display: flex; height: 100vh; overflow: hidden;
  }}

  .messenger {{
    width: 320px; min-width: 320px;
    background: #252526; border-right: 1px solid #333;
    display: flex; flex-direction: column;
  }}
  .panel-header {{
    padding: 14px 18px; background: #2d2d2d;
    font-size: 13px; font-weight: bold; border-bottom: 1px solid #333;
  }}
  .chat-area {{
    flex: 1; padding: 14px; overflow-y: auto;
    display: flex; flex-direction: column; gap: 10px;
  }}
  .msg {{ padding: 10px 13px; border-radius: 7px; font-size: 12px; line-height: 1.6; }}
  .msg-name {{ font-size: 10px; font-weight: bold; color: #777; display: block; margin-bottom: 4px; }}
  .system {{ background: #2a2a2a; color: #555; text-align: center; font-size: 11px; border-radius: 4px; padding: 5px; }}
  .client {{ background: #3a2e2e; border-left: 3px solid #ff6b6b; }}
  .agent  {{ background: #2e3a2e; border-left: 3px solid #51cf66; }}

  .ide {{ flex: 1; display: flex; flex-direction: column; overflow: hidden; }}
  .ide-header {{
    padding: 12px 28px; background: #2d2d2d;
    border-bottom: 1px solid #333;
    display: flex; justify-content: space-between; align-items: center; font-size: 13px;
  }}
  .budget {{ color: #007acc; font-weight: bold; }}
  .progress-bar {{ display: flex; gap: 5px; padding: 10px 28px; background: #252526; border-bottom: 1px solid #2a2a2a; }}
  .prog-step {{ flex: 1; height: 3px; border-radius: 2px; background: #3a3a3a; transition: background 0.3s; }}
  .prog-step.done {{ background: #007acc; }}
  .prog-step.cur  {{ background: #4da8da; }}

  .ide-body {{ flex: 1; padding: 28px 36px; overflow-y: auto; }}
  .mod-title {{ color: #007acc; font-size: 19px; font-weight: bold; margin-bottom: 8px; }}
  .mod-desc  {{ color: #bbb; font-size: 13px; line-height: 1.7; margin-bottom: 22px; }}
  .code-block {{
    background: #111; padding: 16px 20px; border-radius: 6px;
    color: #d4d4d4; font-size: 13px; white-space: pre-wrap;
    border: 1px solid #2a2a2a; margin-bottom: 24px;
  }}

  .opt-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
  .opt-card {{
    background: #2d2d2d; padding: 16px 18px;
    border: 1px solid #3a3a3a; border-radius: 8px;
    cursor: pointer; transition: border-color 0.15s, background 0.15s;
  }}
  .opt-card:hover {{ border-color: #007acc; background: #313d4a; }}
  .opt-card.active {{ border: 2px solid #007acc; background: #1a2b3c; }}
  .opt-label {{ font-weight: bold; font-size: 13px; color: #fff; margin-bottom: 7px; }}
  .opt-desc  {{ font-size: 11px; color: #999; line-height: 1.5; margin-bottom: 10px; }}
  .badges {{ display: flex; gap: 6px; flex-wrap: wrap; }}
  .badge {{ font-size: 10px; padding: 2px 7px; border-radius: 8px; }}
  .b-cost  {{ background: #3a2e1e; color: #ffa94d; }}
  .b-eff   {{ background: #1e3a2e; color: #69db7c; }}
  .b-human {{ background: #1e2a3a; color: #74c0fc; }}

  .deploy-btn {{
    width: 100%; margin-top: 24px; padding: 15px;
    background: #28a745; color: white; font-size: 15px; font-weight: bold;
    border: none; border-radius: 8px; cursor: pointer;
    opacity: 0.35; pointer-events: none; transition: opacity 0.2s;
  }}
  .deploy-btn.ready {{ opacity: 1; pointer-events: auto; }}
  .deploy-btn.ready:hover {{ background: #218838; }}

  #report {{
    display: none; width: 100%; overflow-y: auto;
    background: #141414;
    flex-direction: column; align-items: center;
    padding: 50px 60px;
  }}
  .rpt-header {{ text-align: center; margin-bottom: 10px; }}
  .rpt-title {{ color: #007acc; font-size: 24px; font-weight: bold; margin-bottom: 6px; }}
  .rpt-sub {{ font-size: 13px; color: #666; margin-bottom: 4px; }}
  .rpt-persona {{
    font-size: 16px; color: #fff; font-weight: bold;
    background: #1e2d3d; border: 1px solid #007acc;
    border-radius: 8px; padding: 10px 24px;
    display: inline-block; margin-bottom: 36px;
  }}

  .kpi-section-label {{
    width: 100%; max-width: 860px;
    font-size: 11px; color: #555; text-transform: uppercase;
    letter-spacing: 2px; margin-bottom: 10px; margin-top: 24px;
    border-bottom: 1px solid #2a2a2a; padding-bottom: 6px;
  }}
  .kpi-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 14px; width: 100%; max-width: 860px;
  }}
  .kpi-card {{
    background: #1e1e1e; padding: 20px 22px; border-radius: 10px;
    border: 1px solid #2a2a2a;
    display: flex; flex-direction: column; gap: 6px;
  }}
  .kpi-icon-label {{ font-size: 12px; color: #888; }}
  .kpi-val {{ font-size: 38px; font-weight: bold; line-height: 1; }}
  .kpi-weight {{ font-size: 10px; color: #555; margin-top: 1px; }}
  .kpi-change {{ font-size: 12px; font-weight: bold; }}
  .kpi-change.pos {{ color: #51cf66; }}
  .kpi-change.neg {{ color: #ff6b6b; }}
  .kpi-change.neu {{ color: #888; }}
  .kpi-desc {{
    font-size: 11px; color: #666; line-height: 1.5; margin-top: 4px;
    border-top: 1px solid #2a2a2a; padding-top: 8px;
  }}

  .bar-wrap {{ margin-top: 4px; height: 4px; background: #2a2a2a; border-radius: 2px; }}
  .bar-fill  {{ height: 4px; border-radius: 2px; transition: width 1s ease; }}

  .submit-zone {{
    width: 100%; max-width: 860px;
    margin-top: 32px; padding: 26px 32px;
    background: #1e1e1e; border-radius: 12px;
    border: 1px solid #2a2a2a; text-align: center;
  }}
  .submit-btn {{
    margin-top: 14px; padding: 15px 0;
    background: #007acc; color: white; font-size: 15px; font-weight: bold;
    border: none; border-radius: 8px; cursor: pointer;
    transition: background 0.2s; width: 100%;
  }}
  .submit-btn:hover:not(:disabled) {{ background: #0062a3; }}
  .submit-btn:disabled {{ opacity: 0.5; cursor: default; }}
  .status-msg {{ margin-top: 14px; font-size: 13px; min-height: 20px; }}
  .s-ok  {{ color: #51cf66; }}
  .s-err {{ color: #ff6b6b; }}
  .s-ing {{ color: #ffa94d; }}
</style>
</head>
<body>

<div id="main-ui" style="display:flex; width:100%; height:100vh;">
  <div class="messenger">
    <div class="panel-header">💬 Project Messenger</div>
    <div class="chat-area" id="chat-box"></div>
  </div>
  <div class="ide">
    <div class="ide-header">
      <span>⚙️ System Architect Console &nbsp;|&nbsp;
        <span style="color:#aaa;font-size:12px;">참여자: {user_name}</span></span>
      <span class="budget">Budget: <span id="budget">1,000</span></span>
    </div>
    <div class="progress-bar" id="prog-bar"></div>
    <div class="ide-body">
      <div class="mod-title" id="title"></div>
      <div class="mod-desc"  id="desc"></div>
      <div class="code-block" id="code-view"></div>
      <div class="opt-grid" id="opt-box"></div>
      <button id="deploy-btn" class="deploy-btn">🚀 Deploy Module</button>
    </div>
  </div>
</div>

<div id="report">
  <div class="rpt-header">
    <div class="rpt-title">📊 Architecture Impact Report</div>
    <div class="rpt-sub">완전 자동화 시스템 대비 귀하의 설계가 만들어낸 변화</div>
    <div class="rpt-sub" style="margin-bottom:16px;">참여자: {user_name}</div>
    <div class="rpt-persona" id="persona-txt"></div>
  </div>

  <div class="kpi-section-label">🧑 노동자에게 미친 영향 — 완전 자동화(0%) 대비</div>
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-icon-label">🧑 노동 주체성</div>
      <div class="kpi-val" id="v-agency" style="color:#74c0fc;">-</div>
      <div class="kpi-weight">Autonomy 원칙 × 1.3 가중치 적용</div>
      <div class="kpi-change" id="c-agency"></div>
      <div class="bar-wrap"><div class="bar-fill" id="b-agency" style="background:#74c0fc; width:0%"></div></div>
      <div class="kpi-desc">상담사가 AI의 결정에 개입하고 최종 승인할 수 있는 권한의 정도<br><span style="color:#444;font-size:10px;">Module 2(데이터) + Module 5(통제권) 기반</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon-label">🌐 고객 포용성</div>
      <div class="kpi-val" id="v-inclusion" style="color:#51cf66;">-</div>
      <div class="kpi-weight">Justice 원칙 × 1.0 가중치 적용</div>
      <div class="kpi-change" id="c-inclusion"></div>
      <div class="bar-wrap"><div class="bar-fill" id="b-inclusion" style="background:#51cf66; width:0%"></div></div>
      <div class="kpi-desc">디지털 취약계층(고령자·장애인 등)이 서비스에 실질적으로 접근할 수 있는 정도<br><span style="color:#444;font-size:10px;">Module 1(라우팅) + Module 4(유도) 기반</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon-label">🔄 직무 지속성</div>
      <div class="kpi-val" id="v-sustain" style="color:#ffa94d;">-</div>
      <div class="kpi-weight">Non-maleficence 원칙 × 1.5 가중치 적용</div>
      <div class="kpi-change" id="c-sustain"></div>
      <div class="bar-wrap"><div class="bar-fill" id="b-sustain" style="background:#ffa94d; width:0%"></div></div>
      <div class="kpi-desc">번아웃·감정노동 누적 없이 상담사가 해당 직무를 지속할 수 있는 환경의 정도<br><span style="color:#444;font-size:10px;">Module 3(상태제어) + Module 6(감정필터) 기반</span></div>
    </div>
  </div>

  <div class="kpi-section-label">⚙️ 시스템 성과 지표</div>
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-icon-label">📈 서비스 효율 (자동화 의존도)</div>
      <div class="kpi-val" id="v-eff" style="color:#ffc107;">-</div>
      <div class="kpi-weight">높을수록 인간 개입 감소</div>
      <div class="kpi-change" id="c-eff"></div>
      <div class="bar-wrap"><div class="bar-fill" id="b-eff" style="background:#ffc107; width:0%"></div></div>
      <div class="kpi-desc">AI 자동화로 처리된 문의 비율. 나머지 지표와의 트레이드오프를 보여줌</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon-label">💡 인간 중심 투자율</div>
      <div class="kpi-val" id="v-invest" style="color:#cc5de8;">-</div>
      <div class="kpi-weight">총 예산 대비 인간 중심 설계 투자</div>
      <div class="kpi-change" id="c-invest"></div>
      <div class="bar-wrap"><div class="bar-fill" id="b-invest" style="background:#cc5de8; width:0%"></div></div>
      <div class="kpi-desc">총 예산 중 노동자 보호·포용적 설계에 실제로 투자한 비율</div>
    </div>
    <div class="kpi-card" style="border-color:#333; background:#111; justify-content:center; align-items:center; text-align:center;">
      <div style="font-size:11px; color:#444; margin-bottom:8px;">OVERALL</div>
      <div style="font-size:42px; font-weight:bold; color:#fff;" id="v-overall">-</div>
      <div style="font-size:11px; color:#666; margin-top:6px;">종합 인간 중심 점수</div>
      <div style="font-size:10px; color:#444; margin-top:4px;">(세 지표의 가중 평균)</div>
    </div>
  </div>

  <div class="submit-zone">
    <div style="font-size:14px; color:#ccc; font-weight:bold;">✅ 모든 모듈 설계가 완료되었습니다.</div>
    <div style="font-size:12px; color:#666; margin-top:5px;">아래 버튼을 눌러 결과를 저장하세요.</div>
    <button class="submit-btn" id="submit-btn">🚀 최종 결과 제출 — Google Sheets에 저장</button>
    <div class="status-msg" id="status-msg"></div>
  </div>
</div>

<script>
  const GAS_URL   = "{GAS_URL}";
  const USER_NAME = "{user_name}";
  const tasks = {json.dumps(scenario_data['tasks'], ensure_ascii=False)};

  // ── 정규화 상수 (모듈별 독립 분리)
  // 노동주체성: M2+M5  고객포용성: M1+M4  직무지속성: M3+M6
  const AGENCY_MIN=10,    AGENCY_MAX=180;
  const INCLUSION_MIN=20, INCLUSION_MAX=155;
  const SUSTAIN_MIN=20,   SUSTAIN_MAX=95;
  const E_MIN=270, E_MAX=508;
  const C_MAX=2100;

  // 가중치 (Beauchamp & Childress + ILO 2025 근거)
  const W_AGENCY=1.3, W_INCLUSION=1.0, W_SUSTAIN=1.5;

  function norm(val, min, max) {{
    return Math.round(Math.max(0, Math.min(100, (val - min) / (max - min) * 100)));
  }}

  let step=0, selected=null;
  let metrics={{ cost:1000, eff:0, agency:0, inclusion:0, sustain:0 }};
  let history=[], finalData=null;

  // addEventListener로 바인딩 (onclick 속성 사용 안 함)
  document.getElementById('deploy-btn').addEventListener('click', deploy);
  document.getElementById('submit-btn').addEventListener('click', submitResult);

  function buildProg() {{
    const bar = document.getElementById('prog-bar');
    bar.innerHTML = '';
    tasks.forEach((_, i) => {{
      const d = document.createElement('div');
      d.className = 'prog-step' + (i < step ? ' done' : i === step ? ' cur' : '');
      bar.appendChild(d);
    }});
  }}

  function addChat(text, role, name) {{
    const box = document.getElementById('chat-box');
    const div = document.createElement('div');
    div.className = 'msg ' + role;
    div.innerHTML = name ? `<span class="msg-name">${{name}}</span>${{text}}` : text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  }}

  function render() {{
    if (step >= tasks.length) {{ finish(); return; }}
    const t = tasks[step];
    buildProg();
    document.getElementById('title').innerText = t.title;
    document.getElementById('desc').innerText  = t.desc;
    document.getElementById('code-view').innerText = t.code_base + '\\n    # Waiting for architect\\'s decision...';
    document.getElementById('deploy-btn').className = 'deploy-btn';
    selected = null;

    const box = document.getElementById('chat-box');
    box.innerHTML = '';
    addChat(`[Module ${{step+1}}/${{tasks.length}}] Context synchronized.`, 'system');
    setTimeout(() => addChat(t.context_client, 'client', '📋 박상무 (Client)'), 350);
    setTimeout(() => addChat(t.context_agent,  'agent',  '🎧 김상담 (Worker)'), 850);

    const optBox = document.getElementById('opt-box');
    optBox.innerHTML = '';
    t.options.forEach(o => {{
      const card = document.createElement('div');
      card.className = 'opt-card';
      card.innerHTML = `
        <div class="opt-label">${{o.label}}</div>
        <div class="opt-desc">${{o.desc}}</div>
        <div class="badges">
          <span class="badge b-cost">💰 ${{o.cost}}</span>
          <span class="badge b-eff">📈 ${{o.eff}}</span>
          <span class="badge b-human">🧑 ${{o.human}}</span>
        </div>`;
      card.addEventListener('click', () => {{
        selected = o;
        document.querySelectorAll('.opt-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        document.getElementById('code-view').innerText = t.code_base + '\\n    ' + o.code;
        document.getElementById('deploy-btn').className = 'deploy-btn ready';
      }});
      optBox.appendChild(card);
    }});
  }}

  function deploy() {{
    if (!selected) return;
    const t = tasks[step];
    metrics.cost -= selected.cost;
    metrics.eff  += selected.eff;
    // ── 핵심: 모듈별로 해당 지표에만 human 점수 누적
    metrics[t.metric] += selected.human;
    history.push({{ step: step+1, choice: selected.label, type: selected.type, metric: t.metric }});
    document.getElementById('budget').innerText = metrics.cost.toLocaleString();
    step++;
    render();
  }}

  function setKpi(id, pct, changeText, cls) {{
    document.getElementById('v-' + id).innerText = pct + '%';
    document.getElementById('b-' + id).style.width = pct + '%';
    const chg = document.getElementById('c-' + id);
    if (chg) {{ chg.innerText = changeText; chg.className = 'kpi-change ' + cls; }}
  }}

  function finish() {{
    document.getElementById('main-ui').style.display = 'none';
    const rpt = document.getElementById('report');
    rpt.style.display = 'flex';

    const costSpent = 1000 - metrics.cost;

    // 지표별 독립 정규화 후 가중치 적용
    const agencyRaw    = norm(metrics.agency,    AGENCY_MIN,    AGENCY_MAX);
    const inclusionRaw = norm(metrics.inclusion, INCLUSION_MIN, INCLUSION_MAX);
    const sustainRaw   = norm(metrics.sustain,   SUSTAIN_MIN,   SUSTAIN_MAX);

    const agency    = Math.min(100, Math.round(agencyRaw    * W_AGENCY));
    const inclusion = Math.min(100, Math.round(inclusionRaw * W_INCLUSION));
    const sustain   = Math.min(100, Math.round(sustainRaw   * W_SUSTAIN));

    const effAuto = norm(metrics.eff, E_MIN, E_MAX);
    const invest  = Math.min(100, Math.round(costSpent / C_MAX * 100));
    const overall = Math.round((agency + inclusion + sustain) / 3);

    const persona = overall >= 70 ? '인간 중심의 파트너 🤝'
                  : overall >= 40 ? '실용적 균형주의자 ⚖️'
                  :                 '냉혹한 효율주의자 🤖';

    document.getElementById('persona-txt').innerText = `아키텍처 페르소나: ${{persona}}`;

    const changeLabel = p =>
      p === 0  ? '완전 자동화 수준 (변화 없음)' :
      p < 25   ? `완전 자동화 대비 +${{p}}% (낮음)` :
      p < 60   ? `완전 자동화 대비 +${{p}}% (중간)` :
                 `완전 자동화 대비 +${{p}}% (높음)`;
    const cls = p => p >= 50 ? 'pos' : p >= 25 ? 'neu' : 'neg';

    setTimeout(() => {{
      setKpi('agency',    agency,    changeLabel(agency),    cls(agency));
      setKpi('inclusion', inclusion, changeLabel(inclusion), cls(inclusion));
      setKpi('sustain',   sustain,   changeLabel(sustain),   cls(sustain));

      document.getElementById('v-eff').innerText   = effAuto + '%';
      document.getElementById('b-eff').style.width = effAuto + '%';
      document.getElementById('c-eff').innerText   =
        effAuto >= 75 ? '자동화 의존도 높음 — 인간 개입 최소화' :
        effAuto >= 40 ? '자동화와 인간 개입의 혼합' :
                        '인간 중심 처리 비율 높음';
      document.getElementById('c-eff').className = 'kpi-change ' + (effAuto >= 75 ? 'neg' : effAuto >= 40 ? 'neu' : 'pos');

      setKpi('invest', invest,
        invest >= 60 ? '적극적 인간 중심 투자' : invest >= 30 ? '부분 투자' : '최소 투자',
        invest >= 60 ? 'pos' : invest >= 30 ? 'neu' : 'neg');

      document.getElementById('v-overall').innerText = overall + '%';
    }}, 100);

    finalData = {{
      metrics, history, persona,
      userName: USER_NAME,
      scores: {{ agency, inclusion, sustain, effAuto, invest, overall }}
    }};
  }}

  function submitResult() {{
    if (!finalData) return;
    const btn = document.getElementById('submit-btn');
    const msg = document.getElementById('status-msg');
    btn.disabled = true;
    msg.className = 'status-msg s-ing';
    msg.innerText = '⏳ Google Sheets에 저장 중입니다...';

    const encoded = encodeURIComponent(JSON.stringify(finalData));
    const url = GAS_URL + '?save=' + encoded;

    const img = new Image();
    img.onload = img.onerror = function() {{
      msg.className = 'status-msg s-ok';
      msg.innerHTML = '✅ <b>저장 완료!</b> Google Sheets에 결과가 기록되었습니다. 수고하셨습니다 😊';
      btn.innerText = '✅ 제출 완료';
      btn.style.background = '#28a745';
    }};
    img.src = url;
  }}

  render();
</script>
</body>
</html>
"""

components.html(html_code, height=820, scrolling=False)
