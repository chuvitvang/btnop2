import pandas as pd

# Tải dữ liệu
df = pd.read_csv("C:/Users/Admin/Downloads/dulieu.csv")

# Đảm bảo các cột số là kiểu float và tính toán Total Gold
df[['Silver', 'Bronze', 'Gold']] = df[['Silver', 'Bronze', 'Gold']].astype(float)
df['Total_Gold'] = df['Gold'] + df['Silver'] / 2 + df['Bronze'] / 3

# Sắp xếp và phân hạng các nước theo Total Gold
df_sorted = df.sort_values(by='Total_Gold', ascending=False).reset_index(drop=True)
df_sorted['Rank'] = df_sorted['Total_Gold'].rank(method='dense', ascending=False).astype(int).astype(str)

# Thêm "(tie)" cho đồng hạng
duplicates = df_sorted.duplicated(subset='Total_Gold', keep=False)
df_sorted.loc[duplicates, 'Rank'] += ' (tie)'

# Hàm để thêm hậu tố cho hạng
def add_suffix(rank):
    rank_int = int(rank.split()[0])  # Lấy số hạng
    suffix = 'th' if 10 <= rank_int % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(rank_int % 10, 'th')
    return f"{rank_int}{suffix}{' (tie)' if 'tie' in rank else ''}"

# Thêm hậu tố vào cột Rank
df_sorted['Rank'] = df_sorted['Rank'].apply(add_suffix)

# Lấy danh sách hạng duy nhất cho top 3
top_3_ranks = df_sorted['Rank'].unique()[:3]
top_3_list = [(rank, df_sorted[df_sorted['Rank'] == rank]['Country'].tolist()) for rank in top_3_ranks]

print("List Top 3:")
for i in top_3_list:
    print(i[0], ', '.join(i for i in i[1]))

# Lưu vào file CSV
df_sorted.to_csv("C:/Users/Admin/Downloads/final_data.csv", index=False)
