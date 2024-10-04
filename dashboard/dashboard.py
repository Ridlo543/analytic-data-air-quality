import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Kualitas Udara Wanshouxigong", layout="wide")


# Fungsi untuk memuat data
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_air_quality_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


df = load_data()

with st.sidebar:
    st.title("Dashboard Analisis Kualitas Udara Wanshouxigong")
    st.markdown("Jelajahi tren dan pola kualitas udara.")

    # Pilihan pertanyaan
    question = st.sidebar.selectbox(
        "Pilih pertanyaan analisis:",
        [
            "1. Bagaimana tren PM2.5 dan PM10 selama periode waktu dataset?",
            "2. Apakah ada pola harian dalam tingkat polutan udara?",
            "3. Bagaimana curah hujan mempengaruhi konsentrasi polutan udara?",
            "4. Berapa banyak pola kualitas udara yang berbeda dapat diidentifikasi?",
            "5. Apakah ada perbedaan signifikan dalam pola kualitas udara antara musim panas, gugur, semi, dan musim dingin?",
            "6. Bagaimana tren kualitas udara dari tahun ke tahun?",
            "7. Apakah ada pola mingguan dalam kualitas udara?",
            "8. Bagaimana hubungan antara berbagai polutan?",
        ],
    )

    # Pemilih rentang tanggal
    start_date = st.date_input("Tanggal Mulai", df["date"].min())
    end_date = st.date_input("Tanggal Akhir", df["date"].max())

    # Informasi pembuat
    st.markdown("---")  # Garis pemisah
    st.markdown("### Informasi Pembuat")
    st.markdown("**Nama:** Ridlo Abdullah Ulinnuha")
    st.markdown("**Email:** ridloabdullahulinnuha543@gmail.com")

# Main area
st.title("Analisis Kualitas Udara Wanshouxigong")

# Filter data berdasarkan rentang tanggal
mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
df_filtered = df.loc[mask]

# Fungsi untuk setiap pertanyaan
def question_1():
    st.header("Tren PM2.5 dan PM10")
    df_filtered["year_month"] = df_filtered["date"].dt.to_period("M")
    monthly_avg = (
        df_filtered.groupby("year_month")[["PM2.5", "PM10"]].mean().reset_index()
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_avg["year_month"].astype(str), monthly_avg["PM2.5"], label="PM2.5")
    ax.plot(monthly_avg["year_month"].astype(str), monthly_avg["PM10"], label="PM10")
    ax.set_title("Tren Bulanan PM2.5 dan PM10")
    ax.set_xlabel("Tahun-Bulan")
    ax.set_ylabel("Konsentrasi (µg/m³)")
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig)

    st.write(
        """
    **Insight:**

    1. **Pola Musiman:**
       - Terlihat pola musiman yang jelas untuk kedua PM2.5 dan PM10, dengan puncak-puncak yang terjadi secara berkala.
       - Puncak konsentrasi cenderung terjadi pada bulan-bulan tertentu setiap tahunnya, kemungkinan besar terkait dengan musim kering atau aktivitas tertentu yang berulang tahunan.

    2. **Korelasi PM2.5 dan PM10:**
       - PM2.5 dan PM10 menunjukkan pola yang sangat mirip, dengan PM10 selalu memiliki konsentrasi yang lebih tinggi.
       - Hal ini wajar mengingat PM10 mencakup partikel yang lebih besar termasuk PM2.5.

    3. **Tren Jangka Panjang:**
       - Tidak terlihat adanya tren penurunan atau peningkatan yang jelas dalam jangka panjang.
       - Konsentrasi PM2.5 dan PM10 tampaknya berfluktuasi di sekitar tingkat rata-rata tertentu selama periode pengamatan.

    4. **Puncak Tertinggi:**
       - Puncak tertinggi untuk kedua polutan terlihat terjadi sekitar pertengahan periode pengamatan.
       - Ini mungkin menunjukkan adanya kejadian khusus atau kondisi meteorologi yang ekstrem pada periode tersebut.

    5. **Konsentrasi Minimum:**
       - Terdapat periode-periode dengan konsentrasi yang relatif rendah, yang mungkin berkorelasi dengan musim hujan atau periode dengan aktivitas polusi yang berkurang.

    **Kesimpulan:**
    Analisis tren bulanan PM2.5 dan PM10 menunjukkan adanya pola musiman yang kuat dan konsisten. Kedua polutan ini menunjukkan perilaku yang sangat mirip, mengindikasikan sumber atau faktor penyebab yang serupa. Meskipun terdapat variabilitas yang signifikan antar tahun, tidak terlihat adanya tren jangka panjang yang jelas menuju peningkatan atau penurunan kualitas udara.
    """
    )


