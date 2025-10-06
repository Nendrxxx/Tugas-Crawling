# Analisis Sentimen Pestapora x Freeport

Proyek ini bertujuan untuk menganalisis percakapan publik di Twitter/X terkait kolaborasi **Festival Musik Pestapora** dengan **Freeport Indonesia**.
Analisis dilakukan dengan **crawling data Twitter**, **pembersihan data**, hingga **klasifikasi sentimen** menggunakan model bahasa Indonesia. Hasilnya divisualisasikan dalam dashboard interaktif berbasis **Streamlit**.

---

## Latar Belakang

**Pestapora** merupakan salah satu festival musik terbesar di Indonesia. Pada penyelenggaraan terbaru, keterlibatan **Freeport Indonesia** sebagai sponsor memicu perbincangan publik di media sosial.
Sebagian warganet menanggapinya positif karena dukungan pada acara musik, sementara sebagian lainnya negatif karena kontroversi yang melekat pada Freeport.

Oleh karena itu, dilakukan analisis sentimen untuk:

* Mengetahui **pola respons publik** (positif, negatif, netral).
* Melihat **tren percakapan** pada periode Agustus – September.
* Mengidentifikasi kata-kata dominan yang sering muncul.
* Menyediakan **dashboard interaktif** untuk eksplorasi data.

---

## Alur Analisis

1. **Crawling Data**

   * Menggunakan [selenium-twitter-scraper](https://github.com/godkingjay/selenium-twitter-scraper) untuk mengambil tweet terkait kata kunci/hashtag.
   * Data mentah disimpan dalam folder `scraper/`.

2. **Cleaning Data**

   * Pembersihan teks dari iklan, spam, dan tweet tidak relevan.
   * Disimpan di folder `cleaning/`.

3. **Sentiment Analysis**

   * Menggunakan model [taufiqdp/indonesian-sentiment](https://huggingface.co/taufiqdp/indonesian-sentiment).
   * Hasil prediksi disimpan di `data/Pestapora_sentiment.csv`.

4. **Visualisasi Dashboard**

   * Dibangun dengan **Streamlit**.
   * Menyediakan grafik, wordcloud, serta tampilan interaktif tweet.

---

## Fitur Dashboard

1. **Distribusi Sentimen**

   * Pie chart interaktif: proporsi positif, negatif, netral.

2. **Tren Waktu**

   * Line chart interaktif: perkembangan sentimen per hari (Agustus – September).

3. **Wordcloud**

   * Kata-kata populer divisualisasikan dengan desain berwarna.

4. **Tampilan Tweet**

   * Tweet ditampilkan dalam bentuk kartu (*tweet card*) berisi:

     * Username & waktu posting
     * Isi tweet
     * Sentimen (warna hijau/merah/abu)
     * Likes, retweets, comments
     * Tombol **Lihat di Twitter**

5. **Filter & Pencarian**

   * Filter berdasarkan sentimen
   * Sortir berdasarkan likes, retweet, waktu
   * Search box untuk kata kunci

---

## Instalasi & Menjalankan

1. **Clone Repo**

   ```bash
   git clone https://github.com/Nendrxxx/Tugas-Crawling
   cd Tugas-Crawling
   ```

2. **Buat Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Streamlit**

   ```bash
   streamlit run app.py
   ```

---

## Struktur Proyek

```
pestapora-sentiment/
├── app.py                    # Streamlit dashboard
├── requirements.txt
├── README.md
├── data/
│   └── Pestapora_sentiment.csv
├── cleaning/
│   ├── clean.py
│   └── cleannews.py
├── sentiment_analysis/
│   └── sentimen.py
├── scraper/
│   ├── scraper/
│   ├── tweets/
│   └── sample-command.txt
```

---

## Hasil Utama

* Sebagian besar percakapan bersifat **netral**, namun terdapat perbedaan signifikan antara kelompok **positif** (dukungan acara) dan **negatif** (kritik terhadap Freeport).
* Tren percakapan meningkat tajam pada **awal September**, seiring publikasi sponsor.
* Wordcloud menunjukkan kata kunci dominan: *pestapora*, *freeport*, *musik*, *lingkungan*, dan *kontroversi*.

**Distribusi Sentimen**

* Sentimen Positif: 11.4%
* Sentimen Netral: 32.6%
* Sentimen Negatif: 56.0%

---

## Requirements

```
streamlit
pandas
plotly
matplotlib
wordcloud
selenium
requests
beautifulsoup4
numpy
scikit-learn
torch
transformers
jupyter
```
