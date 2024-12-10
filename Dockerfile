FROM python:3.9-slim

# 必要なライブラリをインストール
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    libsndfile1 \
    && apt-get clean

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# アプリケーションを起動
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]