def question_2():
    st.header("Pola Harian Tingkat Polutan Udara")
    hourly_avg = df_filtered.groupby("hour")[
        ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    ].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    hourly_avg.plot(ax=ax)
    ax.set_title("Pola Harian Konsentrasi Polutan")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Konsentrasi")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    st.pyplot(fig)

    st.write(
        """
    **Insight:**

    1. **Pola CO yang Dominan:**
       - CO menunjukkan konsentrasi yang jauh lebih tinggi dibandingkan polutan lainnya sepanjang hari.
       - Terdapat pola bimodal yang jelas untuk CO, dengan puncak di pagi hari (sekitar jam 8-10) dan malam hari (sekitar jam 20-22).
       - Konsentrasi CO terendah terjadi pada siang hari (sekitar jam 14-16).

    2. **Pola O3 yang Unik:**
       - O3 menunjukkan pola yang berlawanan dengan CO dan polutan lainnya.
       - Konsentrasi O3 mencapai puncak pada siang hari (sekitar jam 12-15) dan terendah pada malam hari.
       - Hal ini konsisten dengan pembentukan ozon yang dipengaruhi oleh radiasi matahari.

    3. **PM2.5 dan PM10:**
       - PM2.5 dan PM10 menunjukkan pola yang sangat mirip, dengan PM10 selalu sedikit lebih tinggi.
       - Keduanya memiliki puncak di pagi hari (sekitar jam 7-9) dan malam hari (sekitar jam 20-22).
       - Konsentrasi terendah terjadi pada siang hari, mirip dengan pola CO.

    4. **NO2 dan SO2:**
       - NO2 dan SO2 menunjukkan fluktuasi yang lebih kecil dibandingkan polutan lainnya.
       - NO2 memiliki pola yang mirip dengan PM dan CO, dengan puncak di pagi dan malam hari.
       - SO2 menunjukkan variasi yang lebih kecil sepanjang hari.

    5. **Pola Umum:**
       - Sebagian besar polutan (kecuali O3) menunjukkan pola bimodal dengan puncak di pagi dan malam hari.
       - Konsentrasi terendah untuk sebagian besar polutan terjadi pada siang hari.

    **Kesimpulan:**
    Analisis pola harian konsentrasi polutan menunjukkan variasi yang signifikan sepanjang hari, dengan pola yang berbeda untuk masing-masing polutan. CO memiliki konsentrasi tertinggi dan menunjukkan pola bimodal yang jelas, kemungkinan besar terkait dengan aktivitas lalu lintas pada jam sibuk pagi dan sore. O3 menunjukkan pola yang berlawanan, mencerminkan sifatnya sebagai polutan sekunder yang terbentuk melalui reaksi fotokimia pada siang hari.
    """
    )


