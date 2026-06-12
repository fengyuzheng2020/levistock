FROM python:3.11-slim

WORKDIR /app

# 配置 DNS 服务器解决容器内 DNS 解析失败问题
RUN echo "nameserver 223.5.5.5" > /etc/resolv.conf && \
    echo "nameserver 223.6.6.6" >> /etc/resolv.conf

# 配置 pip 使用国内镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

COPY . .

# 设置环境变量优化 pip 安装
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install -e .

CMD ["python", "levistock/news/unified_service.py"]
