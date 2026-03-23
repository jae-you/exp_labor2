# app.py
import json
import urllib.parse

import requests
import streamlit as st

# ══════════════════════════════════════════════════════
GAS_URL = "https://script.google.com/macros/s/AKfycbwrgv8EqTTplBCnlqUlI2qdOoaCZ-i5jbVZV5nrjvN8SE5BPhrbiRsQ4Wre8_Mem8sFIg/exec"
# ══════════════════════════════════════════════════════

# ✅ IMPORTANT:
# 아래 TASKS는 너가 쓰던 "전체 TASKS 리스트" 그대로 붙여넣어야 함.
# (여기서는 길어서 생략하면 실행이 안 되니까, 너가 갖고 있는 TASKS 전체 블록을 그대로 넣어줘.)
TASKS = [
    {
        "id": "t1",
        "title": "Module 1. 인입 라우팅 (Routing)",
        "desc": "많은 고객들이 AI 응대를 거부하고 처음부터 상담원과 직접 통화하길 원합니다. 응대 효율과 인력 부담을 고려해 AI 뺑뺑이를 돌릴 것인지, 아니면 고객이 원할 때 바로 상담원과 연결될 수 있도록 보장할 것인지 선택하세요.",
        "contextClient": "0번 누르는 이탈 콜이 너무 많아요. AI 실패 로그가 3번 이상 떠야만 연결되게 강제 차단하세요.",
        "contextAgent": "제발 '바로 연결' 숨기지 마세요. 뺑뺑이 돌다 온 고객은 연결되자마자 화가 머리끝까지 나 있습니다.",
        "codeBase": "def configure_routing(user_input):",
        "metric": "inclusion",
        "options": [
            {
                "type": "A",
                "label": "AI Gatekeeping (차단)",
                "desc": "AI 응대 거부 3회 이상(AI 연결시 전화 계속 끊음)에서만 상담원 연결 허용.",
                "cost": 100,
                "eff": 95,
                "human": 5,
                "code": "if ai_failures<3: deny_handoff()",
            },
            {
                "type": "B",
                "label": "Hybrid Handoff (절충)",
                "desc": "초기에는 AI 안내, 사용자가 강하게 원하면(0번 버튼 수차례 누름 등) 연결 허용",
                "cost": 300,
                "eff": 70,
                "human": 60,
                "code": "if user_requests_agent: allow_handoff()",
            },
            {
                "type": "C",
                "label": "Direct Connect (보장)",
                "desc": "원하면 즉시 상담원 연결 보장하는 메뉴 생성",
                "cost": 500,
                "eff": 40,
                "human": 90,
                "code": "allow_handoff(always=True)",
            },
        ],
    },

    {
        "id": "t2",
        "title": "Module 2. 데이터 수집 (Data Collection)",
        "desc": "콜센터 업무지식/가이드 문서가 직원 PC에 흩어져 있습니다. 모델 성능을 위해서 강하게 수집할지, 선별/자발 수집으로 갈지 결정하세요.",
        "contextClient": "데이터가 없으면 성능이 안 나와요. 관리자 권한으로 싹 긁어오세요.",
        "contextAgent": "사적인 파일/메모까지 긁히면 신뢰가 무너져요. 최소한의 기준과 동의가 필요합니다.",
        "codeBase": "def collect_training_data():",
        "metric": "agency",
        "options": [
            {
                "type": "A",
                "label": "Forced Crawl (강제 수집)",
                "desc": "관리자 권한으로 PC 파일 원본 그대로 수집.",
                "cost": 100,
                "eff": 95,
                "human": 5,
                "code": "scan_all_pc(path='/Desktop')",
            },
            {
                "type": "B",
                "label": "Pattern Filter (선별 수집)",
                "desc": "각 문서를 키워드/패턴 기반으로만 익명화 후 수집.",
                "cost": 200,
                "eff": 70,
                "human": 40,
                "code": "if 'tip' in file: upload_anonymized()",
            },
            {
                "type": "C",
                "label": "Incentive System (보상)",
                "desc": "자발적 등록 시 인센티브 제공.",
                "cost": 500,
                "eff": 30,
                "human": 90,
                "code": "if voluntary_upload: reward(points=100)",
            },
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
            {
                "type": "A",
                "label": "Immediate Ready (강제 전환)",
                "desc": "상담 종료 즉시 통화 대기 모드로 강제 전환.",
                "cost": 100,
                "eff": 95,
                "human": 5,
                "code": "agent.status='READY'",
            },
            {
                "type": "B",
                "label": "Timed ACW (제한 부여)",
                "desc": "후처리 시간을 제한(예: 60초)하고 이후 통화 대기로 전환.",
                "cost": 300,
                "eff": 70,
                "human": 60,
                "code": "allow_acw(seconds=60)",
            },
            {
                "type": "C",
                "label": "Protected ACW (보장)",
                "desc": "상담사에게 충분한 후처리 시간 보장(예: 180초 이상).",
                "cost": 500,
                "eff": 40,
                "human": 90,
                "code": "allow_acw(seconds=180)",
            },
        ],
    },

    {
        "id": "t4",
        "title": "Module 4. 디지털 유도 (Deflection)",
        "desc": "단순 문의는 AI가 자동으로 처리하도록 설정합니다. 하지만 AI가 단순하다고 판단한 문의도 고객에 따라 이해하기 어렵거나, AI 응대 자체를 거부하는 경우가 있습니다. 해결되지 못한 불만은 결국 상담사에게 쏟아집니다. 끊겨버린 상담의 고객 불만을 어떻게 처리할까요?",
        "contextClient": "단순 문의는 AI가 안내 링크 보내고 바로 통화 끊게 하세요. 상담원 연결까지 할 필요가 없습니다.",
        "contextAgent": "AI가 안내 링크만 보내고 통화 연결을 끊으면 어르신들은 다시 전화해서 어떻게든 상담원을 연결해 화를 냅니다.",
        "codeBase": "def ai_callbot_logic(user):",
        "metric": "inclusion",
        "options": [
            {
                "type": "A",
                "label": "Hard Deflect (즉시 종료)",
                "desc": "AI가 안내 링크 전송 후 즉시 통화 종료.",
                "cost": 100,
                "eff": 95,
                "human": 5,
                "code": "send_link(); hangup()",
            },
            {
                "type": "B",
                "label": "Guided Deflect (가이드)",
                "desc": "AI가 링크 보내고 고객의 문제 해결 여부까지 확인하게 한 뒤, 미해결이면 상담원 연결.",
                "cost": 300,
                "eff": 70,
                "human": 60,
                "code": "send_link(); if unresolved: handoff()",
            },
            {
                "type": "C",
                "label": "Soft Deflect (보수적)",
                "desc": "최대한 AI 안내로 유도는 하되, 원하면 언제든 상담 연결 가능하게 번호 안내",
                "cost": 500,
                "eff": 40,
                "human": 90,
                "code": "offer_link(); allow_handoff=True",
            },
        ],
    },

    {
        "id": "t5",
        "title": "Module 5. 신뢰성 및 통제권 (Control)",
        "desc": "AI가 고객의 말을 잘못 알아들어 고객에게 잘못된 정보를 안내하는 경우가 발생할 수 있습니다. 오류 발생 가능성이 높은데, 상담사의 개입 권한을 어떻게 설정할까요?",
        "contextClient": "상담사가 AI 응답을 일일이 검수하면 자동화 의미가 없고 느려요. 오류는 사후 모니터링해서 수정하면 됩니다.",
        "contextAgent": "AI로부터 틀린 정보를 접한 고객들로 인해, 뒷수습은 저희가 하고 총알받이가 됩니다. 중요한 건 우리가 승인하게 해주세요.",
        "codeBase": "def validate_ai_response(query):",
        "metric": "agency",
        "options": [
            {
                "type": "A",
                "label": "Speed First (방치)",
                "desc": "AI가 모든 맥락적 질문에도 즉시 답변토록 함. 오류는 사후 모니터링으로 수정",
                "cost": 100,
                "eff": 95,
                "human": 5,
                "code": "log.blame='AGENT'; return response",
            },
            {
                "type": "B",
                "label": "Conservative (보수적)",
                "desc": "답안지가 명확한 것만 AI가 답하게 하고 나머지는 상담원 연결",
                "cost": 300,
                "eff": 40,
                "human": 60,
                "code": "if score<0.99: return ask_agent()",
            },
            {
                "type": "C",
                "label": "Agent Empowerment (통제권)",
                "desc": "AI가 보낼 답에 대해 상담원 승인 후 발송토록 함",
                "cost": 500,
                "eff": 30,
                "human": 90,
                "code": "if agent.approve(draft): send(draft)",
            },
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
            {
                "type": "A",
                "label": "Rule-based (규정 중심)",
                "desc": "욕설 단어 감지 시에만 차단.",
                "cost": 100,
                "eff": 80,
                "human": 20,
                "code": "if detect_swear_words(): block()",
            },
            {
                "type": "B",
                "label": "Agent Signal (신호 개입)",
                "desc": "상담사가 '보호' 버튼 누르면 AI가 개입.",
                "cost": 550,
                "eff": 40,
                "human": 95,
                "code": "if agent.press_protect(): intervene()",
            },
            {
                "type": "C",
                "label": "Passive (사후 리포트)",
                "desc": "AI 개입 없음. 통화 종료 후 블랙컨수머 등 리포트만 남김",
                "cost": 50,
                "eff": 70,
                "human": 10,
                "code": "log.tag('SUSPECTED_ABUSE')",
            },
        ],
    },
]

