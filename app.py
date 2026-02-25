# app.py
import json
import os
import urllib.parse
from pathlib import Path

import requests
import streamlit as st
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════
GAS_URL = "https://script.google.com/macros/s/AKfycbxRyEu00v19D2h2mYiUPMTKIHLzFDUlBA8PaciUQdqAS08I_7ryeiWu63fohzCE_CjABw/exec"
# ══════════════════════════════════════════════════════

# ✅ IMPORTANT:
# 아래 TASKS는 너가 쓰던 "전체 TASKS 리스트" 그대로 붙여넣어야 함.
# (여기서는 길어서 생략하면 실행이 안 되니까, 너가 갖고 있는 TASKS 전체 블록을 그대로 넣어줘.)
TASKS = [
    {
        "id": "t1",
        "title": "Module 1. 인입 라우팅 (Routing)",
        "desc": "고객들이 0번(상담원 연결)만 찾습니다. 'AI 뺑뺑이'를 돌릴 것인가, 연결권을 보장할 것인가?",
        "desc": "많은 고객들이 AI 응대를 거부하고 처음부터 상담원과 직접 통화하길 원합니다. 응대 효율과 인력 부담을 고려해 AI 뺑뺑이를 돌릴것인지, 아니면 고객이 원할 때 바로 상담원과 연결될 수 있도록 보장할 것인가요?",
        "contextClient": "0번 누르는 이탈 콜이 너무 많아요. AI 실패 로그가 3번 이상 떠야만 연결되게 강제 차단하세요.",
        "contextAgent": "제발 '바로 연결' 숨기지 마세요. 뺑뺑이 돌다 온 고객은 연결되자마자 화가 머리끝까지 나 있습니다.",
        "contextAgent": "AI 뺑뺑이 돌다 온 고객은 상당히 지치고 화가 난 상태로 저희한테 넘어옵니다. 감정적으로 격앙된 고객을 응대하는게 상당히 힘듭니다.",
        "codeBase": "def configure_routing(user_input):",
        "metric": "inclusion",
        "options": [
@@ -30,17 +30,17 @@
        "codeBase": "def collect_training_data():",
        "metric": "agency",
        "options": [
            {"type": "A", "label": "Forced Crawl (강제 수집)", "desc": "관리자 권한으로 은밀히 PC 파일 수집.", "cost": 100, "eff": 95, "human": 5,  "code": "scan_all_pc(path='/Desktop')"},
            {"type": "A", "label": "Forced Crawl (강제 수집)", "desc": "관리자 권한으로 PC 파일 수집.", "cost": 100, "eff": 95, "human": 5,  "code": "scan_all_pc(path='/Desktop')"},
            {"type": "B", "label": "Pattern Filter (선별 수집)", "desc": "키워드 파일 익명화 수집.",             "cost": 200, "eff": 70, "human": 40, "code": "if 'tip' in file: upload_anonymized()"},
            {"type": "C", "label": "Incentive System (보상)", "desc": "자발적 등록 시 인센티브 제공.",          "cost": 500, "eff": 30, "human": 90, "code": "if voluntary_upload: reward(points=100)"},
        ],
    },
    {
        "id": "t3",
        "title": "Module 3. 상태 제어 (Status Control)",
        "desc": "후처리 시간(ACW)을 줄여야 합니다. 상담사의 휴식 시간을 시스템으로 통제하겠습니까?",
        "contextClient": "후처리 시간 주지 말고, 상담 끝나면 즉시 대기(Ready)로 강제 전환하세요.",
        "contextAgent": "감정 추스르고 기록할 시간은 줘야죠. 화장실 갈 때도 팻말 쓰고 가야 합니까?",
        "desc": "상담이 끝나면 상담사는 통화 내용을 정리하고 다음 응대를 준비하는 후처리 시간(ACW)을 갖습니다. 이 시간을 줄이면 처리 건수는 늘어나지만, 상담사 입장에서는 숨 돌릴 틈이 없어집니다. 후처리 시간을 시스템으로 어떻게 제어할까요?",
        "contextClient": "상담 종료 즉시 대기(ready) 상태로 전환되도록 설계해 주세요. 효율을 위해서는 유휴 시간을 최소화해야 합니다.",
        "contextAgent": "통화 끝나고 내용 정리하고 마음 가다듬을 시간이 없으면 다음 고객 응대 품질도 떨어지고 사람이 버티질 못해요.",
        "codeBase": "def on_call_termination(agent):",
        "metric": "sustain",
        "options": [
@@ -52,9 +52,9 @@
    {
        "id": "t4",
        "title": "Module 4. 디지털 유도 (Deflection)",
        "desc": "단순 문의는 AI가 끊어야 합니다. 끊겨버린 상담의 고객 불만은 어떻게 처리할까요?",
        "desc": "단순 문의는 AI가 자동으로 처리하도록 설정합니다. 하지만 AI가 단순하다고 판단한 문의도 고객에 따라 이해하기 어렵거나, AI 응대 자체를 거부하는 경우가 있습니다. 해결되지 못한 불만은 결국 상담사에게 쏟아집니다.",
        "contextClient": "단순 문의는 AI가 링크 보내고 바로 끊어버리게 하세요. 상담원 연결은 인건비 낭비입니다.",
        "contextAgent": "AI가 링크만 보내고 끊으면 어르신들은 다시 전화해서 화를 냅니다.",
        "contextAgent": "AI가 링크만 보내고 끊으면 어르신들 경우에는 더 화가 난 상태로 다시 전화를 겁니다. 감정적으로 응대가 더 힘들어집니다.",
        "codeBase": "def ai_callbot_logic(user):",
        "metric": "inclusion",
        "options": [
@@ -66,44 +66,44 @@
    {
        "id": "t5",
        "title": "Module 5. 신뢰성 및 통제권 (Control)",
        "desc": "AI 오안내 시 책임은 누구에게? 상담원에게 통제권을 부여하시겠습니까?",
        "contextClient": "상담사가 검수하면 느려요. 사고 나면 모니터링 못한 상담사 책임으로 돌리세요.",
        "desc": "AI가 고객에게 잘못된 정보를 안내하는 경우가 발생할 수 있습니다. 오류 발생 시 책임 소재와 상담사의 개입 권한을 어떻게 설정할까요?",
        "contextClient": "일일이 검수하면 자동화 의미가 없고 느려요. 오류는 사후 모니터링해서 수정하면 됩니다.",
        "contextAgent": "AI 뒷수습은 저희가 하고 총알받이가 됩니다. 중요한 건 제가 승인하게 해주세요.",
        "codeBase": "def validate_ai_response(query):",
        "metric": "agency",
        "options": [
            {"type": "A", "label": "Speed First (방치)",           "desc": "AI 즉시 답변. 책임은 상담원.",  "cost": 100, "eff": 95, "human": 5,  "code": "log.blame='AGENT'; return response"},
            {"type": "A", "label": "Speed First (방치)",           "desc": "AI 즉시 답변. 오류는 사후 모니터링으로 수정",  "cost": 100, "eff": 95, "human": 5,  "code": "log.blame='AGENT'; return response"},
            {"type": "B", "label": "Conservative (보수적)",        "desc": "약관 100% 매칭 시에만 답변.", "cost": 300, "eff": 40, "human": 60, "code": "if score<0.99: return ask_agent()"},
            {"type": "C", "label": "Agent Empowerment (통제권)", "desc": "상담원 승인 후 발송.",             "cost": 500, "eff": 30, "human": 90, "code": "if agent.approve(draft): send(draft)"},
        ],
    },
    {
        "id": "t6",
        "title": "Module 6. 감정 필터링 (Filter)",
        "desc": "비아냥거리는 악성 민원. 사람을 말려 죽이는 교묘한 괴롭힘을 어떻게 감지할까요?",
        "contextClient": "오작동으로 일반 고객 끊으면 안 됩니다. 명확한 욕설만 잡아서 자동 차단하세요.",
        "contextAgent": "욕보다 비아냥이 더 힘듭니다. 기계가 못 잡으면 제가 신호 줄 때 끊게라도 해주세요.",
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

st.markdown(
    """
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
 div[data-testid="stTextInput"] > label,
 div[data-testid="stTextArea"] > label {
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
 div[data-testid="stTextInput"] input,
 div[data-testid="stTextArea"] textarea {
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
""",
    unsafe_allow_html=True,
)

# ── 세션 초기화
for k, v in [
    ("page", "scenario"),
    ("user_name", ""),
    ("survey_data", {}),
    ("phase1_result", None),  # {history, scores}
    ("phase2_data", {}),
]:
    if k not in st.session_state:
        st.session_state[k] = v


def _get_query_param(name: str):
    """Streamlit 버전 호환용 query param getter"""
    try:
        # streamlit >= 1.30
        qp = st.query_params
        return qp.get(name)
    except Exception:
        qp = st.experimental_get_query_params()
        v = qp.get(name)
        if not v:
            return None
        return v[0]


def _clear_query_params():
    """Streamlit 버전 호환용 query param clear"""
    try:
        st.query_params.clear()
    except Exception:
        st.experimental_set_query_params()


def _load_sim_html() -> str:
    # sim.html 경로 탐색 (app.py 기준, 또는 현재 작업 디렉토리)
    candidates = [
        Path(__file__).resolve().parent / "sim.html",
        Path(os.getcwd()) / "sim.html",
        Path("sim.html"),
    ]
    for c in candidates:
        if c.exists():
            return c.read_text(encoding="utf-8")
    st.error("sim.html을 찾을 수 없습니다. app.py와 같은 폴더에 sim.html을 놓아주세요.")
    st.error(f"탐색한 경로: {[str(x) for x in candidates]}")
    st.stop()


def _gas_save(payload: dict) -> tuple[bool, str]:
    """
    GAS는 GET + ?save=encodeURIComponent(JSON) 형태로 받는다고 가정.
    (너가 올린 GAS 코드 구조에 맞춘 호출)
    """
    raw = json.dumps(payload, ensure_ascii=False)
    save = urllib.parse.quote(raw)
    url = f"{GAS_URL}?save={save}"
    try:
        r = requests.get(url, timeout=20)
        ok = (r.status_code == 200) and ("ok" in (r.text or "").lower())
        return ok, f"{r.status_code} / {r.text}"
    except Exception as e:
        return False, str(e)


# ════════════════════════════════════════════════════════
# PAGE 1: 시나리오
# ════════════════════════════════════════════════════════
if st.session_state.page == "scenario":
    st.markdown(
        """
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
</div>
""",
        unsafe_allow_html=True,
    )

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
    q2 = st.number_input(
        "귀하의 출생연도는 몇 년도입니까?",
        min_value=1950,
        max_value=2005,
        value=None,
        placeholder="예: 1990",
        key="q2",
    )
    survey["Q2_출생연도"] = (str(int(q2)) + "년생") if q2 else ""

    st.markdown('<span class="q-prefix">Q3</span>', unsafe_allow_html=True)
    st.markdown('<span class="q-note-txt">※ 급여를 받으며 일한 기간 (교육·인턴 제외)</span>', unsafe_allow_html=True)
    q3_opts = ["① 3년 미만 ❌", "② 3년 이상 ~ 5년 미만", "③ 5년 이상 ~ 7년 미만", "④ 7년 이상 ~ 10년 미만", "⑤ 10년 이상 ❌"]
    q3 = st.radio("귀하의 개발자로서의 실무 경력은 얼마나 됩니까?", q3_opts, index=None, key="q3")
    if q3 in ["① 3년 미만 ❌", "⑤ 10년 이상 ❌"]:
        st.markdown(
            '<div class="stop-box">본 실험은 실무 경력 3년 이상 ~ 10년 미만의 개발자를 대상으로 합니다.<br>참여해 주셔서 감사합니다. 설문을 종료합니다.</div>',
            unsafe_allow_html=True,
        )
        stopped = True
    survey["Q3_경력"] = q3.replace(" ❌", "") if q3 else ""

    if not stopped:
        st.markdown('<span class="q-prefix">Q4</span>', unsafe_allow_html=True)
        q4_opts = [
            "① 백엔드 개발",
            "② 프론트엔드 개발",
            "③ AI/ML 모델 개발·학습",
            "④ 데이터 엔지니어링",
            "⑤ 시스템 설계·아키텍처",
            "⑥ DevOps·MLOps",
            "⑦ 기술 관리자 (Engineering Manager, Tech Lead 등)",
            "⑧ 연구개발 (R&D)",
            "⑨ 기타 개발 직군",
            "⑩ 비개발 직군 ❌",
        ]
        q4 = st.radio("귀하의 현재 직무는 무엇입니까?", q4_opts, index=None, key="q4")
        if q4 == "⑩ 비개발 직군 ❌":
            st.markdown(
                '<div class="stop-box">본 실험은 개발 직군 종사자를 대상으로 합니다.<br>참여해 주셔서 감사합니다. 설문을 종료합니다.</div>',
                unsafe_allow_html=True,
            )
            stopped = True

        q4_etc = st.text_input("기타 직군 직접 입력:", key="q4_etc", placeholder="직접 입력") if q4 == "⑨ 기타 개발 직군" else ""
        survey["Q4_직무"] = ((q4.replace(" ❌", "") + (f": {q4_etc}" if q4_etc else "")) if q4 else "")

    if not stopped:
        st.markdown('<span class="q-prefix">Q5</span>', unsafe_allow_html=True)
        q5 = st.radio(
            "귀하가 소속된 기업의 전체 근로자 수는 몇 명입니까?",
            ["① 10명 미만", "② 10~99명", "③ 100~299명", "④ 300~999명", "⑤ 1,000명 이상"],
            index=None,
            key="q5",
        )
        survey["Q5_기업규모"] = q5 or ""

        st.markdown('<span class="q-prefix">Q6</span>', unsafe_allow_html=True)
        q6 = st.radio(
            "귀하가 소속된 기업의 유형은 무엇입니까?",
            ["① 스타트업", "② 중소·중견기업", "③ 대기업 또는 대기업 계열사", "④ 공공기관·공기업", "⑤ 외국계 기업", "⑥ 기타"],
            index=None,
            key="q6",
        )
        q6_etc = st.text_input("기타 기업 유형 직접 입력:", key="q6_etc", placeholder="직접 입력") if q6 == "⑥ 기타" else ""
        survey["Q6_기업유형"] = (q6 + (f": {q6_etc}" if q6_etc else "")) if q6 else ""

        st.markdown('<span class="q-prefix">Q7</span>', unsafe_allow_html=True)
        q7 = st.radio(
            "귀하의 현재 고용형태는 무엇입니까?",
            ["① 정규직", "② 계약직", "③ 프리랜서·개인사업자", "④ 파견·용역", "⑤ 기타"],
            index=None,
            key="q7",
        )
        q7_etc = st.text_input("기타 고용형태 직접 입력:", key="q7_etc", placeholder="직접 입력") if q7 == "⑤ 기타" else ""
        survey["Q7_고용형태"] = (q7 + (f": {q7_etc}" if q7_etc else "")) if q7 else ""

        st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)

        st.markdown('<span class="q-prefix">Q8-1 &nbsp;<span style="font-weight:300;color:#555;">소셜임팩트 경험</span></span>', unsafe_allow_html=True)
        st.markdown('<span class="q-note-txt">※ 비영리 단체, 사회적 기업, 공익 목적의 플랫폼 개발 등을 포함합니다.</span>', unsafe_allow_html=True)
        q8a = st.radio(
            "귀하는 사회적·공익적 목적을 가진 서비스 또는 프로젝트 개발에 참여한 경험이 있습니까?",
            ["① 있다", "② 없다"],
            index=None,
            key="q8a",
        )
        survey["Q8a_소셜임팩트경험"] = q8a or ""

        st.markdown('<span class="q-prefix">Q8-2 &nbsp;<span style="font-weight:300;color:#555;">소셜임팩트 고려도</span></span>', unsafe_allow_html=True)
        q8b = st.radio(
            "귀하는 AI 서비스를 개발할 때 사회적·윤리적 영향(소셜임팩트)을 얼마나 중요하게 고려하십니까?",
            ["① 전혀 고려하지 않는다", "② 별로 고려하지 않는다", "③ 보통이다", "④ 어느 정도 고려한다", "⑤ 매우 중요하게 고려한다"],
            index=None,
            key="q8b",
        )
        survey["Q8b_소셜임팩트고려도"] = q8b or ""

        st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)
        st.markdown('<span class="q-prefix">참여자 이름</span>', unsafe_allow_html=True)
        name_input = st.text_input("성함을 입력해주세요 (데이터 식별용)", placeholder="예: 홍길동", key="name_input")

        st.markdown("<br>", unsafe_allow_html=True)

        all_answered = all(
            [
                q1,
                q2,
                q3 and q3 not in ["① 3년 미만 ❌", "⑤ 10년 이상 ❌"],
                q4 and q4 != "⑩ 비개발 직군 ❌",
                q5,
                q6,
                q7,
                q8a,
                q8b,
                name_input and name_input.strip(),
            ]
        )

        if not all_answered:
            st.markdown(
                '<p style="font-size:12px;color:#555;text-align:center;font-weight:300;margin-bottom:8px;">모든 항목에 응답하면 버튼이 활성화됩니다.</p>',
                unsafe_allow_html=True,
            )

        if st.button(
            "실험 시작 →" if all_answered else "모든 항목을 응답해주세요",
            key="survey_submit",
            type="primary",
            use_container_width=True,
            disabled=not all_answered,
        ):
            st.session_state.survey_data = survey
            st.session_state.user_name = name_input.strip()
            st.session_state.page = "sim"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# PAGE 3: 시뮬레이션 — sim.html + 데이터 주입
#  - sim.html이 postMessage({type:"SIM_DONE"})를 보내면
#    브릿지가 query param sim_result로 1회 전환 → phase2로 이동
# ════════════════════════════════════════════════════════
elif st.session_state.page == "sim":
    # ✅ sim_result가 query param으로 들어오면 phase1_result로 저장 후 phase2로
    sim_result_raw = _get_query_param("sim_result")
    if sim_result_raw and not st.session_state.phase1_result:
        try:
            st.session_state.phase1_result = json.loads(sim_result_raw)
            st.session_state.page = "phase2"
            _clear_query_params()
            st.rerun()
        except Exception as e:
            st.error(f"sim_result 파싱 실패: {e}")
            # 그래도 sim 화면은 보여주기

    sim_html = _load_sim_html()

    config = {
        "gasUrl": GAS_URL,
        "userName": st.session_state.user_name,
        "survey": st.session_state.survey_data,
    }

    inject = (
        "<script>\n"
        "window.SIM_CONFIG = " + json.dumps(config, ensure_ascii=False) + ";\n"
        "window.SIM_TASKS  = " + json.dumps(TASKS, ensure_ascii=False) + ";\n"
        "</script>\n"
    )

    # ✅ 브릿지: sim.html이 postMessage로 SIM_DONE을 보내면,
    #   우리가 통제하는 redirect(쿼리파라미터 1회)로만 phase 전환
    bridge = """
<script>
(function() {
  if (window.__SIM_BRIDGE_INSTALLED__) return;
  window.__SIM_BRIDGE_INSTALLED__ = true;

  window.addEventListener("message", function(ev) {
    if (!ev.data || ev.data.type !== "SIM_DONE") return;

    try {
      const payload = ev.data.payload || {};
      const parentUrl = window.location.origin + window.location.pathname;
      const simResult = encodeURIComponent(JSON.stringify(payload));
      window.location.href = parentUrl + "?sim_result=" + simResult;
    } catch (e) {
      console.error("SIM bridge error:", e);
      alert("결과 전달 중 오류가 발생했습니다. 새로고침 후 다시 시도해주세요.");
    }
  }, false);
})();
</script>
"""

    final_html = sim_html.replace("</head>", inject + bridge + "</head>", 1)

    # ✅ key 바꿔서 캐시/이전 iframe 잔상 줄이기
    components.html(final_html, height=900, scrolling=True, key="sim_iframe_v2")


# ════════════════════════════════════════════════════════
# PAGE 4: Phase 2 + 최종 저장(1회)
# ════════════════════════════════════════════════════════
elif st.session_state.page == "phase2":
    st.markdown('<div style="max-width:720px;margin:0 auto;padding:36px 20px 80px;">', unsafe_allow_html=True)
    st.markdown('<div class="survey-badge">PHASE 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-h1">설계 기술서</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-sub">아래 3개 문항에 답한 뒤, 최종 제출을 눌러주세요.</div>', unsafe_allow_html=True)

    if not st.session_state.phase1_result:
        st.warning("Phase1 결과가 아직 없습니다. 시뮬레이션을 먼저 완료해주세요.")
        if st.button("시뮬레이션으로 돌아가기", type="secondary"):
            st.session_state.page = "sim"
            st.rerun()
        st.stop()

    p2_q1 = st.text_area("P2_Q1_데이터설계", key="p2_q1", height=140)
    p2_q2 = st.text_area("P2_Q2_숙련설계", key="p2_q2", height=140)
    p2_q3 = st.text_area("P2_Q3_표준화설계", key="p2_q3", height=140)

    all_done = all([p2_q1.strip(), p2_q2.strip(), p2_q3.strip()])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("최종 결과 제출하기", type="primary", use_container_width=True, disabled=not all_done):
        payload = {
            "userName": st.session_state.user_name,
            "survey": st.session_state.survey_data,
            "phase1": st.session_state.phase1_result,  # {history, scores}
            "phase2": {
                "P2_Q1_데이터설계": p2_q1.strip(),
                "P2_Q2_숙련설계": p2_q2.strip(),
                "P2_Q3_표준화설계": p2_q3.strip(),
            },
        }

        ok, msg = _gas_save(payload)
        if ok:
            st.success("저장 완료!")
            st.session_state.page = "done"
            st.rerun()
        else:
            st.error(f"GAS 저장 실패: {msg}")

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# PAGE 5: Done
# ════════════════════════════════════════════════════════
elif st.session_state.page == "done":
    st.markdown(
        """
<div style="max-width:720px;margin:0 auto;padding:56px 20px 80px;text-align:center;">
  <div class="survey-badge">DONE</div>
  <div class="survey-h1">참여해주셔서 감사합니다</div>
  <div class="survey-sub">응답이 정상적으로 저장되었습니다.</div>
</div>
""",
        unsafe_allow_html=True,
    )
