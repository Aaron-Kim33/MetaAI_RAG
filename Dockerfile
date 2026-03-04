# 1. 플랫폼을 linux/amd64로 명시하여 브라우저 호환성 확보
FROM --platform=linux/amd64 mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 브라우저 엔진 설치 (플랫폼 명시 덕분에 안정적으로 설치됨)
RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .

# 볼륨 데이터 저장 폴더
RUN mkdir -p /app/data

CMD ["python", "app.py"]