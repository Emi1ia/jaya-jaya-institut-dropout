# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan — Jaya Jaya Institut

- **Nama:** Emilia Loho
- **Email:** lohoemilia@gmail.com
- **ID Dicoding:** emilia_loho

> **Varian dashboard: OCEAN.**
> Palet biru dingin + teal, coral untuk Dropout — `#3D8FC7` / `#2EA98C` / `#E4643B`.
> Urutan baca: angka utama -> komposisi -> faktor finansial -> demografi -> program studi -> monitoring risiko.
> Struktur kode `metabase_setup.py`: linear step pipeline (satu dict `STATE`, fungsi `step_*`, daftar `PIPELINE`).
> Dashboard berjalan di **http://localhost:3004/dashboard/2**
> (container `metabase4`). Detail lengkap ada di `DASHBOARD_VARIANT.md`.

## Business Understanding

Jaya Jaya Institut merupakan institusi pendidikan perguruan tinggi yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak juga siswa yang tidak menyelesaikan pendidikannya alias **dropout**. Jumlah dropout yang tinggi menjadi masalah besar bagi sebuah institusi pendidikan — baik dari sisi finansial maupun reputasi. Oleh karena itu, Jaya Jaya Institut ingin **mendeteksi secepat mungkin** siswa yang berpotensi dropout agar dapat diberikan bimbingan khusus, serta membutuhkan dashboard untuk memudahkan pemantauan performa siswa.

### Permasalahan Bisnis

1. Tingkat dropout siswa yang tinggi, sementara faktor-faktor utama penyebabnya belum diketahui secara pasti.
2. Belum ada mekanisme deteksi dini siswa berisiko dropout, sehingga intervensi selalu terlambat.
3. Belum ada dashboard monitoring yang memudahkan manajemen memahami data dan memantau performa siswa.

### Cakupan Proyek

1. Exploratory Data Analysis (EDA) untuk menemukan faktor-faktor yang memengaruhi dropout.
2. Membangun model machine learning untuk memprediksi risiko dropout siswa.
3. Membuat business dashboard menggunakan **Metabase** untuk monitoring performa siswa.
4. Membangun prototype prediksi berbasis **Streamlit** dan men-deploy-nya ke Streamlit Community Cloud.
5. Menyusun rekomendasi action items untuk menurunkan tingkat dropout.

### Persiapan

