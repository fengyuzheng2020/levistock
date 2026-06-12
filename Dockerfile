FROM python:3.11-slim

WORKDIR /app

# 配置 pip 使用国内镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

COPY . .

# 设置环境变量优化 pip 安装
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install -e .

CMD ["python", "levistock/news/unified_service.py"]
