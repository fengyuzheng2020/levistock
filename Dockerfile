FROM python:3.11-slim

WORKDIR /app

# 阿里云国内pip源，加速下载依赖（关键，国外源阿里云很慢）
ENV PIP_INDEX_URL=https://pypi.org/simple
ENV PIP_TRUSTED_HOST=mirrors.aliyun.com

# 设置环境变量优化 pip 安装
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 先复制依赖文件并安装,利用 Docker 缓存层
COPY requirements.txt .
RUN pip install -r requirements.txt

# 再复制项目代码
COPY . .


CMD ["python", "levistock/news/unified_service.py"]
