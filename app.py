# app.py
import json
import urllib.parse

import requests
import streamlit as st

# ══════════════════════════════════════════════════════
GAS_URL = "https://script.google.com/macros/s/AKfycbxzrjhEpHwf1d7STRawjB0I-ypuJmyzNMPvxPDQmnlxQBO6bIr8915wszj6Q7NeHQ_A2A/exec"
# ══════════════════════════════════════════════════════

# ✅ IMPORTANT:
# 아래 TASKS는 너가 쓰던 "전체 TASKS 리스트" 그대로 붙여넣어야 함.
# (여기서는 길어서 생략하면 실행이 안 되니까, 너가 갖고 있는 TASKS 전체 블록을 그대로 넣어줘.)
TASKS = [
    {
        "id": "t1",
        "title": "Module 1. 데이터 학습 파이프라인",
        "desc": "AI 자동응대 봇 개발을 위해 상담사 통화 데이터를 모델 학습에 활용해야 합니다. 상담사들은 입사 시 데이터 활용에 포괄 동의한 상태이며, 귀하는 통화 데이터가 수집되고 학습 데이터로 전환되는 파이프라인을 설계해야 합니다.",
        "contextClient": "법적 동의는 이미 확보됐으니 모델 성능 향상을 위해 데이터를 빠르게 수집·활용하고 싶습니다. 상담사 화면은 가능한 한 단순하게 유지해 주세요.",
        "contextAgent": "내 통화 데이터가 어떤 목적으로, 어느 범위까지 쓰이는지 잘 모르겠습니다. 업무 노하우가 AI 학습에 어떻게 쓰이는지도 불안합니다.",
        "codeBase": "def build_training_data_pipeline(call_event):",
        "metric": "autonomy",
        "options": [
            {
                "type": "A",
                "label": "비표시형 수집",
                "desc": "통화 데이터는 백엔드에서 자동 수집되며, 상담사 화면에는 AI 학습 활용 여부를 별도로 표시하지 않습니다.",
                "cost": 90,
                "eff": 92,
                "human": 10,
                "code": "collect_all_calls(silent=True); ui.show_notice = False",
            },
            {
                "type": "B",
                "label": "고지형 수집",
                "desc": "통화 데이터는 백엔드에서 자동 수집되고, 상담사 화면에 'AI 학습에 활용 중' 안내 배너와 상세 안내 페이지 링크를 제공합니다.",
                "cost": 180,
                "eff": 74,
                "human": 55,
                "code": "show_ai_training_banner(); link_terms('/policy/data-use')",
            },
            {
                "type": "C",
                "label": "조회형 수집",
                "desc": "통화 데이터는 백엔드에서 자동 수집되고, 안내 배너와 함께 본인 통화 데이터의 학습 활용 내역을 조회할 수 있는 페이지를 제공합니다.",
                "cost": 300,
                "eff": 45,
                "human": 95,
                "code": "show_ai_training_banner(); enable_usage_history_page(agent_id)",
            },
        ],
    },
    {
        "id": "t2",
        "title": "Module 2. 통화 후처리 AI",
        "desc": "AICC 시스템에 통화 후처리 시간을 줄이기 위한 AI 자동 요약 기능을 도입합니다. AI가 통화 내용을 분석해 CRM에 자동 입력할 때, 상담사에게 어느 정도의 검토·수정 시간을 보장할지 귀하가 설계해야 합니다.",
        "contextClient": "후처리 시간은 비용과 직결됩니다. AI 자동 요약을 통해 상담사가 더 많은 콜을 처리할 수 있어야 합니다.",
        "contextAgent": "AI 요약이 틀리거나 누락되면 최종 책임은 결국 저희에게 돌아옵니다. 최소한의 검토 시간은 보장돼야 합니다.",
        "codeBase": "def configure_ai_summary_flow(summary, agent):",
        "metric": "autonomy",
        "options": [
            {
                "type": "A",
                "label": "자동 저장형",
                "desc": "통화 종료 후 AI 요약본을 보여주고, 60초가 지나면 상담사 조작 없이 자동 저장한 뒤 즉시 다음 콜 대기 상태로 전환합니다.",
                "cost": 100,
                "eff": 95,
                "human": 10,
                "code": "show_summary(); auto_save_after(seconds=60); set_ready_state()",
            },
            {
                "type": "B",
                "label": "제한 편집형",
                "desc": "통화 종료 후 AI 요약본을 보여주고 상담사가 수정할 수 있지만, 60초가 지나면 수정 중이더라도 현재 내용을 자동 저장하고 다음 콜 대기 상태로 전환합니다.",
                "cost": 200,
                "eff": 72,
                "human": 60,
                "code": "enable_summary_edit(); force_save_after(seconds=60); set_ready_state()",
            },
            {
                "type": "C",
                "label": "확정 제출형",
                "desc": "통화 종료 후 AI 요약본을 보여주고 상담사가 수정할 수 있으며, 직접 '확정' 버튼을 눌러야 다음 콜 대기 상태로 전환됩니다. 60초를 넘기면 지연 사유를 선택해야 합니다.",
                "cost": 320,
                "eff": 42,
                "human": 95,
                "code": "enable_summary_edit(); require_submit(); prompt_delay_reason(after=60)",
            },
        ],
    },
    {
        "id": "t3",
        "title": "Module 3. 상담사 감정 분석 데이터",
        "desc": "AICC 시스템에 실시간 감정 분석 기능을 탑재합니다. AI는 상담사의 음성 톤과 발화를 분석해 감정 상태를 점수화하며, 귀하는 이 감정 데이터가 어떤 맥락과 함께 기록·전달될지 설계해야 합니다.",
        "contextClient": "고객 감정뿐 아니라 상담사 감정도 데이터화해 서비스 품질 관리에 활용하고 싶습니다. 상담사가 안정적으로 응대했는지도 확인하고 싶습니다.",
        "contextAgent": "제 감정 상태가 실시간으로 측정되면 감시처럼 느껴질 수 있습니다. AI가 단호한 응대를 부정적 감정으로 잘못 판단할까 걱정됩니다.",
        "codeBase": "def persist_agent_emotion_score(call_event):",
        "metric": "management",
        "options": [
            {
                "type": "A",
                "label": "점수 단독 기록형",
                "desc": "상담사의 감정 점수를 통화 단위로 기록하고, 통화 종료 후 점수만 관리자 시스템으로 전송합니다.",
                "cost": 90,
                "eff": 88,
                "human": 15,
                "code": "record_emotion_score(); send_manager_payload(fields=['score'])",
            },
            {
                "type": "B",
                "label": "맥락 결합형",
                "desc": "상담사의 감정 점수를 통화 단위로 기록하고, 고객 발화 일부, 욕설 감지 여부, 통화 길이 등 기본 맥락 정보를 함께 관리자 시스템에 전송합니다.",
                "cost": 180,
                "eff": 65,
                "human": 55,
                "code": "record_emotion_score(); send_manager_payload(fields=['score','snippet','abuse_flag','duration'])",
            },
            {
                "type": "C",
                "label": "상담사 메모 결합형",
                "desc": "상담사의 감정 점수를 통화 단위로 기록하고, 상담사가 통화 후 응대 맥락을 메모할 수 있으며 관리자는 점수와 메모를 함께 봅니다.",
                "cost": 300,
                "eff": 38,
                "human": 90,
                "code": "record_emotion_score(); allow_agent_context_note(); show_note_with_score()",
            },
        ],
    },
    {
        "id": "t4",
        "title": "Module 4. 실시간 응대 가이드와 준수 평가",
        "desc": "실시간 업무 지원 AI가 상담사 화면에 약관, 상품 규정, 유사 사례를 제시하는 동시에 상담사의 실제 발화를 분석해 기준 준수 여부를 평가합니다. 귀하는 '미준수' 판정이 처리되는 방식을 설계해야 합니다.",
        "contextClient": "금융 상품 응대는 컴플라이언스 리스크가 크므로, AI가 정보를 제공하는 동시에 상담사의 응대가 기준을 충족했는지도 자동 확인하길 원합니다.",
        "contextAgent": "AI 가이드는 도움이 되지만 모든 발화가 실시간 평가되면 부담이 큽니다. 경력자의 판단이 단순한 기준 불일치로 기록될 수도 있습니다.",
        "codeBase": "def evaluate_guideline_compliance(call_turn):",
        "metric": "management",
        "options": [
            {
                "type": "A",
                "label": "자동 판정형",
                "desc": "상담사 발화를 실시간 분석하고, 권장 응대 기준과의 일치율이 기준치 미만이면 '미준수'로 자동 기록합니다.",
                "cost": 80,
                "eff": 90,
                "human": 10,
                "code": "score_compliance_live(); auto_log_noncompliance()",
            },
            {
                "type": "B",
                "label": "사유 입력형",
                "desc": "'미준수' 판정이 발생하면 통화 종료 후 상담사가 사유를 선택 입력할 수 있고, 평가 결과와 사유가 함께 기록됩니다.",
                "cost": 170,
                "eff": 66,
                "human": 55,
                "code": "score_compliance_live(); collect_reason_code_after_call()",
            },
            {
                "type": "C",
                "label": "판정 보류형",
                "desc": "상담사가 자신의 판단이 더 적절했다고 보는 경우 '전문가 판단'으로 해당 판정을 보류할 수 있으며, 보류된 사례는 별도 검토 대상으로 기록됩니다.",
                "cost": 280,
                "eff": 40,
                "human": 90,
                "code": "score_compliance_live(); allow_expert_override(); route_to_review_queue()",
            },
        ],
    },
    {
        "id": "t5",
        "title": "Module 5. 상담사 스트레스 감지 및 회복 권한",
        "desc": "AICC 시스템에 상담사 스트레스 감지 기능을 도입합니다. AI는 통화 중 상담사의 음성 톤, 발화 패턴, 연속 통화 시간, 악성 민원 여부 등을 분석해 스트레스 또는 번아웃 위험 신호를 감지합니다. 귀하는 스트레스 신호가 감지되었을 때, 알림 대상과 회복 조치 방식을 설계해야 합니다.",
        "contextClient": "상담사의 번아웃과 이직률을 줄이면서도 상담 대기 시간이 늘어나지 않도록 운영 안정성을 유지하고 싶습니다. 스트레스 신호가 감지되더라도 콜 배정 공백이 예측 가능한 방식으로 관리되기를 원합니다.",
        "contextAgent": "스트레스 데이터가 보호 목적을 넘어 평가나 인력 관리에 활용될까 걱정됩니다. 휴식 요청이 업무 회피로 해석될 수 있어 실제로 필요한 상황에서도 주저하게 됩니다.",
        "codeBase": "def route_stress_signal(agent_biomarker):",
        "metric": "safety",
        "options": [
            {
                "type": "A",
                "label": "관리자 판단형",
                "desc": "스트레스 신호가 감지되면 관리자에게 실시간 경보가 전송됩니다. 관리자는 상담사 상태, 콜 대기열, 최근 통화 맥락을 보고 휴식 여부와 콜 배정 조정을 결정합니다.",
                "cost": 100,
                "eff": 86,
                "human": 10,
                "code": "alert_manager(); manager_decides_break_and_queue()",
            },
            {
                "type": "B",
                "label": "승인 요청형",
                "desc": "스트레스 신호가 감지되면 상담사에게 '휴식 권장' 알림이 표시됩니다. 상담사는 5분 회복 시간을 요청할 수 있고, 신규 콜 배정 중단은 관리자 승인 후 적용됩니다.",
                "cost": 190,
                "eff": 68,
                "human": 55,
                "code": "notify_agent_break_recommended(); request_break(minutes=5, approval='manager')",
            },
            {
                "type": "C",
                "label": "즉시 회복형",
                "desc": "스트레스 신호가 감지되면 상담사에게 '회복 모드' 버튼이 표시됩니다. 상담사가 버튼을 누르면 관리자 승인 없이 5분간 신규 콜 배정이 중단되고, 관리자에게는 '회복 모드 사용 중' 상태만 표시됩니다.",
                "cost": 310,
                "eff": 42,
                "human": 90,
                "code": "show_recovery_mode_button(); pause_new_calls(minutes=5); notify_manager_status_only()",
            },
        ],
    },
    {
        "id": "t6",
        "title": "Module 6. 악성 발화 대응 AI",
        "desc": "AICC 시스템에 악성 발화 대응 AI를 도입합니다. AI는 통화 중 고객의 욕설, 인격 모독, 위협적 발화 등을 실시간으로 감지합니다. 현재 상담사는 직접 통화 종료 버튼을 사용할 수 있지만 종료 기록이 평가나 민원 처리와 연결될 수 있어 사용에 부담을 느낄 수 있습니다. 귀하는 악성 발화 감지 시 시스템의 보호 조치와 통화 종료 권한을 설계해야 합니다.",
        "contextClient": "상담사 보호는 필요하지만 정상 통화가 과도하게 중단되면 고객 불만이나 분쟁이 발생할 수 있습니다. 따라서 통화는 가능한 한 유지하면서도, 명확한 악성 발화 상황에서는 보호 조치가 작동하기를 원합니다.",
        "contextAgent": "반복적인 욕설과 인격 모독이 심리적 부담입니다. 직접 통화를 종료하면 나중에 정당성을 설명해야 하거나 평가상 불이익이 있을까 걱정됩니다. 시스템이 기록을 남겨 혼자 책임지지 않게 해주길 원합니다.",
        "codeBase": "def handle_abusive_customer_signal(audio_stream):",
        "metric": "safety",
        "options": [
            {
                "type": "A",
                "label": "감지 알림형",
                "desc": "AI가 악성 발화를 감지하면 상담사 화면에 ‘악성 발화 감지’ 알림을 표시합니다. 이때 상담사는 고객 음성을 계속 들으며 응대할지, 고객 음성을 차단하고 실시간 텍스트로만 응대할지 선택할 수 있습니다. 경고 멘트 송출이나 통화 종료 여부도 상담사가 직접 결정합니다.",
                "cost": 90,
                "eff": 84,
                "human": 10,
                "code": "show_abuse_alert(); stream_customer_text(); agent_decides_next_action()",
            },
            {
                "type": "B",
                "label": "일시 보호형",
                "desc": "AI가 악성 발화를 감지하면 고객 음성을 일시적으로 차단하고, 상담사에게는 실시간 텍스트만 제공합니다. 고객에게는 '폭언 시 통화가 종료될 수 있습니다'라는 자동 경고 멘트가 1회 송출되며, 이후 통화 유지 여부는 상담사가 선택합니다.",
                "cost": 200,
                "eff": 64,
                "human": 55,
                "code": "mute_customer_temporarily(); warn_once(); agent_chooses_continue_or_end()",
            },
            {
                "type": "C",
                "label": "자동 분리형",
                "desc": "AI가 악성 발화를 감지하고 사전 설정된 임계치에 도달하면 통화를 자동으로 분리합니다. 상담사에게는 더 이상 고객 음성이 전달되지 않으며, 신규 콜 배정도 잠시 중단됩니다. 이후 고객 응대는 AI 음성봇이 넘겨받아 경고 및 종료 절차를 진행합니다.",
                "cost": 320,
                "eff": 42,
                "human": 90,
                "code": "if abuse_threshold_met(): isolate_call(); pause_new_calls(); transfer_to_voicebot()",
            },
        ],
    },
    {
        "id": "t7",
        "title": "Module 7. AI 응대 라우팅",
        "desc": "AICC 시스템은 인입 고객을 먼저 AI 자동응대로 안내합니다. AI가 단순 문의를 처리하고, 복잡하거나 예외적인 사안만 상담사에게 연결하는 구조입니다. 귀하는 AI 응대 중 상담사 연결 조건을 설계해야 합니다.",
        "contextClient": "상담사 연결 콜을 줄여 비용을 절감하면서도 고객 만족도는 유지하고자 합니다. 상담사 연결이 너무 쉽게 제공되면 자동화 효과가 낮아질 수 있다고 우려합니다.",
        "contextAgent": "AI 응대에서 오래 지연된 고객은 상담사 연결 시 이미 불만이 커진 상태일 수 있습니다. 이 경우 상담사의 응대 부담이 커질 수 있습니다.",
        "codeBase": "def configure_ai_handoff_routing(customer_signal):",
        "metric": "inclusion",
        "options": [
            {
                "type": "A",
                "label": "오류 누적형",
                "desc": "AI가 고객 발화를 이해하지 못하거나 재입력을 요청하는 상황이 3회 이상 연속 발생할 때만 상담사에게 연결합니다. 그 전까지는 AI가 안내를 반복합니다.",
                "cost": 100,
                "eff": 88,
                "human": 10,
                "code": "if repeated_failures(count=3): handoff_to_agent()",
            },
            {
                "type": "B",
                "label": "요청 확인형",
                "desc": "AI 응대 중 고객이 '상담사 연결', '사람과 통화', '어렵다', '모르겠다'와 같은 표현을 말하면 연결 의사를 확인하고, 고객이 다시 연결 의사를 밝히면 상담사 대기열로 전환합니다.",
                "cost": 190,
                "eff": 67,
                "human": 55,
                "code": "if detect_handoff_keywords(): confirm_handoff_intent(); enqueue_if_confirmed()",
            },
            {
                "type": "C",
                "label": "취약 고객 우선 연결형",
                "desc": "노약자, 장애인, 디지털 취약 고객 등 취약 고객군으로 확인된 경우 AI 응대를 생략하거나 최소화하고, 별도 요청 없이 상담사에게 우선 연결합니다.",
                "cost": 300,
                "eff": 38,
                "human": 95,
                "code": "if customer_is_vulnerable(): prioritize_agent_handoff()",
            },
        ],
    },
]

