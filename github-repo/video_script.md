# Naskah / Transkrip Video — `emilia_loho-video.mp4`

Durasi **3 menit 56 detik** (batas maksimal 5 menit). Video **tanpa audio** —
seluruh naskah di bawah ini tampil sebagai **subtitle yang sudah di-burn**
ke dalam video, jadi bisa langsung dibaca tanpa mengaktifkan apa pun.
Salinan terpisah dalam format SubRip ada di `emilia_loho-video.srt`.

## Cakupan poin yang diminta reviewer

| Poin yang diminta | Tercakup pada |
|---|---|
| Menjelaskan solusi machine learning yang digunakan | 0:22 – 1:13 (perbandingan model, metrik evaluasi, feature importance, prototype Streamlit) |
| Menjelaskan dashboard yang telah dibuat | 1:13 – 3:01 (pengantar + rekaman layar 14 visualisasi beserta insight) |
| Menjelaskan kesimpulan / conclusion | 3:01 – 3:49 (5 poin kesimpulan) dan 3:25 – 3:49 (6 action items) |

## Struktur video

| Waktu | Bagian | Tampilan |
|---|---|---|
| 0:00 – 0:07 | Pembuka | Slide judul |
| 0:07 – 0:22 | Permasalahan bisnis | Slide: Permasalahan Bisnis |
| 0:22 – 0:38 | Solusi ML — perbandingan model | Slide: Perbandingan Model |
| 0:38 – 0:55 | Solusi ML — evaluasi & feature importance | Slide: Hasil Model |
| 0:55 – 1:13 | Solusi ML — prototype Streamlit | Slide: Prototype Streamlit |
| 1:13 – 1:25 | Dashboard — pengantar | Slide: Metabase Student Monitoring |
| 1:25 – 3:01 | Dashboard — rekaman layar | Rekaman layar Metabase (OCEAN) |
| 3:01 – 3:25 | Kesimpulan | Slide: Kesimpulan Proyek |
| 3:25 – 3:49 | Action items | Slide: Action Items |
| 3:49 – 3:56 | Penutup | Slide: Terima kasih |

## Transkrip lengkap

### 0:00 – 0:07 · Pembuka

- **0:00** — Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan — Jaya Jaya Institut.
- **0:03** — Oleh Emilia Loho, ID Dicoding emilia_loho.

### 0:07 – 0:22 · Permasalahan bisnis

- **0:07** — Jaya Jaya Institut punya 4.424 data siswa, dan 1.421 di antaranya dropout.
- **0:11** — Tingkat dropout mencapai 32,1 persen — hampir satu dari tiga siswa.
- **0:14** — Masalahnya: penyebab dropout belum diketahui, dan belum ada mekanisme deteksi dini.
- **0:18** — Manajemen juga belum punya dashboard untuk memantau performa siswa.

### 0:22 – 0:38 · Solusi ML — perbandingan model

- **0:22** — Solusi machine learning-nya dimulai dengan membandingkan dua algoritma.
- **0:26** — Logistic Regression dan Random Forest diuji dengan 5-fold cross-validation.
- **0:30** — Logistic Regression menang di seluruh metrik: accuracy 94,2 persen, ROC-AUC 0,973.
- **0:34** — Model ini juga ringan dan koefisiennya mudah dijelaskan ke pihak akademik.

### 0:38 – 0:55 · Solusi ML — evaluasi & feature importance

- **0:38** — Pada test set, model mencapai recall 91,9 persen.
- **0:42** — Artinya sekitar 92 dari 100 siswa yang benar-benar berisiko berhasil terdeteksi sejak dini.
- **0:46** — Faktor paling berpengaruh adalah jumlah SKS yang lulus di semester dua dan semester satu.
- **0:51** — Disusul nilai semester, status pembayaran biaya kuliah, dan usia saat mendaftar.

### 0:55 – 1:13 · Solusi ML — prototype Streamlit

- **0:55** — Model dikemas jadi prototype Streamlit yang sudah di-deploy ke cloud.
- **0:59** — Petugas akademik mengisi data siswa lewat tab Akademik, Finansial, dan Demografi.
- **1:03** — Model menghitung probabilitas dropout, lalu menampilkan kategori risikonya.
- **1:07** — Contoh: siswa menunggak dengan 1 SKS lulus mendapat skor 99,8 persen — risiko tinggi.

### 1:13 – 1:25 · Dashboard — pengantar

- **1:13** — Solusi kedua adalah business dashboard yang dibangun di Metabase.
- **1:17** — Berisi 14 visualisasi: kartu KPI, pie chart, bar chart, histogram, dan tabel prioritas.
- **1:21** — Login memakai root@mail.com dengan password root123.