def question_3():
    st.header("Pengaruh Curah Hujan terhadap Konsentrasi Polutan")
    df_filtered["rain_category"] = pd.cut(
        df_filtered["RAIN"],
        bins=[-1, 0, 10, float("inf")],
        labels=["Tidak Hujan", "Hujan Ringan", "Hujan Lebat"],
    )

    rain_effect = df_filtered.groupby("rain_category")[
        ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    ].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    rain_effect.plot(kind="bar", ax=ax)
    ax.set_title("Efek Curah Hujan terhadap Konsentrasi Polutan")
    ax.set_xlabel("Kategori Hujan")
    plt.xticks(rotation=45)
    ax.set_ylabel("Konsentrasi Rata-rata")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    st.pyplot(fig)

    st.write(
        """
    **Insight:**

    1. **Dominasi CO:**
       - CO menunjukkan konsentrasi yang jauh lebih tinggi dibandingkan polutan lainnya dalam semua kategori curah hujan.
       - Konsentrasi CO tampak sedikit lebih tinggi pada kondisi hujan ringan dibandingkan dengan kondisi tidak hujan.

    2. **Efek Hujan pada Partikulat Matter (PM):**
       - Baik PM2.5 maupun PM10 menunjukkan penurunan konsentrasi yang signifikan saat terjadi hujan ringan dibandingkan dengan kondisi tidak hujan.
       - Penurunan ini konsisten dengan efek pencucian atmosfer oleh hujan.

    3. **Pengaruh pada Gas-gas Polutan:**
       - SO2, NO2, dan O3 menunjukkan sedikit penurunan konsentrasi pada kondisi hujan ringan dibandingkan dengan kondisi tidak hujan.
       - Penurunan ini tidak sedrastis yang terlihat pada partikulat matter.

    4. **Hujan Lebat:**
       - Data untuk kondisi hujan lebat tampaknya tidak tersedia atau sangat terbatas, karena tidak ada batang yang terlihat untuk kategori ini pada grafik.

    5. **Variasi antar Polutan:**
       - Meskipun semua polutan menunjukkan tren penurunan saat hujan ringan, tingkat penurunannya bervariasi antar polutan.
       - PM10 tampak mengalami penurunan yang lebih besar dibandingkan PM2.5, yang mungkin disebabkan oleh ukuran partikelnya yang lebih besar.

    **Kesimpulan:**
    Analisis efek curah hujan terhadap konsentrasi polutan menunjukkan bahwa hujan memiliki dampak pembersihan yang signifikan terhadap kualitas udara, terutama untuk partikulat matter (PM2.5 dan PM10). Efek ini kurang terlihat pada gas-gas polutan seperti SO2, NO2, dan O3, meskipun masih ada sedikit penurunan konsentrasi.
    """
    )


def question_4():
    st.header("Identifikasi Pola Kualitas Udara dengan Clustering")

    # Baca hasil clustering
    df_clustered = pd.read_csv("dashboard/data_clustering.csv")

    # Analisis karakteristik setiap cluster
    clustering_features = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    cluster_means = df_clustered.groupby("cluster")[clustering_features].mean()
    st.write("Karakteristik rata-rata setiap cluster:")
    st.write(cluster_means)

    # Visualisasi karakteristik cluster
    plt.figure(figsize=(14, 8))
    cluster_means.plot(kind="bar")
    plt.title("Karakteristik Rata-rata Setiap Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Konsentrasi")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    st.pyplot(plt)

    # Visualisasi scatter plot
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(
        df_clustered["PM2.5"],
        df_clustered["PM10"],
        c=df_clustered["cluster"],
        cmap="viridis",
    )
    plt.xlabel("PM2.5")
    plt.ylabel("PM10")
    plt.title("Clustering Kualitas Udara")
    plt.colorbar(scatter)
    st.pyplot(plt)

    # Insight dan penjelasan
    st.write(
        """
    Berdasarkan hasil clustering, kita dapat mengidentifikasi 3 pola kualitas udara yang berbeda:

    1. Cluster 0: Tingkat polutan sedang
       - PM2.5 dan PM10: Konsentrasi sedang
       - SO2 dan NO2: Konsentrasi rendah
       - CO: Konsentrasi sedang
       - O3: Konsentrasi sedang

    2. Cluster 1: Tingkat polutan tinggi
       - PM2.5 dan PM10: Konsentrasi tinggi
       - SO2 dan NO2: Konsentrasi sedang
       - CO: Konsentrasi sangat tinggi
       - O3: Konsentrasi rendah

    3. Cluster 2: Tingkat polutan rendah hingga sedang
       - PM2.5 dan PM10: Konsentrasi rendah
       - SO2 dan NO2: Konsentrasi rendah
       - CO: Konsentrasi tinggi
       - O3: Konsentrasi rendah

    Insight:
    1. Cluster 1 menunjukkan kondisi kualitas udara terburuk, dengan tingkat PM2.5, PM10, dan CO yang sangat tinggi.
    2. Cluster 0 mewakili kondisi kualitas udara "normal" atau rata-rata.
    3. Cluster 2 menunjukkan kualitas udara yang relatif baik untuk sebagian besar polutan, kecuali CO yang masih tinggi.
    4. CO memiliki variasi yang sangat signifikan antar cluster, mungkin menjadi indikator utama perubahan kualitas udara.
    5. O3 cenderung rendah di semua cluster, menunjukkan bahwa polutan ini mungkin kurang signifikan dalam menentukan kualitas udara keseluruhan.
    6. PM2.5 dan PM10 menunjukkan pola yang serupa di semua cluster, mengindikasikan sumber atau faktor pengaruh yang sama.

    Kesimpulan:
    Analisis clustering ini membantu mengidentifikasi tiga pola kualitas udara yang berbeda, dari yang relatif baik hingga sangat buruk. Pola-pola ini dapat digunakan untuk memahami dinamika polusi udara, mengidentifikasi faktor-faktor yang berkontribusi pada episode polusi tinggi, dan mengembangkan strategi mitigasi yang lebih efektif.
    """
    )


