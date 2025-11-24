# ---------------------------------------------------------
# 1. Load library
# ---------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# ---------------------------------------------------------
# 2. Load Data
# ---------------------------------------------------------
df = pd.read_excel("data_sudah_clean.xlsx")
tahun_cols = ["2016", "2017", "2018", "2019"]

# ---------------------------------------------------------
# 3. Visualisasi 10 sektor tertinggi
# ---------------------------------------------------------
top10_tinggi = df.nlargest(10, "rata_rata_4tahun")
wrap_labels = [textwrap.fill(label, 40) for label in top10_tinggi["Laju Pertumbuhan Ekonomi"]] #wrap text agar tidak terlalu panjang
plt.figure(figsize=(14,8))
plt.barh(wrap_labels, top10_tinggi["rata_rata_4tahun"])
plt.gca().invert_yaxis()
plt.xlabel("Rata-rata 2016-2019 (%)", fontsize=12)
plt.title("10 Sektor dengan Pertumbuhan Ekonomi Tertinggi (2016-2019)")
plt.tight_layout()
# Menambahkan angka rata-rata di setiap ujung bar
for i, v in enumerate(top10_tinggi["rata_rata_4tahun"]):
    plt.text(v + 0.1, i, v, va='center', fontsize=10)
plt.show()

# ---------------------------------------------------------
# 3. Visualisasi 10 sektor terendah
# ---------------------------------------------------------
top10_rendah = df.nsmallest(10, "rata_rata_4tahun")
print(top10_rendah)
wrap_labels = [textwrap.fill(label, 40) for label in top10_rendah["Laju Pertumbuhan Ekonomi"]] #wrap text agar tidak terlalu panjang
plt.figure(figsize=(14,8))
plt.barh(wrap_labels, top10_rendah["rata_rata_4tahun"])
plt.gca().invert_yaxis()
plt.xlabel("Rata-rata 2016-2019 (%)", fontsize=12)
plt.title("10 Sektor dengan Pertumbuhan Ekonomi Terendah (2016-2019)")
plt.tight_layout()
# Menambahkan angka di setiap ujung bar
for i, v in enumerate(top10_rendah["rata_rata_4tahun"]):
    plt.text(v, i, v, va='center', fontsize=10)
plt.show()

# 3. Bar chart – Rata-rata per kategori
kategori_avg = df.groupby("kategori")["rata_rata_4tahun"].mean().sort_values(ascending=True).round(2)
plt.figure(figsize=(14, 8))
plt.barh(kategori_avg.index, kategori_avg.values, color="skyblue")
plt.title("Rata-rata Pertumbuhan per Kategori", fontsize=14)
plt.xlabel("Rata-rata (%)")
plt.tight_layout()
for i, v in enumerate(kategori_avg):
    plt.text(v, i, v, va='center', fontsize=10)
plt.show()

# 4. Bar chart – Migas vs Non-Migas
ringkasan_migas = df.groupby("migas_non")[["2017", "2018", "2019"]].mean().mean(axis=1)
plt.figure(figsize=(8, 6))
plt.bar(ringkasan_migas.index, ringkasan_migas.values, color=["red", "green"])
plt.title("Perbandingan Migas vs Non-Migas", fontsize=14)
plt.ylabel("Rata-rata (%)")
for i, val in enumerate(ringkasan_migas.values):
    plt.text(i, val + 0.1, f"{val:.2f}%", ha='center', fontsize=10)
plt.tight_layout()
plt.show()

#5. Line Chart – Tren Laju Pertumbuhan Ekonomi Kaltim (2016-2019) Top 10 Tertinggi
# ---------------------------------------------------------
plot_df = top10_tinggi.set_index('Laju Pertumbuhan Ekonomi')[tahun_cols]
wrap_labels = [textwrap.fill(label, 40) for label in top10_tinggi["Laju Pertumbuhan Ekonomi"]] #wrap text agar tidak terlalu panjang
plt.figure(figsize=(14,8))
for idx, sector in enumerate(plot_df.index):
    y = plot_df.loc[sector].astype(float).values
    plt.plot([int(c) for c in tahun_cols], y, marker='o', label=wrap_labels[idx], linewidth=1.8)
plt.xlabel("Tahun", fontsize=12)
plt.ylabel("Laju Pertumbuhan (%)", fontsize=12)
plt.title("Tren Laju Pertumbuhan Ekonomi Kaltim (2016-2019) - Top 10 Sektor Tertinggi", fontsize=14, fontweight='bold')
plt.xticks([int(x) for x in tahun_cols])
plt.legend(title="Daftar Sektor", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9)
plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)
plt.tight_layout()
plt.show()