### 1:25 – 3:01 · Dashboard — rekaman layar

- **1:25** — Ini dashboard Student Monitoring yang sudah jadi.
- **1:30** — Empat KPI utama di baris atas: total siswa 4.424, dropout 1.421, atau 32,1 persen.
- **1:35** — KPI keempat adalah rata-rata skor risiko siswa yang masih aktif, yaitu 0,49.
- **1:40** — Pie chart menunjukkan komposisi status siswa: Graduate, Dropout, dan Enrolled.
- **1:45** — Di sebelahnya, rata-rata SKS lulus semester 1 dan 2 dibandingkan antar status.
- **1:51** — Siswa Graduate lulus sekitar 6 SKS, sedangkan siswa Dropout hanya sekitar 2 SKS.
- **1:56** — Baris berikutnya: dropout rate berdasarkan faktor finansial.
- **2:01** — Siswa yang menunggak biaya kuliah dropout-nya 86,6 persen, versus 24,7 persen.
- **2:06** — Penerima beasiswa jauh lebih aman: hanya 12,2 persen, versus 38,7 persen.
- **2:10** — Siswa berstatus debtor dropout 62 persen, dibanding 28,3 persen yang bukan debtor.
- **2:14** — Faktor demografi: dropout naik tajam pada kelompok usia 25 tahun ke atas.
- **2:17** — Siswa laki-laki dropout 45,1 persen, hampir dua kali lipat siswa perempuan.
- **2:20** — Chart besar ini menampilkan dropout rate per program studi, diurutkan dari tertinggi.
- **2:24** — Tertinggi Biofuel Production Tech 66,7 persen, lalu Equinculture 55,3 persen.
- **2:29** — Informatics Engineering 54,1 persen, sedangkan Nursing hanya 15,4 persen.
- **2:33** — Di bawahnya, distribusi skor risiko untuk siswa yang masih aktif.
- **2:38** — Terlihat banyak siswa aktif menumpuk di skor risiko tinggi, mendekati 1.
- **2:43** — Tabel terakhir memuat 304 siswa aktif dengan skor risiko di atas 0,6.
- **2:49** — Lengkap dengan program studi, gender, usia, status pembayaran, dan SKS yang lulus.
- **2:55** — Dari daftar inilah tim akademik bisa langsung menindaklanjuti siswa satu per satu.

### 3:01 – 3:25 · Kesimpulan

- **3:01** — Kesimpulannya. Tingkat dropout Jaya Jaya Institut mencapai 32,1 persen.
- **3:05** — Prediktor terkuat adalah performa akademik dua semester pertama.
- **3:10** — Siswa dropout rata-rata hanya lulus 1,9 SKS di semester dua, versus 6,2 SKS pada graduate.
- **3:15** — Faktor finansial menyusul: menunggak biaya kuliah berujung dropout pada 86,6 persen kasus.
- **3:20** — Dengan model dan dashboard ini, institusi bisa beralih dari reaktif menjadi proaktif.

### 3:25 – 3:49 · Action items

- **3:25** — Rekomendasi action items. Pertama, bangun early-warning system.
- **3:29** — Jalankan skor risiko tiap akhir semester; skor di atas 0,6 masuk prioritas bimbingan.
- **3:34** — Kedua, intervensi finansial proaktif — hubungi siswa sebelum tunggakan menumpuk.
- **3:38** — Ketiga, program remedial untuk siswa yang lulus kurang dari 3 SKS di semester satu.
- **3:42** — Keempat, audit program studi dengan dropout di atas 45 persen.
- **3:46** — Kelima dan keenam, dukungan siswa dewasa dan monitoring rutin lewat dashboard.

### 3:49 – 3:56 · Penutup

- **3:49** — Dengan deteksi dini sejak semester satu, bimbingan bisa diberikan sebelum siswa berhenti.
- **3:53** — Terima kasih.

## Cara memproduksi ulang video ini

Berkas pendukung ada di luar folder submission, tapi alurnya:

1. Slide dibuat dengan Pillow (9 slide, palet OCEAN yang sama dengan dashboard).
2. Setiap slide dirender jadi segmen video 1760x1076 @ 30fps dengan ffmpeg.
3. Rekaman layar dashboard di-scale ke resolusi yang sama lalu digabung
   dengan `concat` demuxer.
4. Subtitle (`.ass`, gaya kotak semi-transparan seperti YouTube) di-burn
   memakai filter `subtitles` milik ffmpeg.
