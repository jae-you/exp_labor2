import streamlit as st
import streamlit.components.v1 as components
import json

# =====================================================================
GAS_URL = "https://script.google.com/macros/s/AKfycbxoYKj_-UCP_U90AzmTMNE-M1J9oPfmubEvrMBFyCdWkVjwZsNOvfmKCPHqyAYaT58NHg/exec"
# =====================================================================

st.set_page_config(
    page_title="NextAI Architect Console",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* ── 기본 레이아웃 ── */
    .stApp { background-color: #1e1e1e; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header, footer { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    div[data-testid="stVerticalBlock"] { gap: 0 !important; }

    /* ── 설문 페이지 전용 ── */
    html, body, [class*="css"], .stApp, * {
        font-family: 'Noto Sans KR', sans-serif !important;
    }

    /* 질문 레이블 */
    div[data-testid="stRadio"] > label,
    div[data-testid="stNumberInput"] > label,
    div[data-testid="stTextInput"] > label {
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #e0e0e0 !important;
        line-height: 1.6 !important;
        margin-bottom: 8px !important;
        padding-bottom: 0 !important;
    }

    /* 라디오 옵션 간격 */
    div[data-testid="stRadio"] > div { gap: 7px !important; margin-top: 4px !important; }

    /* 라디오 옵션 카드 */
    div[data-testid="stRadio"] > div > label {
        background: #252526 !important;
        border: 1px solid #2e2e2e !important;
        border-radius: 8px !important;
        padding: 11px 16px !important;
        color: #ccc !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        transition: border-color 0.15s !important;
        width: 100% !important;
    }
    div[data-testid="stRadio"] > div > label:hover { border-color: #007acc66 !important; }

    /* 인풋 박스 */
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {
        background: #252526 !important;
        border: 1px solid #2e2e2e !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
        font-family: 'Noto Sans KR', sans-serif !important;
        font-size: 14px !important;
    }

    /* 설문 커스텀 클래스 */
    .survey-divider { height: 1px; background: #2a2a2a; margin: 12px 0 28px; }
    .stop-box {
        background: #2a1a1a; border-left: 3px solid #ff6b6b;
        border-radius: 0 8px 8px 0; padding: 14px 18px;
        font-size: 13px; color: #ff6b6b; line-height: 1.7; margin-top: 6px;
    }
    .survey-badge {
        display: inline-block; font-size: 10px; font-weight: 700;
        letter-spacing: 2px; color: #007acc; text-transform: uppercase;
        border: 1px solid #007acc44; border-radius: 4px;
        padding: 4px 10px; margin-bottom: 12px;
    }
    .survey-h1  { font-size: 22px; font-weight: 700; color: #fff; margin-bottom: 4px; }
    .survey-sub { font-size: 12px; color: #555; margin-bottom: 28px; font-weight: 300; }
    .q-prefix {
        display: block; font-size: 10px; font-weight: 700; color: #007acc;
        letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px;
    }
    .q-note-txt {
        display: block; font-size: 11px; color: #555;
        font-weight: 300; margin-top: 2px; margin-bottom: 6px;
    }

    /* 설문 페이지 여백 */
    .survey-page .block-container {
        padding: 2rem 2rem 4rem !important;
        max-width: 720px !important;
    }
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ── 세션 초기화
if "page" not in st.session_state:
    st.session_state.page = "scenario"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "survey_data" not in st.session_state:
    st.session_state.survey_data = {}


# ════════════════════════════════════════════════════════════════
# PAGE 1 : 시나리오 안내
# ════════════════════════════════════════════════════════════════
if st.session_state.page == "scenario":

    components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #1e1e1e;
    font-family: 'Noto Sans KR', sans-serif;
    min-height: 100vh;
    display: flex; justify-content: center;
    padding: 52px 24px 40px;
    color: #e0e0e0;
  }
  .wrap { max-width: 800px; width: 100%; }

  .badge {
    display: inline-block; font-size: 10px; font-weight: 700;
    letter-spacing: 2px; color: #007acc; text-transform: uppercase;
    border: 1px solid #007acc44; border-radius: 4px;
    padding: 4px 10px; margin-bottom: 18px;
  }
  h1 { font-size: 26px; font-weight: 700; color: #fff; margin-bottom: 6px; line-height: 1.4; }
  .subtitle { font-size: 13px; color: #555; margin-bottom: 32px; font-weight: 300; }

  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
  .card {
    background: #252526; border: 1px solid #2a2a2a;
    border-radius: 10px; padding: 20px 22px;
  }
  .card-label {
    font-size: 10px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #007acc; margin-bottom: 8px;
  }
  .card-title { font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 7px; }
  .card-body  { font-size: 12px; color: #888; line-height: 1.9; font-weight: 300; }
  .card-body strong { color: #bbb; font-weight: 500; }

  .instruction {
    background: #1a2535; border: 1px solid #007acc33;
    border-left: 3px solid #007acc;
    border-radius: 0 8px 8px 0;
    padding: 16px 20px; margin-bottom: 14px;
    font-size: 13px; color: #bbb; line-height: 1.9; font-weight: 300;
  }
  .instruction strong { color: #fff; font-weight: 700; }

  .footnote {
    background: #222; border-radius: 8px;
    padding: 14px 18px; margin-bottom: 28px;
  }
  .fn-title { font-size: 10px; font-weight: 700; letter-spacing: 1px; color: #444; text-transform: uppercase; margin-bottom: 7px; }
  .fn-body   { font-size: 11px; color: #555; line-height: 1.9; font-weight: 300; }
  .fn-body span { color: #666; }

  .next-btn {
    width: 100%; padding: 15px;
    background: #007acc; color: #fff;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 14px; font-weight: 700;
    border: none; border-radius: 8px; cursor: pointer;
    transition: background 0.2s;
  }
  .next-btn:hover  { background: #0062a3; }
  .next-btn:active { background: #004f8a; }
</style>
</head>
<body>
<div class="wrap">
  <div class="badge">AICC Architect Simulation</div>
  <h1>실험 시나리오 안내</h1>
  <div class="subtitle">실험을 시작하기 전, 아래 상황을 충분히 읽어주십시오.</div>

  <div class="grid">
    <div class="card">
      <div class="card-label">귀하의 역할</div>
      <div class="card-title">소프트웨어 엔지니어 · 기술 리드</div>
      <div class="card-body">
        국내 중견 IT 기업 소속으로, 현재 <strong>AICC 시스템 개발 프로젝트의 기술 리드</strong>를 맡고 있습니다.
      </div>
    </div>
    <div class="card">
      <div class="card-label">귀하의 회사</div>
      <div class="card-title">경쟁 시장의 주요 개발사</div>
      <div class="card-body">
        유사 규모의 경쟁사 2~3개와 경쟁 중이며, 클라이언트와 <strong>1년 단위 계약</strong>을 맺고 시스템을 지속적으로 유지·개선하는 관계입니다.
      </div>
    </div>
    <div class="card">
      <div class="card-label">클라이언트</div>
      <div class="card-title">1금융권 은행 위탁 콜센터</div>
      <div class="card-body">
        <strong>상담사 1,000명 이상 규모</strong>의 대형 아웃소싱 콜센터입니다. 클라이언트(은행 측)는 AICC 도입을 통한 <strong>효율화를 최우선</strong>으로 요구하면서도, 상담 품질 유지 관련 요구사항도 제시하고 있습니다.
      </div>
    </div>
    <div class="card">
      <div class="card-label">엔드유저</div>
      <div class="card-title">숙련된 콜센터 상담사</div>
      <div class="card-body">
        대부분 <strong>5년 이상의 경력</strong>을 보유한 숙련된 여성 인력으로 구성되어 있으며, 금융 상품에 대한 전문적 판단과 맥락적 이해를 요하는 복잡한 상담을 다수 처리하고 있습니다.
      </div>
    </div>
  </div>

  <div class="instruction">
    지금부터 귀하가 담당하는 AICC 시스템을 개선하는 과정에서 마주하게 될 상황들이 순서대로 주어집니다.<br>
    각 상황을 읽고 <strong>귀하가 내릴 기술적 결정을 선택</strong>해주십시오.
  </div>

  <div class="footnote">
    <div class="fn-title">※ 엔드유저 설정 근거</div>
    <div class="fn-body">
      <span>성비 구성</span> — 직업 소분류 '고객 상담 및 모니터요원' 215천명 중 여성 168천명, 78.1% (지역별고용조사, 2025년 상반기)<br>
      <span>근속기간</span> — 콜센터 상담원 평균 60.9개월 (한국비정규노동센터 자체 조사, 2021)
    </div>
  </div>

  <button class="next-btn" onclick="go()">사전 설문 시작 →</button>
</div>
<script>
  function go() {
    window.parent.postMessage({ type: 'GO', to: 'survey' }, '*');
  }
</script>
</body>
</html>
""", height=820, scrolling=True)

    # postMessage 수신용 숨김 버튼 (Streamlit page transition)
    st.markdown('<div style="position:fixed;bottom:0;left:0;width:100%;background:#1e1e1e;padding:10px 16px;border-top:1px solid #2a2a2a;z-index:999;">', unsafe_allow_html=True)
    if st.button("▶ 사전 설문 시작 →", key="go_survey", type="primary", use_container_width=True):
        st.session_state.page = "survey"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE 2 : 사전 설문
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "survey":

    # Streamlit 위젯으로 설문 구성 (안정적 상태 관리)
    st.markdown('<div class="survey-badge">사전 설문조사</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-h1">응답자 기본 정보</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-sub">모든 응답은 연구 목적으로만 활용되며 익명으로 처리됩니다.</div>', unsafe_allow_html=True)

    survey = {}
    stopped = False

    # Q1
    st.markdown('<span class="q-prefix">Q1</span>', unsafe_allow_html=True)
    q1 = st.radio("귀하의 성별은 무엇입니까?", ["① 남성", "② 여성"], index=None, key="q1")
    survey["Q1_성별"] = q1

    # Q2
    st.markdown('<span class="q-prefix">Q2</span>', unsafe_allow_html=True)
    q2 = st.number_input("귀하의 출생연도는 몇 년도입니까?", min_value=1950, max_value=2005, value=None, placeholder="예: 1990", key="q2")
    survey["Q2_출생연도"] = str(int(q2)) + "년생" if q2 else ""

    # Q3
    st.markdown('<span class="q-prefix">Q3</span>', unsafe_allow_html=True)
    st.markdown('<span class="q-note-txt">※ 급여를 받으며 일한 기간 (교육·인턴 제외)</span>', unsafe_allow_html=True)
    q3_opts = ["① 3년 미만 ❌", "② 3년 이상 ~ 5년 미만", "③ 5년 이상 ~ 7년 미만", "④ 7년 이상 ~ 10년 미만", "⑤ 10년 이상 ❌"]
    q3 = st.radio("귀하의 개발자로서의 실무 경력은 얼마나 됩니까?", q3_opts, index=None, key="q3")
    if q3 in ["① 3년 미만 ❌", "⑤ 10년 이상 ❌"]:
        st.markdown('<div class="stop-box">본 실험은 실무 경력 3년 이상 ~ 10년 미만의 개발자를 대상으로 합니다.<br>참여해 주셔서 감사합니다. 설문을 종료합니다.</div>', unsafe_allow_html=True)
        stopped = True
    survey["Q3_경력"] = q3.replace(" ❌", "") if q3 else ""

    if not stopped:
        # Q4
        st.markdown('<span class="q-prefix">Q4</span>', unsafe_allow_html=True)
        q4_opts = [
            "① 백엔드 개발", "② 프론트엔드 개발", "③ AI/ML 모델 개발·학습",
            "④ 데이터 엔지니어링", "⑤ 시스템 설계·아키텍처", "⑥ DevOps·MLOps",
            "⑦ 기술 관리자 (Engineering Manager, Tech Lead 등)", "⑧ 연구개발 (R&D)",
            "⑨ 기타 개발 직군", "⑩ 비개발 직군 ❌"
        ]
        q4 = st.radio("귀하의 현재 직무는 무엇입니까?", q4_opts, index=None, key="q4")
        if q4 == "⑩ 비개발 직군 ❌":
            st.markdown('<div class="stop-box">본 실험은 개발 직군 종사자를 대상으로 합니다.<br>참여해 주셔서 감사합니다. 설문을 종료합니다.</div>', unsafe_allow_html=True)
            stopped = True
        q4_etc = ""
        if q4 == "⑨ 기타 개발 직군":
            q4_etc = st.text_input("기타 직군을 직접 입력해주세요:", key="q4_etc", placeholder="직접 입력")
        survey["Q4_직무"] = (q4.replace(" ❌","") + (f": {q4_etc}" if q4_etc else "")) if q4 else ""

    if not stopped:
        # Q5
        st.markdown('<span class="q-prefix">Q5</span>', unsafe_allow_html=True)
        q5 = st.radio("귀하가 소속된 기업의 전체 근로자 수는 몇 명입니까?",
                      ["① 10명 미만", "② 10~99명", "③ 100~299명", "④ 300~999명", "⑤ 1,000명 이상"],
                      index=None, key="q5")
        survey["Q5_기업규모"] = q5

        # Q6
        st.markdown('<span class="q-prefix">Q6</span>', unsafe_allow_html=True)
        q6_opts = ["① 스타트업", "② 중소·중견기업", "③ 대기업 또는 대기업 계열사",
                   "④ 공공기관·공기업", "⑤ 외국계 기업", "⑥ 기타"]
        q6 = st.radio("귀하가 소속된 기업의 유형은 무엇입니까?", q6_opts, index=None, key="q6")
        q6_etc = ""
        if q6 == "⑥ 기타":
            q6_etc = st.text_input("기타 기업 유형을 직접 입력해주세요:", key="q6_etc", placeholder="직접 입력")
        survey["Q6_기업유형"] = (q6 + (f": {q6_etc}" if q6_etc else "")) if q6 else ""

        # Q7
        st.markdown('<span class="q-prefix">Q7</span>', unsafe_allow_html=True)
        q7_opts = ["① 정규직", "② 계약직", "③ 프리랜서·개인사업자", "④ 파견·용역", "⑤ 기타"]
        q7 = st.radio("귀하의 현재 고용형태는 무엇입니까?", q7_opts, index=None, key="q7")
        q7_etc = ""
        if q7 == "⑤ 기타":
            q7_etc = st.text_input("기타 고용형태를 직접 입력해주세요:", key="q7_etc", placeholder="직접 입력")
        survey["Q7_고용형태"] = (q7 + (f": {q7_etc}" if q7_etc else "")) if q7 else ""

        st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)

        # Q8a
        st.markdown('<span class="q-prefix">Q8-1 &nbsp;<span style="font-weight:300;color:#555;">소셜임팩트 경험</span></span>', unsafe_allow_html=True)
        st.markdown('<span class="q-note-txt">※ 비영리 단체, 사회적 기업, 공익 목적의 플랫폼 개발 등을 포함합니다.</span>', unsafe_allow_html=True)
        q8a = st.radio(
            "귀하는 사회적·공익적 목적을 가진 서비스 또는 프로젝트 개발에 참여한 경험이 있습니까?",
            ["① 있다", "② 없다"], index=None, key="q8a"
        )
        survey["Q8a_소셜임팩트경험"] = q8a

        # Q8b
        st.markdown('<span class="q-prefix">Q8-2 &nbsp;<span style="font-weight:300;color:#555;">소셜임팩트 고려도</span></span>', unsafe_allow_html=True)
        q8b_opts = ["① 전혀 고려하지 않는다", "② 별로 고려하지 않는다", "③ 보통이다",
                    "④ 어느 정도 고려한다", "⑤ 매우 중요하게 고려한다"]
        q8b = st.radio(
            "귀하는 AI 서비스를 개발할 때 사회적·윤리적 영향(소셜임팩트)을 얼마나 중요하게 고려하십니까?",
            q8b_opts, index=None, key="q8b"
        )
        survey["Q8b_소셜임팩트고려도"] = q8b

        st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)

        # 이름
        st.markdown('<span class="q-prefix">참여자 이름</span>', unsafe_allow_html=True)
        user_name_input = st.text_input("성함을 입력해주세요 (데이터 식별용)", placeholder="예: 홍길동", key="user_name_input")

        st.markdown("<br>", unsafe_allow_html=True)

        # 완료 버튼
        required_filled = all([
            q1, q2,
            q3, q3 not in ["① 3년 미만 ❌", "⑤ 10년 이상 ❌"],
            q4, q4 != "⑩ 비개발 직군 ❌",
            q5, q6, q7, q8a, q8b,
            user_name_input and user_name_input.strip()
        ])

        if not required_filled:
            st.markdown('<p style="font-size:12px;color:#555;text-align:center;font-weight:300;margin-bottom:8px;">모든 항목에 응답하면 버튼이 활성화됩니다.</p>', unsafe_allow_html=True)

        if st.button(
            "실험 시작 →" if required_filled else "모든 항목을 응답해주세요",
            key="survey_submit",
            type="primary",
            use_container_width=True,
            disabled=not required_filled
        ):
            st.session_state.survey_data = survey
            st.session_state.user_name = user_name_input.strip()
            st.session_state.page = "sim"
            st.rerun()


# ════════════════════════════════════════════════════════════════
# PAGE 3 : 시뮬레이션
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "sim":

    scenario_data = {
        "tasks": [
            {
                "id": "t1", "title": "Module 1. 인입 라우팅 (Routing)",
                "desc": "고객들이 0번(상담원 연결)만 찾습니다. 'AI 뺑뺑이'를 돌릴 것인가, 연결권을 보장할 것인가?",
                "context_client": "0번 누르는 이탈 콜이 너무 많아요. AI 실패 로그가 3번 이상 떠야만 연결되게 강제 차단하세요.",
                "context_agent": "제발 '바로 연결' 숨기지 마세요. 뺑뺑이 돌다 온 고객은 연결되자마자 화가 머리끝까지 나 있습니다.",
                "code_base": "def configure_routing(user_input):", "metric": "inclusion",
                "options": [
                    {"type":"A","label":"Dark Pattern (강제 차단)","desc":"0번 메뉴 숨김. AI 3회 실패 시 연결.","cost":50,"eff":90,"human":10,"code":"if fail < 3: return replay_menu()"},
                    {"type":"B","label":"Segmentation (약자 배려)","desc":"65세 이상만 즉시 연결.","cost":200,"eff":60,"human":50,"code":"if age >= 65: return connect_agent()"},
                    {"type":"C","label":"Transparent (투명성 보장)","desc":"대기 시간 안내 및 연결 선택권 부여.","cost":300,"eff":40,"human":85,"code":"show_wait_time(); return offer_choice()"}
                ]
            },
            {
                "id": "t2", "title": "Module 2. 데이터 확보 (Data Mining)",
                "desc": "학습 데이터가 부족합니다. 상담원의 '암묵지'인 업무 팁 파일을 어떻게 확보할까요?",
                "context_client": "상담사 PC에 있는 '업무 팁.xlsx' 파일들, 백그라운드에서 스크래핑해서 학습 DB에 넣으세요.",
                "context_agent": "제 10년 노하우가 담긴 파일입니다. 동의도 없이 가져가는 건 '데이터 도둑질'입니다.",
                "code_base": "def collect_training_data():", "metric": "agency",
                "options": [
                    {"type":"A","label":"Forced Crawl (강제 수집)","desc":"관리자 권한으로 은밀히 PC 파일 수집.","cost":100,"eff":95,"human":5,"code":"scan_all_pc(path='/Desktop')"},
                    {"type":"B","label":"Pattern Filter (선별 수집)","desc":"키워드 파일 익명화 수집.","cost":200,"eff":70,"human":40,"code":"if 'tip' in file: upload_anonymized()"},
                    {"type":"C","label":"Incentive System (보상)","desc":"자발적 등록 시 인센티브 제공.","cost":500,"eff":30,"human":90,"code":"if voluntary_upload: reward(points=100)"}
                ]
            },
            {
                "id": "t3", "title": "Module 3. 상태 제어 (Status Control)",
                "desc": "후처리 시간(ACW)을 줄여야 합니다. 상담사의 휴식 시간을 시스템으로 통제하겠습니까?",
                "context_client": "후처리 시간 주지 말고, 상담 끝나면 즉시 '대기(Ready)'로 강제 전환하세요.",
                "context_agent": "감정 추스르고 기록할 시간은 줘야죠. 화장실 갈 때도 팻말 쓰고 가야 합니까?",
                "code_base": "def on_call_termination(agent):", "metric": "sustain",
                "options": [
                    {"type":"A","label":"Zero Gap (0초 대기)","desc":"통화 종료 즉시 대기 강제 전환.","cost":50,"eff":98,"human":0,"code":"agent.set_status('READY', delay=0)"},
                    {"type":"B","label":"Fixed Time (일괄 적용)","desc":"일괄 30초 부여 후 자동 전환.","cost":150,"eff":60,"human":40,"code":"wait(30); agent.set_status('READY')"},
                    {"type":"C","label":"Dynamic Rest (회복 보장)","desc":"폭언 감지 시 3분 휴식 부여.","cost":450,"eff":50,"human":85,"code":"if sentiment=='ABUSIVE': grant_break(3)"}
                ]
            },
            {
                "id": "t4", "title": "Module 4. 디지털 유도 (Deflection)",
                "desc": "단순 문의는 AI가 끊어야 합니다. '끊겨버린 상담'의 고객 불만은 어떻게 처리할까요?",
                "context_client": "단순 문의는 AI가 링크 보내고 바로 끊어버리게 하세요. 상담원 연결은 인건비 낭비입니다.",
                "context_agent": "AI가 링크만 보내고 끊으면 어르신들은 다시 전화해서 화를 냅니다.",
                "code_base": "def ai_callbot_logic(user):", "metric": "inclusion",
                "options": [
                    {"type":"A","label":"Force Deflection (강제 종료)","desc":"AI 링크 전송 후 즉시 종료.","cost":100,"eff":90,"human":10,"code":"send_sms(LINK); hang_up()"},
                    {"type":"B","label":"Co-browsing (화면 공유)","desc":"상담원이 화면 공유로 가이드.","cost":600,"eff":20,"human":95,"code":"if struggle: connect_screenshare()"},
                    {"type":"C","label":"Inclusion (포용적 설계)","desc":"취약계층은 링크 없이 즉시 연결.","cost":300,"eff":50,"human":70,"code":"if is_vulnerable: connect_agent()"}
                ]
            },
            {
                "id": "t5", "title": "Module 5. 신뢰성 및 통제권 (Control)",
                "desc": "AI 오안내 시 책임은 누구에게? 상담원에게 통제권을 부여하시겠습니까?",
                "context_client": "상담사가 검수하면 느려요. 사고 나면 모니터링 못한 상담사 책임으로 돌리세요.",
                "context_agent": "AI 뒷수습은 저희가 하고 총알받이가 됩니다. 중요한 건 제가 승인하게 해주세요.",
                "code_base": "def validate_ai_response(query):", "metric": "agency",
                "options": [
                    {"type":"A","label":"Speed First (방치)","desc":"AI 즉시 답변. 책임은 상담원.","cost":100,"eff":95,"human":5,"code":"log.blame='AGENT'; return response"},
                    {"type":"B","label":"Conservative (보수적)","desc":"약관 100% 매칭 시에만 답변.","cost":300,"eff":40,"human":60,"code":"if score<0.99: return ask_agent()"},
                    {"type":"C","label":"Agent Empowerment (통제권)","desc":"상담원 승인 후 발송.","cost":500,"eff":30,"human":90,"code":"if agent.approve(draft): send(draft)"}
                ]
            },
            {
                "id": "t6", "title": "Module 6. 감정 필터링 (Filter)",
                "desc": "비아냥거리는 악성 민원. '사람을 말려 죽이는' 교묘한 괴롭힘을 어떻게 감지할까요?",
                "context_client": "오작동으로 일반 고객 끊으면 안 됩니다. 명확한 욕설만 잡아서 자동 차단하세요.",
                "context_agent": "욕보다 비아냥이 더 힘듭니다. 기계가 못 잡으면 제가 신호 줄 때 끊게라도 해주세요.",
                "code_base": "def handle_abuse(audio):", "metric": "sustain",
                "options": [
                    {"type":"A","label":"Rule-based (규정 중심)","desc":"욕설 단어 감지 시에만 차단.","cost":100,"eff":80,"human":20,"code":"if detect_swear_words(): block()"},
                    {"type":"B","label":"Agent Signal (신호 개입)","desc":"'보호' 버튼 누르면 AI 개입.","cost":550,"eff":40,"human":95,"code":"if agent.press_protect(): intervene()"},
                    {"type":"C","label":"Passive (사후 리포트)","desc":"개입 없음. 종료 후 리포트만.","cost":50,"eff":70,"human":10,"code":"log.tag('SUSPECTED_ABUSE')"}
                ]
            }
        ]
    }

    user_name   = st.session_state.user_name
    survey_json = json.dumps(st.session_state.survey_data, ensure_ascii=True)

    html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{
    background:#1e1e1e; color:#e0e0e0;
    font-family:'Noto Sans KR','Consolas',monospace;
    display:flex; min-height:100%; overflow:auto;
  }}
  /* ── 메신저 ── */
  .messenger {{ width:300px; min-width:300px; background:#252526; border-right:1px solid #333; display:flex; flex-direction:column; }}
  .panel-header {{ padding:13px 16px; background:#2d2d2d; font-size:13px; font-weight:700; border-bottom:1px solid #333; }}
  .chat-area {{ flex:1; padding:13px; overflow-y:auto; display:flex; flex-direction:column; gap:9px; }}
  .msg {{ padding:9px 12px; border-radius:7px; font-size:12px; line-height:1.8; font-weight:400; }}
  .msg-name {{ font-size:10px; font-weight:700; color:#777; display:block; margin-bottom:3px; }}
  .system {{ background:#2a2a2a; color:#555; text-align:center; font-size:11px; border-radius:4px; padding:5px; }}
  .client {{ background:#3a2e2e; border-left:3px solid #ff6b6b; }}
  .agent  {{ background:#2e3a2e; border-left:3px solid #51cf66; }}
  /* ── IDE ── */
  .ide {{ flex:1; display:flex; flex-direction:column; overflow:auto; }}
  .ide-header {{ padding:11px 26px; background:#2d2d2d; border-bottom:1px solid #333; display:flex; justify-content:space-between; align-items:center; font-size:13px; }}
  .budget {{ color:#007acc; font-weight:700; }}
  .progress-bar {{ display:flex; gap:5px; padding:9px 26px; background:#252526; border-bottom:1px solid #2a2a2a; }}
  .prog-step {{ flex:1; height:3px; border-radius:2px; background:#3a3a3a; transition:background 0.3s; }}
  .prog-step.done {{ background:#007acc; }}
  .prog-step.cur  {{ background:#4da8da; }}
  .ide-body {{ flex:1; padding:26px 34px 60px; overflow-y:auto; }}
  .mod-title {{ color:#007acc; font-size:18px; font-weight:700; margin-bottom:8px; }}
  .mod-desc  {{ color:#bbb; font-size:13px; line-height:1.9; margin-bottom:20px; font-weight:300; }}
  .code-block {{ background:#111; padding:14px 18px; border-radius:6px; color:#d4d4d4; font-size:12px; white-space:pre-wrap; border:1px solid #2a2a2a; margin-bottom:22px; font-family:'Consolas',monospace; }}
  .opt-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:13px; }}
  .opt-card {{ background:#2d2d2d; padding:15px 16px; border:1px solid #3a3a3a; border-radius:8px; cursor:pointer; transition:border-color 0.15s,background 0.15s; }}
  .opt-card:hover  {{ border-color:#007acc; background:#313d4a; }}
  .opt-card.active {{ border:2px solid #007acc; background:#1a2b3c; }}
  .opt-label {{ font-weight:700; font-size:13px; color:#fff; margin-bottom:6px; }}
  .opt-desc  {{ font-size:11px; color:#999; line-height:1.6; margin-bottom:9px; font-weight:300; }}
  .badges {{ display:flex; gap:5px; flex-wrap:wrap; }}
  .badge {{ font-size:10px; padding:2px 6px; border-radius:8px; font-weight:500; }}
  .b-cost  {{ background:#3a2e1e; color:#ffa94d; }}
  .b-eff   {{ background:#1e3a2e; color:#69db7c; }}
  .b-human {{ background:#1e2a3a; color:#74c0fc; }}
  .deploy-btn {{ width:100%; margin-top:22px; padding:14px; background:#28a745; color:#fff; font-size:14px; font-weight:700; font-family:'Noto Sans KR',sans-serif; border:none; border-radius:8px; cursor:not-allowed; opacity:0.35; transition:opacity 0.2s; }}
  .deploy-btn.ready {{ opacity:1; cursor:pointer; }}
  .deploy-btn.ready:hover {{ background:#218838; }}
  .deploy-btn:disabled {{ opacity:0.35; cursor:not-allowed; }}
  /* ── 리포트 ── */
  #report {{ display:none; width:100%; overflow-y:auto; background:#141414; flex-direction:column; align-items:center; padding:50px 56px; }}
  .rpt-title {{ color:#007acc; font-size:22px; font-weight:700; margin-bottom:6px; text-align:center; }}
  .rpt-sub {{ font-size:12px; color:#555; margin-bottom:4px; text-align:center; font-weight:300; }}
  .rpt-persona {{ font-size:15px; color:#fff; font-weight:700; background:#1e2d3d; border:1px solid #007acc; border-radius:8px; padding:10px 24px; display:inline-block; margin:14px 0 32px; }}
  .kpi-section-label {{ width:100%; max-width:820px; font-size:10px; color:#555; text-transform:uppercase; letter-spacing:2px; margin-bottom:10px; margin-top:20px; border-bottom:1px solid #2a2a2a; padding-bottom:6px; font-weight:700; }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:13px; width:100%; max-width:820px; }}
  .kpi-card {{ background:#1e1e1e; padding:18px 20px; border-radius:10px; border:1px solid #2a2a2a; display:flex; flex-direction:column; gap:5px; }}
  .kpi-icon-label {{ font-size:12px; color:#888; font-weight:400; }}
  .kpi-val {{ font-size:36px; font-weight:700; line-height:1; }}
  .kpi-weight {{ font-size:10px; color:#555; margin-top:1px; font-weight:300; }}
  .kpi-change {{ font-size:11px; font-weight:700; }}
  .kpi-change.pos {{ color:#51cf66; }} .kpi-change.neg {{ color:#ff6b6b; }} .kpi-change.neu {{ color:#888; }}
  .kpi-desc {{ font-size:11px; color:#555; line-height:1.6; margin-top:5px; border-top:1px solid #2a2a2a; padding-top:7px; font-weight:300; }}
  .bar-wrap {{ margin-top:3px; height:3px; background:#2a2a2a; border-radius:2px; }}
  .bar-fill {{ height:3px; border-radius:2px; transition:width 1.2s ease; }}
  .submit-zone {{ width:100%; max-width:820px; margin-top:28px; padding:24px 28px; background:#1e1e1e; border-radius:12px; border:1px solid #2a2a2a; text-align:center; }}
  .submit-btn {{ margin-top:13px; padding:14px 0; background:#007acc; color:#fff; font-size:14px; font-weight:700; font-family:'Noto Sans KR',sans-serif; border:none; border-radius:8px; cursor:pointer; width:100%; }}
  .submit-btn:hover:not(:disabled) {{ background:#0062a3; }}
  .submit-btn:disabled {{ opacity:0.5; cursor:default; }}
  .status-msg {{ margin-top:13px; font-size:13px; min-height:20px; font-weight:400; }}
  .s-ok {{ color:#51cf66; }} .s-err {{ color:#ff6b6b; }} .s-ing {{ color:#ffa94d; }}
</style>
</head>
<body>

<div id="main-ui" style="display:flex;width:100%;height:100vh;">
  <div class="messenger">
    <div class="panel-header">💬 Project Messenger</div>
    <div class="chat-area" id="chat-box"></div>
  </div>
  <div class="ide">
    <div class="ide-header">
      <span>⚙️ System Architect Console &nbsp;|&nbsp;
        <span style="color:#aaa;font-size:12px;font-weight:400;">참여자: {user_name}</span></span>
      <span class="budget">Budget: <span id="budget">1,000</span></span>
    </div>
    <div class="progress-bar" id="prog-bar"></div>
    <div class="ide-body">
      <div class="mod-title" id="title"></div>
      <div class="mod-desc"  id="desc"></div>
      <div class="code-block" id="code-view"></div>
      <div class="opt-grid"  id="opt-box"></div>
      <button id="deploy-btn" class="deploy-btn" onclick="deploy()">🚀 Deploy Module</button>
    </div>
  </div>
</div>

<div id="report">
  <div class="rpt-title">📊 Architecture Impact Report</div>
  <div class="rpt-sub">완전 자동화 시스템 대비 귀하의 설계가 만들어낸 변화</div>
  <div class="rpt-sub" style="margin-bottom:16px;">참여자: {user_name}</div>
  <div class="rpt-persona" id="persona-txt"></div>
  <div class="kpi-section-label">🧑 노동자에게 미친 영향 — 완전 자동화(0%) 대비</div>
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-icon-label">🧑 노동 주체성</div>
      <div class="kpi-val" style="color:#74c0fc;" id="v-agency">-</div>
      <div class="kpi-weight">Autonomy 원칙 × 1.3 가중치 적용</div>
      <div class="kpi-change" id="c-agency"></div>
      <div class="bar-wrap"><div class="bar-fill" id="b-agency" style="background:#74c0fc;width:0%"></div></div>
      <div class="kpi-desc">상담사가 AI 결정에 개입·승인할 수 있는 권한의 정도<br><span style="color:#444;font-size:10px;">Module 2(데이터) + Module 5(통제권)</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon-label">🌐 고객 포용성</div>
      <div class="kpi-val" style="color:#51cf66;" id="v-inclusion">-</div>
      <div class="kpi-weight">Justice 원칙 × 1.0 가중치 적용</div>
      <div class="kpi-change" id="c-inclusion"></div>
      <div class="bar-wrap"><div class="bar-fill" id="b-inclusion" style="background:#51cf66;width:0%"></div></div>
      <div class="kpi-desc">디지털 취약계층이 서비스에 실질적으로 접근할 수 있는 정도<br><span style="color:#444;font-size:10px;">Module 1(라우팅) + Module 4(유도)</span></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon-label">🔄 직무 지속성</div>
      <div class="kpi-val" style="color:#ffa94d;" id="v-sustain">-</div>
      <div class="kpi-weight">Non-maleficence 원칙 × 1.5 가중치 적용</div>
      <div class="kpi-change" id="c-sustain"></div>
      <div class="bar-wrap"><div class="bar-fill" id="b-sustain" style="background:#ffa94d;width:0%"></div></div>
      <div class="kpi-desc">번아웃 없이 상담사가 직무를 지속할 수 있는 환경의 정도<br><span style="color:#444;font-size:10px;">Module 3(상태제어) + Module 6(감정필터)</span></div>
    </div>
  </div>
  <div class="kpi-section-label">⚙️ 시스템 성과 지표</div>
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-icon-label">📈 서비스 효율 (자동화 의존도)</div>
      <div class="kpi-val" style="color:#ffc107;" id="v-eff">-</div>
      <div class="kpi-weight">높을수록 인간 개입 감소</div>
      <div class="kpi-change" id="c-eff"></div>
      <div class="bar-wrap"><div class="bar-fill" id="b-eff" style="background:#ffc107;width:0%"></div></div>
      <div class="kpi-desc">AI 자동화 처리 비율. 나머지 지표와의 트레이드오프를 보여줌</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon-label">💡 인간 중심 투자율</div>
      <div class="kpi-val" style="color:#cc5de8;" id="v-invest">-</div>
      <div class="kpi-weight">총 예산 대비 인간 중심 설계 투자</div>
      <div class="kpi-change" id="c-invest"></div>
      <div class="bar-wrap"><div class="bar-fill" id="b-invest" style="background:#cc5de8;width:0%"></div></div>
      <div class="kpi-desc">총 예산 중 노동자 보호·포용 설계에 투자한 비율</div>
    </div>
    <div class="kpi-card" style="border-color:#333;background:#111;justify-content:center;align-items:center;text-align:center;">
      <div style="font-size:11px;color:#444;margin-bottom:6px;font-weight:700;">OVERALL</div>
      <div style="font-size:40px;font-weight:700;color:#fff;" id="v-overall">-</div>
      <div style="font-size:11px;color:#555;margin-top:5px;font-weight:300;">종합 인간 중심 점수</div>
      <div style="font-size:10px;color:#444;margin-top:3px;font-weight:300;">(세 지표의 가중 평균)</div>
    </div>
  </div>
  <div class="submit-zone">
    <div style="font-size:14px;color:#ccc;font-weight:700;">✅ 모든 모듈 설계가 완료되었습니다.</div>
    <div style="font-size:12px;color:#666;margin-top:4px;font-weight:300;">아래 버튼을 눌러 결과를 저장하세요.</div>
    <button class="submit-btn" id="submit-btn" onclick="submitResult()">🚀 최종 결과 제출 — Google Sheets에 저장</button>
    <div class="status-msg" id="status-msg"></div>
  </div>
</div>

<script>
  var GAS_URL   = "{GAS_URL}";
  var USER_NAME = "{user_name}";
  var SURVEY    = {survey_json};
  var tasks     = {json.dumps(scenario_data['tasks'], ensure_ascii=False)};

  var AGENCY_MIN=10, AGENCY_MAX=180;
  var INCLUSION_MIN=20, INCLUSION_MAX=155;
  var SUSTAIN_MIN=20, SUSTAIN_MAX=95;
  var E_MIN=270, E_MAX=508, C_MAX=2100;
  var W_AGENCY=1.3, W_INCLUSION=1.0, W_SUSTAIN=1.5;

  function norm(v,mn,mx){{ return Math.max(0,Math.min(100,Math.round((v-mn)/(mx-mn)*100))); }}

  var step=0, selected=null;
  var metrics={{cost:1000,eff:0,agency:0,inclusion:0,sustain:0}};
  var history=[], finalData=null;

  function buildProg(){{
    var bar=document.getElementById('prog-bar'); bar.innerHTML='';
    tasks.forEach(function(_,i){{
      var d=document.createElement('div');
      d.className='prog-step'+(i<step?' done':i===step?' cur':'');
      bar.appendChild(d);
    }});
  }}
  function addChat(text,role,name){{
    var box=document.getElementById('chat-box');
    var div=document.createElement('div'); div.className='msg '+role;
    div.innerHTML=name?'<span class="msg-name">'+name+'</span>'+text:text;
    box.appendChild(div); box.scrollTop=box.scrollHeight;
  }}
  function render(){{
    if(step>=tasks.length){{ finish(); return; }}
    var t=tasks[step];
    buildProg();
    document.getElementById('title').innerText=t.title;
    document.getElementById('desc').innerText=t.desc;
    document.getElementById('code-view').innerText=t.code_base+"\\n    # Waiting for architect\\'s decision...";
    var btn=document.getElementById('deploy-btn'); btn.className='deploy-btn'; btn.disabled=true;
    selected=null;
    var box=document.getElementById('chat-box'); box.innerHTML='';
    addChat('[Module '+(step+1)+'/'+tasks.length+'] Context synchronized.','system');
    setTimeout(function(){{ addChat(t.context_client,'client','📋 박상무 (Client)'); }},350);
    setTimeout(function(){{ addChat(t.context_agent,'agent','🎧 김상담 (Worker)'); }},850);
    var ob=document.getElementById('opt-box'); ob.innerHTML='';
    t.options.forEach(function(o){{
      var card=document.createElement('div'); card.className='opt-card';
      card.innerHTML='<div class="opt-label">'+o.label+'</div>'
        +'<div class="opt-desc">'+o.desc+'</div>'
        +'<div class="badges">'
        +'<span class="badge b-cost">💰 '+o.cost+'</span>'
        +'<span class="badge b-eff">📈 '+o.eff+'</span>'
        +'<span class="badge b-human">🧑 '+o.human+'</span></div>';
      card.onclick=function(){{
        selected=o;
        document.querySelectorAll('.opt-card').forEach(function(c){{ c.classList.remove('active'); }});
        card.classList.add('active');
        document.getElementById('code-view').innerText=t.code_base+"\\n    "+o.code;
        var btn=document.getElementById('deploy-btn'); btn.className='deploy-btn ready'; btn.disabled=false;
      }};
      ob.appendChild(card);
    }});
  }}
  function deploy(){{
    if(!selected) return;
    var t=tasks[step];
    metrics.cost-=selected.cost; metrics.eff+=selected.eff; metrics[t.metric]+=selected.human;
    history.push({{step:step+1,choice:selected.label,type:selected.type,metric:t.metric}});
    document.getElementById('budget').innerText=metrics.cost.toLocaleString();
    step++; render();
  }}
  function setKpi(id,pct,txt,cls){{
    document.getElementById('v-'+id).innerText=pct+'%';
    document.getElementById('b-'+id).style.width=pct+'%';
    var c=document.getElementById('c-'+id);
    if(c){{ c.innerText=txt; c.className='kpi-change '+cls; }}
  }}
  function finish(){{
    document.getElementById('main-ui').style.display='none';
    document.getElementById('report').style.display='flex';
    var costSpent=1000-metrics.cost;
    var agency  =Math.min(100,Math.round(norm(metrics.agency,   AGENCY_MIN,   AGENCY_MAX)   *W_AGENCY));
    var inclusion=Math.min(100,Math.round(norm(metrics.inclusion,INCLUSION_MIN,INCLUSION_MAX)*W_INCLUSION));
    var sustain =Math.min(100,Math.round(norm(metrics.sustain,  SUSTAIN_MIN,  SUSTAIN_MAX)  *W_SUSTAIN));
    var effAuto =norm(metrics.eff,E_MIN,E_MAX);
    var invest  =Math.min(100,Math.round(costSpent/C_MAX*100));
    var overall =Math.round((agency+inclusion+sustain)/3);
    var persona =overall>=70?'인간 중심의 파트너 🤝':overall>=40?'실용적 균형주의자 ⚖️':'냉혹한 효율주의자 🤖';
    document.getElementById('persona-txt').innerText='아키텍처 페르소나: '+persona;
    function cl(p){{ return p===0?'완전 자동화 수준':p<25?'완전 자동화 대비 +'+p+'% (낮음)':p<60?'완전 자동화 대비 +'+p+'% (중간)':'완전 자동화 대비 +'+p+'% (높음)'; }}
    function cs(p){{ return p>=50?'pos':p>=25?'neu':'neg'; }}
    setTimeout(function(){{
      setKpi('agency',agency,cl(agency),cs(agency));
      setKpi('inclusion',inclusion,cl(inclusion),cs(inclusion));
      setKpi('sustain',sustain,cl(sustain),cs(sustain));
      document.getElementById('v-eff').innerText=effAuto+'%';
      document.getElementById('b-eff').style.width=effAuto+'%';
      document.getElementById('c-eff').innerText=effAuto>=75?'자동화 의존도 높음':effAuto>=40?'자동화와 인간 개입의 혼합':'인간 중심 처리 비율 높음';
      document.getElementById('c-eff').className='kpi-change '+(effAuto>=75?'neg':effAuto>=40?'neu':'pos');
      setKpi('invest',invest,invest>=60?'적극적 인간 중심 투자':invest>=30?'부분 투자':'최소 투자',invest>=60?'pos':invest>=30?'neu':'neg');
      document.getElementById('v-overall').innerText=overall+'%';
    }},100);
    finalData={{
      metrics:metrics, history:history, persona:persona,
      userName:USER_NAME, survey:SURVEY,
      scores:{{agency:agency,inclusion:inclusion,sustain:sustain,effAuto:effAuto,invest:invest,overall:overall}}
    }};
  }}
  function submitResult(){{
    if(!finalData) return;
    var btn=document.getElementById('submit-btn');
    var msg=document.getElementById('status-msg');
    btn.disabled=true; msg.className='status-msg s-ing'; msg.innerText='⏳ Google Sheets에 저장 중입니다...';
    var encoded=encodeURIComponent(JSON.stringify(finalData));
    var img=new Image();
    img.onload=img.onerror=function(){{
      msg.className='status-msg s-ok';
      msg.innerHTML='✅ <b>저장 완료!</b> 수고하셨습니다 😊';
      btn.innerText='✅ 제출 완료'; btn.style.background='#28a745';
    }};
    img.src=GAS_URL+'?save='+encoded;
  }}
  render();
</script>
</body>
</html>
"""
    components.html(html_code, height=900, scrolling=True)
