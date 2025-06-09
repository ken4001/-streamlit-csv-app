import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io

# 設定網頁標題與寬度
st.set_page_config(page_title="資料視覺化工具", layout="wide")
st.title("📊 CSV 資料視覺化工具")

# 上傳 CSV
uploaded_file = st.file_uploader("請上傳 CSV 檔案", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("檔案上傳成功！")

    # 顯示資料表
    if st.checkbox("顯示資料表"):
        st.dataframe(df)

    # 自動分析
    st.subheader("📌 資料內容")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    analysis_lines = [
        f"這份資料共有 {df.shape[0]} 筆資料與 {df.shape[1]} 個欄位。",
        f"數值欄位包含：{', '.join(numeric_cols) if numeric_cols else '無'}。",
        f"類別欄位包含：{', '.join(categorical_cols) if categorical_cols else '無'}。"
    ]

    for line in analysis_lines:
        st.write(line)

    # 圖表設定
    st.subheader("📈 圖表設定")
    chart_type = st.selectbox("選擇圖表類型", ["散點圖", "長條圖", "直方圖", "箱形圖", "圓餅圖", "熱力圖"])

    # 欄位選擇
    st.subheader("欄位選擇")
    selected_numeric_cols = st.multiselect("選擇數值欄位 (可多選)", numeric_cols, default=numeric_cols[:2])
    selected_cat_cols = st.multiselect("選擇類別欄位 (可多選)", categorical_cols)

    fig = None

    if chart_type == "散點圖":
        if len(selected_numeric_cols) < 2:
            st.warning("散點圖需要至少兩個數值欄位")
        else:
            x_axis = st.selectbox("X 軸", selected_numeric_cols)
            y_axis = st.selectbox("Y 軸", [col for col in selected_numeric_cols if col != x_axis])
            color = st.selectbox("顏色分組（可選）", [None] + selected_cat_cols)
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color, title="散點圖")
            st.plotly_chart(fig)

    elif chart_type == "長條圖":
        if not selected_cat_cols:
            st.warning("長條圖需要選擇至少一個類別欄位")
        else:
            cat_col = st.selectbox("類別欄位", selected_cat_cols)
            count_data = df[cat_col].value_counts()
            fig = px.bar(x=count_data.index, y=count_data.values,
                         labels={"x": cat_col, "y": "數量"}, title="長條圖")
            st.plotly_chart(fig)

    elif chart_type == "直方圖":
        if not selected_numeric_cols:
            st.warning("直方圖需要選擇數值欄位")
        else:
            num_col = st.selectbox("數值欄位", selected_numeric_cols)
            bins = st.slider("分箱數量", 5, 50, 20)
            fig = px.histogram(df, x=num_col, nbins=bins, title="直方圖")
            st.plotly_chart(fig)

    elif chart_type == "箱形圖":
        if not selected_numeric_cols:
            st.warning("箱形圖需要選擇數值欄位")
        else:
            y_col = st.selectbox("數值欄位 (Y軸)", selected_numeric_cols)
            x_col = st.selectbox("分組欄位 (X軸，可選)", [None] + selected_cat_cols)
            fig = px.box(df, y=y_col, x=x_col if x_col else None, title="箱形圖")
            st.plotly_chart(fig)

    elif chart_type == "圓餅圖":
        if not selected_cat_cols:
            st.warning("圓餅圖需要選擇類別欄位")
        else:
            cat_col = st.selectbox("類別欄位", selected_cat_cols)
            counts = df[cat_col].value_counts()
            fig = px.pie(names=counts.index, values=counts.values, title="圓餅圖", hole=0.3)
            st.plotly_chart(fig)

    elif chart_type == "熱力圖":
        if len(selected_numeric_cols) < 2:
            st.warning("熱力圖需要至少兩個數值欄位")
        else:
            corr = df[selected_numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

else:
    st.info("請先上傳 CSV 檔案。")
