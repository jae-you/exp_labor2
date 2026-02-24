import streamlit as st
import streamlit.components.v1 as components
import json
import urllib.request
import urllib.parse

# ══════════════════════════════════════════════════════
# GAS_URL 업데이트
GAS_URL = "https://script.google.com/macros/s/AKfycbyEB0gBk4KjbhH-18lRGSGG8yE3v0KHiCv90KZDDEvFtmcp7cTO3sDszG66l7fUW4GlTg/exec"
# ══════════════════════════════════════════════════════

# [데이터 전송 헬퍼 함수]
def send_to_gas(payload):
    try:
        encoded = urllib.parse.urlencode({"save": json.dumps(payload, ensure_ascii=False)})
        urllib.request.urlopen(f"{GAS_URL}?{encoded}", timeout=5)
        return True
    except Exception:
        return False

# 업데이트된 TASKS 데이터
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

# (CSS 및 스타일 부분 생략 - 원본 유지)
st.set_page_config(page_title="AICC Simulation", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
  html, body, * { font-family: 'Noto Sans KR', sans-serif !important; }
  .stApp { background: #1e1e1e; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  header, footer, section[data-testid="stSidebar"],
  [data-testid="collapsedControl"] { display: none !important; }
  /* (기타 스타일 생략) */
</style>
""", unsafe_allow_html=True)

# ── 세션 초기화
for k, v in [("page", "scenario"), ("user_name", ""), ("survey_data", {}), ("phase2_step", 1)]:
    if k not in st.session_state:
        st.session_state[k] = v

# PAGE 1: 시나리오
if st.session_state.page == "scenario":
    # (원본 시나리오 컨텐츠 유지)
    if st.button("사전 설문 시작 →", type="primary", use_container_width=True, key="go_survey"):
        st.session_state.page = "survey"
        st.rerun()

# PAGE 2: 설문 (수정: 제출 시 GAS 전송 추가)
elif st.session_state.page == "survey":
    # (원본 설문 UI 구성 유지)
    # ...
    # (survey dictionary 수집 로직)
    
    # [설문 UI 하단 제출 버튼 부분]
    if st.button("실험 시작 →", key="survey_submit", type="primary", use_container_width=True):
        st.session_state.survey_data = survey # 실제 코드에서는 위에서 정의된 survey 변수 사용
        st.session_state.user_name = name_input.strip()
        
        # [수정] 설문 데이터 즉시 저장
        send_to_gas({
            "phase": "survey",
            "userName": st.session_state.user_name,
            "data": st.session_state.survey_data
        })
        
        st.session_state.page = "sim"
        st.rerun()

# PAGE 3: 시뮬레이션
elif st.session_state.page == "sim":
    # (원본 sim.html 호출 및 injection 유지)
    # ...
    # (GOTO_PHASE2 이벤트 리스너 유지)

# PAGE 4–6: Phase 2 (수정: 단계별 저장 및 최종 저장 보강)
elif st.session_state.page == "phase2":
    PHASE2_QS = [
        # (원본 질문 리스트 유지)
    ]
    
    step = st.session_state.phase2_step
    q = next(x for x in PHASE2_QS if x["step"] == step)
    
    # (Phase 2 UI 및 TextArea 구성 유지)
    # ...

    if st.button(btn_label, type="primary", use_container_width=True, key=f"p2_next_{step}", disabled=not is_ok):
        # [수정] Phase 2 답변 저장
        payload = {
            "phase": "phase2",
            "userName": st.session_state.user_name,
            "step": step,
            "gasKey": q["gas_key"],
            "answer": answer
        }
        
        # 마지막 단계라면 설문 답변까지 포함해서 "최종 패키지"로 보냄
        if step == 3:
            payload["is_final"] = True
            payload["survey_snapshot"] = st.session_state.survey_data
            
        send_to_gas(payload)

        if step < 3:
            st.session_state.phase2_step = step + 1
            st.rerun()
        else:
            st.session_state.page = "done"
            st.rerun()

# PAGE 7: 완료
elif st.session_state.page == "done":
    # (완료 화면 유지)
