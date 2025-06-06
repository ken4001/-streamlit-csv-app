import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV上傳",layout="centered")
st.title("上傳CSV檔")
st.markdown("選擇一個CSV檔，幫你顯示內容")

uploaded_file=st.file_uploader("選擇檔案",type=["csv"])

if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    if df.empty:
       st.error("檔案內沒內容，重新上傳")
    else:
       st.success("讀取成功")
       st.write(df)
else:
    st.info("上傳CSV檔")

st.write("檔案內容")
st.write(df.head())
st.write("欄位名稱",df.columns.tolist())

column_select=st.selectbox("選擇欄位分析",df.columns)
st.write(f"選擇欄位:{column_select}")
st.write(f"欄位數據摘要",df[column_select].describe())



if df[column_select].dtype in ["int64", "float64"]:
    min_val, max_val = st.slider(f"🔍 設定 {column_select} 範圍", 
                                 float(df[column_select].min()), 
                                 float(df[column_select].max()), 
                                 (float(df[column_select].min()), float(df[column_select].max())))
    df_filtered = df[(df[column_select] >= min_val) & (df[column_select] <= max_val)]
    st.write(f"✅ 篩選後的 {column_select} 數據：")
    st.dataframe(df_filtered)

