
# 📊 AI Asosida Kompyuter Faoliyatini Monitoring Qilish Tizimi

Bu dastur kompyuterdagi foydalanuvchi faoliyatini (klaviatura yozishmalari, sichqoncha bosishlari va faol oynalarni) avtomatik ravishda kuzatib boruvchi va **Google Gemini AI** yordamida aqlli xulosa chiqaruvchi Python skriptidir. Barcha ma'lumotlar va AI tahlili belgilangan vaqt oralig'ida Telegram bot orqali yuborib turiladi.

## 🚀 Xususiyatlari

* **Klaviatura Kuzatuvi (Keylogger):** Bosilgan harflar va so'zlarni xavfsiz tarzda matnga yig'ib boradi (maxsus tugmalar, masalan, Shift, Ctrl kabilar e'tiborsiz qoldiriladi).
* **Sichqoncha Kuzatuvi (Mouse Tracker):** Ekranning qaysi kordinatalarida `(X, Y)` sichqoncha bosilganligini qayd etadi.
* **Faol Oynalar (Active Windows):** Foydalanuvchi qaysi dasturlar yoki veb-saytlarda ishlayotganini aniqlaydi.
* **Sun'iy Z इंटेill (AI) Tahlili:** Yig'ilgan statistikani Google GenAI (`gemini-2.5-flash`) modeliga yuborib, foydalanuvchi aynan nima ish bilan bandligi haqida qisqa va aniq xulosa oladi.
* **Telegram Integratsiyasi:** Har hisobot davrida (masalan, 20 soniya) umumiy statistika va AI xulosasini Telegram xabar tarzida, to'liq yozishmalar va kordinatalarni esa `.txt` fayl ko'rinishida yuboradi.

## 🛠 Talablar

Dasturni ishga tushirish uchun kompyuteringizda **Python 3.x** o'rnatilgan bo'lishi kerak. Shuningdek, quyidagi kutubxonalarni o'rnatishingiz zarur:

```bash
pip install requests pygetwindow pynput google-genai
```

## ⚙️ O'rnatish va Sozlash

1.  Ushbu kodni kompyuteringizga ko'chirib oling (masalan, `monitor.py` nomi bilan saqlang).
2.  Kodni matn muharririda oching va quyidagi **Sozlamalar** qismini o'zingizning ma'lumotlaringiz bilan almashtiring:

    ```python
    # --- SOZLAMALAR ---
    BOT_TOKEN = 'SIZNING_TELEGRAM_BOT_TOKENINGIZ'
    CHAT_ID = 'SIZNING_TELEGRAM_CHAT_ID_RAQAMINGIZ'
    GEMINI_API_KEY = 'SIZNING_GOOGLE_GEMINI_API_KALITINGIZ'
    INTERVAL_SEC = 20  # Hisobot yuborish oralig'i (soniyalarda)
    ```

    * `BOT_TOKEN`: BotFather orqali yaratilgan Telegram bot tokeni.
    * `CHAT_ID`: Hisobotlar borishi kerak bo'lgan akkaunt yoki guruhning ID raqami.
    * `GEMINI_API_KEY`: Google AI Studio orqali olingan API kalit.

## ▶️ Dasturni Ishga Tushirish

Terminal yoki buyruqlar satrida (Command Prompt/PowerShell) quyidagi buyruqni kiriting:

```bash
python monitor.py
```

Dastur ishga tushganda sizdan rozilik so'raydi:
`Dasturni ishga tushirishga rozimisiz? (H/Y):`
`H` yoki `ha` deb yozib Enter bossangiz, monitoring boshlanadi. Dasturni to'xtatish uchun terminalda `Ctrl + C` tugmalarini bosing.

## 📂 Hisobot Ko'rinishi

Telegram botingizga quyidagi ko'rinishda xabar keladi:

> 📊 Yangi hisobot (2023-10-27 15:30:00)
> 🤖 AI: Foydalanuvchi Telegram dasturida kimgadir xabar yozmoqda.

Va unga qo'shib `report_15-30-00.txt` nomli fayl yuboriladi. Fayl ichida batafsil statistika, bosilgan kordinatalar va yozilgan matn (keylog) bo'ladi.

## ⚠️ Xavfsizlik va Maxfiylik Ogohlantir