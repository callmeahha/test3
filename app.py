import streamlit as st 
import pandas as pd  

st.title("통합데이터 서비스")
st.image('image.png')

data=pd.read_csv('id.csv')
data["PW"]=data["PW"].astype(str)
data

with st.form("login_form"):
    
    ID=st.text_input("ID", placeholder="아이디를 입력하세요.")

    PW=st.text_input("Password", placeholder="비밀번호를 입력하세요.", type="password")

    submit_button=st.form_submit_button("로그인")
   
if submit_button:
    if not ID or not PW:
        st.warning("ID와 비번 모두 입력해주세요.")
    else:
        user=data[(data["ID"]==ID)&(data["PW"]==PW)]
        
        if not user.empty:
            st.success(f"{ID}님 환영합니다! ")
            st.switch_page("pages/dashboard.py")  # 새로운 페이지로 전환
        else:
            st.warning('사용자 정보가 일치하지 않습니다.')