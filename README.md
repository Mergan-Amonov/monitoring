# 🖥️ AI Asosidagi Kompyuter Faoliyatini Kuzatish Tizimi

Bu loyiha foydalanuvchi roziligi asosida kompyuterdagi ish faoliyatini kuzatuvchi, statistik ma'lumotlarni yig'uvchi va ularni **Google Gemini Sun'iy Intellekti** yordamida tahlil qilib, Telegram bot orqali avtomatik hisobot yuboruvchi Python dasturidir.

Tizim maxfiylikni to'liq saqlagan holda ishlaydi va kiritilgan matnlarni emas, faqat miqdoriy ko'rsatkichlarni tahlil qiladi.

## ✨ Asosiy Xususiyatlar

* **Haqiqiy Sun'iy Intellekt Tahlili:** Dastur qotib qolgan qoidalarga emas, balki Google Gemini (1.5 Flash) neyron tarmog'iga tayanadi. U raqamlar va ochiq dasturlarni tahlil qilib, insonga xos aqlli xulosalar chiqaradi.
* **Mutlaq Maxfiylik:** Dastur kiritilgan parollar yoki yozishmalarni (harflarni) o'qimaydi va saqlamaydi. Faqatgina tugmalar va sichqoncha bosilishlarining *umumiy soni* hisoblanadi.
* **Foydalanuvchi Roziligi:** Dastur faqat foydalanuvchi terminalda tasdiqlaganidan so'nggina ishga tushadi.
* **Telegram Integratsiyasi:** Har bir interval yakunida faoliyat xulosasi va batafsil `.txt` fayl belgilangan Telegram chatiga yuboriladi.
* **Moslashuvchan Vaqt:** Monitoring oralig'ini o'z ehtiyojingizga qarab soniyalarda belgilashingiz mumkin (hozirda test uchun 20 soniya qilib sozlangan).

## 🛠 Texnologiyalar va Kutubxonalar

Loyiha **Python** tilida yozilgan. Quyidagi kutubxonalardan foydalaniladi:
* `google-generativeai` — Google Gemini API bilan ishlab, aqlli xulosalar olish uchun.
* `pynput` — Klaviatura va sichqoncha hodisalarini kuzatish uchun.
* `pygetwindow` — Kompyuterdagi faol oynalarni (dasturlarni) aniqlash uchun.
* `requests` — Telegram Bot API bilan ishlash uchun.

## 🚀 O'rnatish va Sozlash

### 1-qadam: Kutubxonalarni o'rnatish
Terminal (yoki buyruqlar satri) orqali kerakli modullarni o'rnating:
```bash
pip install pynput pygetwindow requests google-generativeai