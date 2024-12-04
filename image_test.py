import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 단계별 평균 금리 데이터
stage_data = {
    "단계": ["0단계: 연체 중", "1단계: 초기 대출자", "2단계: 초기 대출 그룹", "3단계: 안정적인 상환자", "4단계: 우수 고객"],
    "평균 금리 (%)": [15.0, 12.0, 10.0, 8.0, 5.0]
}
df_stages = pd.DataFrame(stage_data)

# 단계 순서를 역순으로 정렬
df_stages = df_stages.iloc[::-1].reset_index(drop=True)

# Streamlit 인터페이스
st.title("금융 여정 시뮬레이터")
st.write("현재 상태를 확인하고, 단계별 금리가 줄어드는 모습을 확인하세요!")

# 사용자 입력
st.sidebar.header("사용자 입력")
avg_interest = st.sidebar.number_input("평균 금리 (%)", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
loan_amount = st.sidebar.number_input("대출 금액 (₩)", min_value=0, max_value=100000000, value=5000000, step=100000)
age = st.sidebar.number_input("나이", min_value=18, max_value=100, value=30)
card_loans = st.sidebar.number_input("카드 대출 건수", min_value=0, max_value=10, value=1, step=1)
credit_loans = st.sidebar.number_input("신용 대출 건수", min_value=0, max_value=10, value=0, step=1)
gender = st.sidebar.selectbox("성별", ["남성", "여성"])
total_loans = st.sidebar.number_input("대출 총 건수", min_value=0, max_value=10, value=1, step=1)
delinquency = st.sidebar.checkbox("연체 여부", value=False)

# 단계 계산
if delinquency:
    current_stage = "0단계: 연체 중"
elif total_loans == 0:
    current_stage = "1단계: 초기 대출자"
elif avg_interest > 10:
    current_stage = "2단계: 초기 대출 그룹"
elif avg_interest <= 10 and total_loans > 1:
    current_stage = "3단계: 안정적인 상환자"
elif avg_interest <= 7:
    current_stage = "4단계: 우수 고객"
else:
    current_stage = "알 수 없음"

# 현재 단계 표시
st.subheader(f"현재 단계: {current_stage}")

# 같은 그룹 정보
if current_stage == "0단계: 연체 중":
    st.write("- 연체 상환 중.")
    st.write("- 금융 거래 이력을 복구하고 신용 점수를 회복.")
elif current_stage == "1단계: 초기 대출자":
    st.write("- 신용 체크카드 개설.")
    st.write("- 1금융권 대출 이력 없음.")
elif current_stage == "2단계: 초기 대출 그룹":
    st.write("- 평균 금리: 12%")
    st.write("- 상품: 카드 대출, 소액 신용 대출.")
elif current_stage == "3단계: 안정적인 상환자":
    st.write("- 평균 금리: 9%")
    st.write("- 상품: 신용 대출, 주택 담보 대출.")
elif current_stage == "4단계: 우수 고객":
    st.write("- 평균 금리: 5%")
    st.write("- 상품: 주택 담보 대출, 우수 고객 전용 상품.")

# 단계별 다음 행동 제안
st.write(f"**다음 단계로 이동하려면:**")
if current_stage == "0단계: 연체 중":
    st.write("- 연체를 상환하세요. 연체가 지속되면 신용 점수가 하락합니다.")
    st.write("- 상환 후 신용 체크카드를 발급받아 금융 거래 이력을 복구하세요.")
elif current_stage == "1단계: 초기 대출자":
    st.write("- 신용 체크카드를 발급받으세요.")
    st.write("- 1금융권에서 대출 2건 이상의 이력을 쌓으세요.")
elif current_stage == "2단계: 초기 대출 그룹":
    st.write("- 대출 상환 이력을 쌓아 신용 점수를 개선하세요.")
    st.write("- 추가 대출 시 1금융권의 신용 대출을 고려하세요.")
elif current_stage == "3단계: 안정적인 상환자":
    st.write("- 신용 대출 건수를 2건 이상으로 늘리세요.")
    st.write("- 금리 협상을 통해 평균 금리를 낮추세요.")
elif current_stage == "4단계: 우수 고객":
    st.write("축하합니다! 최상의 대출 조건을 이용할 수 있는 등급입니다.")

# 단계별 색상 (선택된 단계는 진한 색상)
stage_colors = ["#FF6347", "#FFD700", "#90EE90", "#87CEEB", "#9370DB"]  # 단계별 색상
colors = [
    stage_colors[i] if stage == current_stage else "rgba(211, 211, 211, 0.5)"
    for i, stage in enumerate(df_stages["단계"])
]

# Plotly Funnel Chart
fig = go.Figure()

fig.add_trace(go.Funnel(
    y=df_stages["단계"],
    x=df_stages["평균 금리 (%)"],
    text=[f"{val}%" for val in df_stages["평균 금리 (%)"]],  # % 추가
    textinfo="text",  # 자동 비율 대신 텍스트만 표시
    marker=dict(
        color=colors,  # 동적 색상 설정
        line=dict(color="black", width=2)  # 테두리 추가
    )
))

# 레이아웃 업데이트
fig.update_layout(
    title="단계별 평균 금리 (선택된 단계 강조)",
    funnelmode="stack",  # 스택 모드로 차트 정렬
)

# Streamlit에서 그래프 표시
st.plotly_chart(fig, use_container_width=True)
