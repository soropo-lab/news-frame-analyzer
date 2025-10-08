# -*- coding: utf-8 -*-
"""
뉴스 분석기 (모바일 UI + 자동 크롤러)
 - 국내 주요 언론 본문 수집 및 편향 분석
 - 결과를 HTML 표로 시각화
"""

import streamlit as st
import webbrowser
from streamlit.components.v1 import html as st_html

from analyzer.crawler_auto import get_article_text
from analyzer.gpt_analyzer import analyze_bias
from analyzer.formatter import result_to_html_table

# ------------------------------
# 페이지 설정
# ------------------------------
st.set_page_config(
    page_title="뉴스 분석기",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------------------------
# 모바일 UI 스타일
# ------------------------------
st.markdown("""
    <style>
    body {
        background-color: #f8fafc;
        font-family: 'Pretendard', sans-serif;
    }
    .block-container {
        padding: 1.2rem 1.2rem 3rem 1.2rem;
        max-width: 600px;
        margin: auto;
    }
    h1 {
        text-align: center;
        font-size: 1.8rem;
        margin-top: 0.5rem;
    }
    .caption {
        text-align: center;
        color: #6b7280;
        margin-bottom: 1rem;
    }
    button[kind="primary"] {
        border-radius: 8px !important;
        padding: 0.7rem 1.2rem !important;
        font-size: 1.05rem !important;
    }
    .stTextInput>div>div>input {
        font-size: 1.05rem;
        padding: 0.8rem;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# 헤더
# ------------------------------
st.markdown("<h1>뉴스 분석기</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption'>국내 주요 언론 기사를 자동으로 분석합니다.</p>", unsafe_allow_html=True)

# ------------------------------
# 상단 버튼
# ------------------------------
col1, col2 = st.columns(2)
with col1:
    if st.button("Google 뉴스 열기"):
        webbrowser.open("https://news.google.com/")
with col2:
    st.info("URL 입력 후 [분석 시작] 버튼을 누르세요.", icon="💡")

# ------------------------------
# URL 입력
# ------------------------------
url = st.text_input(
    "뉴스 기사 URL",
    placeholder="예: https://news.jtbc.co.kr/article/NB12265505",
    label_visibility="collapsed"
)

# ------------------------------
# 분석 버튼
# ------------------------------
analyze_btn = st.button("분석 시작")

# ------------------------------
# 분석 프로세스
# ------------------------------
if analyze_btn and url:
    with st.spinner("기사 수집 중..."):
        article = get_article_text(url)

    if not article or article.startswith("__ERROR__") or len(article) < 200:
        st.error("기사 본문을 충분히 가져오지 못했습니다. 다른 URL로 시도해 주세요.")
        st.text(article[:300])
    else:
        with st.spinner("분석 중..."):
            result = analyze_bias(article)
        st.success("분석이 완료되었습니다.")
        st.subheader("분석 결과")
        st_html(result_to_html_table(result), height=520, scrolling=True)

# ------------------------------
# 하단 안내
# ------------------------------
st.markdown("""
---
<p style="text-align:center; color:#94a3b8; font-size:0.85rem;">
© 2025 Park Tae-woong | Powered by OpenRouter.ai
</p>
""", unsafe_allow_html=True)
