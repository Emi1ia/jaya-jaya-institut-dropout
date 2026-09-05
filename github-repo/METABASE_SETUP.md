# Metabase Dashboard — Setup Guide

Panduan membuat dashboard **"Jaya Jaya Institut — Student Monitoring"**.
Semua langkah sudah diotomatisasi; kamu hanya perlu Docker.

---

## 0. Prasyarat

Pasang **Docker Desktop for Windows**:

```powershell
winget install -e --id Docker.DockerDesktop
```

Jalankan Docker Desktop dan tunggu ikon whale-nya hijau (`Engine running`),
lalu verifikasi:

```powershell
docker version
```

> **Catatan port.** Di mesin ini port `3000` sudah dipakai Grafana, sehingga
> Metabase dijalankan di port **3030** (`-p 3030:3000`) dan script dipanggil
> dengan `MB_HOST=http://localhost:3030`. Kalau port 3000 kamu bebas, pakai
> `-p 3000:3000` dan `MB_HOST` tidak perlu diisi.

---

## 1. Siapkan sumber data

Metabase tidak bisa membaca CSV langsung, jadi `data_dashboard.csv` di-load ke
sebuah database SQLite bernama `students.db` (tabel `students`, 4.424 baris).

```powershell
.\.venv\Scripts\python.exe load_dashboard_db.py
```

> SQLite dipilih (bukan Postgres) karena filenya bisa langsung di-mount ke
> dalam container Metabase — tidak perlu container kedua, tidak perlu
> `sqlalchemy`/`psycopg2`. File `students.db` sudah dibuat dan diverifikasi.

---

## 2. Jalankan Metabase dengan database ter-mount

Jalankan dari dalam folder `submission/`:

```powershell
docker run -d -p 3000:3000 --name metabase `
  -v "${PWD}\students.db:/data/students.db" `
  metabase/metabase
```

Bash/Git Bash:

```bash
docker run -d -p 3000:3000 --name metabase \
  -v "$(pwd)/students.db:/data/students.db" \
  metabase/metabase
```

Tunggu sampai siap (butuh ±1–3 menit pada run pertama):

```powershell
docker logs -f metabase
```

Berhenti menunggu ketika muncul baris **`Metabase Initialization COMPLETE`**
(tekan `Ctrl+C` untuk keluar dari log).

---

## 3. Bangun dashboard secara otomatis

```powershell
.\.venv\Scripts\python.exe metabase_setup.py
# kalau Metabase jalan di port lain:
$env:MB_HOST = "http://localhost:3030"; .\.venv\Scripts\python.exe metabase_setup.py
```

Script ini (via Metabase API, stdlib saja) akan:

1. Membuat akun admin `root@mail.com` / `root123` — kalau Metabase belum
   pernah di-setup. Kalau sudah, dia cukup login.
2. Menambahkan database SQLite `Jaya Jaya Institut` → `/data/students.db`
   dan menunggu sync schema selesai.
3. Membuat **14 question** (lihat daftar di bawah).
4. Membuat dashboard **"Jaya Jaya Institut - Student Monitoring"** dan menata
   semua kartu pada grid 24 kolom.

Script bersifat **idempotent** — aman dijalankan ulang.

Di akhir, script mencetak URL dashboard, misalnya
`http://localhost:3000/dashboard/1`.

---

## Daftar question yang dibuat

| # | Question | Visualisasi |
|---|---|---|
| 1 | Total Siswa | Scalar (4.424) |
| 2 | Jumlah Dropout | Scalar (1.421) |
| 3 | Persentase Dropout | Scalar (32,1 %) |
| 4 | Rata-rata Skor Risiko — Siswa Enrolled | Scalar (0,485) |
| 5 | Distribusi Status Siswa | Pie |
| 6 | Dropout Rate per Program Studi (urut menurun) | Row chart |
| 7 | Dropout Rate per Status Pembayaran | Bar (No 86,6 % vs Yes 24,7 %) |
| 8 | Dropout Rate per Status Beasiswa | Bar (No 38,7 % vs Yes 12,2 %) |
| 9 | Dropout Rate per Status Debtor | Bar (Yes 62,0 % vs No 28,3 %) |
| 10 | Dropout Rate per Kelompok Usia | Bar (17-20 … 40+) |
| 11 | Dropout Rate per Gender | Bar (Male 45,1 % vs Female 25,1 %) |
| 12 | Rata-rata SKS Lulus Semester 1–2 per Status | Bar (2 seri) |
| 13 | Distribusi Skor Risiko — Siswa Enrolled | Bar / histogram (bin 0,1) |
| 14 | Siswa Enrolled Berisiko Tinggi (skor > 0,6) | Table (304 siswa) |

Seluruh SQL sudah diuji langsung terhadap `students.db` dan angkanya konsisten
dengan yang ditulis di `README.md`.