def determine_season(date):
    month = pd.to_datetime(date).month
    if 3 <= month <= 5:
        return "Spring"
    elif 6 <= month <= 8:
        return "Summer"
    elif 9 <= month <= 11:
        return "Autumn"
    else:
        return "Winter"


def question_5():
    st.header("Perbedaan Pola Kualitas Udara antar Musim")

    # Baca hasil clustering
    df_clustered = pd.read_csv("dashboard/data_clustering.csv")

    # Konversi kolom 'date' ke tipe datetime
    df_clustered["date"] = pd.to_datetime(df_clustered["date"])

    # Tentukan musim
    df_clustered["season"] = df_clustered["date"].apply(determine_season)

    # Analisis distribusi musim dalam setiap cluster
    season_distribution = pd.crosstab(
        df_clustered["cluster"], df_clustered["season"], normalize="index"
    )
    st.write("\nDistribusi musim dalam setiap cluster:")
    st.write(season_distribution)

    # Visualisasi distribusi musim
    plt.figure(figsize=(10, 6))
    season_distribution.plot(kind="bar", stacked=True)
    plt.title("Distribusi Musim dalam Setiap Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Proporsi")
    plt.legend(title="Musim")
    plt.tight_layout()
    st.pyplot(plt)

    # Analisis rata-rata polutan per musim
    seasonal_means = df_clustered.groupby("season")[
        ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    ].mean()
    st.write("\nRata-rata konsentrasi polutan per musim:")
    st.write(seasonal_means)

    # Visualisasi rata-rata polutan per musim
    plt.figure(figsize=(12, 6))
    seasonal_means.plot(kind="bar")
    plt.title("Rata-rata Konsentrasi Polutan per Musim")
    plt.xlabel("Musim")
    plt.ylabel("Konsentrasi")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    st.pyplot(plt)

    st.write(
        """
    Berdasarkan analisis perbedaan pola kualitas udara antar musim dan cluster, kita dapat menyimpulkan:

    1. Variasi Konsentrasi Polutan antar Musim:
       - CO: Menunjukkan variasi yang sangat signifikan antar musim, dengan konsentrasi tertinggi di musim dingin (Winter) dan terendah di musim semi (Spring).
       - PM2.5 dan PM10: Cenderung lebih tinggi di musim dingin (Winter) dan musim gugur (Autumn).
       - SO2 dan NO2: Menunjukkan variasi yang lebih kecil antar musim, namun tetap ada pola yang terlihat.
       - O3: Relatif stabil antar musim, dengan sedikit peningkatan di musim panas (Summer).

    2. Distribusi Musim dalam Cluster:
       - Cluster 0: Didominasi oleh musim dingin (Winter, 36.78%) dan musim semi (Spring, 28.96%), dengan proporsi musim panas (Summer) yang paling rendah (7.02%).
       - Cluster 1: Memiliki distribusi yang lebih merata, dengan dominasi musim gugur (Autumn, 33.89%) dan musim panas (Summer, 25.27%). Musim dingin (Winter) memiliki proporsi terendah (16.61%).
       - Cluster 2: Didominasi oleh musim panas (Summer, 34.71%) dan musim semi (Spring, 26.11%), dengan proporsi musim gugur (Autumn) yang paling rendah (19.57%).

    3. Implikasi:
       - Cluster 0 mungkin mencerminkan kondisi kualitas udara yang lebih buruk, terutama terkait dengan polutan musim dingin seperti PM2.5 dan CO.
       - Cluster 1 menunjukkan variasi musiman yang lebih seimbang, mungkin mencerminkan daerah dengan fluktuasi kualitas udara yang moderat sepanjang tahun.
       - Cluster 2 kemungkinan mencerminkan kondisi kualitas udara yang lebih baik, dengan dominasi musim panas dan semi yang umumnya memiliki tingkat polusi yang lebih rendah.

    Kesimpulan:
    Terdapat perbedaan signifikan dalam pola kualitas udara antar musim dan cluster. Setiap cluster memiliki karakteristik musiman yang berbeda, yang mungkin mencerminkan kondisi geografis, meteorologis, atau aktivitas manusia yang berbeda. Pemahaman tentang variasi ini penting untuk merancang strategi pengendalian polusi udara yang efektif dan tepat sasaran untuk setiap cluster dan musim.
    """
    )