**Sumber data:** [Dicoding — students' performance dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md) — 4.424 baris × 37 kolom berisi data demografi, sosial-ekonomi, dan performa akademik siswa, dengan target `Status` (Dropout / Enrolled / Graduate).

**Setup environment (venv):**

Proyek ini dikembangkan dan diuji menggunakan **Python 3.11** (disarankan Python 3.11 atau lebih baru).

```bash
python --version                 # pastikan Python 3.11+
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Menjalankan notebook:** buka `notebook.ipynb` di Jupyter/Colab lalu *Run All*. Notebook memuat seluruh tahapan: business understanding, data understanding, EDA, data preparation, modeling, evaluation, hingga kesimpulan.

**File pendukung:**

- `train_model.py` — script training model (menghasilkan `model/model.joblib` dan `model/metadata.json`).
- `prepare_dashboard_data.py` — menghasilkan `data_dashboard.csv` (data berlabel + skor risiko model) yang menjadi sumber data dashboard Metabase.
- `load_dashboard_db.py` — memuat `data_dashboard.csv` ke `students.db` (SQLite, tabel `students`) agar bisa dibaca Metabase.
- `metabase_setup.py` — membangun seluruh question & dashboard Metabase secara otomatis lewat Metabase API.
- `DEPLOYMENT.md` — panduan deploy prototype ke Streamlit Community Cloud.
- `validate_submission.py` — memeriksa kelengkapan struktur submission (lihat `METABASE_SETUP.md` untuk panduan dashboard).

### Struktur Berkas

```
submission/
├── model/
│   ├── model.joblib               # model final (Logistic Regression pipeline)
│   ├── metadata.json              # metrik evaluasi, daftar fitur, feature importance
│   └── feature_defaults.json      # nilai default fitur untuk input aplikasi
├── notebook.ipynb                 # seluruh proses data science (sudah dieksekusi)
├── app.py                         # prototype Streamlit
├── requirements.txt               # dependencies
├── README.md                      # dokumentasi proyek (berkas ini)
├── METABASE_SETUP.md              # panduan membangun ulang dashboard Metabase
├── DASHBOARD_VARIANT.md           # catatan varian: palet, tata letak, struktur kode
├── metabase.db.mv.db              # export database instance Metabase (berisi dashboard)
├── students.db                    # sumber data dashboard (SQLite, tabel `students`)
├── data.csv                       # dataset asli (pemisah `;`)
├── data_dashboard.csv             # dataset berlabel + kolom dropout_risk_score
├── train_model.py                 # script training & evaluasi model
├── prepare_dashboard_data.py      # data.csv -> data_dashboard.csv
├── load_dashboard_db.py           # data_dashboard.csv -> students.db
├── metabase_setup.py              # otomatisasi pembuatan question & dashboard via API
├── validate_submission.py         # pengecekan kelengkapan berkas submission
├── video_script.md                # naskah video presentasi
├── emilia_loho-dashboard.png      # screenshot dashboard Metabase
├── emilia_loho-video.mp4          # video penjelasan (3:56, subtitle ter-burn)
└── emilia_loho-video.srt          # berkas subtitle terpisah
```

## Business Dashboard

Dashboard dibuat menggunakan **Metabase** (via Docker) dengan sumber data `data_dashboard.csv` yang telah diperkaya label kategori yang mudah dibaca serta kolom `dropout_risk_score` dari model.

Dashboard **"Jaya Jaya Institut — Student Monitoring"** menampilkan:

1. **KPI utama** — total siswa, jumlah & persentase dropout, rata-rata skor risiko siswa aktif (Enrolled).
2. **Distribusi status siswa** (Dropout / Enrolled / Graduate).
3. **Dropout rate per program studi** — memperlihatkan konsentrasi dropout di Biofuel Production Tech (67%), Equinculture (55%), Informatics Engineering (54%).
4. **Dropout rate berdasarkan faktor finansial** — status pembayaran (menunggak = 86,6% dropout), beasiswa, dan debtor.
5. **Dropout rate per kelompok usia dan gender**.
6. **Perbandingan performa akademik** (rata-rata SKS lulus semester 1–2) antar status.
7. **Distribusi skor risiko** siswa Enrolled — daftar siswa aktif berisiko tinggi (skor > 0,6) untuk diprioritaskan bimbingan.

**Akses Metabase (lokal):**

| Item | Nilai |
|---|---|
| URL | `http://localhost:3004/dashboard/2` |
| Email | `root@mail.com` |
| Password | `root123` |

> Jika port `3004` sudah terpakai di mesin Anda, jalankan container dengan
> `-p <port lain>:3000` lalu akses melalui `http://localhost:3004`. Kredensial di atas
> sudah tersimpan di dalam `metabase.db.mv.db`, sehingga reviewer dapat langsung
> login tanpa setup ulang.

Sumber data dashboard dimuat ke SQLite (`students.db`, tabel `students`) karena
Metabase tidak dapat membaca CSV secara langsung:

```bash
python load_dashboard_db.py        # data_dashboard.csv -> students.db
```

Cara menjalankan Metabase beserta file dashboard yang sudah diekspor:

```bash
docker run -d -p 3004:3000 --name metabase4 \
  -v $(pwd)/metabase.db.mv.db:/metabase.db/metabase.db.mv.db \
  -v $(pwd)/students.db:/data/students.db \
  metabase/metabase
```

Panduan lengkap membangun ulang dashboard dari nol (termasuk SQL setiap
question) ada di **`METABASE_SETUP.md`**.

Screenshot dashboard tersedia pada berkas `emilia_loho-dashboard.png`.

## Menjalankan Sistem Machine Learning

Prototype sistem machine learning dibuat dengan Streamlit. Pengguna mengisi data siswa (akademik, finansial, demografi), lalu sistem menampilkan **probabilitas dropout** beserta kategori risiko (rendah / sedang / tinggi) dan rekomendasi tindak lanjut.

**Menjalankan secara lokal:**

```bash
streamlit run app.py
```

**Akses prototype (Streamlit Community Cloud):**

🔗 **[https://emilia-loho-jaya-jaya-institut.streamlit.app](https://emilia-loho-jaya-jaya-institut.streamlit.app)**

Repository: [github.com/emilialoho/jaya-jaya-institut-dropout](https://github.com/emilialoho/jaya-jaya-institut-dropout)

> Langkah deploy (push ke GitHub → Streamlit Community Cloud) dijelaskan
> tahap demi tahap pada **`DEPLOYMENT.md`**. Nama aplikasi yang dipakai saat
> deploy harus `emilia-loho-jaya-jaya-institut` agar cocok dengan link di atas.

Cara memakai: isi data siswa pada tab **Akademik / Finansial / Demografi**,
lalu tekan **Prediksi Risiko Dropout**. Contoh kasus risiko tinggi — tunggakan
biaya `Yes`, biaya kuliah lancar `No`, SKS lulus semester 1–2 = 1, nilai 6–7 →
probabilitas dropout **100,0 % (🔴 RISIKO TINGGI)**.

Model yang digunakan: **Logistic Regression** (pipeline dengan StandardScaler), dipilih setelah dibandingkan dengan Random Forest melalui 5-fold cross-validation.

| Metrik (test set) | Nilai |
|---|---|
| Accuracy | 94,2% |
| Precision | 93,2% |
| Recall | 91,9% |
| F1-score | 92,6% |
| ROC-AUC | 0,973 |

## Video Penjelasan

Video penjelasan tersedia pada berkas **`emilia_loho-video.mp4`** — durasi **3 menit 56 detik**
(batas maksimal 5 menit).

Video ini **tidak memiliki audio**; seluruh penjelasan disampaikan melalui **teks
subtitle (caption) yang sudah di-burn ke dalam video**, sehingga dapat langsung
dibaca tanpa mengaktifkan pengaturan apa pun. Berkas subtitle terpisah juga
disertakan pada `emilia_loho-video.srt` bila reviewer ingin membacanya sebagai teks.

Struktur video mengikuti tiga poin yang diminta:

| Waktu | Bagian | Isi |
|---|---|---|
| 0:00 – 0:22 | Pembuka & permasalahan | Identitas, konteks Jaya Jaya Institut, 3 permasalahan bisnis |
| 0:22 – 1:13 | **Solusi machine learning** | Perbandingan Logistic Regression vs Random Forest, metrik evaluasi, feature importance, dan cara kerja prototype Streamlit |
| 1:13 – 3:01 | **Dashboard** | Penjelasan dashboard Metabase + rekaman layar seluruh 14 visualisasi beserta insight-nya |
| 3:01 – 3:56 | **Kesimpulan & action items** | 5 poin kesimpulan dan 6 rekomendasi action items |

Naskah lengkapnya ada pada `video_script.md`.

## Conclusion

1. Tingkat dropout Jaya Jaya Institut mencapai **32,1%** — hampir 1 dari 3 siswa tidak menyelesaikan pendidikannya.
2. Faktor terkuat yang memengaruhi dropout adalah **performa akademik semester awal** (jumlah SKS lulus dan nilai semester 1–2 — siswa dropout rata-rata hanya lulus 1,9 SKS di semester 2 vs 6,2 SKS pada graduate) dan **faktor finansial**: siswa yang menunggak biaya kuliah dropout **86,6%** vs 24,7% yang lancar, debtor dropout 62%, sedangkan penerima beasiswa hanya 12,2%.
3. Faktor demografi juga berpengaruh: siswa laki-laki (45,1% vs 25,1%) dan siswa yang mendaftar pada usia **25+ tahun** (>51%) lebih berisiko, serta dropout terkonsentrasi pada program studi tertentu.
4. Model **Logistic Regression** mampu memprediksi dropout dengan accuracy 94,2%, recall 91,9%, dan ROC-AUC 0,973 — recall tinggi berarti ±92 dari 100 siswa yang benar-benar berisiko berhasil terdeteksi sejak dini.
5. Dengan kombinasi model prediksi (deteksi dini) dan dashboard monitoring, Jaya Jaya Institut dapat beralih dari penanganan **reaktif** menjadi **proaktif** — siswa berisiko teridentifikasi sejak semester 1–2, sebelum benar-benar berhenti.

### Fitur Paling Berpengaruh terhadap Prediksi Model

Berdasarkan analisis *feature importance*, berikut fitur-fitur dengan kontribusi terbesar dalam memprediksi dropout:

| Peringkat | Fitur | Importance | Interpretasi |
|---|---|---|---|
| 1 | `Curricular_units_2nd_sem_approved` | 0,226 | Semakin sedikit SKS yang lulus di semester 2, semakin tinggi risiko dropout — prediktor tunggal terkuat. |
| 2 | `Curricular_units_1st_sem_approved` | 0,144 | Jumlah SKS lulus semester 1; risiko sudah terbaca sejak semester pertama. |
| 3 | `Curricular_units_2nd_sem_grade` | 0,127 | Rata-rata nilai semester 2 yang rendah menandakan siswa kesulitan mengikuti perkuliahan. |
| 4 | `Curricular_units_1st_sem_grade` | 0,068 | Rata-rata nilai semester 1. |
| 5 | `Tuition_fees_up_to_date` | 0,052 | Ketepatan pembayaran biaya kuliah — faktor non-akademik terkuat; siswa yang menunggak jauh lebih berisiko dropout. |
| 6 | `Age_at_enrollment` | 0,030 | Semakin tua usia saat mendaftar, semakin tinggi risiko (umumnya bekerja sambil kuliah). |
| 7 | `Scholarship_holder` | 0,026 | Penerima beasiswa jauh lebih jarang dropout. |
| 8 | `Admission_grade` | 0,026 | Nilai masuk yang rendah berkontribusi pada risiko. |

Secara ringkas, **performa akademik dua semester pertama** (SKS lulus dan nilai) mendominasi prediksi model, diikuti **kondisi finansial** (status pembayaran dan beasiswa) serta **usia saat mendaftar**. Hal ini konsisten dengan temuan EDA dan menjadi dasar rekomendasi action items di bawah.

## Rekomendasi Action Items

1. **Bangun early-warning system berbasis model** — jalankan skor risiko untuk seluruh siswa aktif setiap akhir semester; siswa dengan skor > 0,6 otomatis masuk daftar prioritas bimbingan khusus (academic advising + konseling).
2. **Intervensi finansial proaktif** — hubungi siswa yang mulai menunggak biaya kuliah sebelum tunggakan menumpuk (kelompok ini dropout 86,6%); tawarkan skema cicilan dan perluas program beasiswa, karena penerima beasiswa dropout 3× lebih jarang.
3. **Program remedial semester awal** — wajibkan academic advising dan kelas remedial bagi siswa yang lulus < 3 SKS pada semester 1, karena SKS lulus semester 1–2 adalah prediktor dropout terkuat.
4. **Audit program studi berisiko tinggi** — evaluasi kurikulum, beban studi, dan dukungan pengajaran pada program dengan dropout > 45% (Biofuel Production Tech, Equinculture, Informatics Engineering, Management kelas malam).
5. **Dukungan untuk siswa dewasa dan kelas malam** — sediakan jadwal fleksibel, kelas hybrid, dan layanan konseling khusus bagi siswa usia 25+ yang umumnya bekerja sambil kuliah.
6. **Monitoring rutin melalui dashboard Metabase** — tinjau KPI dropout rate per program studi, status pembayaran, dan distribusi skor risiko setiap bulan pada rapat manajemen akademik.
