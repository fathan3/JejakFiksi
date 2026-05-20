# JejakFiksi 📚✨

[![Live Demo](https://img.shields.io/badge/Demo-Live%20on%20Vercel-blue?style=for-the-badge&logo=vercel)](https://jejakfiksi.vercel.app/)

**JejakFiksi** adalah aplikasi Sistem Temu Kembali Informasi (Information Retrieval) Buku Novel Modern berbasis Web. Aplikasi ini membantu pengguna mencari dan menemukan novel yang relevan berdasarkan masukan tema, alur cerita, atau genre tertentu menggunakan metode pencarian tingkat lanjut.

Aplikasi ini dideploy secara langsung dan dapat diakses di: **[https://jejakfiksi.vercel.app/](https://jejakfiksi.vercel.app/)**

---

## 🚀 Fitur Utama

- **Dua Metode Temu Kembali Informasi**:
  - **Cosine Similarity (TF-IDF)**: Mengukur kemiripan sudut antara vektor query dengan vektor dokumen novel berdasarkan pembobotan TF-IDF manual.
  - **BM25 (Best Matching 25)**: Algoritma pencarian probabilistik modern yang menghitung skor relevansi dengan mempertimbangkan frekuensi term, panjang dokumen, dan rata-rata panjang seluruh dokumen dalam korpus.
- **Preprocessing Teks Kustom**:
  - *Case Folding* (mengubah teks menjadi huruf kecil).
  - Penghapusan karakter non-alfanumerik.
  - Tokenisasi kalimat menjadi term-term bersih.
- **Tampilan Premium & Responsif (Sleek Dark Mode)**:
  - Desain gelap elegan yang terinspirasi dari produk SaaS modern (seperti Linear dan Vercel).
  - Mikro-interaksi halus pada form pencarian dan hover kartu hasil pencarian.
  - Responsif di perangkat desktop maupun ponsel.

---

## 🛠️ Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML5, Vanilla CSS3 (Sleek Dark Theme)
- **Deployment**: Vercel (Menggunakan `@vercel/python` serverless handler)

---

## 📁 Struktur Proyek

```text
ta-tki/
│
├── app.py                             # Logic backend Flask & algoritma IR (TF-IDF & BM25)
├── dataset_final_search_engine (1).json # Dataset novel (judul, sinopsis, url)
├── requirements.txt                   # Dependensi Python proyek
├── vercel.json                        # Konfigurasi deployment Vercel
│
└── templates/
    └── index.html                     # Tampilan frontend aplikasi (HTML & CSS)
```

---

## 💻 Cara Menjalankan Secara Lokal

1. **Clone repositori ini**:
   ```bash
   git clone <repository-url>
   cd ta-tki
   ```

2. **Buat dan aktifkan virtual environment** (opsional tapi disarankan):
   ```bash
   python -m venv venv
   # Di Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # Di Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependensi yang diperlukan**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi Flask**:
   ```bash
   python app.py
   ```

5. **Akses aplikasi di browser**:
   Buka alamat [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## ☁️ Deployment ke Vercel

Proyek ini telah dikonfigurasi agar siap dideploy di Vercel menggunakan file `vercel.json`:

```json
{
    "version": 2,
    "builds": [
        {
            "src": "app.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "app.py"
        }
    ]
}
```

Cukup hubungkan repositori Anda ke dashboard Vercel, pilih kerangka Python, dan Vercel akan menangani deployment secara otomatis.
