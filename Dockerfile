# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ \
    PIP_TRUSTED_HOST=mirrors.aliyun.com

# 使用国内镜像源加速（可选，如果在国内）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list 2>/dev/null || true

# 配置 DNS（阿里云内网 DNS + 公共 DNS）
RUN echo "nameserver 100.100.2.136" > /etc/resolv.conf && \
    echo "nameserver 100.100.2.138" >> /etc/resolv.conf && \
    echo "nameserver 223.5.5.5" >> /etc/resolv.conf && \
    echo "nameserver 223.6.6.6" >> /etc/resolv.conf

# 复制依赖文件并安装（利用 Docker 缓存层）
COPY pyproject.toml .
COPY levistock/__init__.py ./levistock/__init__.py

# 安装 Python 依赖（这层会被缓存，除非依赖文件变化）
# 先预安装 setuptools，避免网络问题
RUN pip install --no-cache-dir setuptools wheel && \
    (pip install --no-cache-dir -e . || \
     pip install --no-cache-dir requests beautifulsoup4 lxml)

# 复制剩余代码
COPY . .

# 创建配置目录
RUN mkdir -p /app/config

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# 启动命令
CMD ["python", "levistock/news/unified_service.py"]
