# ベースイメージを指定（Python 3.9を使用する例）
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナ内にコピー
COPY requirements.txt requirements.txt
COPY . .

# 必要なPythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flaskアプリケーションを環境変数で設定
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# アプリを起動するポートを指定
EXPOSE 8080

# Flaskアプリを起動
CMD ["flask", "run"]