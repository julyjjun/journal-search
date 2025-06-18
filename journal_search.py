import streamlit as st
import sqlite3
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="Journal Search", layout="centered")
st.title("📚 Journal 정보 검색기")

# DB 연결 & 데이터 캐싱
@st.cache_data
def load_data():
    conn = sqlite3.connect("short_2024_journal_level.db")
    df = pd.read_sql('SELECT * FROM "short data"', conn)
    conn.close()
    return df

df_all = load_data()

# 저널 리스트
journals = df_all["Journal Title"].dropna().unique().tolist()
journals.sort()

# 자동완성 selectbox
selected_journal = st.selectbox(
    "🔍 저널 이름을 입력하세요",
    options=[""] + journals
)

# 결과 표시
if selected_journal:
    df_result = df_all[df_all["Journal Title"] == selected_journal]
    st.success(f"🔍 '{selected_journal}' 검색 결과 {len(df_result)}개")
    
    # 홈페이지 링크 처리
    homepage_url = str(df_result.iloc[0].get("HOMEPAGE", "")).strip()
    if homepage_url.startswith("http"):
        st.markdown(f"👉 [저널 홈페이지 바로가기]({homepage_url})", unsafe_allow_html=True)
    else:
        st.warning("홈페이지 정보가 없거나 잘못되었습니다.")
    
    # 결과 데이터프레임 출력
    st.dataframe(df_result, use_container_width=True)

else:
    st.info(f"전체 {len(df_all)}개의 저널 리스트입니다.")
    st.dataframe(df_all, use_container_width=True)

# ⏳ 자동 새로고침: 15분(900초)마다
st.markdown(
    """
    <meta http-equiv="refresh" content="900">
    """,
    unsafe_allow_html=True
)





