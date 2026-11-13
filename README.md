# NOTA AI — Basic Pitch sinov servisi

Bu servis Spotify Basic Pitch orqali audio fayldagi taxminiy notalarni ajratadi. Hozircha asl nota bilan taqqoslash va ball berish yo'q.

## Ishga tushirish
Python 3.10 va ffmpeg tavsiya etiladi.

```bash
pip install -r requirements.txt
export NOTA_ANALYSIS_KEY='strong-random-secret'
uvicorn main:app --host 0.0.0.0 --port 8000
```

Sinov:
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/analyze -H 'x-api-key: strong-random-secret' -F 'audio=@sample.wav'
```

Muhim: API kalitini faqat server muhit o'zgaruvchisida saqlang; brauzer kodiga qo'shmang. Production uchun rate limiting, queue, audio duration limits, background jobs va izolyatsiyalangan server kerak. Vercel Next.js ilovasidan maxfiy server-to-server so'rov yuboriladi. Docker image hajmi va ishga tushish vaqti uchun alohida container hosting tavsiya etiladi.
