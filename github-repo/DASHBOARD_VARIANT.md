# Dashboard — OCEAN

Membangun dashboard **"Jaya Jaya Institut — Student Monitoring"** di Metabase
lewat Metabase API. Isi analitiknya (14 question, SQL, angka) **identik**
dengan varian `dashboard_sunset/` dan `dashboard_berry/`; yang berbeda hanya
palet warna, tata letak kartu, dan **cara kode di dalam `metabase_setup.py`
disusun**.

| Item | Nilai |
|---|---|
| Port Metabase | `3004` |
| Container | `metabase4` |
| URL dashboard | http://localhost:3004/dashboard/2 |
| Login | `root@mail.com` / `root123` |

## Desain

Palet **ocean** — biru dingin + teal, coral khusus untuk slice Dropout.

| Peran | Hex | Dipakai untuk |
|---|---|---|
| `RATE` (primer) | `#3D8FC7` | semua seri `dropout_rate_pct` |
| `SECONDARY` | `#2EA98C` | jumlah siswa / seri kedua |
| `DANGER` | `#E4643B` | slice Dropout pada pie |

Urutan baca dashboard: **angka utama → komposisi → faktor finansial →
demografi → program studi → monitoring risiko.**

## Struktur kode `metabase_setup.py`

Ditulis sebagai **linear step pipeline**. Seluruh state satu run disimpan di
satu dict `STATE`; tiap tahap adalah fungsi `step_*` yang membaca/menulis dict
itu, dan `PIPELINE` di bagian bawah mendaftar urutan eksekusinya.

```
1. settings    hosts, kredensial, nama
2. palette     warna OCEAN
3. sql         SQL{} per kartu + helper rate_by()
4. presets     blok visualization_settings yang dipakai ulang
5. blueprint   CARDS: daftar kartu berurutan
6. transport   pembungkus urllib tipis di atas Metabase API
7. steps       step_wait / step_admin / step_database / step_sync /
               step_cards / step_dashboard / step_report
8. pipeline    PIPELINE + main()
```

Menambah tahap = menulis satu fungsi `step_*` dan menambah satu nama ke
`PIPELINE`.

## Cara menjalankan

Prasyarat: `students.db` sudah ada di folder induk (`python load_dashboard_db.py`).

```bash
# 1. jalankan Metabase dengan students.db ter-mount
docker run -d -p 3004:3000 --name metabase4 \
  -v "$(pwd)/../students.db:/data/students.db" \
  metabase/metabase

# 2. tunggu sampai "Metabase Initialization COMPLETE"
docker logs -f metabase4

# 3. bangun dashboard
python metabase_setup.py
```

Metabase di port lain:

```bash
MB_HOST=http://localhost:3999 python metabase_setup.py
```

Script **idempotent** — akun admin hanya dibuat pada instance baru, koneksi
database dipakai ulang, dan kartu/dashboard hasil run sebelumnya diperbarui
di tempat.

## Question yang dibuat (14)

| # | Question | Visualisasi | Ukuran (kolom × baris) |
|---|---|---|---|
| 1 | Total Siswa | scalar | 6 × 3 |
| 2 | Jumlah Dropout | scalar | 6 × 3 |
| 3 | Persentase Dropout | scalar | 6 × 3 |
| 4 | Rata-rata Skor Risiko — Siswa Enrolled | scalar | 6 × 3 |
| 5 | Distribusi Status Siswa | pie | 12 × 6 |
| 6 | Rata-rata SKS Lulus Semester 1–2 per Status | bar (2 seri) | 12 × 6 |
| 7 | Dropout Rate per Status Pembayaran | bar | 8 × 5 |
| 8 | Dropout Rate per Status Beasiswa | bar | 8 × 5 |
| 9 | Dropout Rate per Status Debtor | bar | 8 × 5 |
| 10 | Dropout Rate per Kelompok Usia | bar | 12 × 5 |
| 11 | Dropout Rate per Gender | bar | 12 × 5 |
| 12 | Dropout Rate per Program Studi | row | 24 × 15 |
| 13 | Distribusi Skor Risiko — Siswa Enrolled | bar | 24 × 6 |
| 14 | Siswa Enrolled Berisiko Tinggi (skor > 0,6) | table | 24 × 8 |

## Screenshot & export

```bash
docker cp metabase4:/metabase.db/metabase.db.mv.db ./
```

Kalau file terkunci: `docker stop metabase4`, jalankan `docker cp`, lalu
`docker start metabase4`.
