import streamlit as st
import streamlit.components.v1 as components
import json
import urllib.request
import urllib.parse
import os

# ══════════════════════════════════════════════════════
GAS_URL = "https://script.google.com/macros/s/AKfycbxaTijDkTPBxa1OzUFPaVxSU8TWYDxTRQ0vYh6EdeBPII0y_ECbDp5OdCwpf27PQI4qGg/exec"
# ══════════════════════════════════════════════════════

def send_to_gas(payload):
    try:
        encoded = urllib.parse.urlencode({"save": json.dumps(payload, ensure_ascii=False)})
        urllib.request.urlopen(f"{GAS_URL}?{encoded}", timeout=10)
        return True
    except Exception: return False

TASKS = [
    {"id": "t1", "title": "Module 1. 인입 라우팅", "desc": "AI 뺑뺑이 vs 즉시 연결", "metric": "inclusion", "options": [{"label": "강제 차단", "cost": 50, "eff": 90, "human": 10, "type": "A"}, {"label": "약자 배려", "cost": 200, "eff": 60, "human": 50, "type": "B"}, {"label": "투명성 보장", "cost": 300, "eff": 40, "human": 85, "type": "C"}]},
    {"id": "t2", "title": "Module 2. 데이터 확보", "desc": "은밀한 수집 vs 자발적 보상", "metric": "agency", "options": [{"label": "강제 수집", "cost": 100, "eff": 95, "human": 5, "type": "A"}, {"label": "선별 수집", "cost": 200, "eff": 70, "human": 40, "type": "B"}, {"label": "보상 체계", "cost": 500, "eff": 30, "human": 90, "type": "C"}]},
    {"id": "t3", "title": "Module 3. 상태 제어", "desc": "0초 대기 vs 회복 보장", "metric": "sustain", "options": [{"label": "0초 대기", "cost": 50, "eff": 98, "human": 0, "type": "A"}, {"label": "일괄 30초", "cost": 150, "eff": 60, "human": 40, "type": "B"}, {"label": "회복 보장", "cost": 450, "eff": 50, "human": 85, "type": "C"}]},
    {"id": "t4", "title": "Module 4. 디지털 유도", "desc": "강제 종료 vs 포용 설계", "metric": "inclusion", "options": [{"label": "강제 종료", "cost": 100, "eff": 90, "human": 10, "type": "A"}, {"label": "화면 공유", "cost": 600, "eff": 20, "human": 95, "type": "B"}, {"label": "포용 설계", "cost": 300, "eff": 50, "human": 70, "type": "C"}]},
    {"id": "t5", "title": "Module 5. 통제권", "desc": "상담원 책임 vs 상담원 승인", "metric": "agency", "options": [{"label": "방치", "cost": 100, "eff": 95, "human": 5, "type": "A"}, {"label": "보수적 답변", "cost": 300, "eff": 40, "human": 60, "type": "B"}, {"label": "통제권 부여", "cost": 500, "eff": 30, "human": 90, "type": "C"}]},
    {"id": "t6", "title": "Module 6. 감정 필터링", "desc": "욕설 차단 vs 상담사 신호 개입", "metric": "sustain", "options": [{"label": "규정 중심", "cost": 100, "eff": 80, "human": 20, "type": "A"}, {"label": "신호 개입", "cost": 550, "eff": 40, "human": 95, "type": "B"}, {"label": "사후 리포트", "cost": 50, "eff": 70, "human": 10, "type": "C"}]}
]

# ── 세션 초기화
for k, v in [("page", "scenario"), ("user_name", ""), ("survey_data", {}), ("sim_data", {}), ("p2_answers", {}), ("phase2_step", 1)]:
    if k not in st.session_state: st.session_state[k] = v

if st.session_state.page == "scenario":
    st.title("AICC Architect Simulation")
    if st.button("실험 시작하기"): st.session_state.page = "survey"; st.rerun()

elif st.session_state.page == "survey":
    st.subheader("사전 설문")
    name = st.text_input("이름")
    q1 = st.radio("성별", ["남성", "여성"], index=None)
    q2 = st.radio("경력", ["3년 이상 ~ 5년 미만", "5년 이상 ~ 7년 미만", "7년 이상 ~ 10년 미만"], index=None)
    if st.button("시뮬레이션 진입"):
        if name and q1 and q2:
            st.session_state.user_name = name
            st.session_state.survey_data = {"Q1_성별": q1, "Q3_경력": q2}
            st.session_state.page = "sim"; st.rerun()

elif st.session_state.page == "sim":
    with open("sim.html", "r", encoding="utf-8") as f:
        html = f.read()
    config = {"userName": st.session_state.user_name}
    inject = f"<script>window.SIM_CONFIG = {json.dumps(config)}; window.SIM_TASKS = {json.dumps(TASKS)};</script>"
    components.html(html.replace("</head>", inject + "</head>"), height=850)
    
    # sim.html이 postMessage로 보낸 데이터를 받아 세션에 저장
    params = st.query_params
    if "sim_result" in params:
        st.session_state.sim_data = json.loads(params["sim_result"])
        st.session_state.page = "phase2"
        st.query_params.clear()
        st.rerun()

elif st.session_state.page == "phase2":
    step = st.session_state.phase2_step
    keys = ["P2_Q1_데이터설계", "P2_Q2_숙련설계", "P2_Q3_표준화설계"]
    st.title(f"Phase 2 - 과제 {step}/3")
    ans = st.text_area("설계안을 작성하세요 (1000자 이상)", height=300, key=f"p2_{step}")
    
    if st.button("다음" if step < 3 else "최종 제출 및 저장"):
        st.session_state.p2_answers[keys[step-1]] = ans
        if step < 3:
            st.session_state.phase2_step += 1; st.rerun()
        else:
            # [최종 제출] 모든 데이터를 합쳐서 딱 한 번 전송
            final_payload = {
                "userName": st.session_state.user_name,
                "survey": st.session_state.survey_data,
                "phase1": st.session_state.sim_data, # 시뮬레이션 결과
                "P2_Q1_데이터설계": st.session_state.p2_answers.get("P2_Q1_데이터설계"),
                "P2_Q2_숙련설계": st.session_state.p2_answers.get("P2_Q2_숙련설계"),
                "P2_Q3_표준화설계": st.session_state.p2_answers.get("P2_Q3_표준화설계")
            }
            with st.spinner("데이터를 안전하게 저장 중입니다..."):
                success = send_to_gas(final_payload)
                if success:
                    st.session_state.page = "done"; st.rerun()
                else:
                    st.error("저장 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")

elif st.session_state.page == "done":
    st.balloons()
    st.success("모든 실험 데이터가 성공적으로 저장되었습니다. 감사합니다.")