def question_6():
    st.header("Tren Kualitas Udara dari Tahun ke Tahun")

    # Kode untuk membuat visualisasi
    yearly_trend = df_filtered.groupby("year")[
        ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    ].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    yearly_trend.plot(ax=ax)
    ax.set_title("Tren Tahunan Polutan")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Konsentrasi Rata-rata")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    st.pyplot(fig)

    first_year = yearly_trend.index.min()
    last_year = yearly_trend.index.max()
    percent_change = (
        (yearly_trend.loc[last_year] - yearly_trend.loc[first_year])
        / yearly_trend.loc[first_year]
    ) * 100

    st.write(
        f"Perubahan persentase konsentrasi polutan dari {first_year} ke {last_year}:"
    )
    st.write(percent_change)

    st.write(
        """
    ***Insight:***

    1. **Penurunan Umum Polutan:**
       - Mayoritas polutan menunjukkan tren penurunan dari tahun 2013 hingga 2017.
       - O3 mengalami penurunan paling signifikan sebesar 27.63%.
       - PM10 juga menunjukkan penurunan yang cukup besar, yaitu 16.14%.

    2. **Perubahan Spesifik per Polutan:**
       - PM2.5: Menurun sebesar 5.44%
       - PM10: Menurun sebesar 16.14%
       - SO2: Sedikit menurun sebesar 2.78%
       - NO2: Satu-satunya polutan yang meningkat, meski hanya sebesar 1.53%
       - CO: Menurun sebesar 7.23%
       - O3: Penurunan terbesar sebesar 27.63%

    3. **Analisis Tren:**
       - Tren penurunan terlihat konsisten untuk sebagian besar polutan dari tahun ke tahun.
       - Penurunan tajam terlihat pada awal periode (2013-2014) untuk beberapa polutan seperti PM10 dan O3.
       - Setelah 2015, beberapa polutan menunjukkan stabilisasi atau sedikit peningkatan.

    4. **Implikasi Positif:**
       - Penurunan umum dalam konsentrasi polutan menunjukkan perbaikan kualitas udara secara keseluruhan.
       - Penurunan signifikan O3 dan PM10 mungkin hasil dari kebijakan pengendalian polusi yang efektif.

    **Kesimpulan:**
    Tren kualitas udara dari 2013 hingga 2017 menunjukkan perbaikan yang signifikan untuk sebagian besar polutan. Penurunan tajam O3 dan PM10 adalah indikator positif dari efektivitas kebijakan pengendalian polusi udara. Namun, peningkatan kecil NO2 dan stabilisasi beberapa polutan dalam beberapa tahun terakhir menunjukkan perlunya pemantauan dan upaya berkelanjutan. Secara keseluruhan, data menunjukkan kemajuan dalam meningkatkan kualitas udara di wilayah tersebut, tetapi juga menekankan pentingnya mempertahankan dan meningkatkan upaya pengendalian polusi untuk memastikan tren positif ini berlanjut di masa depan.
    """
    )


