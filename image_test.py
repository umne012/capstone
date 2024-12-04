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

# 사용자 입력: 평균 금리는 슬라이더로 변경
avg_interest = st.sidebar.slider("평균 금리 (%)", min_value=0, max_value=20, value=12, step=1)

# 나이, 대출 금액, 연체 여부
loan_amount = st.sidebar.number_input("대출 금액 (₩)", min_value=0, max_value=100000000, value=5000000, step=100000)
age = st.sidebar.number_input("나이", min_value=18, max_value=100, value=30)
delinquency = st.sidebar.checkbox("연체 여부", value=False)

# 성별: 라디오 버튼
gender = st.sidebar.radio("성별", ["남성", "여성"])

# 대출 종류 멀티셀렉트
loan_types = [
    "부동산 관련 담보대출", "기타할부 및 리스", "신용대출", 
    "신차 할부", "중고차 할부", "카드대출", "부동산 외 담보대출"
]
selected_loans = st.sidebar.multiselect("대출 종류", loan_types)

# 선택된 대출 종류에 대한 건수 입력
loan_counts = {}
for loan in selected_loans:
    loan_counts[loan] = st.sidebar.number_input(f"{loan} 건수", min_value=0, max_value=10, value=0, step=1)

# 종류별 대출 총 건수 계산
total_loans_by_type = sum(loan_counts.values())

# 업권 코드 멀티셀렉트
upkwon_types = ["1금융권", "2금융권", "3금융권"]
selected_upkwon = st.sidebar.multiselect("업권 코드", upkwon_types)

# 선택된 업권 코드에 대한 건수 입력
upkwon_counts = {}
for upkwon in selected_upkwon:
    upkwon_counts[upkwon] = st.sidebar.number_input(f"{upkwon} 대출 건수", min_value=0, max_value=10, value=0, step=1)

# 업권별 대출 총 건수 계산
total_loans_by_upkwon = sum(upkwon_counts.values())

# 대출 총 건수 자동 계산 (종류별 대출 총 건수 기준)
st.sidebar.write(f"**종류별 대출 총 건수:** {total_loans_by_type}")
st.sidebar.write(f"**업권별 대출 총 건수:** {total_loans_by_upkwon}")

# 총 건수 오류 메시지
if total_loans_by_type != total_loans_by_upkwon:
    st.sidebar.error("종류별 대출 총 건수와 업권별 대출 총 건수가 일치하지 않습니다")

# 단계 계산
if delinquency:
    current_stage = "0단계: 연체 중"
elif total_loans_by_type == 0:
    current_stage = "1단계: 초기 대출자"
elif avg_interest > 10:
    current_stage = "2단계: 초기 대출 그룹"
elif avg_interest <= 10 and total_loans_by_type > 1:
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
stage_colors = ["#FF6347", "#FFD700", "#90EE90", "#87CEEB", "#9370DB"]
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
    funnelmode="stack",
)

# Streamlit에서 그래프 표시
st.plotly_chart(fig, use_container_width=True)
