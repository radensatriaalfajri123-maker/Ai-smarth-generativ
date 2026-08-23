import os
import time
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ambil kedua API Key dari .env
keys = [os.getenv("GROQ_API_KEY_1"), os.getenv("GROQ_API_KEY_2")]
# Filter jika ada key yang kosong
api_keys = [k for k in keys if k]

# Simpan waktu kapan user diblokir (Simulasi Paywall sementara di memori)
# Jika produksi massal, bagian ini idealnya menggunakan Database/Redis
user_block_status = {
    "is_blocked": False,
    "unblock_time": 0
}

@app.post("/api/chat")
async def chat_ai(
    text: str = Form(default=""), 
    file: UploadFile = File(default=None)
):
    global user_block_status

    # 1. Cek apakah user sedang dalam masa tunggu 1 jam (Paywall aktif)
    current_time = time.time()
    if user_block_status["is_blocked"]:
        if current_time < user_block_status["unblock_time"]:
            time_left = int((user_block_status["unblock_time"] - current_time) / 60)
            return {
                "status": "paywall",
                "reply": f"⚠️ Kuota AI Gratis Habis! Semua API Key penuh.\n\nSilakan bayar Rp 5.000, Rp 10.000, atau Rp 30.000 untuk akses instan, ATAU tunggu {time_left} menit lagi sampai kuota reset otomatis.",
                "time_left_minutes": time_left
            }
        else:
            # Masa tunggu 1 jam sudah lewat, buka blokir otomatis
            user_block_status["is_blocked"] = False

    # 2. Validasi Batasan Kata Input
    word_count = len(text.split())
    if word_count > 1000:
        raise HTTPException(status_code=400, detail="Input melebihi batas 1000 kata.")

    # 3. Coba kirim menggunakan Multi-API Key secara bergantian (Rotation)
    ai_reply = None
    for index, key in enumerate(api_keys):
        try:
            client = Groq(api_key=key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[
                    {"role": "system", "content": "Kamu adalah AI SMARTH GENERATIV. Kamu super cerdas dan tidak kaku."},
                    {"role": "user", "content": text}
                ],
                max_tokens=2000
            )
            ai_reply = response.choices.message.content
            # Jika berhasil mendapat jawaban, keluar dari perulangan kunci
            break 
        except Exception as e:
            print(f"API Key ke-{index+1} gagal atau terkena limit rate. Mencoba key berikutnya...")
            continue

    # 4. Jika kedua API Key gagal/habis kuota, aktifkan Paywall 1 Jam
    if not ai_reply:
        user_block_status["is_blocked"] = True
        user_block_status["unblock_time"] = current_time + 3600  # 3600 detik = 1 jam
        
        return {
            "status": "paywall",
            "reply": "⚠️ Limit Tercapai! Kuota gratis pada kedua API Key kami telah habis.\n\nPilih paket instan:\n- Hemat: Rp 5.000\n- Populer: Rp 10.000\n- Pro: Rp 30.000\n\nAtau tunggu 1 jam. Sistem akan memberikan notifikasi otomatis saat AI aktif kembali.",
            "time_left_minutes": 60
        }

    return {"status": "success", "reply": ai_reply}

# Endpoint tambahan untuk simulasi pembayaran sukses (Bypass Tunggu 1 Jam)
@app.post("/api/pay-success")
async def pay_success():
    global user_block_status
    user_block_status["is_blocked"] = False
    user_block_status["unblock_time"] = 0
    return {"status": "success", "message": "Pembayaran berhasil! AI SMARTH GENERATIV aktif kembali sekarang."}

