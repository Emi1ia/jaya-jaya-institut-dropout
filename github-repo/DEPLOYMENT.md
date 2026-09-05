# Deploy Prototype ke Streamlit Community Cloud

Ini satu-satunya langkah yang harus dikerjakan sendiri, karena butuh akun
GitHub dan akun Streamlit milik Anda. Perkiraan waktu: **5–10 menit**.

> **PENTING — nama aplikasi**
> README.md sudah menuliskan link berikut sebagai alamat prototype:
>
> ```
> https://emilia-loho-jaya-jaya-institut.streamlit.app
> ```
>
> Agar dokumentasi dan aplikasi cocok, isi kolom **App URL** di Streamlit
> dengan `emilia-loho-jaya-jaya-institut` (langkah 4 di bawah).
> Kalau Anda memilih nama lain, **ubah juga link di `README.md`** —
> ada di bagian "Menjalankan Sistem Machine Learning". Jalankan
> `python validate_submission.py` untuk memastikan link terisi.

---

## 1. Buat repository GitHub

Buat repository **public** bernama `jaya-jaya-institut-dropout`
(repository private tidak bisa dipakai di Streamlit Community Cloud tier gratis).

## 2. Upload berkas yang dibutuhkan

Aplikasi hanya butuh empat hal ini agar bisa jalan di cloud:

```
app.py
requirements.txt
model/model.joblib
model/metadata.json
model/feature_defaults.json
```

Silakan ikut sertakan berkas lain (notebook, README, dsb.) supaya reviewer bisa
melihat keseluruhan proyek — tapi **jangan** meng-upload `.venv/`.

Lewat terminal:

```bash
cd submission
git init
git add app.py requirements.txt model/ README.md notebook.ipynb \
        train_model.py prepare_dashboard_data.py .gitignore
git commit -m "Jaya Jaya Institut - dropout early warning system"
git branch -M main
git remote add origin https://github.com/<username-github-anda>/jaya-jaya-institut-dropout.git
git push -u origin main
```

Atau cukup pakai tombol **Add file → Upload files** di web GitHub.

> Kalau username GitHub Anda bukan `emilialoho`, perbarui juga baris
> "Repository:" pada `README.md`.

## 3. Login ke Streamlit

Buka <https://share.streamlit.io> lalu **Sign in with GitHub** dan izinkan
Streamlit mengakses repository Anda.

## 4. Deploy

Klik **Create app → Deploy a public app from GitHub**, lalu isi:

| Kolom | Nilai |
|---|---|
| Repository | `<username-github-anda>/jaya-jaya-institut-dropout` |
| Branch | `main` |
| Main file path | `app.py` |
| App URL | `emilia-loho-jaya-jaya-institut` |

> **PENTING — versi Python.**
> Buka **Advanced settings** sebelum menekan Deploy, lalu pilih **Python 3.12**
> (3.11 / 3.13 / 3.14 juga aman). **Jangan pilih 3.9 atau 3.10** — pandas 3.0.2,
> numpy 2.4.4, dan scikit-learn 1.8.0 tidak menyediakan wheel untuk versi
> tersebut, sehingga pip akan mencoba compile dari source dan build-nya gagal.
> Versi Python **tidak bisa diubah setelah deploy** — kalau salah pilih, aplikasi
> harus dihapus lalu di-deploy ulang. Berkas `runtime.txt` sering diabaikan oleh
> Streamlit Cloud, jadi andalkan **Advanced settings**, bukan `runtime.txt`.

Klik **Deploy**. Proses instalasi dependency memakan waktu 2–5 menit.

## 5. Uji aplikasinya

Setelah muncul, coba skenario risiko tinggi berikut untuk memastikan model
benar-benar termuat:

- Tab **Akademik** — SKS lulus semester 1 = `1`, SKS lulus semester 2 = `1`,
  rata-rata nilai semester 1 = `6.5`, semester 2 = `6.0`
- Tab **Finansial** — Biaya kuliah lancar = `No`, Tunggakan (debtor) = `Yes`
- Tekan **🔮 Prediksi Risiko Dropout**

Hasil yang diharapkan: probabilitas dropout **±100,0 %** dengan label
**🔴 RISIKO TINGGI**. Kalau angkanya keluar seperti ini, model berhasil dimuat
di cloud dan aplikasi siap dinilai.

## 6. Pastikan aplikasi tetap aktif

Streamlit Community Cloud **menidurkan** aplikasi yang tidak diakses beberapa
hari. Buka link-nya sekali lagi sesaat sebelum submit supaya reviewer tidak
mendapati halaman "app is sleeping".

---

## Troubleshooting

**Error saat `pip install` / dependency gagal**
`requirements.txt` sudah dipin ke versi yang dipakai saat training
(pandas 3.0.2, numpy 2.4.4, scikit-learn 1.8.0, joblib 1.5.3). Jangan diubah —
`model.joblib` di-pickle dengan scikit-learn 1.8.0, dan versi lain bisa
memunculkan warning atau gagal memuat model.

**`FileNotFoundError: model/model.joblib`**
Folder `model/` belum ikut ter-push. Pastikan ketiga berkas di dalamnya ada di
GitHub — `app.py` mencarinya secara relatif terhadap lokasi berkasnya sendiri.

**Aplikasi blank / terus "Running"**
Cek tab **Manage app → Logs** di pojok kanan bawah untuk melihat pesan error
yang sebenarnya.

**Repository tidak muncul di daftar Streamlit**
Buka <https://github.com/settings/installations>, pilih Streamlit, lalu berikan
akses ke repository tersebut.
