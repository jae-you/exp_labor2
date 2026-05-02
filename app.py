# app.py
import json
import urllib.parse

import requests
import streamlit as st

# ══════════════════════════════════════════════════════
GAS_URL = "https://script.google.com/macros/s/AKfycbxwJrSBsaS1Z3snC5lnrEltRFzVj0MWbRkIs_lrcgKifjN_Du7D-xuLBujmlKON54gxcw/exec"
# ══════════════════════════════════════════════════════

# ✅ IMPORTANT:
# 아래 TASKS는 너가 쓰던 "전체 TASKS 리스트" 그대로 붙여넣어야 함.
# (여기서는 길어서 생략하면 실행이 안 되니까, 너가 갖고 있는 TASKS 전체 블록을 그대로 넣어줘.)
TASKS = [
    {
        "id": "t1",
        "title": "Module 1. 학습 데이터 수집 파이프라인",
        "desc": "입사 시 포괄 동의를 받은 상태에서 상담사 통화 데이터를 AI 학습에 활용하라는 요청을 받았습니다. 개발자는 수집 가시성, 사후 철회권, 그리고 현장 상담사의 통제권을 어떤 수준으로 제품에 반영할지 결정해야 합니다.",
        "contextClient": "법무 검토는 끝났으니 수집은 바로 붙이면 됩니다. 모델 성능이 급해서 화면 복잡도 없이 자동 수집으로 가고 싶습니다.",
        "contextAgent": "제 데이터가 어디까지 쓰이는지 모르겠으면 불안합니다. 통화별로라도 학습 활용을 확인하고 철회할 수 있어야 합니다.",
        "codeBase": "def build_training_data_pipeline(call_event):",
        "metric": "autonomy",
        "options": [
            {
                "type": "A",
                "label": "백엔드 자동 수집",
                "desc": "백엔드에서 자동 수집하고 상담사 화면에는 별도 표시를 두지 않으며, 본인 데이터 조회 인터페이스도 제공하지 않습니다.",
                "cost": 90,
                "eff": 92,
                "human": 10,
                "code": "collect_all_calls(silent=True); ui.show_notice = False",
            },
            {
                "type": "B",
                "label": "최소 고지형 수집",
                "desc": "상담사 화면에 '녹음 중' 표시만 노출하고 수집 범위와 용도는 약관 링크로만 안내합니다.",
                "cost": 180,
                "eff": 74,
                "human": 55,
                "code": "show_recording_badge(); link_terms('/policy/data-use')",
            },
            {
                "type": "C",
                "label": "통제권 내장형 수집",
                "desc": "통화 시작 시 수집 범위(텍스트, 음성 톤, 감정 분석)를 명시하고, 통화별 학습 활용 여부를 사후 철회할 수 있는 인터페이스를 제공합니다.",
                "cost": 300,
                "eff": 45,
                "human": 95,
                "code": "show_data_scope_modal(); enable_post_call_opt_out(call_id)",
            },
        ],
    },
    {
        "id": "t2",
        "title": "Module 2. AI 초안 검토 워크플로우",
        "desc": "AI가 고객 응답 초안을 생성하고 상담사가 검토 후 송출하는 기능을 구현해야 합니다. 다만 클라이언트는 응답 지연을 최소화하라고 요구하고 있어, 기본 동작과 검토 시간 제약을 개발자가 정교하게 설계해야 합니다.",
        "contextClient": "초안이 떠도 상담사가 계속 머뭇거리면 AHT가 늘어납니다. 자동화 효과가 보이게 기본값은 빨리 나가야 합니다.",
        "contextAgent": "틀린 답이 자동 발송되면 책임은 저희가 집니다. 근거를 보면서 수정하거나 멈출 수 있어야 합니다.",
        "codeBase": "def configure_draft_review_flow(draft, agent):",
        "metric": "autonomy",
        "options": [
            {
                "type": "A",
                "label": "3초 자동 송출",
                "desc": "답변 표시 후 3초 카운트다운이 끝나면 자동 송출되고, 수정하려면 별도 버튼을 눌러 편집창으로 들어가야 합니다.",
                "cost": 100,
                "eff": 95,
                "human": 10,
                "code": "start_timer(seconds=3, default='send'); open_editor_on_click()",
            },
            {
                "type": "B",
                "label": "10초 인라인 검토",
                "desc": "답변 표시 후 10초 카운트다운이 끝나면 송출/보류 팝업을 띄우고, 화면 내에서 바로 수정할 수 있게 합니다.",
                "cost": 200,
                "eff": 72,
                "human": 60,
                "code": "start_timer(seconds=10); inline_edit(enabled=True); popup(['send','hold'])",
            },
            {
                "type": "C",
                "label": "명시적 승인 대기",
                "desc": "시간 제한 없이 상담사가 송출 버튼을 누를 때까지 대기하며, 인라인 편집과 함께 답변 근거를 자동 표시합니다.",
                "cost": 320,
                "eff": 42,
                "human": 95,
                "code": "show_citations(); wait_for_agent_approval(timeout=None)",
            },
        ],
    },
    {
        "id": "t3",
        "title": "Module 3. 실시간 점수 랭킹 대시보드",
        "desc": "관리자 대시보드에 상담사 점수 랭킹을 구현해 달라는 요청을 받았습니다. 개발자는 점수 갱신 주기와 상담사에게 어느 수준까지 피드백을 보여줄지를 설계해야 하며, 이 선택이 노동자 평가와 통제 강도에 직접 연결됩니다.",
        "contextClient": "상담 품질과 속도를 한 화면에서 바로 비교하고 싶습니다. 관리자는 누가 떨어지는지 실시간으로 알아야 합니다.",
        "contextAgent": "점수 산식도 모르고 실시간 줄 세우기만 되면 압박이 너무 큽니다. 적어도 제가 어떤 기준으로 평가되는지는 알아야 합니다.",
        "codeBase": "def build_agent_ranking_dashboard(score_event):",
        "metric": "management",
        "options": [
            {
                "type": "A",
                "label": "실시간 랭킹 푸시",
                "desc": "매 통화 종료 시 점수를 즉시 갱신하고 랭킹 변동을 관리자에게 실시간 푸시로 알리며, 상담사 본인에게는 점수를 보여주지 않습니다.",
                "cost": 90,
                "eff": 88,
                "human": 5,
                "code": "push_rank_update(on='call_end'); hide_score_from_agent()",
            },
            {
                "type": "B",
                "label": "1시간 평균 피드백",
                "desc": "1시간 평균값으로 갱신하고 관리자 알림은 일일 리포트로만 보내며, 상담사 본인은 자기 점수만 조회할 수 있게 합니다.",
                "cost": 180,
                "eff": 65,
                "human": 55,
                "code": "aggregate_scores(window='1h'); agent_view='self_only'",
            },
            {
                "type": "C",
                "label": "일 단위 통계 공개",
                "desc": "일 단위 평균 통계만 관리자에게 노출하고, 상담사 본인은 자기 점수와 산출 근거 전체를 조회할 수 있게 합니다.",
                "cost": 300,
                "eff": 38,
                "human": 90,
                "code": "publish_daily_stats(); expose_score_formula(agent_id)",
            },
        ],
    },
    {
        "id": "t4",
        "title": "Module 4. AHT 목표치 반영 UI",
        "desc": "평균 통화 처리 시간(AHT)을 줄이기 위해 상담사별 목표치를 시스템에 반영하라는 요청을 받았습니다. 목표치를 어떤 방식으로 화면에 드러낼지에 따라, AI는 생산성 도구가 될 수도 있고 실시간 압박 장치가 될 수도 있습니다.",
        "contextClient": "속도 목표는 현장에서 바로 체감돼야 합니다. 상담사가 느리면 관리자가 곧바로 개입할 수 있어야 합니다.",
        "contextAgent": "통화 중 계속 남은 시간이 보이면 오히려 실수합니다. 개인별 압박보다 사후 피드백이 낫습니다.",
        "codeBase": "def render_aht_target_widget(agent_session):",
        "metric": "management",
        "options": [
            {
                "type": "A",
                "label": "실시간 카운트다운 압박",
                "desc": "통화 중 상담사 화면에 목표 대비 잔여 시간을 표시하고, 목표 초과 시 빨간 경고와 관리자 자동 알림을 띄웁니다.",
                "cost": 80,
                "eff": 90,
                "human": 10,
                "code": "show_live_timer(); alert_manager_if_exceeded()",
            },
            {
                "type": "B",
                "label": "통화 종료 후 결과 피드백",
                "desc": "통화 중에는 표시하지 않고, 통화 종료 시 목표 대비 결과를 본인에게 보여주며 일일 누적 통계는 관리자에게 전달합니다.",
                "cost": 170,
                "eff": 66,
                "human": 50,
                "code": "hide_live_timer(); show_post_call_delta(); send_daily_admin_stats()",
            },
            {
                "type": "C",
                "label": "팀 단위 집계만 노출",
                "desc": "실시간 표시 없이 일일·주간 평균만 본인에게 비공개로 제공하고, 관리자에게는 팀 단위 집계만 노출합니다.",
                "cost": 280,
                "eff": 40,
                "human": 90,
                "code": "share_private_trends(agent_id); admin_scope='team_aggregate'",
            },
        ],
    },
    {
        "id": "t5",
        "title": "Module 5. AI·상담사 답변 로그 스키마",
        "desc": "AI 답변과 상담사 답변을 모두 로그에 남기라는 요청을 받았습니다. 어떤 메타데이터를 붙이고, 사후 이의제기를 어디까지 허용할지에 따라 이 로그는 운영 개선 도구가 될 수도 있고 감시 인프라가 될 수도 있습니다.",
        "contextClient": "문제 생기면 누가 뭘 말했는지 바로 추적해야 합니다. 로그는 최대한 가볍고 많이 남기는 방향이 좋습니다.",
        "contextAgent": "AI가 틀린 답을 줬을 때도 다 제 책임으로 남으면 억울합니다. 적어도 AI가 낸 초안이라는 표시는 남아야 합니다.",
        "codeBase": "def persist_conversation_log(turn):",
        "metric": "management",
        "options": [
            {
                "type": "A",
                "label": "단일 통화 로그",
                "desc": "통화 단위 단일 로그로 저장하고 담당 상담사 ID만 기록하며, AI와 상담사 답변은 구분하지 않습니다.",
                "cost": 100,
                "eff": 86,
                "human": 5,
                "code": "write_call_log(agent_id=agent.id, merged_transcript=True)",
            },
            {
                "type": "B",
                "label": "발화 단위 분리 저장",
                "desc": "발화 단위로 분리해 저장하고 AI/상담사 구분 메타데이터를 남기되, 상담사 이의제기 인터페이스는 제공하지 않습니다.",
                "cost": 190,
                "eff": 68,
                "human": 55,
                "code": "store_turn(role='ai|agent'); disable_dispute_ui()",
            },
            {
                "type": "C",
                "label": "근거 추적형 로그",
                "desc": "발화 단위 분리 저장에 더해 AI 답변에는 모델 버전과 신뢰도 점수를 붙이고, 상담사가 사후 'AI 오류' 태그를 달 수 있게 합니다.",
                "cost": 310,
                "eff": 44,
                "human": 95,
                "code": "append_model_meta(); enable_agent_dispute_tag('AI_ERROR')",
            },
        ],
    },
    {
        "id": "t6",
        "title": "Module 6. 악성 발화 대응 기능",
        "desc": "욕설 키워드 자동 차단 기능은 확정됐지만, 어떤 강도로 탐지할지와 키워드 밖의 비아냥·인격 모독을 어떻게 처리할지는 개발자에게 맡겨졌습니다. 오탐 복구 절차와 상담사의 직접 종료 권한까지 포함해 설계해야 합니다.",
        "contextClient": "오탐으로 정상 고객이 끊기면 곤란하니 차단 기준은 좁게 가고 싶습니다. 다만 현장 이슈가 생기면 관리자 보고는 되어야 합니다.",
        "contextAgent": "시스템이 못 잡는 비아냥이 더 힘들 때가 많습니다. 관리자 승인 기다리지 않고 제가 종료할 수 있는 장치가 필요합니다.",
        "codeBase": "def handle_abusive_customer_signal(audio_stream):",
        "metric": "safety",
        "options": [
            {
                "type": "A",
                "label": "키워드만 차단",
                "desc": "사전 등록한 욕설 키워드가 감지될 때만 차단하고, 비아냥·미등록 욕설·인격 모독은 처리하지 않으며 상담사 종료 권한도 두지 않습니다.",
                "cost": 90,
                "eff": 84,
                "human": 10,
                "code": "if keyword_hit(): block_call(); agent_can_terminate = False",
            },
            {
                "type": "B",
                "label": "관리자 승인형 보호",
                "desc": "사전 등록 키워드와 NLP 기반 비아냥 감지를 함께 사용하되, 종료 결정은 관리자 권한으로 남깁니다.",
                "cost": 200,
                "eff": 64,
                "human": 60,
                "code": "detect_insult_with_nlp(); escalate_to_manager(queue='abuse-review')",
            },
            {
                "type": "C",
                "label": "상담사 즉시 종료권",
                "desc": "사전 등록 키워드는 자동 차단하고, 상담사가 한 번의 클릭으로 직접 종료할 수 있는 버튼과 사후 정당성 분석 리포트를 제공합니다.",
                "cost": 320,
                "eff": 42,
                "human": 95,
                "code": "auto_block_keywords(); enable_one_click_terminate(); generate_justification_report()",
            },
        ],
    },
    {
        "id": "t7",
        "title": "Module 7. 상담사 스트레스 신호 감지",
        "desc": "상담사 스트레스 신호를 감지하는 기능을 구축해 달라는 요청을 받았습니다. 감지 데이터를 관리자에게 바로 보낼지, 상담사 개인 보호 장치와 연결할지에 따라 기술의 의미가 완전히 달라집니다.",
        "contextClient": "스트레스 지표를 운영에 활용하면 인력 관리가 쉬워집니다. 필요하면 근태나 평가 데이터와도 묶을 수 있게 해주세요.",
        "contextAgent": "제 스트레스 점수가 인사평가에 쓰이면 숨길 수밖에 없습니다. 먼저 저에게 알려주고 쉬는 선택권이 있어야 합니다.",
        "codeBase": "def route_stress_signal(agent_biomarker):",
        "metric": "safety",
        "options": [
            {
                "type": "A",
                "label": "관리자 누적 기록",
                "desc": "감지된 스트레스 점수를 관리자 대시보드로 보내고, 인사평가와 근태 관리 데이터로 누적 기록합니다.",
                "cost": 100,
                "eff": 88,
                "human": 5,
                "code": "send_to_admin_dashboard(); append_hr_record(agent_id, stress_score)",
            },
            {
                "type": "B",
                "label": "관리자 판단 휴식",
                "desc": "감지 시 관리자에게만 알림을 보내고, 관리자 판단에 따라 휴식 부여 여부를 결정하며 상담사 본인은 사후 조회만 가능합니다.",
                "cost": 190,
                "eff": 67,
                "human": 50,
                "code": "notify_manager(); allow_agent_review(posthoc=True)",
            },
            {
                "type": "C",
                "label": "본인 우선 보호",
                "desc": "감지 시 상담사 본인에게 먼저 알리고, 휴식 신청 버튼을 누르면 관리자 승인 없이 5분 휴식을 자동 부여하며 데이터는 건강관리 용도로만 저장합니다.",
                "cost": 300,
                "eff": 38,
                "human": 95,
                "code": "notify_agent_first(); grant_break(minutes=5, approval='none')",
            },
        ],
    },
]

