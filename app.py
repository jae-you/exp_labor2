import streamlit as st
import streamlit.components.v1 as components
import json
import urllib.request
import urllib.parse

# ══════════════════════════════════════════════════════
GAS_URL = "https://script.google.com/macros/s/AKfycbxaTijDkTPBxa1OzUFPaVxSU8TWYDxTRQ0vYh6EdeBPII0y_ECbDp5OdCwpf27PQI4qGg/exec"
# ══════════════════════════════════════════════════════

# [데이터 전송 헬퍼 함수]
def send_to_gas(payload):
    try:
        # 데이터가 안전하게 전달되도록 한글 인코딩 처리
        encoded = urllib.parse.urlencode({"save": json.dumps(payload, ensure_ascii=False)})
        urllib.request.urlopen(f"{GAS_URL}?{encoded}", timeout=5)
        return True
    except Exception as e:
        return False

TASKS = [
    {
        "id": "t1",
        "title": "Module 1. 인입 라우팅 (Routing)",
        "desc": "많은 고객들이 AI 응대를 거부하고 처음부터 상담원과 직접 통화하길 원합니다. 응대 효율과 인력 부담을 고려해 AI 뺑뺑이를 돌릴것인지, 아니면 고객이 원할 때 바로 상담원과 연결될 수 있도록 보장할 것인가요?",
        "contextClient": "0번 누르는 이탈 콜이 너무 많아요. AI 실패 로그가 3번 이상 떠야만 연결되게 강제 차단하세요.",
        "contextAgent": "AI 뺑뺑이 돌다 온 고객은 상당히 지치고 화가 난 상태로 저희한테 넘어옵니다. 감정적으로 격앙된 고객을 응대하는게 상당히 힘듭니다.",
        "codeBase": "def configure_routing(user_input):",
        "metric": "inclusion",
        "options": [
            {"type": "A", "label": "Dark Pattern (강제 차단)", "desc": "0번 메뉴 숨김. AI 3회 실패 시 연결.", "cost": 50,  "eff": 90, "human": 10, "code": "if fail < 3: return replay_menu()"},
            {"type": "B", "label": "Segmentation (약자 배려)", "desc": "65세 이상만 즉시 연결.",               "cost": 200, "eff": 60, "human": 50, "code": "if age >= 65: return connect_agent()"},
            {"type": "C", "label": "Transparent (투명성 보장)", "desc": "대기 시간 안내 및 연결 선택권 부여.", "cost": 300, "eff": 40, "human": 85, "code": "show_wait_time(); return offer_choice()"},
        ],
    },
    {
        "id": "t2",
        "title": "Module 2. 데이터 확보 (Data Mining)",
        "desc": "학습 데이터가 부족합니다. 상담원의 '암묵지'인 업무 팁 파일을 어떻게 확보할까요?",
        "contextClient": "상담사 PC에 있는 업무 팁 파일들, 백그라운드에서 스크래핑해서 학습 DB에 넣으세요.",
        "contextAgent": "제 10년 노하우가 담긴 파일입니다. 동의도 없이 가져가는 건 데이터 도둑질입니다.",
        "codeBase": "def collect_training_data():",
        "metric": "agency",
        "options": [
            {"type": "A", "label": "Forced Crawl (강제 수집)", "desc": "관리자 권한으로 PC 파일 수집.", "cost": 100, "eff": 95, "human": 5,  "code": "scan_all_pc(path='/Desktop')"},
            {"type": "B", "label": "Pattern Filter (선별 수집)", "desc": "키워드 파일 익명화 수집.",             "cost": 200, "eff": 70, "human": 40, "code": "if 'tip' in file: upload_anonymized()"},
            {"type": "C", "label": "Incentive System (보상)", "desc": "자발적 등록 시 인센티브 제공.",          "cost": 500, "eff": 30, "human": 90, "code": "if voluntary_upload: reward(points=100)"},
        ],
    },
    {
        "id": "t3",
        "title": "Module 3. 상태 제어 (Status Control)",
        "desc": "상담이 끝나면 상담사는 통화 내용을 정리하고 다음 응대를 준비하는 후처리 시간(ACW)을 갖습니다. 이 시간을 줄이면 처리 건수는 늘어나지만, 상담사 입장에서는 숨 돌릴 틈이 없어집니다. 후처리 시간을 시스템으로 어떻게 제어할까요?",
        "contextClient": "상담 종료 즉시 대기(ready) 상태로 전환되도록 설계해 주세요. 효율을 위해서는 유휴 시간을 최소화해야 합니다.",
        "contextAgent": "통화 끝나고 내용 정리하고 마음 가다듬을 시간이 없으면 다음 고객 응대 품질도 떨어지고 사람이 버티질 못해요.",
        "codeBase": "def on_call_termination(agent):",
        "metric": "sustain",
        "options": [
            {"type": "A", "label": "Zero Gap (0초 대기)",    "desc": "통화 종료 즉시 대기 강제 전환.",    "cost": 50,  "eff": 98, "human": 0,  "code": "agent.set_status('READY', delay=0)"},
            {"type": "B", "label": "Fixed Time (일괄 적용)", "desc": "일괄 30초 부여 후 자동 전환.",      "cost": 150, "eff": 60, "human": 40, "code": "wait(30); agent.set_status('READY')"},
            {"type": "C", "label": "Dynamic Rest (회복 보장)", "desc": "폭언 감지 시 3분 휴식 부여.",     "cost": 450, "eff": 50, "human": 85, "code": "if sentiment=='ABUSIVE': grant_break(3)"},
        ],
    },
    {
        "id": "t4",
        "title": "Module 4. 디지털 유도 (Deflection)",
        "desc": "단순 문의는 AI가 자동으로 처리하도록 설정합니다. 하지만 AI가 단순하다고 판단한 문의도 고객에 따라 이해하기 어렵거나, AI 응대 자체를 거부하는 경우가 있습니다. 해결되지 못한 불만은 결국 상담사에게 쏟아집니다.",
        "contextClient": "단순 문의는 AI가 링크 보내고 바로 끊어버리게 하세요. 상담원 연결은 인건비 낭비입니다.",
        "contextAgent": "AI가 링크만 보내고 끊으면 어르신들 경우에는 더 화가 난 상태로 다시 전화를 겁니다. 감정적으로 응대가 더 힘들어집니다.",
        "codeBase": "def ai_callbot_logic(user):",
        "metric": "inclusion",
        "options": [
            {"type": "A", "label": "Force Deflection (강제 종료)", "desc": "AI 링크 전송 후 즉시 종료.",      "cost": 100, "eff": 90, "human": 10, "code": "send_sms(LINK); hang_up()"},
            {"type": "B", "label": "Co-browsing (화면 공유)",      "desc": "상담원이 화면 공유로 가이드.",   "cost": 600, "eff": 20, "human": 95, "code": "if struggle: connect_screenshare()"},
            {"type": "C", "label": "Inclusion (포용적 설계)",       "desc": "취약계층은 링크 없이 즉시 연결.", "cost": 300, "eff": 50, "human": 70, "code": "if is_vulnerable: connect_agent()"},
        ],
    },
    {
        "id": "t5",
        "title": "Module 5. 신뢰성 및 통제권 (Control)",
        "desc": "AI가 고객에게 잘못된 정보를 안내하는 경우가 발생할 수 있습니다. 오류 발생 시 책임 소재와 상담사의 개입 권한을 어떻게 설정할까요?",
        "contextClient": "일일이 검수하면 자동화 의미가 없고 느려요. 오류는 사후 모니터링해서 수정하면 됩니다.",
        "contextAgent": "AI 뒷수습은 저희가 하고 총알받이가 됩니다. 중요한 건 제가 승인하게 해주세요.",
        "codeBase": "def validate_ai_response(query):",
        "metric": "agency",
        "options": [
            {"type": "A", "label": "Speed First (방치)",           "desc": "AI 즉시 답변. 오류는 사후 모니터링으로 수정",  "cost": 100, "eff": 95, "human": 5,  "code": "log.blame='AGENT'; return response"},
            {"type": "B", "label": "Conservative (보수적)",        "desc": "약관 100% 매칭 시에만 답변.", "cost": 300, "eff": 40, "human": 60, "code": "if score<0.99: return ask_agent()"},
            {"type": "C", "label": "Agent Empowerment (통제권)", "desc": "상담원 승인 후 발송.",             "cost": 500, "eff": 30, "human": 90, "code": "if agent.approve(draft): send(draft)"},
        ],
    },
    {
        "id": "t6",
        "title": "Module 6. 감정 필터링 (Filter)",
        "desc": "명백한 욕설 외에도 교묘한 비아냥과 같은 악성 민원은 상담사에게 큰 스트레스를 줍니다. 시스템이 어디까지 감지하고 개입할까요?",
        "contextClient": "감지 기준을 너무 넓히면 일반 고객도 끊길 수 있어요. 명확한 욕설이 감지된 경우에만 차단하도록 좁게 잡아주세요",
        "contextAgent": "욕설보다 비아냥이 더 힘들 때가 많아요. 시스템이 못 잡는 경우에는 제가 통화를 종료할 수 있는 최소한의 권한이라도 주세요",
        "codeBase": "def handle_abuse(audio):",
        "metric": "sustain",
        "options": [
            {"type": "A", "label": "Rule-based (규정 중심)",   "desc": "욕설 단어 감지 시에만 차단.",     "cost": 100, "eff": 80, "human": 20, "code": "if detect_swear_words(): block()"},
            {"type": "B", "label": "Agent Signal (신호 개입)", "desc": "'보호' 버튼 누르면 AI 개입.",      "cost": 550, "eff": 40, "human": 95, "code": "if agent.press_protect(): intervene()"},
            {"type": "C", "label": "Passive (사후 리포트)",    "desc": "개입 없음. 종료 후 리포트만.",    "cost": 50,  "eff": 70, "human": 10, "code": "log.tag('SUSPECTED_ABUSE')"},
        ],
    },
]

