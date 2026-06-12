FROM python:3.11-slim

WORKDIR /app

# 设置环境变量优化 pip 安装
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 先复制依赖文件并安装,利用 Docker 缓存层
COPY requirements.txt .
RUN pip install -r requirements.txt

# 再复制项目代码
COPY . .


CMD ["python", "levistock/news/unified_service.py"]
