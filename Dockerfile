# ベースイメージを指定（Python 3.9を使用する例）
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナ内にコピー
COPY requirements.txt requirements.txt
COPY . .

# 必要なPythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションを実行
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]