def question_7():
    st.header("Pola Mingguan Kualitas Udara")
    df_filtered["day_of_week"] = df_filtered["date"].dt.dayofweek
    weekly_pattern = df_filtered.groupby("day_of_week")[
        ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    ].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    weekly_pattern.plot(ax=ax)
    ax.set_title("Pola Mingguan Polutan")
    ax.set_xlabel("Hari dalam Minggu")
    ax.set_ylabel("Konsentrasi Rata-rata")
    plt.xticks(
        range(7), ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    )
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    st.pyplot(fig)

    weekday_avg = weekly_pattern.iloc[:5].mean()
    weekend_avg = weekly_pattern.iloc[5:].mean()

    st.write("Rata-rata konsentrasi polutan:")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Hari Kerja:")
        st.write(weekday_avg)
    with col2:
        st.write("Akhir Pekan:")
        st.write(weekend_avg)

    st.write(
        """
    *Insight:*

    1. **Perbedaan Hari Kerja vs Akhir Pekan:**
       - Secara umum, konsentrasi polutan sedikit lebih tinggi pada akhir pekan dibandingkan hari kerja.
       - PM2.5 meningkat 2.86% pada akhir pekan (72.77 vs 70.75 pada hari kerja).
       - PM10 meningkat 3.25% pada akhir pekan (98.21 vs 95.11 pada hari kerja).
       - CO menunjukkan peningkatan terbesar, yaitu 2.97% pada akhir pekan (1170.62 vs 1136.83 pada hari kerja).

    2. **Pola Harian:**
       - CO menunjukkan fluktuasi paling signifikan sepanjang minggu, dengan puncak pada hari Jumat.
       - PM2.5 dan PM10 menunjukkan pola yang serupa, dengan sedikit peningkatan menjelang akhir pekan.
       - NO2 relatif stabil sepanjang minggu dengan sedikit penurunan pada akhir pekan.
       - O3 menunjukkan variasi minimal antar hari dalam seminggu.

    3. **Konsistensi Polutan:**
       - SO2 dan O3 menunjukkan perbedaan minimal antara hari kerja dan akhir pekan.
       - NO2 sedikit lebih rendah pada akhir pekan, mungkin karena berkurangnya aktivitas industri atau lalu lintas.

    4. **Implikasi:**
       - Peningkatan polutan pada akhir pekan mungkin disebabkan oleh peningkatan aktivitas rekreasi atau perjalanan.
       - Stabilitas relatif beberapa polutan menunjukkan sumber polusi yang konsisten sepanjang minggu.

    **Kesimpulan:**
    Analisis pola mingguan kualitas udara menunjukkan perbedaan kecil namun konsisten antara hari kerja dan akhir pekan. Akhir pekan cenderung memiliki tingkat polusi yang sedikit lebih tinggi untuk sebagian besar polutan, terutama PM2.5, PM10, dan CO. Ini mungkin mencerminkan perubahan pola aktivitas manusia, seperti peningkatan perjalanan rekreasi atau kegiatan luar ruangan pada akhir pekan. Namun, perbedaan ini relatif kecil, menunjukkan bahwa sumber polusi utama mungkin konsisten sepanjang minggu. NO2 yang sedikit lebih rendah pada akhir pekan bisa mengindikasikan pengurangan aktivitas industri atau lalu lintas kendaraan bermotor. Temuan ini menekankan pentingnya strategi pengendalian polusi yang mempertimbangkan variasi mingguan dan memfokuskan pada sumber-sumber yang konsisten sepanjang minggu.
    """
    )