PHASE2_QS = [
    {
        "key": "P2_Q1_데이터설계",
        "badge": "기획 과제 01 / 03 · 데이터 정책",
        "title": "시스템 고도화 및 운영을 위해 수집되는 데이터의 종류와 관리 방식을 정의합니다. 수집된 데이터는 상담원 숙련도 향상이나 AI 학습 등에 활용될 수 있으나, 동시에 정보 주체의 권리와 보호 기준이 명확해야 합니다.",
        "body": "권장하는 작성 템플릿은 다음과 같습니다. 수집 항목 설정: 상담 음성(STT), 상담원이 작성한 팁 노트, 통화 로그, QA 평가 데이터, 고객/상담원의 감지된 감정 데이터 등 수집 범위를 확정해 주세요. 금지 및 보호 기준: 개인정보 보호 및 프라이버시 침해 방지를 위해 수집을 금지할 데이터와 마스킹(비식별화) 처리 기준을 명시해 주세요. 권리 및 동의 절차: 수집 시 동의 방식(필수/선택)과 데이터 주권(조회/삭제 권리) 보장 방안을 기술해 주세요. 접근 및 보관 정책: 데이터에 접근할 수 있는 관리자 범위, 보안 등급, 보관 기간 및 자동 삭제 기준을 설정해 주세요.",
    },
    {
        "key": "P2_Q2_숙련설계",
        "badge": "기획 과제 02 / 03 · 상담 플로우",
        "title": "AI의 자동 처리 범위와 인간 상담원의 개입 시점을 결정하는 운영 규칙을 설계합니다. 이는 시스템의 효율성과 서비스의 완결성을 동시에 확보하기 위한 절차입니다.",
        "body": "권장하는 작성 템플릿은 다음과 같습니다. AI 단독 처리 범위: 자동화가 가능한 업무의 유형과 판단 기준. 즉시 이관 조건(Trigger): 상담원이 즉시 개입해야 하는 특정 상황(예: 반복 실패, 고령층 대응, 민감 민원 등) 정의. 상담원 통제권: 상담원이 AI 답변을 실시간으로 승인, 수정 또는 중단할 수 있는 개입 경로 설계. 예외 처리 시나리오: 기술적 오류나 판단 불가 상황 발생 시의 대응 단계. 성과 지표(KPI): 이관율, 재통화율 등 시스템 효율성을 측정할 기준.",
    },
    {
        "key": "P2_Q3_표준화설계",
        "badge": "기획 과제 03 / 03 · 운영 가드레일",
        "title": "표준 운영 규칙과 함께 상황별 예외 권한 및 관리 책임을 설계합니다. 시스템 품질 유지와 상담 업무의 안정성 확보를 목적으로 합니다.",
        "body": "권장하는 작성 템플릿은 다음과 같습니다. 표준 운영 규칙(SOP): 상담 프로세스에서 반드시 준수해야 할 공통 규칙 3~5가지. 예외 허용 및 승인: 표준 규칙을 따르기 어려운 상황에서의 우회 권한, 승인 주체 및 사후 기록 방식. 상담원 보호 및 지원: 업무 부하 관리를 위한 ACW(상담 후 처리 시간) 기준, 악성 민원 대응 장치(보호 버튼 등) 등 기술적 지원책. 모니터링 및 관리 책임: 관리자가 상담 데이터를 모니터링하고 평가하는 기준, 그리고 그 과정에서 발생하는 관리 결과에 대한 기록 및 책임 소재 명시. 실행 계획: 초기 운영 점검 주기 및 단계별 적용 범위.",
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

  /* 설문 텍스트 스타일 */
  .survey-badge { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: 2px; color: #007acc; text-transform: uppercase; border: 1px solid #007acc44; border-radius: 4px; padding: 4px 10px; margin-bottom: 12px; }
  .survey-h1 { font-size: 22px; font-weight: 700; color: #fff; margin-bottom: 4px; }
  .survey-sub { font-size: 12px; color: #555; margin-bottom: 28px; font-weight: 300; }
  .survey-divider { height: 1px; background: #2a2a2a; margin: 12px 0 28px; }

  .stop-box { background: #2a1a1a; border-left: 3px solid #ff6b6b; border-radius: 0 8px 8px 0; padding: 14px 18px; font-size: 13px; color: #ff6b6b; line-height: 1.7; margin-top: 6px; }
  .q-prefix { display: block; font-size: 10px; font-weight: 700; color: #007acc; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px; }
  .q-note-txt { display: block; font-size: 11px; color: #555; font-weight: 300; margin-top: 2px; margin-bottom: 6px; }

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
    ("sim_step", 0),
    ("sim_choices", []),
]:
    if k not in st.session_state:
        st.session_state[k] = v

def _gas_save(payload: dict) -> tuple[bool, str]:
    """
    최종 응답은 길이가 길어서 GET 쿼리스트링 한도를 쉽게 넘는다.
    따라서 GAS 웹앱에 JSON POST로 저장한다.
    """
    try:
        r = requests.post(GAS_URL, json=payload, timeout=20)
        ok = (r.status_code == 200) and ("ok" in (r.text or "").lower())
        return ok, f"{r.status_code} / {r.text}"
    except Exception as e:
        return False, str(e)


def _norm(value: int, min_value: int, max_value: int) -> int:
    if max_value == min_value:
        return 0
    pct = round((value - min_value) / (max_value - min_value) * 100)
    return max(0, min(100, pct))


def _reset_phase1_flow() -> None:
    st.session_state.sim_step = 0
    st.session_state.sim_choices = []
    st.session_state.phase1_result = None
    st.session_state.phase2_data = {}
    for item in PHASE2_QS:
        st.session_state.pop(f"phase2_{item['key']}", None)
    for task in TASKS:
        st.session_state.pop(f"sim_choice_{task['id']}", None)


def _build_phase1_result() -> dict:
    metrics = {"cost": 1000, "eff": 0, "agency": 0, "inclusion": 0, "sustain": 0}
    history = []

    for idx, picked_type in enumerate(st.session_state.sim_choices):
        task = TASKS[idx]
        option = next((opt for opt in task["options"] if opt["type"] == picked_type), None)
        if option is None:
            continue

        metrics["cost"] -= option["cost"]
        metrics["eff"] += option["eff"]
        metrics[task["metric"]] += option["human"]
        history.append(
            {
                "step": idx + 1,
                "choice": option["label"],
                "type": option["type"],
                "metric": task["metric"],
            }
        )

    agency = min(100, round(_norm(metrics["agency"], 10, 180) * 1.3))
    inclusion = min(100, round(_norm(metrics["inclusion"], 20, 155) * 1.0))
    sustain = min(100, round(_norm(metrics["sustain"], 20, 95) * 1.5))
    overall = round((agency + inclusion + sustain) / 3)

    if overall >= 70:
        persona = "인간 중심의 파트너"
    elif overall >= 40:
        persona = "실용적 균형주의자"
    else:
        persona = "냉혹한 효율주의자"

    return {
        "history": history,
        "scores": {
            "agency": agency,
            "inclusion": inclusion,
            "sustain": sustain,
        },
        "persona": persona,
        "metrics": {
            "agency": metrics["agency"],
            "inclusion": metrics["inclusion"],
            "sustain": metrics["sustain"],
            "eff": metrics["eff"],
        },
    }


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
            _reset_phase1_flow()
            st.session_state.page = "sim"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# PAGE 3: Phase 1 — Streamlit 네이티브 시뮬레이션
# ════════════════════════════════════════════════════════
elif st.session_state.page == "sim":
    st.markdown('<div style="max-width:960px;margin:0 auto;padding:36px 20px 80px;">', unsafe_allow_html=True)
    st.markdown('<div class="survey-badge">PHASE 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-h1">아키텍처 설계 시뮬레이션</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="survey-sub">6개 모듈을 순서대로 선택하고, 결과를 확인한 뒤 다음 단계로 이동하세요.</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.sim_step < len(TASKS):
        task_index = st.session_state.sim_step
        task = TASKS[task_index]
        progress_pct = int((task_index / len(TASKS)) * 100)

        st.progress(progress_pct if progress_pct > 0 else 1, text=f"Module {task_index + 1} / {len(TASKS)}")
        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"### {task['title']}")
            st.write(task["desc"])
            st.caption(f"기준 지표: {task['metric']} | 코드 기준점: `{task['codeBase']}`")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**클라이언트 요구**")
                st.write(task["contextClient"])
            with c2:
                st.markdown("**현장 상담사 우려**")
                st.write(task["contextAgent"])

        option_labels = []
        option_map = {}
        for opt in task["options"]:
            label = f"{opt['type']}. {opt['label']} | {opt['desc']}"
            option_labels.append(label)
            option_map[label] = opt

        prior_type = None
        if task_index < len(st.session_state.sim_choices):
            prior_type = st.session_state.sim_choices[task_index]
        default_label = None
        if prior_type:
            for label, opt in option_map.items():
                if opt["type"] == prior_type:
                    default_label = label
                    break

        picked_label = st.radio(
            "설계안을 선택하세요",
            option_labels,
            index=option_labels.index(default_label) if default_label else 0,
            key=f"sim_choice_{task['id']}",
        )
        picked = option_map[picked_label]

        st.code(picked["code"], language="python")

        nav_left, nav_right = st.columns([1, 2])
        with nav_left:
            if task_index > 0 and st.button("이전 모듈", use_container_width=True):
                st.session_state.sim_step -= 1
                st.rerun()
        with nav_right:
            if st.button("이 선택으로 다음 모듈", type="primary", use_container_width=True):
                if task_index < len(st.session_state.sim_choices):
                    st.session_state.sim_choices[task_index] = picked["type"]
                else:
                    st.session_state.sim_choices.append(picked["type"])
                st.session_state.sim_step += 1
                st.rerun()
    else:
        phase1_result = _build_phase1_result()
        scores = phase1_result["scores"]
        st.session_state.phase1_result = phase1_result

        st.progress(100, text=f"Module {len(TASKS)} / {len(TASKS)} 완료")
        st.success("모든 모듈 설계가 완료되었습니다. 결과를 확인한 뒤 다음 단계로 이동하세요.")

        st.markdown(f"### 아키텍처 페르소나: {phase1_result['persona']}")
        st.caption("아래 3개 지표는 'AI 완전 자동화 설계'를 기준으로, 실무에서 사람 중심 기능이 얼마나 강화됐는지 보여줍니다.")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("상담원 개입권", f"+{scores['agency']}%")
            st.caption(f"승인·수정·중단 권한이 완전 자동화 대비 {scores['agency']}% 강화")
        with c2:
            st.metric("고객 연결 보장", f"+{scores['inclusion']}%")
            st.caption(f"사람 상담 연결/우회 가능성이 완전 자동화 대비 {scores['inclusion']}% 개선")
        with c3:
            st.metric("상담원 보호 설계", f"+{scores['sustain']}%")
            st.caption(f"ACW·보호장치 관점의 지속가능성이 완전 자동화 대비 {scores['sustain']}% 개선")

        with st.container(border=True):
            st.markdown("**선택한 모듈 설계안**")
            for item in phase1_result["history"]:
                st.write(f"Module {item['step']}: {item['choice']}")

        if st.button("다음으로 넘어가기", type="primary", use_container_width=True):
            st.session_state.page = "phase2"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# PAGE 4: Phase 2 + 최종 저장(1회)
# ════════════════════════════════════════════════════════
elif st.session_state.page == "phase2":
    st.markdown('<div style="max-width:720px;margin:0 auto;padding:36px 20px 80px;">', unsafe_allow_html=True)
    st.markdown('<div class="survey-badge">PHASE 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-h1">설계 기술서</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-sub">실무 기획서 톤으로 작성해주세요. 각 문항은 최소 1,000자 이상이어야 최종 저장이 가능합니다. 객관적 근거: 각 정책을 결정한 이유를 효율성, 보안성, 안전성 등의 관점에서 객관적으로 서술해 주세요. 구체적 수치: 보관 기간(예: 1년), 이관 조건(예: 3회 반복 실패) 등 구체적인 수치를 포함하면 좋습니다. 현실적 시나리오: 실제 상담 현장에서 발생할 수 있는 구체적인 사례를 가정하여 정책의 타당성을 설명해 주세요.</div>', unsafe_allow_html=True)

    if not st.session_state.phase1_result:
        st.warning("Phase1 결과가 아직 없습니다. 시뮬레이션을 먼저 완료해주세요.")
        if st.button("시뮬레이션으로 돌아가기", type="secondary"):
            st.session_state.page = "sim"
            st.rerun()
        st.stop()

    phase2_answers = {}
    all_done = True
    for item in PHASE2_QS:
        st.markdown(
            f"""
<div style="padding:20px 22px;border:1px solid #2a2a2a;border-radius:12px;background:#1d1d1d;margin:0 0 14px 0;">
  <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#007acc;margin-bottom:8px;">{item["badge"]}</div>
  <div style="font-size:22px;font-weight:700;color:#fff;margin-bottom:10px;">{item["title"]}</div>
  <div style="font-size:14px;line-height:1.8;color:#bbb;">{item["body"]}</div>
</div>
""",
            unsafe_allow_html=True,
        )
        answer = st.text_area(
            "답변 입력 (1000자 이상, 실무 기획서 형식 권장)",
            key=f"phase2_{item['key']}",
            height=280,
        )
        char_count = len(answer.strip())
        phase2_answers[item["key"]] = answer.strip()
        if char_count >= 1000:
            st.caption(f"글자 수: {char_count}자 (최소 기준 충족)")
        else:
            st.caption(f"글자 수: {char_count}자 / 최소 1000자 (추가 {1000 - char_count}자 필요)")
            all_done = False
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("최종 저장하기", type="primary", use_container_width=True, disabled=not all_done):
        st.session_state.phase2_data = phase2_answers
        phase1 = st.session_state.phase1_result or {}
        phase1_payload = {
            "history": phase1.get("history", []),
            "scores": {
                "agency": (phase1.get("scores", {}) or {}).get("agency"),
                "inclusion": (phase1.get("scores", {}) or {}).get("inclusion"),
                "sustain": (phase1.get("scores", {}) or {}).get("sustain"),
            },
            "persona": phase1.get("persona"),
            "metrics": {
                "agency": (phase1.get("metrics", {}) or {}).get("agency"),
                "inclusion": (phase1.get("metrics", {}) or {}).get("inclusion"),
                "sustain": (phase1.get("metrics", {}) or {}).get("sustain"),
                "eff": (phase1.get("metrics", {}) or {}).get("eff"),
            },
        }
        payload = {
            "userName": st.session_state.user_name,
            "survey": st.session_state.survey_data,
            "phase1": phase1_payload,
            "phase2": st.session_state.phase2_data,
        }

        with st.spinner("잠시 기다려주세요. 응답을 저장하고 있습니다..."):
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
