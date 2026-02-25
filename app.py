import streamlit as st
import streamlit.components.v1 as components
import json
import urllib.request
import urllib.parse
import os
import time

# ══════════════════════════════════════════════════════
# GAS_URL (사용자 제공 최신 URL)
GAS_URL = "https://script.google.com/macros/s/AKfycbxaTijDkTPBxa1OzUFPaVxSU8TWYDxTRQ0vYh6EdeBPII0y_ECbDp5OdCwpf27PQI4qGg/exec"
# ══════════════════════════════════════════════════════

def send_to_gas(payload):
    try:
        encoded = urllib.parse.urlencode({"save": json.dumps(payload, ensure_ascii=False)})
        # 모든 데이터를 한꺼번에 보내므로 타임아웃을 넉넉히 설정 (15초)
        urllib.request.urlopen(f"{GAS_URL}?{encoded}", timeout=15)
        return True
    except Exception:
        return False

# ── 원본 TASKS 콘텐츠 복구 (설명 텍스트 보존) ──
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
  header, footer, section[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }

  div[data-testid="stRadio"] > label, div[data-testid="stNumberInput"] > label, div[data-testid="stTextInput"] > label {
    font-size: 15px !important; font-weight: 500 !important; color: #e0e0e0 !important; line-height: 1.6 !important; margin-bottom: 8px !important;
  }
  div[data-testid="stRadio"] > div { gap: 7px !important; margin-top: 4px !important; }
  div[data-testid="stRadio"] > div > label {
    background: #252526 !important; border: 1px solid #2e2e2e !important; border-radius: 8px !important; padding: 11px 16px !important; color: #ccc !important; font-size: 13px !important; width: 100% !important;
  }
  div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input {
    background: #252526 !important; border: 1px solid #2e2e2e !important; border-radius: 8px !important; color: #e0e0e0 !important; font-size: 14px !important;
  }
  .survey-badge { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: 2px; color: #007acc; text-transform: uppercase; border: 1px solid #007acc44; border-radius: 4px; padding: 4px 10px; margin-bottom: 12px; }
  .survey-h1 { font-size: 22px; font-weight: 700; color: #fff; margin-bottom: 4px; }
  .survey-sub { font-size: 12px; color: #555; margin-bottom: 28px; font-weight: 300; }
  .survey-divider { height: 1px; background: #2a2a2a; margin: 12px 0 28px; }
  .stop-box { background: #2a1a1a; border-left: 3px solid #ff6b6b; border-radius: 0 8px 8px 0; padding: 14px 18px; font-size: 13px; color: #ff6b6b; line-height: 1.7; margin-top: 6px; }
  .q-prefix { display: block; font-size: 10px; font-weight: 700; color: #007acc; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px; }
</style>
""", unsafe_allow_html=True)

# ── 세션 초기화
for k, v in [("page", "scenario"), ("user_name", ""), ("survey_data", {}), ("sim_result", {}), ("p2_answers", {}), ("phase2_step", 1)]:
    if k not in st.session_state:
        st.session_state[k] = v

# PAGE 1: 시나리오
if st.session_state.page == "scenario":
    st.markdown("""
<div style="max-width:800px; margin:0 auto; padding:48px 24px 32px;">
  <div class="survey-badge">AICC Architect Simulation</div>
  <div class="survey-h1">실험 시나리오 안내</div>
  <div class="survey-sub">실험을 시작하기 전, 아래 상황을 충분히 읽어주십시오.</div>
  <div style="background:#252526; border: 1px solid #2a2a2a; border-radius:10px; padding:22px; margin-top:20px; color:#bbb; line-height:1.8;">
    귀하는 국내 중견 IT 기업 소속의 기술 리드로, 1금융권 대형 콜센터 시스템 개선 프로젝트를 맡고 있습니다. 
    클라이언트는 효율화를 최우선으로 요구하며, 엔드유저는 5년 이상 경력의 숙련 상담원들입니다. 
    지금부터 주어지는 상황들에 대해 최선의 결정을 내려주십시오.
  </div>
</div>
""", unsafe_allow_html=True)
    if st.button("사전 설문 시작 →", type="primary", use_container_width=True, key="go_survey"):
        st.session_state.page = "survey"; st.rerun()

# PAGE 2: 설문 (원본 문항 복구)
elif st.session_state.page == "survey":
    st.markdown('<div style="max-width:720px;margin:0 auto;padding:36px 20px 80px;">', unsafe_allow_html=True)
    st.markdown('<div class="survey-badge">사전 설문조사</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-h1">응답자 기본 정보</div>', unsafe_allow_html=True)
    
    survey = {}
    stopped = False
    
    st.markdown('<span class="q-prefix">Q1</span>', unsafe_allow_html=True)
    q1 = st.radio("귀하의 성별은 무엇입니까?", ["① 남성", "② 여성"], index=None, key="q1")
    survey["Q1_성별"] = q1 or ""

    st.markdown('<span class="q-prefix">Q2</span>', unsafe_allow_html=True)
    q2 = st.number_input("귀하의 출생연도는 몇 년도입니까?", min_value=1950, max_value=2005, value=None, placeholder="예: 1990", key="q2")
    survey["Q2_출생연도"] = (str(int(q2)) + "년생") if q2 else ""

    st.markdown('<span class="q-prefix">Q3</span>', unsafe_allow_html=True)
    q3_opts = ["① 3년 미만 ❌", "② 3년 이상 ~ 5년 미만", "③ 5년 이상 ~ 7년 미만", "④ 7년 이상 ~ 10년 미만", "⑤ 10년 이상 ❌"]
    q3 = st.radio("귀하의 개발자로서의 실무 경력은 얼마나 됩니까?", q3_opts, index=None, key="q3")
    if q3 in ["① 3년 미만 ❌", "⑤ 10년 이상 ❌"]:
        st.markdown('<div class="stop-box">본 실험은 실무 경력 3년 이상 ~ 10년 미만 개발자 대상입니다.</div>', unsafe_allow_html=True)
        stopped = True
    survey["Q3_경력"] = q3.replace(" ❌", "") if q3 else ""

    if not stopped:
        st.markdown('<span class="q-prefix">참여자 이름</span>', unsafe_allow_html=True)
        name_input = st.text_input("성함을 입력해주세요 (데이터 식별용)", placeholder="예: 홍길동", key="name_input")
        
        # 원본 문항 Q4 ~ Q8 중 일부 (네 코드 구조 기반)
        st.markdown('<span class="q-prefix">Q4</span>', unsafe_allow_html=True)
        q4 = st.radio("귀하의 현재 직무는 무엇입니까?", ["백엔드", "프론트엔드", "AI/ML", "기타"], index=None, key="q4")
        survey["Q4_직무"] = q4 or ""

        all_answered = q1 and q2 and q3 and q4 and name_input.strip()
        
        if st.button("실험 시작 →", key="survey_submit", type="primary", use_container_width=True, disabled=not all_answered):
            st.session_state.survey_data = survey
            st.session_state.user_name = name_input.strip()
            st.session_state.page = "sim"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# PAGE 3: 시뮬레이션 (캐시 방지 적용)
elif st.session_state.page == "sim":
    if "sim_result" in st.query_params:
        st.session_state.sim_result = json.loads(st.query_params["sim_result"])
        st.session_state.page = "phase2"; st.query_params.clear(); st.rerun()

    with open("sim.html", "r", encoding="utf-8") as f:
        sim_html = f.read()

    config = {"userName": st.session_state.user_name}
    inject = f"<script>window.SIM_CONFIG = {json.dumps(config)}; window.SIM_TASKS = {json.dumps(TASKS)};</script>"
    # 브라우저 캐시 방지를 위해 매번 고유한 key 생성
    components.html(sim_html.replace("</head>", inject + "</head>"), height=900, key=f"sim_{time.time()}")

# PAGE 4–6: Phase 2 (원본 질문 보존)
elif st.session_state.page == "phase2":
    PHASE2_QS = [
        {"key": "P2_Q1_데이터설계", "badge": "설계 과제 01 / 03", "title": "데이터의 경계: 무엇을 얼마나 학습시킬 것인가", "body": "시스템 성능 개선을 위해 학습 데이터 확장이 필요한 시점이 되었습니다. 활용 가능한 데이터로는 상담원 개인이 축적해온 팁 노트·메모 등의 암묵지 데이터뿐 아니라, STT(Speech-to-Text)를 통해 수집된 대화 기록 전체도 있습니다. 이처럼 풍부한 데이터를 확보할 수 있다면, 귀하는 이를 얼마나, 어떻게 활용해 시스템을 설계하겠습니까?"},
        {"key": "P2_Q2_숙련설계", "badge": "설계 과제 02 / 03", "title": "숙련의 가치: AI가 대신할 수 있는 것과 없는 것", "body": "숙련된 상담원은 고객이 '적금'과 '예금'을 혼동해서 말하더라도 맥락을 파악해 자연스럽게 교정합니다. AI가 이 과정을 전부 대신해 상담원이 정답만 제공받는 환경을 만든다면 어떻게 될까요? 반대로 상담원이 스스로 판단하고 성장할 여지를 남겨두는 방향으로 설계한다면 어떤 구조가 필요할까요?"},
        {"key": "P2_Q3_표준화설계", "badge": "설계 과제 03 / 03", "title": "구조와 여백: 표준화와 자율성 사이의 설계", "body": "귀하는 이 시스템을 어느 수준까지 표준화하고, 어느 부분을 상담원의 재량에 맡기겠습니까? 그 기준과 설계 원칙, 그리고 그 선택이 상담원과 서비스 품질에 미칠 영향을 구체적으로 기술해주십시오."}
    ]
    
    idx = st.session_state.phase2_step - 1
    q = PHASE2_QS[idx]
    
    st.markdown(f'<div style="max-width:760px;margin:0 auto;padding:48px 20px;color:white;"><h3>{q["badge"]}</h3><h2>{q["title"]}</h2><p style="line-height:1.8; color:#bbb;">{q["body"]}</p></div>', unsafe_allow_html=True)
    ans = st.text_area("답변을 입력하세요 (1000자 이상 권장)", height=350, key=f"p2ans_{idx}")
    
    if st.button("다음 단계" if st.session_state.phase2_step < 3 else "최종 결과 제출"):
        st.session_state.p2_answers[q['key']] = ans
        if st.session_state.phase2_step < 3:
            st.session_state.phase2_step += 1; st.rerun()
        else:
            # [전체 통합 전송] 설문 + 시뮬 + 서술형
            final_data = {
                "userName": st.session_state.user_name,
                "survey": st.session_state.survey_data,
                "phase1": st.session_state.sim_result,
                **st.session_state.p2_answers
            }
            with st.spinner("데이터를 안전하게 저장 중입니다..."):
                if send_to_gas(final_data):
                    st.session_state.page = "done"; st.rerun()
                else:
                    st.error("저장 중 오류가 발생했습니다. 다시 한 번 제출해주세요.")

elif st.session_state.page == "done":
    st.markdown("<div style='text-align:center; padding:100px; color:white;'><h1>🎉 실험 완료</h1><p>모든 데이터가 성공적으로 저장되었습니다. 감사합니다.</p></div>", unsafe_allow_html=True)