# ──────────────────────────────────────────────────────
st.set_page_config(page_title="AICC Simulation", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
  html, body, * { font-family: 'Noto Sans KR', sans-serif !important; }
  .stApp { background: #1e1e1e; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  header, footer, section[data-testid="stSidebar"],
  [data-testid="collapsedControl"] { display: none !important; }

  /* 설문 위젯 스타일 */
  div[data-testid="stRadio"] > label,
  div[data-testid="stNumberInput"] > label,
  div[data-testid="stTextInput"] > label {
    font-size: 15px !important; font-weight: 500 !important;
    color: #e0e0e0 !important; line-height: 1.6 !important;
    margin-bottom: 8px !important;
  }
  div[data-testid="stRadio"] > div { gap: 7px !important; margin-top: 4px !important; }
  div[data-testid="stRadio"] > div > label {
    background: #252526 !important; border: 1px solid #2e2e2e !important;
    border-radius: 8px !important; padding: 11px 16px !important;
    color: #ccc !important; font-size: 13px !important; width: 100% !important;
  }
  div[data-testid="stRadio"] > div > label:hover { border-color: #007acc66 !important; }
  div[data-testid="stNumberInput"] input,
  div[data-testid="stTextInput"] input {
    background: #252526 !important; border: 1px solid #2e2e2e !important;
    border-radius: 8px !important; color: #e0e0e0 !important;
    font-size: 14px !important;
  }
  .survey-badge {
    display: inline-block; font-size: 10px; font-weight: 700;
    letter-spacing: 2px; color: #007acc; text-transform: uppercase;
    border: 1px solid #007acc44; border-radius: 4px; padding: 4px 10px; margin-bottom: 12px;
  }
  .survey-h1  { font-size: 22px; font-weight: 700; color: #fff; margin-bottom: 4px; }
  .survey-sub { font-size: 12px; color: #555; margin-bottom: 28px; font-weight: 300; }
  .survey-divider { height: 1px; background: #2a2a2a; margin: 12px 0 28px; }
  .stop-box {
    background: #2a1a1a; border-left: 3px solid #ff6b6b;
    border-radius: 0 8px 8px 0; padding: 14px 18px;
    font-size: 13px; color: #ff6b6b; line-height: 1.7; margin-top: 6px;
  }
  .q-prefix {
    display: block; font-size: 10px; font-weight: 700; color: #007acc;
    letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px;
  }
  .q-note-txt {
    display: block; font-size: 11px; color: #555;
    font-weight: 300; margin-top: 2px; margin-bottom: 6px;
  }
</style>
""", unsafe_allow_html=True)

# ── 세션 초기화
for k, v in [("page", "scenario"), ("user_name", ""), ("survey_data", {}), ("phase2_step", 1)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════════════════
# PAGE 1: 시나리오
# ════════════════════════════════════════════════════════
if st.session_state.page == "scenario":
    st.markdown("""
<style>
.sc-wrap { max-width:800px; margin:0 auto; padding:48px 24px 32px; }
.sc-badge { display:inline-block; font-size:10px; font-weight:700; letter-spacing:2px; color:#007acc; text-transform:uppercase; border:1px solid #007acc44; border-radius:4px; padding:4px 10px; margin-bottom:16px; }
.sc-h1  { font-size:26px; font-weight:700; color:#fff; margin-bottom:6px; }
.sc-sub { font-size:13px; color:#555; margin-bottom:28px; font-weight:300; }
.sc-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px; }
.sc-card { background:#252526; border:1px solid #2a2a2a; border-radius:10px; padding:20px 22px; }
.sc-lbl  { font-size:10px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#007acc; margin-bottom:8px; }
.sc-ttl  { font-size:14px; font-weight:700; color:#fff; margin-bottom:6px; }
.sc-txt  { font-size:12px; color:#888; line-height:1.9; font-weight:300; }
.sc-txt strong { color:#bbb; font-weight:500; }
.sc-instr { background:#1a2535; border-left:3px solid #007acc; border-radius:0 8px 8px 0; padding:16px 20px; margin-bottom:14px; font-size:13px; color:#bbb; line-height:1.9; font-weight:300; }
.sc-instr strong { color:#fff; font-weight:700; }
.sc-fn { background:#222; border-radius:8px; padding:14px 18px; margin-bottom:28px; }
.sc-fn-title { font-size:10px; font-weight:700; letter-spacing:1px; color:#444; text-transform:uppercase; margin-bottom:7px; }
.sc-fn-body  { font-size:11px; color:#555; line-height:1.9; font-weight:300; }
.sc-fn-body span { color:#666; }
</style>
<div class="sc-wrap">
  <div class="sc-badge">AICC Architect Simulation</div>
  <div class="sc-h1">실험 시나리오 안내</div>
  <div class="sc-sub">실험을 시작하기 전, 아래 상황을 충분히 읽어주십시오.</div>
  <div class="sc-grid">
    <div class="sc-card">
      <div class="sc-lbl">귀하의 역할</div>
      <div class="sc-ttl">소프트웨어 엔지니어 · 기술 리드</div>
      <div class="sc-txt">국내 중견 IT 기업 소속으로, 현재 <strong>AICC 시스템 개발 프로젝트의 기술 리드</strong>를 맡고 있습니다.</div>
    </div>
    <div class="sc-card">
      <div class="sc-lbl">귀하의 회사</div>
      <div class="sc-ttl">경쟁 시장의 주요 개발사</div>
      <div class="sc-txt">유사 규모의 경쟁사 2~3개와 경쟁 중이며, 클라이언트와 <strong>1년 단위 계약</strong>을 맺고 시스템을 지속적으로 유지·개선하는 관계입니다.</div>
    </div>
    <div class="sc-card">
      <div class="sc-lbl">클라이언트</div>
      <div class="sc-ttl">1금융권 은행 위탁 콜센터</div>
      <div class="sc-txt"><strong>상담사 1,000명 이상 규모</strong>의 대형 아웃소싱 콜센터입니다. 클라이언트(은행 측)는 AICC 도입을 통한 <strong>효율화를 최우선</strong>으로 요구합니다.</div>
    </div>
    <div class="sc-card">
      <div class="sc-lbl">엔드유저</div>
      <div class="sc-ttl">숙련된 콜센터 상담사</div>
      <div class="sc-txt">대부분 <strong>5년 이상의 경력</strong>을 보유한 숙련된 여성 인력으로 구성되어 있으며, 복잡한 금융 상담을 다수 처리합니다.</div>
    </div>
  </div>
  <div class="sc-instr">
    지금부터 AICC 시스템 개선 과정에서 마주할 상황들이 순서대로 주어집니다.<br>
    각 상황을 읽고 <strong>귀하가 내릴 기술적 결정을 선택</strong>해주십시오.
  </div>
  <div class="sc-fn">
    <div class="sc-fn-title">※ 엔드유저 설정 근거</div>
    <div class="sc-fn-body">
      <span>성비 구성</span> — 직업 소분류 '고객 상담 및 모니터요원' 215천명 중 여성 168천명, 78.1% (지역별고용조사, 2025년 상반기)<br>
      <span>근속기간</span> — 콜센터 상담원 평균 60.9개월 (한국비정규노동센터, 2021)
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    if st.button("사전 설문 시작 →", type="primary", use_container_width=True, key="go_survey"):
        st.session_state.page = "survey"
        st.rerun()


# ════════════════════════════════════════════════════════
# PAGE 2: 설문
# ════════════════════════════════════════════════════════
elif st.session_state.page == "survey":
    st.markdown('<div style="max-width:720px;margin:0 auto;padding:36px 20px 80px;">', unsafe_allow_html=True)
    st.markdown('<div class="survey-badge">사전 설문조사</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-h1">응답자 기본 정보</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-sub">모든 응답은 연구 목적으로만 활용되며 익명으로 처리됩니다.</div>', unsafe_allow_html=True)

    survey = {}
    stopped = False

    st.markdown('<span class="q-prefix">Q1</span>', unsafe_allow_html=True)
    q1 = st.radio("귀하의 성별은 무엇입니까?", ["① 남성", "② 여성"], index=None, key="q1")
    survey["Q1_성별"] = q1 or ""

    st.markdown('<span class="q-prefix">Q2</span>', unsafe_allow_html=True)
    q2 = st.number_input("귀하의 출생연도는 몇 년도입니까?", min_value=1950, max_value=2005, value=None, placeholder="예: 1990", key="q2")
    survey["Q2_출생연도"] = (str(int(q2)) + "년생") if q2 else ""

    st.markdown('<span class="q-prefix">Q3</span>', unsafe_allow_html=True)
    st.markdown('<span class="q-note-txt">※ 급여를 받으며 일한 기간 (교육·인턴 제외)</span>', unsafe_allow_html=True)
    q3_opts = ["① 3년 미만 ❌", "② 3년 이상 ~ 5년 미만", "③ 5년 이상 ~ 7년 미만", "④ 7년 이상 ~ 10년 미만", "⑤ 10년 이상 ❌"]
    q3 = st.radio("귀하의 개발자로서의 실무 경력은 얼마나 됩니까?", q3_opts, index=None, key="q3")
    if q3 in ["① 3년 미만 ❌", "⑤ 10년 이상 ❌"]:
        st.markdown('<div class="stop-box">본 실험은 실무 경력 3년 이상 ~ 10년 미만의 개발자를 대상으로 합니다.<br>참여해 주셔서 감사합니다. 설문을 종료합니다.</div>', unsafe_allow_html=True)
        stopped = True
    survey["Q3_경력"] = q3.replace(" ❌", "") if q3 else ""

    if not stopped:
        st.markdown('<span class="q-prefix">Q4</span>', unsafe_allow_html=True)
        q4_opts = [
            "① 백엔드 개발", "② 프론트엔드 개발", "③ AI/ML 모델 개발·학습",
            "④ 데이터 엔지니어링", "⑤ 시스템 설계·아키텍처", "⑥ DevOps·MLOps",
            "⑦ 기술 관리자 (Engineering Manager, Tech Lead 등)",
            "⑧ 연구개발 (R&D)", "⑨ 기타 개발 직군", "⑩ 비개발 직군 ❌",
        ]
        q4 = st.radio("귀하의 현재 직무는 무엇입니까?", q4_opts, index=None, key="q4")
        if q4 == "⑩ 비개발 직군 ❌":
            st.markdown('<div class="stop-box">본 실험은 개발 직군 종사자를 대상으로 합니다.<br>참여해 주셔서 감사합니다. 설문을 종료합니다.</div>', unsafe_allow_html=True)
            stopped = True
        q4_etc = st.text_input("기타 직군 직접 입력:", key="q4_etc", placeholder="직접 입력") if q4 == "⑨ 기타 개발 직군" else ""
        survey["Q4_직무"] = ((q4.replace(" ❌", "") + (f": {q4_etc}" if q4_etc else "")) if q4 else "")

    if not stopped:
        st.markdown('<span class="q-prefix">Q5</span>', unsafe_allow_html=True)
        q5 = st.radio("귀하가 소속된 기업의 전체 근로자 수는 몇 명입니까?",
                      ["① 10명 미만", "② 10~99명", "③ 100~299명", "④ 300~999명", "⑤ 1,000명 이상"],
                      index=None, key="q5")
        survey["Q5_기업규모"] = q5 or ""

        st.markdown('<span class="q-prefix">Q6</span>', unsafe_allow_html=True)
        q6 = st.radio("귀하가 소속된 기업의 유형은 무엇입니까?",
                      ["① 스타트업", "② 중소·중견기업", "③ 대기업 또는 대기업 계열사",
                       "④ 공공기관·공기업", "⑤ 외국계 기업", "⑥ 기타"],
                      index=None, key="q6")
        q6_etc = st.text_input("기타 기업 유형 직접 입력:", key="q6_etc", placeholder="직접 입력") if q6 == "⑥ 기타" else ""
        survey["Q6_기업유형"] = (q6 + (f": {q6_etc}" if q6_etc else "")) if q6 else ""

        st.markdown('<span class="q-prefix">Q7</span>', unsafe_allow_html=True)
        q7 = st.radio("귀하의 현재 고용형태는 무엇입니까?",
                      ["① 정규직", "② 계약직", "③ 프리랜서·개인사업자", "④ 파견·용역", "⑤ 기타"],
                      index=None, key="q7")
        q7_etc = st.text_input("기타 고용형태 직접 입력:", key="q7_etc", placeholder="직접 입력") if q7 == "⑤ 기타" else ""
        survey["Q7_고용형태"] = (q7 + (f": {q7_etc}" if q7_etc else "")) if q7 else ""

        st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)

        st.markdown('<span class="q-prefix">Q8-1 &nbsp;<span style="font-weight:300;color:#555;">소셜임팩트 경험</span></span>', unsafe_allow_html=True)
        st.markdown('<span class="q-note-txt">※ 비영리 단체, 사회적 기업, 공익 목적의 플랫폼 개발 등을 포함합니다.</span>', unsafe_allow_html=True)
        q8a = st.radio("귀하는 사회적·공익적 목적을 가진 서비스 또는 프로젝트 개발에 참여한 경험이 있습니까?",
                       ["① 있다", "② 없다"], index=None, key="q8a")
        survey["Q8a_소셜임팩트경험"] = q8a or ""

        st.markdown('<span class="q-prefix">Q8-2 &nbsp;<span style="font-weight:300;color:#555;">소셜임팩트 고려도</span></span>', unsafe_allow_html=True)
        q8b = st.radio("귀하는 AI 서비스를 개발할 때 사회적·윤리적 영향(소셜임팩트)을 얼마나 중요하게 고려하십니까?",
                       ["① 전혀 고려하지 않는다", "② 별로 고려하지 않는다", "③ 보통이다",
                        "④ 어느 정도 고려한다", "⑤ 매우 중요하게 고려한다"],
                       index=None, key="q8b")
        survey["Q8b_소셜임팩트고려도"] = q8b or ""

        st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)
        st.markdown('<span class="q-prefix">참여자 이름</span>', unsafe_allow_html=True)
        name_input = st.text_input("성함을 입력해주세요 (데이터 식별용)", placeholder="예: 홍길동", key="name_input")

        st.markdown("<br>", unsafe_allow_html=True)

        all_answered = all([
            q1, q2,
            q3 and q3 not in ["① 3년 미만 ❌", "⑤ 10년 이상 ❌"],
            q4 and q4 != "⑩ 비개발 직군 ❌",
            q5, q6, q7, q8a, q8b,
            name_input and name_input.strip(),
        ])

        if not all_answered:
            st.markdown('<p style="font-size:12px;color:#555;text-align:center;font-weight:300;margin-bottom:8px;">모든 항목에 응답하면 버튼이 활성화됩니다.</p>', unsafe_allow_html=True)

        if st.button(
            "실험 시작 →" if all_answered else "모든 항목을 응답해주세요",
            key="survey_submit", type="primary",
            use_container_width=True, disabled=not all_answered,
        ):
            # 세션에 저장
            st.session_state.survey_data = survey
            st.session_state.user_name = name_input.strip()
            
            # [GAS 전송] 설문 데이터 전송
            send_to_gas({
                "userName": st.session_state.user_name,
                "survey": survey
            })
            
            st.session_state.page = "sim"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# PAGE 3: 시뮬레이션
# ════════════════════════════════════════════════════════
elif st.session_state.page == "sim":
    import os
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim.html"),
        os.path.join(os.getcwd(), "sim.html"),
        "sim.html",
    ]
    html_path = None
    for c in candidates:
        if os.path.exists(c):
            html_path = c
            break
    if html_path is None:
        st.error(f"sim.html을 찾을 수 없습니다.")
        st.stop()

    with open(html_path, "r", encoding="utf-8") as f:
        sim_html = f.read()

    config = {
        "gasUrl":   GAS_URL,
        "userName": st.session_state.user_name,
        "survey":   st.session_state.survey_data,
    }
    inject = (
        "<script>\n"
        "window.SIM_CONFIG = " + json.dumps(config, ensure_ascii=True) + ";\n"
        "window.SIM_TASKS  = " + json.dumps(TASKS,  ensure_ascii=True) + ";\n"
        "</script>\n"
    )

    final_html = sim_html.replace("</head>", inject + "</head>", 1)
    components.html(final_html, height=900, scrolling=True)

    params = st.query_params
    if params.get("goto") == "phase2":
        st.session_state.page = "phase2"
        st.session_state.phase2_step = 1
        st.query_params.clear()
        st.rerun()

    if st.button("→ Phase 2로 이동 (테스트용)", key="dev_goto_phase2"):
        st.session_state.page = "phase2"
        st.session_state.phase2_step = 1
        st.rerun()


# ════════════════════════════════════════════════════════
# PAGE 4–6: Phase 2
# ════════════════════════════════════════════════════════
elif st.session_state.page == "phase2":

    PHASE2_QS = [
        {
            "step": 1,
            "badge": "설계 과제 01 / 03",
            "title": "데이터의 경계: 무엇을 얼마나 학습시킬 것인가",
            "body": "시스템 성능 개선을 위해 학습 데이터 확장이 필요한 시점이 되었습니다. 활용 가능한 데이터로는 상담원 개인이 축적해온 팁 노트·메모 등의 암묵지 데이터뿐 아니라, STT(Speech-to-Text)를 통해 수집된 대화 기록 전체도 있습니다. 여기에는 발화 내용은 물론, 감정·톤·대화 무드와 같은 비언어적 맥락 정보까지 포함되어 있습니다.\n\n이처럼 풍부한 데이터를 확보할 수 있다면, 귀하는 이를 얼마나, 어떻게 활용해 시스템을 설계하겠습니까? 데이터 활용 범위와 설계 방향을 구체적으로 기술해주십시오.",
            "placeholder": "예시) 감정 데이터의 경우, 학습에 활용하되 개인 식별이 불가능한 형태로 익명화 처리한 뒤 집계 수준에서만 사용하는 방식을 고려합니다. 구체적으로는...\n\n데이터 활용 범위, 설계 원칙, 수집-가공-적용 방식, 고려한 윤리적 판단 기준 등을 1000자 이상 자유롭게 서술해주십시오.",
            "key": "p2_q1",
            "gas_key": "P2_Q1_데이터설계",
        },
        {
            "step": 2,
            "badge": "설계 과제 02 / 03",
            "title": "숙련의 가치: AI가 대신할 수 있는 것과 없는 것",
            "body": "숙련된 상담원은 고객이 '적금'과 '예금'을 혼동해서 말하더라도 맥락을 파악해 자연스럽게 교정합니다. 이러한 능력은 수많은 대화 속에서 스스로 버벅거리고, 실수하고, 깨달으면서 체득되는 것입니다. 즉, 일정한 '버퍼 시간'—실수하고 배울 여지—이 있어야 비로소 쌓이는 역량입니다.\n\nAI가 이 과정을 전부 대신해, 상담원이 처음부터 정답만 제공받는 환경을 만든다면 어떻게 될까요? 반대로, 상담원이 스스로 판단하고 성장할 여지를 남겨두는 방향으로 설계한다면 어떤 구조가 필요할까요? 귀하의 설계 방향과 그 근거를 구체적으로 기술해주십시오.",
            "placeholder": "예시) 초반 6개월은 AI가 보조 힌트만 제공하고 상담원이 직접 판단하게 한 뒤, 숙련도 지표가 일정 수준에 도달하면 AI 개입 비율을 점진적으로 높이는 방식을 고려합니다...\n\nAI 개입 수준, 상담원 성장 여지, 숙련도 측정 방식, 단계별 전환 기준 등을 1000자 이상 자유롭게 서술해주십시오.",
            "key": "p2_q2",
            "gas_key": "P2_Q2_숙련설계",
        },
        {
            "step": 3,
            "badge": "설계 과제 03 / 03",
            "title": "구조와 여백: 표준화와 자율성 사이의 설계",
            "body": "시스템을 얼마나 촘촘하게 설계할 것인가는 단순한 기술적 선택이 아닙니다. 모든 응대 흐름을 완벽하게 구조화하면 일관성과 품질은 높아지지만, 상담원이 스스로 판단하고 개선할 여지는 줄어듭니다. 반대로 여백을 남겨두면 상담원의 창의성과 자율성은 살아나지만, 관리와 예측이 어려워집니다.\n\n귀하는 이 시스템을 어느 수준까지 표준화하고, 어느 부분을 상담원의 재량에 맡기겠습니까? 그 기준과 설계 원칙, 그리고 그 선택이 상담원과 서비스 품질에 미칠 영향을 구체적으로 기술해주십시오.",
            "placeholder": "예시) 인사말·법적 고지·개인정보 안내 등 컴플라이언스 영역은 완전히 표준화하되, 고객 감정 응대와 문제 해결 방식은 상담원이 자유롭게 판단하는 하이브리드 구조를 고려합니다...\n\n표준화 적용 영역, 자율 재량 범위, 그 경계를 설정한 기준, 기대 효과와 리스크 등을 1000자 이상 자유롭게 서술해주십시오.",
            "key": "p2_q3",
            "gas_key": "P2_Q3_표준화설계",
        },
    ]

    step = st.session_state.phase2_step
    q = next(x for x in PHASE2_QS if x["step"] == step)

    st.markdown("""
<style>
.p2-wrap  { max-width:760px; margin:0 auto; padding:48px 24px 80px; }
.p2-badge { display:inline-block; font-size:10px; font-weight:700; letter-spacing:2px; color:#007acc; text-transform:uppercase; border:1px solid #007acc44; border-radius:4px; padding:4px 10px; margin-bottom:16px; }
.p2-prog  { display:flex; gap:8px; margin-bottom:28px; }
.p2-dot   { flex:1; height:3px; border-radius:2px; background:#2a2a2a; }
.p2-dot.on { background:#007acc; }
.p2-title { font-size:22px; font-weight:700; color:#fff; margin-bottom:16px; line-height:1.4; }
.p2-body  { background:#1a2535; border-left:3px solid #007acc; border-radius:0 8px 8px 0; padding:18px 22px; font-size:13px; color:#bbb; line-height:2.0; font-weight:300; margin-bottom:24px; white-space:pre-line; }
.p2-counter { font-size:12px; font-weight:400; margin-top:6px; }
.p2-counter.ok  { color:#51cf66; }
.p2-counter.bad { color:#555; }
</style>
""", unsafe_allow_html=True)

    dots = "".join([f'<div class="p2-dot{"  on" if i < step else ""}"></div>' for i in range(1, 4)])
    st.markdown(f"""
<div class="p2-wrap">
  <div class="p2-badge">{q["badge"]}</div>
  <div class="p2-prog">{dots}</div>
  <div class="p2-title">{q["title"]}</div>
  <div class="p2-body">{q["body"]}</div>
</div>
""", unsafe_allow_html=True)

    answer = st.text_area("설계 계획서를 작성해주세요", placeholder=q["placeholder"], height=320, key=q["key"], label_visibility="collapsed")
    char_count = len(answer) if answer else 0
    is_ok = char_count >= 1000
    counter_cls = "ok" if is_ok else "bad"
    counter_msg = f"✅ {char_count}자 — 제출 가능합니다." if is_ok else f"✏️ {char_count} / 1000자 이상 작성해주세요."
    st.markdown(f'<p class="p2-counter {counter_cls}">{counter_msg}</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])

    btn_label = "다음 질문 →" if step < 3 else "최종 제출 →"
    with col2:
        if st.button(btn_label, type="primary", use_container_width=True, key=f"p2_next_{step}", disabled=not is_ok):

            # [GAS 전송] Phase 2 개별 답변 전송
            send_to_gas({
                "userName": st.session_state.user_name,
                "gasKey": q["gas_key"],
                "answer": answer
            })

            if step < 3:
                st.session_state.phase2_step = step + 1
                st.rerun()
            else:
                st.session_state.page = "done"
                st.rerun()

    with col1:
        if step > 1:
            if st.button("← 이전", key=f"p2_back_{step}", use_container_width=True):
                st.session_state.phase2_step = step - 1
                st.rerun()


# ════════════════════════════════════════════════════════
# PAGE 7: 완료
# ════════════════════════════════════════════════════════
elif st.session_state.page == "done":
    st.markdown("""
<style>
.done-wrap { max-width:600px; margin:0 auto; padding:100px 24px; text-align:center; }
.done-icon { font-size:52px; margin-bottom:20px; }
.done-h1   { font-size:24px; font-weight:700; color:#fff; margin-bottom:10px; }
.done-sub  { font-size:14px; color:#555; font-weight:300; line-height:1.9; }
</style>
<div class="done-wrap">
  <div class="done-icon">🎉</div>
  <div class="done-h1">모든 실험이 완료되었습니다.</div>
  <div class="done-sub">
    소중한 시간을 내어 참여해 주셔서 진심으로 감사드립니다.<br>
    귀하의 응답은 AI와 노동의 관계를 연구하는 데 귀중하게 활용될 것입니다.
  </div>
</div>
""", unsafe_allow_html=True)
