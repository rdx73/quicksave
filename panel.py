import os
import json
from flask import session

# TOKEN LOGIN (Ganti sesuai keinginan kamu)
ADMIN_TOKEN = "QUICKSAVE-2026-SAKTI"

# --- FUNGSI LAMA (JANGAN DIHAPUS) ---

def get_config():
    if not os.path.exists('config.json'):
        # Default config jika file belum ada
        return {"meta_tags": "", "scripts": ""}
    with open('config.json', 'r') as f:
        return json.load(f)

def save_settings(data):
    # Simpan meta tags dan script plugins
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)
    return True

def update_cookies(content):
    # Update file cookies.txt agar Deno tetap sakti
    try:
        with open('cookies.txt', 'w') as f:
            f.write(content)
        return True
    except:
        return False

# --- FUNGSI BARU (DASHBOARD, STATS, & LOGS) ---

def login_admin(token):
    if token == ADMIN_TOKEN:
        session['admin_token'] = token
        return True
    return False

def is_logged_in():
    return session.get('admin_token') == ADMIN_TOKEN

def logout_admin():
    session.pop('admin_token', None)

def get_stats():
    if not os.path.exists('stats.json'):
        return {"total_downloads": 0, "page_views": 0}
    with open('stats.json', 'r') as f:
        return json.load(f)

def add_download_count():
    s = get_stats()
    s['total_downloads'] += 1
    with open('stats.json', 'w') as f:
        json.dump(s, f)

def add_view_count():
    s = get_stats()
    s['page_views'] += 1
    with open('stats.json', 'w') as f:
        json.dump(s, f)

def log_download(title, platform):
    import datetime
    # Format waktu Indonesia
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Bersihkan judul dari karakter line break agar log tidak berantakan
    clean_title = title.replace('\n', ' ').strip()
    log_entry = f"[{now}] [{platform}] - {clean_title}\n"
    with open('download_logs.txt', 'a', encoding='utf-8') as f:
        f.write(log_entry)

def get_logs(limit=10):
    """Mengambil riwayat download untuk ditampilkan di tabel dashboard"""
    if not os.path.exists('download_logs.txt'):
        return []
    
    with open('download_logs.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    logs = []
    # Ambil baris dari yang paling baru (bawah ke atas)
    for line in reversed(lines):
        if len(logs) >= limit:
            break
        try:
            # Parsing format: [Waktu] [Platform] - Judul
            parts = line.split('] ')
            time_part = parts[0].replace('[', '')
            platform_part = parts[1].replace('[', '')
            title_part = parts[2].replace('- ', '').strip()
            
            logs.append({
                "time": time_part,
                "platform": platform_part,
                "title": title_part
            })
        except:
            continue
    return logs
