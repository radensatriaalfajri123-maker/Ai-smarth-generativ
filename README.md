# AI SMARTH GENERATIV 🚀

Aplikasi Web AI super cepat dan tidak kaku menggunakan teknologi **Groq API (Llama 3)**. Dilengkapi dengan tampilan teks pelangi yang dinamis, batasan input kata, sistem rotasi multi-API key, serta fitur proteksi paywall otomatis.

## 🔥 Fitur Unggulan
- **Rainbow UI & Smooth Animation**: Tampilan modern estetik dengan teks pelangi bergerak.
- **Input Guard**: Pembatasan ketat maksimal 1000 kata per pesan untuk keamanan server.
- **Multi-API Key Rotation**: Menggunakan 2 API Key bergantian untuk kuota yang lebih melimpah.
- **Smart Paywall**: Jika kuota kedua API Key habis, sistem otomatis mengaktifkan masa tunggu 1 jam atau opsi pembayaran simulasi (Rp 5.000, Rp 10.000, Rp 30.000).
- **Browser Notification**: Memberikan notifikasi otomatis ke komputer/HP user setelah masa tunggu 1 jam selesai.

## 🛠️ Arsitektur Proyek
```text
ai-smarth-generativ/
├── frontend/        # Tampilan Web (HTML, CSS, JS)
└── backend/         # Mesin API (Python FastAPI)
```

## 🚀 Cara Menjalankan Secara Lokal

### 1. Persiapan Backend
Masuk ke folder backend, instal semua pustaka, dan buat file rahasia `.env`:
```bash
cd backend
pip install -r requirements.txt
```

Buat file bernama `.env` di dalam folder `backend/` lalu isi:
```text
GROQ_API_KEY_1=isi_api_key_groq_pertama_kamu
GROQ_API_KEY_2=isi_api_key_groq_kedua_kamu
```

### 2. Jalankan Server API
Mulai server backend Python menggunakan Uvicorn:
```bash
python main.py
```
Server akan berjalan di `http://127.0.0.1:8000`.

### 3. Jalankan Frontend
Kamu tidak perlu instal apa-apa untuk tampilan. Cukup masuk ke folder `frontend/` dan klik dua kali pada file `index.html` untuk membukanya di browser!

