"""
Program Analisis Laju Pertumbuhan Ekonomi
"""

# ---------------------------------------------------------
# Load library
# ---------------------------------------------------------
import pandas as pd

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
#    NOTE: karena me-rename data frame maka harus ditandai sebagai salinan ".copy()"
# ---------------------------------------------------------
df_clean = df[~(df[tahun_cols] == 0).all(axis=1)].copy()

# ---------------------------------------------------------
# 4. Mencari rata-rata 4 tahun (2016-2019)
# ---------------------------------------------------------
df_clean["rata_rata_4tahun"] = df_clean[tahun_cols].mean(axis=1).round(2)

# ---------------------------------------------------------
# 5. TOP 10 TERTINGGI & TERENDAH
# ---------------------------------------------------------
top10_tinggi = df_clean.nlargest(10, "rata_rata_4tahun")
top10_rendah = df_clean.nsmallest(10, "rata_rata_4tahun")

# ---------------------------------------------------------
# 6. Fungsi untuk menentukan kategori besar (Agregat, Pertanian,
#    Industri, Perdagangan, Transportasi, dst.)
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

# Menghitung perbandingan migas/non-migas tiap tahun 
# dan membulatkannya menjadi 2 digit di belakang koma
ringkasan_migas = df_clean.groupby("migas_non")[tahun_cols].mean().round(2)

# ---------------------------------------------------------
# 8. SIMPAN HASIL
# ---------------------------------------------------------
top10_tinggi.to_excel("top10_tinggi.xlsx", index=False)
top10_rendah.to_excel("top10_rendah.xlsx", index=False)
df_clean.to_excel("data_sudah_clean.xlsx", index=False)
ringkasan_migas.to_excel("ringkasan_migas_vs_non.xlsx")

print("Analisis selesai! File hasil sudah disimpan:")
print("- data_sudah_clean.xlsx")
print("- top10_tinggi.xlsx")
print("- top10_rendah.xlsx")
print("- ringkasan_migas_vs_non.xlsx")