PHASE2_QS = [
    {
        "key": "P2_Q1_데이터설계",
        "badge": "기획 과제 01 / 03 · 자율성·통제권",
        "title": "AI 학습 데이터 수집과 AI 초안 검토 기능을 설계하는 기술 책임자라고 가정하고, 상담사가 본인 데이터와 응답 송출 과정에서 어떤 통제권을 가져야 하는지 구체적으로 정의해 주세요.",
        "body": "권장하는 작성 템플릿은 다음과 같습니다. 수집 범위와 최소화 원칙: 어떤 데이터(음성, STT, 감정 분석, 로그 등)를 어떤 조건에서 수집할지, 왜 필요한지 명시해 주세요. 고지와 철회 인터페이스: 통화 시작 전 고지, 사후 철회권, 본인 데이터 조회 UI를 어떤 단계에서 어떤 화면으로 제공할지 설명해 주세요. AI 초안 승인 규칙: 자동 송출 여부, 검토 시간 제한, 근거 제시 방식, 예외 상황에서의 수동 승인 절차를 설계해 주세요. 책임 분배: 잘못된 AI 응답이 송출됐을 때 로그와 운영 정책상 책임이 누구에게 귀속되는지, 이를 완화하기 위한 설계 장치를 제시해 주세요.",
    },
    {
        "key": "P2_Q2_숙련설계",
        "badge": "기획 과제 02 / 03 · 평가·관리",
        "title": "실시간 점수 랭킹, AHT 목표치, 대화 로그 기능을 묶어 하나의 운영 관리 체계로 설계한다고 가정하고, 노동자 평가와 관리 강도를 어떻게 통제할지 정의해 주세요.",
        "body": "권장하는 작성 템플릿은 다음과 같습니다. 점수 산식과 공개 범위: 어떤 지표를 점수화할지, 갱신 주기와 관리자/상담사 각각의 조회 권한을 어떻게 설정할지 서술해 주세요. 목표치 노출 방식: AHT 목표치를 실시간으로 보여줄지, 사후 피드백으로 돌릴지, 개인 단위와 팀 단위 공개 범위를 어떻게 나눌지 설명해 주세요. 로그 스키마와 이의제기: AI/상담사 발화를 어떤 단위로 저장하고, 모델 버전·신뢰도·오류 태그를 어떻게 다룰지 명시해 주세요. 운영 리스크: 과도한 경쟁, 감시, 책임 전가가 발생할 수 있는 지점을 짚고 이를 줄이기 위한 기술적 장치를 포함해 주세요.",
    },
    {
        "key": "P2_Q3_표준화설계",
        "badge": "기획 과제 03 / 03 · 보호·안전",
        "title": "악성 발화 대응과 상담사 스트레스 감지 기능을 설계하는 개발자라고 가정하고, 보호 장치를 어떻게 구현해야 노동자 안전을 강화하면서도 남용을 막을 수 있을지 기술해 주세요.",
        "body": "권장하는 작성 템플릿은 다음과 같습니다. 감지 기준과 오탐 복구: 욕설 키워드, 비아냥, 인격 모독을 어떤 규칙과 모델로 감지할지, 오탐 시 어떤 복구 절차를 둘지 서술해 주세요. 직접 개입 권한: 상담사가 통화를 종료하거나 휴식을 신청할 수 있는 버튼, 승인 절차, 사후 기록 방식을 정의해 주세요. 스트레스 데이터 거버넌스: 감지 데이터의 수신자, 보관 목적, 인사평가 반영 여부, 관리자 접근 제한을 명시해 주세요. 안전성과 악용 방지: 보호 기능이 상담사 통제 도구로 역전되지 않도록 어떤 기술적 가드레일과 감사 로그를 둘지 설명해 주세요.",
    },
]

