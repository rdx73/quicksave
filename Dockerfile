# 1. Ambil stage Deno resmi (Gunakan tag 'bin' agar lebih ringan)
FROM denoland/deno:bin AS deno-stage

# 2. Gunakan image Python sebagai base utama
FROM python:3.10-slim-bookworm

# 3. PERBAIKAN: Jalur asal di image denoland/deno adalah /deno
COPY --from=deno-stage /deno /usr/local/bin/deno

# 4. Install dependency sistem (FFmpeg, dll)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# 5. Berikan izin eksekusi & Atur Environment (Saran Admin & Fin)
RUN chmod +x /usr/local/bin/deno
ENV PATH="/usr/local/bin:$PATH"
ENV YTDLP_JS_RUNTIME=deno

WORKDIR /app

# 6. Setup User koyeb
RUN useradd -m koyeb
ENV YTDLP_CACHE_DIR=/app/yt_cache

# 7. Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade yt-dlp-ejs==0.4.0

# 8. Copy project & Pindahkan kepemilikan
COPY . .
RUN mkdir -p $YTDLP_CACHE_DIR && \
    chown -R koyeb:koyeb /app && \
    chmod -R 755 $YTDLP_CACHE_DIR

# 9. Cek versi SEBELUM pindah ke USER koyeb (Saran Penting Admin)
RUN deno --version && yt-dlp --version

# 10. Switch ke user koyeb
USER koyeb

# Port & Start Command
EXPOSE 8000
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-8000} app:app --timeout 120"]
