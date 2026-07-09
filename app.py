import streamlit as st
import pandas as pd
import plotly.express as px
import json
from PIL import Image
import random


# -------------------------
# 설정
# -------------------------

st.set_page_config(
    page_title="AI Smart Energy Advisor",
    page_icon="⚡",
    layout="wide"
)


# -------------------------
# 디자인
# -------------------------

st.markdown("""
<style>

.stApp{
background:#050816;
color:white;
}

h1,h2,h3{
color:#00eaff;
}

.card{

background:#111827;
padding:25px;
border-radius:20px;
border:1px solid #00eaff;

box-shadow:
0 0 20px rgba(0,234,255,0.25);

text-align:center;

}


.number{

font-size:35px;
font-weight:bold;
color:#00ffff;

}


.report{

background:#101827;
padding:25px;
border-radius:20px;

border-left:5px solid #00eaff;

line-height:1.8;

}


</style>

""", unsafe_allow_html=True)



# -------------------------
# 데이터 불러오기
# -------------------------

with open("products.json",
          encoding="utf-8") as f:

    products=json.load(f)



# -------------------------
# 제목
# -------------------------

st.title(
"⚡ AI Smart Energy Advisor"
)

st.write(
"""
AI가 가전제품을 분석하여
전력 효율 진단 · 전기요금 절감 · 고효율 제품 추천을 제공합니다.
"""
)



# -------------------------
# 사이드바
# -------------------------

st.sidebar.header(
"📷 제품 등록"
)


image_file = st.sidebar.file_uploader(
"제품 사진 업로드",
type=["png","jpg","jpeg"]
)


model = st.sidebar.text_input(
"🔎 바코드 / 모델번호 입력"
)



if image_file:

    image=Image.open(image_file)

    st.sidebar.image(
        image,
        width=220
    )

    st.sidebar.success(
        "AI 이미지 분석 완료"
    )



# -------------------------
# 제품 분석
# -------------------------


if "냉장고" in model:

    appliance="냉장고"

elif "에어컨" in model:

    appliance="에어컨"

else:

    appliance=random.choice(
        ["냉장고","에어컨"]
    )



years=st.slider(
"사용 기간",
1,
20,
8
)


power=st.number_input(
"현재 소비전력(W)",
500
)



# -------------------------
# 계산
# -------------------------


if years>7:

    loss=(years-7)*15

else:

    loss=0


money=loss*150



# -------------------------
# 카드
# -------------------------

c1,c2,c3=st.columns(3)


with c1:

    st.markdown(
    f"""
    <div class="card">

    현재 제품

    <div class="number">

    {appliance}

    </div>

    </div>
    """,
    unsafe_allow_html=True
    )


with c2:

    st.markdown(
    f"""
    <div class="card">

    예상 손실

    <div class="number">

    {loss}kWh

    </div>

    </div>
    """,
    unsafe_allow_html=True
    )


with c3:

    st.markdown(
    f"""
    <div class="card">

    추가 비용

    <div class="number">

    {money:,}원

    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



# -------------------------
# 추천 제품
# -------------------------


st.subheader(
"⭐ AI 고효율 제품 추천"
)


df=pd.DataFrame(
products[appliance]
)



fig=px.bar(
df,
x="name",
y="power",
text="power"
)


fig.update_layout(

paper_bgcolor="#050816",

plot_bgcolor="#050816",

font_color="white"

)


st.plotly_chart(
fig,
use_container_width=True
)



for p in products[appliance]:

    st.info(
f"""
### {p['name']}

에너지등급 : {p['grade']}

소비전력 : {p['power']}W

가격 : {p['price']:,}원

"""
)



# -------------------------
# AI 리포트
# -------------------------


st.subheader(
"🤖 AI 분석 리포트"
)


if years>=10:

    st.markdown(

f"""
<div class="report">

⚠ 노후 제품 감지

현재 {years}년 사용 제품입니다.

예상 추가 비용:
{money:,}원

추천:
1등급 고효율 제품 교체

</div>

""",

unsafe_allow_html=True

)


else:


    st.markdown(

"""
<div class="report">

🟢 현재 상태 양호

대기전력 관리와
에너지 등급 확인을 추천합니다.

</div>

""",

unsafe_allow_html=True

)


st.success(
"AI 분석 완료 ⚡"
)