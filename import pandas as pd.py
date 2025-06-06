import pandas as pd

# 建立擴充的測試數據
data = {
    "姓名": [f"User{i}" for i in range(1, 21)],  # 生成 20 個不同的姓名
    "年齡": [i + 20 for i in range(20)],  # 讓年齡從 20 到 39
    "城市": ["台北", "新北", "高雄", "台中"] * 5  # 重複填充城市
}

# 轉換成 DataFrame
df = pd.DataFrame(data)

# 儲存為 CSV 檔案
df.to_csv("test_data_20.csv", index=False, encoding="utf-8-sig")

print("✅ 20 筆資料的 CSV 檔案已成功建立！")