---

## 4. Membuat question secara manual (kalau mau klik-per-klik)

Kalau ingin membuatnya sendiri lewat UI: **+ New → SQL query → pilih database
"Jaya Jaya Institut"**, tempel SQL berikut, lalu pilih tipe visualisasi di kiri
bawah dan **Save**.

<details>
<summary>SQL untuk tiap question</summary>

```sql
-- 1. Total Siswa  (Scalar)
SELECT COUNT(*) AS total_siswa FROM students;

-- 2. Jumlah Dropout  (Scalar)
SELECT SUM(is_dropout) AS jumlah_dropout FROM students;

-- 3. Persentase Dropout  (Scalar)
SELECT ROUND(AVG(is_dropout) * 100, 1) AS dropout_rate_pct FROM students;

-- 4. Rata-rata skor risiko siswa Enrolled  (Scalar)
SELECT ROUND(AVG(dropout_risk_score), 3) AS avg_risk_score
FROM students WHERE status = 'Enrolled';

-- 5. Distribusi status siswa  (Pie)
SELECT status AS label, COUNT(*) AS jumlah_siswa
FROM students GROUP BY status ORDER BY jumlah_siswa DESC;

-- 6. Dropout rate per program studi  (Row chart)
SELECT course AS label, COUNT(*) AS jumlah_siswa,
       ROUND(AVG(is_dropout) * 100, 1) AS dropout_rate_pct
FROM students GROUP BY course ORDER BY dropout_rate_pct DESC;

-- 7/8/9. Dropout rate per faktor finansial  (Bar)
--   ganti `tuition_up_to_date` dengan `scholarship_holder` atau `debtor`
SELECT tuition_up_to_date AS label, COUNT(*) AS jumlah_siswa,
       ROUND(AVG(is_dropout) * 100, 1) AS dropout_rate_pct
FROM students GROUP BY tuition_up_to_date ORDER BY dropout_rate_pct DESC;

-- 10. Dropout rate per kelompok usia  (Bar)
SELECT age_group AS label, COUNT(*) AS jumlah_siswa,
       ROUND(AVG(is_dropout) * 100, 1) AS dropout_rate_pct
FROM students GROUP BY age_group ORDER BY label;

-- 11. Dropout rate per gender  (Bar)
SELECT gender AS label, COUNT(*) AS jumlah_siswa,
       ROUND(AVG(is_dropout) * 100, 1) AS dropout_rate_pct
FROM students GROUP BY gender ORDER BY dropout_rate_pct DESC;

-- 12. Rata-rata SKS lulus semester 1-2 per status  (Bar, 2 seri)
SELECT status AS label,
       ROUND(AVG(units_2nd_sem_approved), 2) AS avg_units_2nd_sem_approved,
       ROUND(AVG(units_1st_sem_approved), 2) AS avg_units_1st_sem_approved
FROM students GROUP BY status ORDER BY avg_units_2nd_sem_approved DESC;

-- 13. Histogram skor risiko siswa Enrolled  (Bar)
SELECT CAST(dropout_risk_score * 10 AS INT) / 10.0 AS risk_bucket,
       COUNT(*) AS jumlah_siswa
FROM students WHERE status = 'Enrolled'
GROUP BY risk_bucket ORDER BY risk_bucket;

-- 14. Siswa Enrolled berisiko tinggi  (Table)
SELECT course, gender, age_group, tuition_up_to_date, debtor,
       scholarship_holder, units_1st_sem_approved, units_2nd_sem_approved,
       grade_2nd_sem, dropout_risk_score
FROM students
WHERE status = 'Enrolled' AND dropout_risk_score > 0.6
ORDER BY dropout_risk_score DESC;
```

</details>

---

## 5. Screenshot & export untuk submission

1. Buka dashboard, atur zoom browser ke ±67–80 % agar seluruh kartu terlihat,
   lalu screenshot dan simpan sebagai **`emilia_loho-dashboard.png`** di
   folder `submission/`.

2. Export database internal Metabase (berisi definisi dashboard):

   ```powershell
   docker cp metabase:/metabase.db/metabase.db.mv.db ./
   ```

   > Kalau file terkunci, hentikan container dulu: `docker stop metabase`,
   > jalankan `docker cp`, lalu `docker start metabase`.

---

## 6. Reviewer menjalankan ulang dashboard

Dengan `metabase.db.mv.db` dan `students.db` di folder yang sama:

```bash
docker run -d -p 3000:3000 --name metabase \
  -v "$(pwd)/metabase.db.mv.db:/metabase.db/metabase.db.mv.db" \
  -v "$(pwd)/students.db:/data/students.db" \
  metabase/metabase
```

Login: `root@mail.com` / `root123`.
