import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV上傳",layout="centered")
st.title("上傳CSV檔")
st.markdown("選擇一個CSV檔，幫你顯示內容")

uploaded_file=st.file_uploader("選擇檔案",type=["csv"])

if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.success("讀取成功")
    st.weite(df)
else:
    st.info("上傳CSV檔")