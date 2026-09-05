# Checklist Sebelum Submit

**Emilia Loho · lohoemilia@gmail.com · ID Dicoding: emilia_loho**

## Status kelima kriteria

| # | Kriteria | Status | Bukti |
|---|---|---|---|
| 1 | Menggunakan templat proyek yang disediakan | ✅ Selesai | `README.md` mengikuti struktur templat: Business Understanding → Permasalahan Bisnis → Cakupan Proyek → Persiapan → Business Dashboard → Menjalankan Sistem ML → Conclusion → Rekomendasi Action Items |
| 2 | Seluruh proses data science + deployment | ✅ Selesai | `notebook.ipynb` (14 cell kode, semua tereksekusi, tanpa error) mencakup business understanding hingga evaluation. Conclusion ada di README dan notebook. **Deployment butuh 1 langkah manual — lihat di bawah.** |
| 3 | Minimal satu dashboard | ✅ Selesai | Metabase, 14 visualisasi (KPI, pie, bar, row, histogram, tabel). Export `metabase.db.mv.db` + screenshot `emilia_loho-dashboard.png`. Login `root@mail.com` / `root123` tercantum di README |
| 4 | Solusi ML siap pakai (Streamlit) | ⚠️ **1 langkah manual** | `app.py` selesai dan teruji. **Deploy ke Streamlit Community Cloud harus Anda lakukan sendiri** — panduan di `DEPLOYMENT.md` |
| 5 | Rekomendasi action items | ✅ Selesai | 6 action items di `README.md`, juga ditampilkan di video menit 3:25 |

### Saran tambahan (opsional) yang sudah dipenuhi

| Saran | Status |
|---|---|
| Video maksimal 5 menit menjelaskan solusi ML, dashboard, dan kesimpulan | ✅ `emilia_loho-video.mp4` — 3 menit 56 detik, subtitle ter-burn |
| Dokumentasi tiap tahapan lewat text cell di notebook | ✅ 14 sel markdown berisi penjelasan dan insight tiap tahap |
| Visualisasi data yang baik dan efektif | ✅ Palet OCEAN konsisten, colourblind-safe, label nilai di setiap bar |
| Prototype dengan UI yang bagus dan mudah dipakai | ✅ Tab Akademik / Finansial / Demografi, kartu metrik, indikator risiko berwarna |

---

## ⚠️ Yang masih harus Anda kerjakan sendiri

**Deploy prototype ke Streamlit Community Cloud.** Langkah ini butuh akun GitHub
dan akun Streamlit milik Anda, jadi tidak bisa dikerjakan lebih dulu.

1. Buka **`DEPLOYMENT.md`** dan ikuti langkah 1–6 (sekitar 5–10 menit).
2. Saat mengisi **App URL**, gunakan persis `emilia-loho-jaya-jaya-institut`
   supaya cocok dengan link yang sudah ditulis di `README.md`.
3. Kalau Anda memakai nama lain, ubah link di `README.md` bagian
   "Menjalankan Sistem Machine Learning".
4. Jalankan `python validate_submission.py` sekali lagi untuk konfirmasi.

---

## Verifikasi terakhir sebelum upload

```bash
python validate_submission.py     # harus: 0 blocking issue(s)
```

- [ ] Prototype sudah ter-deploy dan link-nya bisa dibuka di browser
- [ ] Link Streamlit di `README.md` sesuai dengan aplikasi yang benar-benar hidup
- [ ] Buka sekali lagi link Streamlit sesaat sebelum submit (aplikasi gratis
      bisa "tidur" kalau lama tidak diakses)
- [ ] Video `emilia_loho-video.mp4` bisa diputar dan subtitle-nya terbaca
- [ ] Folder yang di-zip **tidak** berisi `.venv/`

## Isi berkas submission

| Berkas | Keterangan |
|---|---|
| `README.md` | Dokumentasi utama — kriteria 1, 2, 5 |
| `notebook.ipynb` | Seluruh proses data science, sudah dieksekusi |
| `app.py` + `model/` | Prototype Streamlit dan artefak model |
| `requirements.txt` | Dependency terpin sesuai versi saat training |
| `metabase.db.mv.db` | Export instance Metabase berisi dashboard |
| `emilia_loho-dashboard.png` | Screenshot dashboard |
| `emilia_loho-video.mp4` | Video penjelasan 3:56 dengan subtitle |
| `emilia_loho-video.srt` | Subtitle terpisah |
| `students.db`, `data.csv`, `data_dashboard.csv` | Data sumber |
| `DEPLOYMENT.md` | Panduan deploy Streamlit |
| `METABASE_SETUP.md`, `DASHBOARD_VARIANT.md` | Panduan membangun ulang dashboard |
| `video_script.md` | Transkrip lengkap video |
| `validate_submission.py` | Pengecekan otomatis kelengkapan submission |
