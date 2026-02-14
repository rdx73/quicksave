import requests
import yt_dlp
import os

def get_general_info(video_url):
    # --- TAHAP 1: COBALT ---
    try:
        api_url = "https://api.cobalt.tools/api/json"
        payload = {"url": video_url, "vQuality": "720"}
        res = requests.post(api_url, json=payload, timeout=6)
        data = res.json()
        if 'url' in data:
            return {'success': True, 'title': 'Video Ready', 'download_url': data['url']}
    except: pass

    # --- TAHAP 2: YT-DLP MOBILE SPOOF ---
    mobile_headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    ydl_opts = {
        'quiet': True,
        'format': 'best',
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'http_headers': mobile_headers,
        # TAMBAHAN BIAR AWET:
        'nocheckcertificate': True,
        'geo_bypass': True,
        'ext': 'mp4',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # Ambil URL terbaik, utamakan yang ada link langsung
            d_url = info.get('url')
            if not d_url and 'formats' in info:
                d_url = info['formats'][-1]['url']

            return {
                'success': True,
                'title': info.get('title', 'QuickSave Video'),
                'thumbnail': info.get('thumbnail'),
                'download_url': d_url
            }
    except Exception as e:
        return {'success': False, 'error': str(e)}