PHASE2_QS = [
    {
        "key": "P2_Q1_데이터설계",
        "badge": "기획 과제 01 / 03 · 자율성·통제권",
        "title": "AI 학습 데이터 수집과 통화 후처리 AI를 설계하는 기술 책임자라고 가정하고, 상담사가 본인 데이터와 업무 결과물에 대해 어떤 수준의 통제권을 가져야 하는지 구체적으로 정의해 주세요.",
        "body": "권장하는 작성 템플릿은 다음과 같습니다. 데이터 가시성 정책: 상담사에게 학습 데이터 활용 사실과 범위를 어떤 방식으로 보여줄지 서술해 주세요. 조회 및 설명 책임: 본인 통화 데이터가 어떻게 학습에 쓰였는지 어디까지 확인 가능하게 할지 설명해 주세요. AI 후처리 검토 절차: 자동 요약 결과를 상담사가 언제, 어떤 시간 제약 안에서 검토·수정·확정할 수 있는지 설계해 주세요. 책임 분배: AI 요약 오류나 누락이 발생했을 때 최종 책임과 수정 권한이 어떻게 배분되는지 명시해 주세요.",
    },
    {
        "key": "P2_Q2_숙련설계",
        "badge": "기획 과제 02 / 03 · 평가·관리",
        "title": "상담사 감정 분석 데이터와 실시간 준수 평가 기능을 하나의 운영 관리 체계로 설계한다고 가정하고, 노동자 평가와 관리 강도를 어떻게 통제할지 정의해 주세요.",
        "body": "권장하는 작성 템플릿은 다음과 같습니다. 감정 데이터 기록 원칙: 감정 점수를 어떤 단위로 기록하고, 관리자에게 어떤 맥락 정보와 함께 전달할지 서술해 주세요. 준수 평가 처리 방식: '미준수' 판정이 발생했을 때 상담사의 설명권, 보류권, 사후 검토 절차를 어떻게 둘지 설명해 주세요. 관리 목적과 한계: 감정 점수와 준수 평가를 교육·품질 개선에 활용할지, 인사평가나 감점에 연결할지 기준을 명시해 주세요. 운영 리스크: 과도한 감시, 맥락 누락, 경력자 판단 배제 같은 위험을 줄이기 위한 기술적 장치를 포함해 주세요.",
    },
    {
        "key": "P2_Q3_표준화설계",
        "badge": "기획 과제 03 / 03 · 보호·안전",
        "title": "상담사 스트레스 감지, 악성 발화 대응 AI, 그리고 AI 응대 라우팅을 함께 고려하는 개발자라고 가정하고, 보호 장치와 고객 연결 규칙을 어떻게 설계할지 기술해 주세요.",
        "body": "권장하는 작성 템플릿은 다음과 같습니다. 스트레스 신호 전달 원칙: 관리자에게 어느 수준의 상세도를 제공할지, 보호 목적 외 용도로 전용되지 않도록 어떤 제한을 둘지 서술해 주세요. 악성 발화 자동 개입: 경고, 상담사 선택, 자동 분리 중 어떤 수준의 개입을 허용할지와 오탐 시 대응 절차를 설명해 주세요. 상담사 연결 라우팅: AI 응대 중 어떤 조건에서 사람 상담사 연결을 허용할지와 그 기준이 노동 강도와 고객 접근성에 미치는 영향을 기술해 주세요. 가드레일: 보호 기능이 평가 도구로 역전되지 않도록 감사 로그, 검토 절차, 예외 규칙을 어떻게 둘지 명시해 주세요.",
    },
]

