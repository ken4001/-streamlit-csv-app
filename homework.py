import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

st.set_page_config(page_title="📊 資料視覺化分析儀表板", layout="wide")
st.title("📊 資料視覺化分析儀表板")

# 上傳 CSV
uploaded_file = st.file_uploader("📂 請上傳 CSV 檔案", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ 檔案 `{uploaded_file.name}` 已成功讀取！")
    st.write("🔍 資料預覽：", df.shape)
    st.dataframe(df)

    # 欄位分類
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    st.sidebar.header("🎯 資料篩選條件")
    filter_col = st.sidebar.selectbox("選擇篩選欄位", numeric_cols + cat_cols)

    # 數值篩選或分類篩選
    if filter_col in numeric_cols:
        min_val, max_val = float(df[filter_col].min()), float(df[filter_col].max())
        selected_range = st.sidebar.slider("篩選數值範圍", min_val, max_val, (min_val, max_val))
        df = df[(df[filter_col] >= selected_range[0]) & (df[filter_col] <= selected_range[1])]
    else:
        selected_vals = st.sidebar.multiselect("篩選分類值", df[filter_col].unique())
        if selected_vals:
            df = df[df[filter_col].isin(selected_vals)]

    st.subheader("📊 視覺化圖表")

    chart_type = st.selectbox("選擇圖表類型", ["長條圖", "圓餅圖", "散點圖"])

    if chart_type == "長條圖":
        col = st.selectbox("分類欄位", cat_cols)
        if col:
            count_data = df[col].value_counts()
            fig = px.bar(x=count_data.index, y=count_data.values,
                         labels={"x": col, "y": "數量"},
                         title=f"{col} 的長條圖")
            st.plotly_chart(fig)

    elif chart_type == "圓餅圖":
        col = st.selectbox("分類欄位", cat_cols)
        if col:
            count_data = df[col].value_counts()
            fig = px.pie(names=count_data.index, values=count_data.values,
                         title=f"{col} 的圓餅圖")
            st.plotly_chart(fig)

    elif chart_type == "散點圖":
        x = st.selectbox("X 軸", numeric_cols)
        y = st.selectbox("Y 軸", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        if x and y:
            fig = px.scatter(df, x=x, y=y, title=f"{x} vs {y} 散點圖")
            st.plotly_chart(fig)

    st.subheader("📦 分群與主成分分析")

    if len(numeric_cols) >= 2:
        num_cluster = st.slider("選擇分群數量", 2, 6, 3)
        df_clean = df[numeric_cols].dropna().copy()
        kmeans = KMeans(n_clusters=num_cluster, random_state=42)
        df_clean["Cluster"] = kmeans.fit_predict(df_clean)

        st.markdown("### 🔹 KMeans 分群圖（前三欄）")
        fig = px.scatter_matrix(df_clean, dimensions=numeric_cols[:3], color="Cluster")
        st.plotly_chart(fig)

        st.markdown("### 🔹 主成分分析（PCA）")
        pca = PCA(n_components=2)
        components = pca.fit_transform(df_clean[numeric_cols])
        df_pca = pd.DataFrame(components, columns=["PC1", "PC2"])
        df_pca["Cluster"] = df_clean["Cluster"]

        # 將原始欄位（如編號）加入 tooltip
        tooltip_data = df.loc[df_clean.index].copy()
        for col in tooltip_data.columns:
            df_pca[col] = tooltip_data[col].values

        fig2 = px.scatter(
            df_pca,
            x="PC1",
            y="PC2",
            color="Cluster",
            title="PCA 主成分視覺化",
            hover_data=["編號", "類別", "銷售額", "利潤", "數量"]
        )
        st.plotly_chart(fig2)
else:
    st.info("請先上傳一個 CSV 檔案以開始分析")