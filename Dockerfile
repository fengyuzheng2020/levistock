FROM python:3.11-slim

WORKDIR /app
# 国内构建加速：Alpine 源 + Go 模块代理
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

COPY . .
RUN pip install -e .

CMD ["python", "levistock/news/unified_service.py"]