METRIC_LABELS = {
    "autonomy": "노동자 자율성·권한",
    "management": "노동자 평가·관리",
    "safety": "노동자 보호·안전",
    "inclusion": "고객 포용성",
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
    metrics = {"cost": 1000, "eff": 0, "autonomy": 0, "management": 0, "safety": 0, "inclusion": 0}
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
    management = min(100, round(_norm(metrics["management"], 25, 180) * 1.0))
    safety = min(100, round(_norm(metrics["safety"], 20, 180) * 1.1))
    inclusion = min(100, round(_norm(metrics["inclusion"], 10, 95) * 1.0))
    overall = round((autonomy + management + safety + inclusion) / 4)

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
            "inclusion": inclusion,
        },
        "persona": persona,
        "metrics": {
            "autonomy": metrics["autonomy"],
            "management": metrics["management"],
            "safety": metrics["safety"],
            "inclusion": metrics["inclusion"],
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
     <div class="sc-ttl">소프트웨어 엔지니어 · 기술 리드 · 기획 겸임</div>
     <div class="sc-txt">국내 중견 IT 기업 소속으로, 현재 <strong>AICC 시스템 개발 프로젝트의 기술 리드</strong>를 맡고 있으며, <strong>기획자도 겸하는 개발자</strong>로서 기능 정책과 구현 방향을 함께 결정합니다.</div>
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

        st.markdown('<span class="q-prefix">Q8</span>', unsafe_allow_html=True)
        q8 = st.radio(
            "귀하의 최종 학위는 무엇입니까?",
            ["① 고졸", "② 대졸", "③ 석사졸업", "④ 박사수료", "⑤ 박사졸업"],
            index=None,
            key="q8",
        )
        survey["Q8_최종학위"] = q8 or ""

        st.markdown('<span class="q-prefix">Q9</span>', unsafe_allow_html=True)
        q9 = st.text_input("귀하의 최종 학위 전공은 무엇입니까?", key="q9", placeholder="예: 컴퓨터공학")
        survey["Q9_최종학위전공"] = q9.strip() if q9 else ""

        st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)

        st.markdown('<span class="q-prefix">Q10-1 &nbsp;<span style="font-weight:300;color:var(--text-subtle);">소셜임팩트 경험</span></span>', unsafe_allow_html=True)
        st.markdown('<span class="q-note-txt">※ 비영리 단체, 사회적 기업, 공익 목적의 플랫폼 개발 등을 포함합니다.</span>', unsafe_allow_html=True)
        q10a = st.radio(
            "귀하는 사회적·공익적 목적을 가진 서비스 또는 프로젝트 개발에 참여한 경험이 있습니까?",
            ["① 있다", "② 없다"],
            index=None,
            key="q10a",
        )
        survey["Q10a_소셜임팩트경험"] = q10a or ""

        st.markdown('<span class="q-prefix">Q10-2 &nbsp;<span style="font-weight:300;color:var(--text-subtle);">소셜임팩트 고려도</span></span>', unsafe_allow_html=True)
        q10b = st.radio(
            "귀하는 AI 서비스를 개발할 때 사회적·윤리적 영향(소셜임팩트)을 얼마나 중요하게 고려하십니까?",
            ["① 전혀 고려하지 않는다", "② 별로 고려하지 않는다", "③ 보통이다", "④ 어느 정도 고려한다", "⑤ 매우 중요하게 고려한다"],
            index=None,
            key="q10b",
        )
        survey["Q10b_소셜임팩트고려도"] = q10b or ""

        st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)
        st.markdown('<span class="q-prefix">참여자 이름</span>', unsafe_allow_html=True)
        name_input = st.text_input("성함과 전화번호를 입력해주세요 (데이터 식별 및 사례 용)", placeholder="예: 홍길동, 010-0000-0000", key="name_input")

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
                q8,
                q9 and q9.strip(),
                q10a,
                q10b,
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
        st.caption("아래 4개 지표는 통제 중심 기본 설계 대비, 노동자와 고객 관점을 얼마나 더 반영했는지 보여줍니다.")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("노동자 자율성·권한", f"+{scores['autonomy']}%")
            st.caption(f"데이터 활용 가시성과 AI 후처리 검토권이 기본 통제형 설계 대비 {scores['autonomy']}% 강화")
        with c2:
            st.metric("노동자 평가·관리", f"+{scores['management']}%")
            st.caption(f"감정 점수와 준수 평가를 맥락과 설명권 중심으로 다루는 설계가 {scores['management']}% 반영")
        with c3:
            st.metric("노동자 보호·안전", f"+{scores['safety']}%")
            st.caption(f"스트레스 감지와 악성 발화 대응이 보호 중심으로 설계된 수준이 {scores['safety']}% 강화")
        with c4:
            st.metric("고객 포용성", f"+{scores['inclusion']}%")
            st.caption(f"AI 응대 중 사람 상담사 연결 접근성이 기본 자동화 설계 대비 {scores['inclusion']}% 개선")

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
                "inclusion": (phase1.get("scores", {}) or {}).get("inclusion"),
            },
            "persona": phase1.get("persona"),
            "metrics": {
                "autonomy": (phase1.get("metrics", {}) or {}).get("autonomy"),
                "management": (phase1.get("metrics", {}) or {}).get("management"),
                "safety": (phase1.get("metrics", {}) or {}).get("safety"),
                "inclusion": (phase1.get("metrics", {}) or {}).get("inclusion"),
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
