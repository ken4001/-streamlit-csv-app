import pandas as pd
import random
import os

# **指定存放路徑**
output_folder = "C:/Users/ken80/Desktop/streamlit_project"
output_file = os.path.join(output_folder, "商品銷售數據.csv")

# **定義欄位（中文名稱）**
columns = ["發票日期", "商品名稱", "銷售區域", "零售商", "銷售方式", "州別", "單位價格", "總銷售額", "銷售數量"]

# **建立 100 筆隨機資料**
data = []
for i in range(100):
    row = [
        f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",  # 隨機日期
        random.choice(["耐吉運動鞋", "愛迪達外套", "彪馬短褲", "UA 運動上衣"]),  # 隨機商品名稱
        random.choice(["亞洲", "歐洲", "北美洲", "南美洲"]),  # 隨機銷售區域
        random.choice(["Amazon", "沃爾瑪", "耐吉專賣店", "愛迪達門市"]),  # 隨機零售商
        random.choice(["線上購買", "實體店購買"]),  # 隨機銷售方式
        random.choice(["加州", "德州", "紐約州", "佛州", "伊利諾州"]),  # 隨機州別
        round(random.uniform(10, 300), 2),  # 隨機單位價格
        round(random.uniform(1000, 50000), 2),  # 隨機總銷售額
        random.randint(1, 500)  # 隨機銷售數量
    ]
    data.append(row)

# **建立 DataFrame**
df = pd.DataFrame(data, columns=columns)

# **儲存成 CSV（使用 `utf-8-sig` 來避免亂碼）**
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"✅ CSV 檔案已成功生成！請查看 `{output_file}`")