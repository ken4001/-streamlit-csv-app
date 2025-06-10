import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os

# **設定 Streamlit 頁面**
st.set_page_config(page_title="資料視覺化工具", layout="wide")
st.title("📊 CSV 資料視覺化工具")

# **適應不同系統的桌面路徑**
if os.name == 'nt':  # Windows 系統
    desktop_path = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
else:  # Linux / Mac（例如 Streamlit Cloud）
    desktop_path = os.path.join(os.environ.get('HOME', ''), 'Desktop')

# **上傳 CSV 檔案**
uploaded_file = st.file_uploader("📂 請上傳 CSV 檔案", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ 檔案上傳成功！")

    # **編輯 CSV 資料**
    st.subheader("📝 編輯資料表")
    edited_df = st.data_editor(df, num_rows="dynamic")

    # **下載 CSV**
    if st.checkbox("✅ 匯出成新的 CSV 檔案"):
        output_name = st.text_input("請輸入輸出檔案名稱（不含副檔名）", value="edited_output")
        if output_name:
            csv_output_path = os.path.join(desktop_path, f"{output_name}.csv")
            try:
                edited_df.to_csv(csv_output_path, index=False, encoding='utf-8-sig')
                st.success(f"✅ CSV 已匯出至桌面：{output_name}.csv")
            except PermissionError:
                st.error("❌ 檔案寫入失敗，請確認該檔案未被其他應用程式開啟。")

    # **顯示資料內容**
    st.subheader("📌 資料概覽")
    numeric_cols = edited_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = edited_df.select_dtypes(include=['object', 'category']).columns.tolist()

    st.write(f"資料共有 {edited_df.shape[0]} 筆，{edited_df.shape[1]} 個欄位。")
    st.write(f"數值欄位：{', '.join(numeric_cols) if numeric_cols else '無'}")
    st.write(f"類別欄位：{', '.join(categorical_cols) if categorical_cols else '無'}")

    # **選擇圖表類型**
    st.subheader("📈 圖表視覺化")
    chart_type = st.selectbox("選擇圖表類型", ["散點圖", "長條圖", "直方圖", "箱形圖", "圓餅圖", "熱力圖"])

    selected_numeric_cols = st.multiselect("選擇數值欄位", numeric_cols, default=numeric_cols[:2])
    selected_cat_cols = st.multiselect("選擇類別欄位", categorical_cols)

    fig = None

    # **散點圖**
    if chart_type == "散點圖" and len(selected_numeric_cols) >= 2:
        x_axis = st.selectbox("X 軸", selected_numeric_cols)
        y_axis = st.selectbox("Y 軸", [col for col in selected_numeric_cols if col != x_axis])
        color = st.selectbox("顏色分組（可選）", [None] + selected_cat_cols)
        fig = px.scatter(edited_df, x=x_axis, y=y_axis, color=color, title="散點圖")
        st.plotly_chart(fig)

    # **長條圖**
    elif chart_type == "長條圖" and selected_cat_cols:
        cat_col = st.selectbox("類別欄位", selected_cat_cols)
        count_data = edited_df[cat_col].value_counts()
        fig = px.bar(x=count_data.index, y=count_data.values, labels={"x": cat_col, "y": "數量"}, title="長條圖")
        st.plotly_chart(fig)

    # **直方圖**
    elif chart_type == "直方圖" and selected_numeric_cols:
        num_col = st.selectbox("數值欄位", selected_numeric_cols)
        bins = st.slider("分箱數量", 5, 50, 20)
        fig = px.histogram(edited_df, x=num_col, nbins=bins, title="直方圖")
        st.plotly_chart(fig)

    # **箱形圖**
    elif chart_type == "箱形圖" and selected_numeric_cols:
        y_col = st.selectbox("數值欄位 (Y 軸)", selected_numeric_cols)
        x_col = st.selectbox("分組欄位 (X 軸，可選)", [None] + selected_cat_cols)
        fig = px.box(edited_df, y=y_col, x=x_col if x_col else None, title="箱形圖")
        st.plotly_chart(fig)

    # **圓餅圖**
    elif chart_type == "圓餅圖" and selected_cat_cols:
        cat_col = st.selectbox("類別欄位", selected_cat_cols)
        counts = edited_df[cat_col].value_counts()
        fig = px.pie(names=counts.index, values=counts.values, title="圓餅圖", hole=0.3)
        st.plotly_chart(fig)

    # **熱力圖**
    elif chart_type == "熱力圖" and len(selected_numeric_cols) >= 2:
        corr = edited_df[selected_numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

else:
    st.info("📂 請先上傳 CSV 檔案。")