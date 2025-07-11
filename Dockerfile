# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリ
WORKDIR /app

# OS パッケージ更新＆必要ライブラリ（Pillow 用）をインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
       build-essential \
       libjpeg-dev \
       libpng-dev && \
    rm -rf /var/lib/apt/lists/*

# 依存関係をコピー＆インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY app.py .

# Streamlit ポートを開放
EXPOSE 8501

# 起動コマンド
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
