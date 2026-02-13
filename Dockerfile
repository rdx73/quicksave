FROM python:3.10-slim-bookworm

# 1. Install dependency sistem
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    ca-certificates \
    unzip \
 && rm -rf /var/lib/apt/lists/*

# 2. Install Deno secara global ke /usr/local/bin (Sesuai saran Fin & Adifagos)
# Menggunakan flag -s -- -d agar langsung masuk ke folder yang bisa diakses semua user
RUN curl -fsSL https://deno.land/x/install/install.sh | sh -s -- -d /usr/local/bin

# 3. Berikan izin eksekusi eksplisit (Sesuai saran Fin)
RUN chmod +x /usr/local/bin/deno

# 4. Atur Environment Path agar Deno terdeteksi
ENV PATH="/usr/local/bin:$PATH"
ENV YTDLP_JS_RUNTIME=deno

WORKDIR /app

# 5. Setup User koyeb
RUN useradd -m koyeb
ENV YTDLP_CACHE_DIR=/app/yt_cache

# 6. Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade yt-dlp-ejs==0.4.0

# 7. Copy project & Pindahkan kepemilikan
COPY . .
RUN mkdir -p $YTDLP_CACHE_DIR && \
    chown -R koyeb:koyeb /app && \
    chmod -R 755 $YTDLP_CACHE_DIR

# 8. Jalankan pengecekan versi (untuk memastikan build sukses)
RUN deno --version && yt-dlp --version

USER koyeb

# Port fleksibel
EXPOSE 8000
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-8000} app:app --timeout 120"]
