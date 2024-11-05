# ベースイメージを指定
FROM python:3.10

# 必要なパッケージをインストール（SDL2とZbarを含む）
RUN apt-get update && \
    apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libzbar0 netcat-openbsd default-mysql-client && \
    apt-get clean

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt /app/

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー
COPY . /app/

# Djangoの静的ファイルをコンテナ内に収集
RUN python manage.py collectstatic --noinput

# ポートの指定
EXPOSE 8000

# サーバーを起動
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