def question_8():
    st.header("Korelasi antar Variabel Kualitas Udara")
    clustering_features = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    # Kode untuk membuat heatmap
    correlation_matrix = df[clustering_features + ["TEMP", "RAIN"]].corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    plt.title("Heatmap Korelasi Variabel Kualitas Udara")
    st.pyplot(fig)

    # Identifikasi korelasi tertinggi
    correlation_matrix_abs = correlation_matrix.abs()
    np.fill_diagonal(correlation_matrix_abs.values, 0)
    highest_corr = correlation_matrix_abs.unstack().sort_values(ascending=False)[:5]
    st.write("Pasangan variabel dengan korelasi tertinggi:")
    st.write(highest_corr)

    st.write(
        """
    **Insight:**

    1. **Korelasi Kuat antar Polutan:**
       - PM2.5 dan PM10 menunjukkan korelasi positif yang sangat kuat (0.851), mengindikasikan sumber atau perilaku yang serupa.
       - PM2.5 juga berkorelasi kuat dengan CO (0.754), menunjukkan kemungkinan sumber bersama seperti pembakaran.
       - CO dan NO2 memiliki korelasi yang cukup kuat (0.686), mungkin terkait dengan emisi kendaraan bermotor.

    2. **Hubungan Polutan dengan Faktor Meteorologi:**
       - O3 memiliki korelasi positif moderat dengan TEMP (0.59), konsisten dengan pembentukan ozon yang dipengaruhi suhu.
       - NO2 menunjukkan korelasi negatif moderat dengan O3 (-0.53), mungkin mencerminkan siklus fotokimia NO2-O3.
       - Sebagian besar polutan memiliki korelasi negatif lemah dengan TEMP, kecuali O3.
       - RAIN memiliki korelasi yang sangat lemah dengan semua polutan, menunjukkan pengaruh minimal pada konsentrasi polutan.

    3. **Kelompok Polutan:**
       - PM2.5, PM10, CO, dan NO2 membentuk kelompok dengan korelasi positif yang kuat satu sama lain.
       - SO2 menunjukkan korelasi positif moderat dengan kelompok ini tetapi tidak sekuat yang lain.
       - O3 berdiri sendiri dengan korelasi negatif terhadap sebagian besar polutan lain.

    4. **Implikasi untuk Sumber Polusi:**
       - Korelasi kuat antara PM2.5, PM10, CO, dan NO2 mungkin mengindikasikan sumber bersama seperti lalu lintas atau industri.
       - Perilaku unik O3 mencerminkan sifatnya sebagai polutan sekunder yang terbentuk melalui reaksi fotokimia.

    **Kesimpulan:**
    Analisis korelasi menunjukkan hubungan kompleks antar variabel kualitas udara. Korelasi kuat antara PM2.5, PM10, CO, dan NO2 mengindikasikan sumber polusi bersama, kemungkinan besar terkait dengan aktivitas antropogenik seperti lalu lintas dan industri. O3 menunjukkan pola yang berbeda, menegaskan perannya sebagai polutan sekunder yang dipengaruhi oleh faktor meteorologi, terutama suhu. Hubungan yang lemah antara curah hujan dan polutan menunjukkan bahwa hujan mungkin tidak memiliki efek pembersihan yang signifikan pada kualitas udara di daerah ini.
    """
    )


# Menampilkan konten berdasarkan pertanyaan yang dipilih
if question.startswith("1."):
    question_1()
elif question.startswith("2."):
    question_2()
elif question.startswith("3."):
    question_3()
elif question.startswith("4."):
    question_4()
elif question.startswith("5."):
    question_5()
elif question.startswith("6."):
    question_6()
elif question.startswith("7."):
    question_7()
elif question.startswith("8."):
    question_8()