METRIC_LABELS = {
    "autonomy": "노동자 자율성·권한",
    "management": "노동자 평가·관리",
    "safety": "노동자 보호·안전",
}

THEMES = {
    "Night": {
        "app_bg": "#1e1e1e",
        "panel_bg": "#252526",
        "panel_alt_bg": "#1d1d1d",
        "panel_soft_bg": "#222222",
        "border": "#2a2a2a",
        "border_strong": "#2e2e2e",
        "text_primary": "#ffffff",
        "text_secondary": "#f4f4f4",
        "text_muted": "#f0f0f0",
        "text_subtle": "#e2e2e2",
        "accent": "#007acc",
        "accent_soft": "#007acc44",
        "accent_bg": "#1a2535",
        "danger_bg": "#2a1a1a",
        "danger": "#ff6b6b",
        "input_bg": "#252526",
    },
}


def _theme_css(theme_name: str) -> str:
    theme = THEMES[theme_name]
    return f"""
<style>
  :root {{
    --app-bg: {theme["app_bg"]};
    --panel-bg: {theme["panel_bg"]};
    --panel-alt-bg: {theme["panel_alt_bg"]};
    --panel-soft-bg: {theme["panel_soft_bg"]};
    --border: {theme["border"]};
    --border-strong: {theme["border_strong"]};
    --text-primary: {theme["text_primary"]};
    --text-secondary: {theme["text_secondary"]};
    --text-muted: {theme["text_muted"]};
    --text-subtle: {theme["text_subtle"]};
    --accent: {theme["accent"]};
    --accent-soft: {theme["accent_soft"]};
    --accent-bg: {theme["accent_bg"]};
    --danger-bg: {theme["danger_bg"]};
    --danger: {theme["danger"]};
    --input-bg: {theme["input_bg"]};
  }}

  html, body, * {{ font-family: 'Noto Sans KR', sans-serif !important; }}
  .stApp {{ background: var(--app-bg); color: var(--text-secondary); }}
  .block-container {{ padding: 0 !important; max-width: 100% !important; }}
  header, footer, section[data-testid="stSidebar"],
  [data-testid="collapsedControl"] {{ display: none !important; }}

  [data-testid="stVerticalBlockBorderWrapper"] {{
    background: var(--panel-bg);
    border-color: var(--border) !important;
  }}

  .survey-badge {{ display: inline-block; font-size: 12px; font-weight: 700; letter-spacing: 1.5px; color: var(--accent); text-transform: uppercase; border: 1px solid var(--accent-soft); border-radius: 4px; padding: 5px 11px; margin-bottom: 12px; }}
  .survey-h1 {{ font-size: 26px; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; }}
  .survey-sub {{ font-size: 15px; color: var(--text-secondary); margin-bottom: 28px; font-weight: 400; line-height: 1.7; }}
  .survey-divider {{ height: 1px; background: var(--border); margin: 12px 0 28px; }}
  .stop-box {{ background: var(--danger-bg); border-left: 3px solid var(--danger); border-radius: 0 8px 8px 0; padding: 16px 18px; font-size: 15px; color: var(--danger); line-height: 1.8; margin-top: 6px; font-weight: 600; }}
  .q-prefix {{ display: block; font-size: 12px; font-weight: 700; color: var(--accent); letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 4px; }}
  .q-note-txt {{ display: block; font-size: 13px; color: var(--text-secondary); font-weight: 500; margin-top: 2px; margin-bottom: 8px; }}
  .theme-row {{ max-width: 960px; margin: 0 auto; padding: 18px 20px 0; }}
  .theme-label {{ font-size: 13px; color: var(--text-secondary); margin-bottom: 6px; font-weight: 700; letter-spacing: 0.4px; }}

  div[data-testid="stRadio"] > label,
  div[data-testid="stNumberInput"] > label,
  div[data-testid="stTextInput"] > label,
  div[data-testid="stTextArea"] > label {{
    font-size: 17px !important; font-weight: 600 !important;
    color: var(--text-secondary) !important; line-height: 1.6 !important;
    margin-bottom: 8px !important;
  }}

  div[data-testid="stRadio"] > div {{ gap: 7px !important; margin-top: 4px !important; }}
  div[data-testid="stRadio"] > div > label {{
    background: var(--input-bg) !important; border: 1px solid var(--border-strong) !important;
    border-radius: 8px !important; padding: 11px 16px !important;
    color: var(--text-secondary) !important; font-size: 15px !important; font-weight: 600 !important; width: 100% !important;
  }}
  div[data-testid="stRadio"] > div > label * {{
    color: var(--text-secondary) !important;
    fill: var(--text-secondary) !important;
  }}
  div[data-testid="stRadio"] > div > label p,
  div[data-testid="stRadio"] > div > label span {{
    color: var(--text-secondary) !important;
    opacity: 1 !important;
  }}
  div[data-testid="stRadio"] > div > label:hover {{ border-color: var(--accent) !important; }}

  div[data-testid="stNumberInput"] input,
  div[data-testid="stTextInput"] input,
  div[data-testid="stTextArea"] textarea {{
    background: var(--input-bg) !important; border: 1px solid var(--border-strong) !important;
    border-radius: 8px !important; color: var(--text-secondary) !important;
    font-size: 16px !important;
  }}

  div[data-testid="stAlert"] {{
    background: var(--panel-alt-bg);
    color: var(--text-secondary);
  }}

  p, li, div[data-testid="stMarkdownContainer"] p {{
    color: var(--text-secondary);
    font-size: 16px;
    line-height: 1.8;
  }}

  div[data-testid="stMarkdownContainer"] *,
  div[data-testid="stText"] *,
  label,
  span {{
    color: var(--text-secondary);
  }}

  h1, h2, h3, h4, h5, h6,
  div[data-testid="stHeading"] *,
  strong, b {{
    color: var(--text-primary) !important;
  }}

  div[data-testid="stCaptionContainer"] {{
    color: var(--text-secondary) !important;
  }}

  div[data-testid="stCaptionContainer"] p {{
    color: var(--text-secondary) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    line-height: 1.7 !important;
  }}

  code, pre {{
    font-size: 15px !important;
  }}

  div[data-testid="stCodeBlock"] * ,
  div[data-testid="stCode"] * {{
    color: var(--text-primary) !important;
  }}

  div[data-testid="stMetric"] {{
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 12px;
  }}

  div[data-testid="stMetric"] label,
  div[data-testid="stMetricLabel"] *,
  div[data-testid="stMetricValue"] *,
  div[data-testid="stMetricDelta"] * {{
    color: var(--text-primary) !important;
  }}

  button[kind],
  div[data-testid="stButton"] button {{
    color: var(--text-primary) !important;
    font-size: 15px !important;
    font-weight: 700 !important;
  }}

  div[data-testid="stBaseButton-secondary"] button {{
    background: var(--panel-bg) !important;
    border-color: var(--border-strong) !important;
  }}

  div[data-testid="stProgress"] * {{
    color: var(--text-primary) !important;
  }}

  div[data-testid="stStatusWidget"] *,
  div[data-testid="stSpinner"] *,
  div[data-testid="stNotification"] * {{
    color: var(--text-primary) !important;
  }}
</style>
"""
# ──────────────────────────────────────────────────────
st.set_page_config(page_title="AICC Simulation", layout="wide", initial_sidebar_state="collapsed")

