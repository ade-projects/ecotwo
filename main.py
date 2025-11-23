"""
Program Analisis Laju Pertumbuhan Ekonomi
"""

# ---------------------------------------------------------
# Load library
# ---------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
file_path = "Data Pertumbuhan Ekonomi Kaltim.csv"
df = pd.read_csv(file_path, sep=";")

# ---------------------------------------------------------
# 2. Parsing: ubah data kolom menjadi float
# ---------------------------------------------------------
tahun_cols = ["2016", "2017", "2018", "2019"]

for col in tahun_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

# ---------------------------------------------------------
# 3. DATA CLEANSING: Hapus baris yang 0% di 4 tahun berturut-turut (2016-2019)
# ---------------------------------------------------------
df["zero_3_tahun"] = (
    ((df["2016"] == 0) & (df["2017"] == 0) & (df["2018"] == 0)) |
    ((df["2017"] == 0) & (df["2018"] == 0) & (df["2019"] == 0))
)

df["zero_semua"] = (df[tahun_cols] == 0).all(axis=1)

df_clean = df[~(df["zero_3_tahun"] | df["zero_semua"])].copy()

df_clean.drop(columns=["zero_3_tahun", "zero_semua"], inplace=True)

# ---------------------------------------------------------
# 4. Hitung rata-rata pertumbuhan (2017–2019 sebagai periode 3 tahun)
# ---------------------------------------------------------
periode_3_tahun = ["2017", "2018", "2019"]
df_clean["rata_rata_3tahun"] = df_clean[periode_3_tahun].mean(axis=1)

# ---------------------------------------------------------
# 5. TOP 10 TERTINGGI & TERENDAH
# ---------------------------------------------------------
top10_tinggi = df_clean.nlargest(10, "rata_rata_3tahun")
top10_rendah = df_clean.nsmallest(10, "rata_rata_3tahun")

# ---------------------------------------------------------
# Fungsi untuk menentukan kategori besar (Agregat, Pertanian,
# Industri, Perdagangan, Transportasi, dst.)
# ---------------------------------------------------------

def tentukan_kategori(nama):
    nama_lower = nama.lower()

    # 1. Agregat GDP
    if any(k in nama_lower for k in [
        "agregat", "laju pertumbuhan ekonomi", 
        "dengan migas", "tanpa migas"
    ]):
        return "Agregat (GDP)"

    # 2. Pertanian, Kehutanan, Perikanan
    elif any(k in nama_lower for k in [
        "pertanian", "perkebunan", "peternakan", "perikanan",
        "kehutanan", "perburuan", "tanaman", "hortikultura"
    ]):
        return "Pertanian, Kehutanan & Perikanan"

    # 3. Pertambangan
    elif any(k in nama_lower for k in [
        "pertambangan", "penggalian", "batubara", 
        "minyak", "gas bumi"
    ]):
        return "Pertambangan & Penggalian"

    # 4. Industri / Manufaktur
    elif any(k in nama_lower for k in [
        "industri", "manufaktur", "pengolahan"
    ]):
        return "Industri Pengolahan"

    # 5. Utilitas (Listrik / Gas / Air)
    elif any(k in nama_lower for k in [
        "listrik", "gas", "ketenagalistrikan", "pengadaan air"
    ]):
        return "Utilitas (Listrik/Gas/Air)"

    # 6. Perdagangan & Reparasi
    elif any(k in nama_lower for k in [
        "perdagangan"
    ]):
        return "Perdagangan & Reparasi"

    # 7. Transportasi & Pergudangan
    elif any(k in nama_lower for k in [
        "transportasi", "angkutan", "pergudangan",
    ]):
        return "Transportasi & Pergudangan"

    # 8. Akomodasi & Makan Minum
    elif any(k in nama_lower for k in [
        "akomodasi", "penyediaan"
    ]):
        return "Akomodasi & Jasa Makanan"

    # 9. Jasa Keuangan & Asuransi
    elif any(k in nama_lower for k in [
        "keuangan", "asuransi", "bank"
    ]):
        return "Jasa Keuangan & Asuransi"

    # Default
    return "Lainnya"

df_clean["kategori"] = df_clean["Laju Pertumbuhan Ekonomi"].apply(tentukan_kategori)

# ---------------------------------------------------------
# 7. MIGAS vs NON-MIGAS
# ---------------------------------------------------------
def migas_label(nama):
    nama = nama.lower()
    if any(k in nama for k in ["migas", "minyak", "gas"]):
        return "migas"
    return "non-migas"

df_clean["migas_non"] = df_clean["Laju Pertumbuhan Ekonomi"].apply(migas_label)

ringkasan_migas = df_clean.groupby("migas_non")[periode_3_tahun].mean()

# ---------------------------------------------------------
# 8. Deteksi tahun minus (merugi)
# ---------------------------------------------------------
df_minus = df_clean[
    (df_clean[tahun_cols] < 0).any(axis=1)
][["Laju Pertumbuhan Ekonomi"] + tahun_cols]

# ---------------------------------------------------------
# 9. SIMPAN HASIL
# ---------------------------------------------------------
top10_tinggi.to_excel("top10_tinggi.xlsx", index=False)
top10_rendah.to_excel("top10_rendah.xlsx", index=False)
df_clean.to_excel("data_sudah_clean.xlsx", index=False)
ringkasan_migas.to_excel("ringkasan_migas_vs_non.xlsx")
df_minus.to_excel("tahun_minus.xlsx", index=False)

print("Analisis selesai! File hasil sudah disimpan:")
print("- data_sudah_clean.xlsx")
print("- top10_tinggi.xlsx")
print("- top10_rendah.xlsx")
print("- ringkasan_migas_vs_non.xlsx")
print("- tahun_minus.xlsx")
