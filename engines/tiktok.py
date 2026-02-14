import requests
import yt_dlp
import os

def get_tt_info(video_url):
    # --- TAHAP 1: TikWM (Utama - Tanpa Watermark) ---
    try:
        api_url = "https://www.tikwm.com/api/"
        payload = {'url': video_url}
        res = requests.post(api_url, data=payload, timeout=7)
        data = res.json()
        
        if data.get('code') == 0:
            video_data = data['data']
            return {
                'success': True,
                'title': video_data.get('title', 'TikTok Video'),
                'thumbnail': video_data.get('cover'),
                'duration': f"{video_data.get('duration', 0)}s",
                'download_url': video_data.get('play')
            }
    except:
        pass # Jika TikWM error, lanjut ke tahap 2

    # --- TAHAP 2: YT-DLP (Cadangan - Pake Cookies Tuyul) ---
    try:
        ydl_opts = {
            'quiet': True,
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return {
                'success': True,
                'title': info.get('title', 'TikTok Video'),
                'thumbnail': info.get('thumbnail'),
                'download_url': info.get('url') # Mungkin ada watermark
            }
    except Exception as e:
        return {'success': False, 'error': f"TikTok Error: {str(e)}"}
