import streamlit as st
import sqlite3
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="Journal Search", layout="wide")
st.title("📚 Journal 정보 검색기")
#st.write("입력하면 추천 + 홈페이지 링크가 자동으로 표시됩니다.")

# DB 연결 & 데이터 캐싱
@st.cache_data
def load_data():
    conn = sqlite3.connect("final_2024_journal_level.db")
    df = pd.read_sql('SELECT * FROM "new data"', conn)
    conn.close()
    # 컬럼 이름 보기 쉽게 변경
    column_rename_map = {
        "5YEAR\nIF": "5 YEAR\nIF",
        "Category Description":"Category"
        # 필요한 컬럼명만 추가로 변경
    }
    df.rename(columns=column_rename_map, inplace=True)
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

    # 홈페이지 링크 제대로 처리하기
    homepage_url = str(df_result.iloc[0].get("HOMEPAGE", "")).strip()

    if homepage_url.startswith("http"):
        st.markdown(f"👉 [저널 홈페이지 바로가기]({homepage_url})", unsafe_allow_html=True)
    else:
        st.warning("홈페이지 정보가 없거나 잘못되었습니다.")

    # 👉 dataframe 출력 시 HOMEPAGE 컬럼 제거
    if "HOMEPAGE" in df_result.columns:
        df_display = df_result.drop(columns=["HOMEPAGE"])
    else:
        df_display = df_result.copy()  # 혹시 없으면 그대로 출력

    st.dataframe(df_display, use_container_width=True)

else:
    st.info(f"전체 {len(df_all)}개의 저널 리스트입니다.")
    if "HOMEPAGE" in df_all.columns:
        st.dataframe(df_all.drop(columns=["HOMEPAGE"]), use_container_width=True)
    else:
        st.dataframe(df_all, use_container_width=True)




