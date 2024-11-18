import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(
    page_title="편의점 영양성분 분석",
    layout="wide"
)

# 페이지 헤더
st.title("편의점 영양성분 분석 대시보드")

# CSV 파일 직접 로드
try:
    df = pd.read_csv("편의점 평균 영양.csv", encoding='cp949')
except:
    try:
        df = pd.read_csv("편의점 평균 영양.csv", encoding='utf-8')
    except:
        st.error("파일을 읽는데 실패했습니다.")
        st.stop()

# 탭 생성
tab1, tab2, tab3 = st.tabs(["데이터 미리보기", "그래프 분석", "지도 시각화"])

# 탭1: 데이터 미리보기
with tab1:
    st.subheader("데이터 미리보기")
    st.dataframe(df)
    
    # 기본 정보 표시
    st.subheader("데이터 기본 정보")
    col1, col2 = st.columns(2)
    with col1:
        st.write("총 데이터 수:", len(df))
    with col2:
        st.write("분석 항목:", ", ".join(df.columns.tolist()))

# 탭2: 그래프 분석
with tab2:
    # 영양성분 선택
    nutrient = st.selectbox(
        "분석할 항목 선택",
        ["탄수화물", "단백질", "지방", "당류", "칼로리", "평균 가격"]
    )
    
    # 첫 번째 차트: 분포도
    st.subheader(f"{nutrient} 분포")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    plt.hist(df[nutrient], bins=20)
    plt.title(f'{nutrient} 분포도')
    plt.xlabel(nutrient)
    plt.ylabel('빈도')
    st.pyplot(fig1)
    
    # 두 번째 차트: 상관관계 히트맵
    st.subheader("영양성분 간 상관관계")
    corr = df[["탄수화물", "단백질", "지방", "당류", "칼로리", "평균 가격"]].corr()
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    plt.imshow(corr, cmap='coolwarm', aspect='auto')
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("상관관계 히트맵")
    st.pyplot(fig2)
    
    # 세 번째 차트: 산점도
    st.subheader("영양성분 비교")
    col1, col2 = st.columns(2)
    with col1:
        x_nutrient = st.selectbox(
            "X축 선택", 
            ["탄수화물", "단백질", "지방", "당류", "칼로리", "평균 가격"],
            key='x'
        )
    with col2:
        y_nutrient = st.selectbox(
            "Y축 선택", 
            ["탄수화물", "단백질", "지방", "당류", "칼로리", "평균 가격"],
            key='y'
        )
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    plt.scatter(df[x_nutrient], df[y_nutrient])
    plt.xlabel(x_nutrient)
    plt.ylabel(y_nutrient)
    plt.title(f'{x_nutrient}와 {y_nutrient}의 관계')
    st.pyplot(fig3)

# 탭3: 지도 시각화
with tab3:
    st.subheader("사업장 위치 지도")
    
    try:
        # places.csv 파일 로드
        places_df = pd.read_csv("places.csv", encoding='cp949')
    except:
        try:
            places_df = pd.read_csv("places.csv", encoding='utf-8')
        except:
            st.error("파일을 읽는데 실패했습니다.")
            st.stop()
    # 지도 생성
    m = folium.Map(
        location=[places_df['Latitude'].iloc[0], places_df['Longitude'].iloc[0]],  # 첫 번째 위치 사용
        zoom_start=12
    )

    # 마커 클러스터 생성
    marker_cluster = MarkerCluster().add_to(m)

    # 각 위치에 마커 추가
    for idx, row in places_df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['사업장명'],
            tooltip=row['사업장명']
        ).add_to(marker_cluster)
    # 지도를 Streamlit에 표시
    st_folium(m, width=800, height=600)