import pandas as pd
import matplotlib.pyplot as plt

# Load data hasil cleaning
df = pd.read_excel("data_sudah_clean.xlsx")
tahun_cols = ["2016", "2017", "2018", "2019"]

# 1. Line chart – Top 10 sektor tertinggi
top10_tinggi = df.nlargest(10, "rata_rata_3tahun")
plt.figure(figsize=(12, 6))
for i, row in top10_tinggi.iterrows():
    plt.plot(tahun_cols, row[tahun_cols], label=row["Laju Pertumbuhan Ekonomi"])
plt.title("Top 10 Sektor Tertinggi (2016–2019)", fontsize=14)
plt.xlabel("Tahun")
plt.ylabel("Pertumbuhan (%)")
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Line chart – Top 10 sektor terendah
top10_rendah = df.nsmallest(10, "rata_rata_3tahun")
plt.figure(figsize=(12, 6))
for i, row in top10_rendah.iterrows():
    plt.plot(tahun_cols, row[tahun_cols], label=row["Laju Pertumbuhan Ekonomi"])
plt.title("Top 10 Sektor Terendah (2016–2019)", fontsize=14)
plt.xlabel("Tahun")
plt.ylabel("Pertumbuhan (%)")
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Bar chart – Rata-rata per kategori
kategori_avg = df.groupby("kategori")["rata_rata_3tahun"].mean().sort_values(ascending=True)
plt.figure(figsize=(10, 6))
plt.barh(kategori_avg.index, kategori_avg.values, color="skyblue")
plt.title("Rata-rata Pertumbuhan per Kategori", fontsize=14)
plt.xlabel("Rata-rata (%)")
plt.tight_layout()
plt.show()

# 4. Bar chart – Migas vs Non-Migas
ringkasan_migas = df.groupby("migas_non")[["2017", "2018", "2019"]].mean().mean(axis=1)
plt.figure(figsize=(6, 4))
plt.bar(ringkasan_migas.index, ringkasan_migas.values, color=["red", "green"])
plt.title("Perbandingan Migas vs Non-Migas", fontsize=14)
plt.ylabel("Rata-rata (%)")
for i, val in enumerate(ringkasan_migas.values):
    plt.text(i, val + 0.2, f"{val:.2f}%", ha='center', fontsize=10)
plt.tight_layout()
plt.show()

# 5. Heatmap – Sektor dengan nilai minus
df_minus = df[(df[tahun_cols] < 0).any(axis=1)]
plt.figure(figsize=(12, 8))
plt.imshow(df_minus[tahun_cols], cmap="coolwarm", aspect="auto")
plt.title("Sektor dengan Pertumbuhan Negatif (2016–2019)", fontsize=14)
plt.xticks(ticks=range(len(tahun_cols)), labels=tahun_cols)
plt.yticks(ticks=range(len(df_minus)), labels=df_minus["Laju Pertumbuhan Ekonomi"], fontsize=8)
plt.colorbar(label="Pertumbuhan (%)")
plt.tight_layout()
plt.show()