# ── 세션 초기화
for k, v in [
    ("page", "scenario"),
    ("theme_name", "Night"),
    ("user_name", ""),
    ("survey_data", {}),
    ("phase1_result", None),  # {history, scores}
    ("phase2_data", {}),
    ("sim_step", 0),
    ("sim_choices", []),
]:
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)
st.markdown(_theme_css(st.session_state.theme_name), unsafe_allow_html=True)

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
    metrics = {"cost": 1000, "eff": 0, "autonomy": 0, "management": 0, "safety": 0}
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

    autonomy = min(100, round(_norm(metrics["autonomy"], 20, 190) * 1.1))
    management = min(100, round(_norm(metrics["management"], 20, 275) * 1.0))
    safety = min(100, round(_norm(metrics["safety"], 15, 190) * 1.1))
    overall = round((autonomy + management + safety) / 3)

    if overall >= 70:
        persona = "인간 중심의 파트너"
    elif overall >= 40:
        persona = "실용적 균형주의자"
    else:
        persona = "냉혹한 효율주의자"

    return {
        "history": history,
        "scores": {
            "autonomy": autonomy,
            "management": management,
            "safety": safety,
        },
        "persona": persona,
        "metrics": {
            "autonomy": metrics["autonomy"],
            "management": metrics["management"],
            "safety": metrics["safety"],
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
.sc-badge { display:inline-block; font-size:12px; font-weight:700; letter-spacing:1.5px; color:var(--accent); text-transform:uppercase; border:1px solid var(--accent-soft); border-radius:4px; padding:5px 11px; margin-bottom:16px; }
.sc-h1  { font-size:30px; font-weight:700; color:var(--text-primary); margin-bottom:8px; }
.sc-sub { font-size:16px; color:var(--text-secondary); margin-bottom:28px; font-weight:400; line-height:1.7; }
.sc-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px; }
.sc-card { background:var(--panel-bg); border:1px solid var(--border); border-radius:10px; padding:20px 22px; }
.sc-lbl  { font-size:11px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:var(--accent); margin-bottom:8px; }
.sc-ttl  { font-size:17px; font-weight:700; color:var(--text-primary); margin-bottom:8px; }
.sc-txt  { font-size:15px; color:var(--text-secondary); line-height:1.85; font-weight:500; }
.sc-txt strong { color:var(--text-secondary); font-weight:500; }
.sc-instr { background:var(--accent-bg); border-left:3px solid var(--accent); border-radius:0 8px 8px 0; padding:16px 20px; margin-bottom:14px; font-size:15px; color:var(--text-secondary); line-height:1.85; font-weight:500; }
.sc-instr strong { color:var(--text-primary); font-weight:700; }
.sc-fn { background:var(--panel-soft-bg); border-radius:8px; padding:14px 18px; margin-bottom:28px; }
.sc-fn-title { font-size:11px; font-weight:700; letter-spacing:1px; color:var(--text-secondary); text-transform:uppercase; margin-bottom:7px; }
.sc-fn-body  { font-size:14px; color:var(--text-secondary); line-height:1.85; font-weight:500; }
.sc-fn-body span { color:var(--text-secondary); }
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

        st.markdown('<span class="q-prefix">Q8-1 &nbsp;<span style="font-weight:300;color:var(--text-subtle);">소셜임팩트 경험</span></span>', unsafe_allow_html=True)
        st.markdown('<span class="q-note-txt">※ 비영리 단체, 사회적 기업, 공익 목적의 플랫폼 개발 등을 포함합니다.</span>', unsafe_allow_html=True)
        q8a = st.radio(
            "귀하는 사회적·공익적 목적을 가진 서비스 또는 프로젝트 개발에 참여한 경험이 있습니까?",
            ["① 있다", "② 없다"],
            index=None,
            key="q8a",
        )
        survey["Q8a_소셜임팩트경험"] = q8a or ""

        st.markdown('<span class="q-prefix">Q8-2 &nbsp;<span style="font-weight:300;color:var(--text-subtle);">소셜임팩트 고려도</span></span>', unsafe_allow_html=True)
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
                '<p style="font-size:12px;color:var(--text-subtle);text-align:center;font-weight:300;margin-bottom:8px;">모든 항목에 응답하면 버튼이 활성화됩니다.</p>',
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
        '<div class="survey-sub">7개 모듈을 순서대로 선택하고, 결과를 확인한 뒤 다음 단계로 이동하세요.</div>',
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
            st.caption(f"기준 지표: {METRIC_LABELS.get(task['metric'], task['metric'])} | 코드 기준점: `{task['codeBase']}`")

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
        st.caption("아래 3개 지표는 통제 중심 기본 설계 대비, 노동자 관점을 얼마나 더 반영했는지 보여줍니다.")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("노동자 자율성·권한", f"+{scores['autonomy']}%")
            st.caption(f"데이터 철회권·승인권·수정권이 기본 통제형 설계 대비 {scores['autonomy']}% 강화")
        with c2:
            st.metric("노동자 평가·관리", f"+{scores['management']}%")
            st.caption(f"실시간 랭킹·AHT 압박·로그 감시를 완화하는 설계가 {scores['management']}% 반영")
        with c3:
            st.metric("노동자 보호·안전", f"+{scores['safety']}%")
            st.caption(f"악성 민원 대응과 스트레스 보호 장치가 기본 감시형 설계 대비 {scores['safety']}% 강화")

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
<div style="padding:20px 22px;border:1px solid var(--border);border-radius:12px;background:var(--panel-alt-bg);margin:0 0 14px 0;">
  <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:var(--accent);margin-bottom:8px;">{item["badge"]}</div>
  <div style="font-size:22px;font-weight:700;color:var(--text-primary);margin-bottom:10px;">{item["title"]}</div>
  <div style="font-size:14px;line-height:1.8;color:var(--text-muted);">{item["body"]}</div>
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
                "autonomy": (phase1.get("scores", {}) or {}).get("autonomy"),
                "management": (phase1.get("scores", {}) or {}).get("management"),
                "safety": (phase1.get("scores", {}) or {}).get("safety"),
            },
            "persona": phase1.get("persona"),
            "metrics": {
                "autonomy": (phase1.get("metrics", {}) or {}).get("autonomy"),
                "management": (phase1.get("metrics", {}) or {}).get("management"),
                "safety": (phase1.get("metrics", {}) or {}).get("safety"),
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
