FROM python:3.10-slim-bookworm

# 1. Install dependency sistem + Deno (Sesuai saran Adifagos)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    ca-certificates \
    unzip \
 && curl -fsSL https://deno.land/x/install/install.sh | sh \
 && rm -rf /var/lib/apt/lists/*

# 2. Atur Environment Path untuk Deno
ENV DENO_INSTALL="/root/.deno"
ENV PATH="$DENO_INSTALL/bin:$PATH"

# Pastikan deno terbaca
RUN deno --version && which deno

WORKDIR /app

# 3. Setup User & Cache
RUN useradd -m koyeb
ENV YTDLP_CACHE_DIR=/app/yt_cache
# Tambahkan variabel lingkungan agar yt-dlp otomatis melirik deno
ENV YTDLP_JS_RUNTIME=deno

# 4. Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade yt-dlp-ejs==0.4.0

# 5. Pre-cache solver yt-dlp menggunakan Deno
RUN mkdir -p $YTDLP_CACHE_DIR && \
    yt-dlp --cache-dir $YTDLP_CACHE_DIR \
    --extractor-args "youtube:js_runtime=deno" \
    --version

# 6. Copy project & Permission
COPY . .
RUN chown -R koyeb:koyeb /app && \
    chown -R koyeb:koyeb /root/.deno && \
    chmod -R 755 $YTDLP_CACHE_DIR

USER koyeb

# Port fleksibel (cloud friendly)
EXPOSE 8000
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-8000} app:app --timeout 120"]
