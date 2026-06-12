# 阿里云 Docker 部署优化指南

## 🎯 阿里云专属优化

### 1. 使用阿里云 PyPI 镜像

```dockerfile
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
ENV PIP_TRUSTED_HOST=mirrors.aliyun.com
```

**优势：**
- ✅ 内网加速，速度极快
- ✅ 稳定性高，99.9% 可用
- ✅ 与 ECS 同地域，延迟最低

### 2. 使用阿里云内网 DNS

```dockerfile
# 阿里云内网 DNS（优先）
nameserver 100.100.2.136
nameserver 100.100.2.138

# 阿里公共 DNS（备用）
nameserver 223.5.5.5
nameserver 223.6.6.6
```

**优势：**
- ✅ 内网解析，零延迟
- ✅ 自动解析阿里云服务
- ✅ 避免跨地域 DNS 查询

### 3. 使用阿里云 APT 镜像

```dockerfile
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list
```

---

## 🚀 快速部署

### 方法1：使用部署脚本（推荐）

```bash
# 标准构建（已包含阿里云优化）
./deploy.sh start

# 或者快速构建
./deploy.sh start fast
```

### 方法2：手动构建

```bash
# 使用阿里云优化的 Dockerfile
docker build -t levistock:latest .

# 启动容器（自动配置阿里云 DNS）
docker run -d \
    --name levistock-service \
    --dns 100.100.2.136 \
    --dns 100.100.2.138 \
    --dns 223.5.5.5 \
    --dns 223.6.6.6 \
    -v $(pwd)/config/config.py:/app/levistock/news/config.py:ro \
    levistock:latest
```

---

## 📊 性能对比

| 配置项 | 通用配置 | 阿里云优化 | 提升 |
|--------|----------|------------|------|
| PyPI 镜像 | pypi.org | mirrors.aliyun.com | 10-50x |
| DNS 解析 | 8.8.8.8 | 100.100.2.136 | 5-20x |
| APT 镜像 | deb.debian.org | mirrors.aliyun.com | 5-10x |
| **总构建时间** | **2-5分钟** | **30-60秒** | **4-6x** |

---

## 🔧 阿里云 ECS 额外优化

### 1. 配置 Docker daemon

编辑 `/etc/docker/daemon.json`：

```json
{
  "registry-mirrors": [
    "https://<your-id>.mirror.aliyuncs.com"
  ],
  "dns": [
    "100.100.2.136",
    "100.100.2.138",
    "223.5.5.5",
    "223.6.6.6"
  ]
}
```

获取你的加速器地址：
- 登录 [阿里云容器镜像服务](https://cr.console.aliyun.com/)
- 左侧菜单：镜像加速器
- 复制加速器地址

重启 Docker：

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 2. 使用 VPC 内网

如果多个 ECS 在同一 VPC：

```bash
# 容器间通信使用内网 IP
docker run --network host ...
```

### 3. 挂载 NAS/OSS（可选）

如果需要持久化数据：

```bash
# 挂载 NAS
docker run -v /mnt/nas/data:/app/data ...

# 挂载 OSS（需要 ossfs）
docker run -v /mnt/oss/data:/app/data ...
```

---

## 🐛 常见问题

### Q1: 构建时仍然很慢？

**A:** 检查是否使用了阿里云镜像：

```bash
# 查看构建日志
docker build --progress=plain -t levistock:latest . 2>&1 | grep aliyun

# 应该看到类似输出：
# Looking up indexes: mirrors.aliyun.com
```

### Q2: DNS 解析失败？

**A:** 检查 DNS 配置：

```bash
# 查看容器 DNS
docker exec -it levistock-service cat /etc/resolv.conf

# 测试 DNS
docker exec -it levistock-service ping mirrors.aliyun.com
```

### Q3: 如何验证使用了内网 DNS？

**A:** 

```bash
# 在容器内执行
docker exec -it levistock-service nslookup mirrors.aliyun.com

# 应该返回内网 IP（以 100. 或 172. 开头）
```

### Q4: pip install 超时？

**A:** 增加超时时间：

```dockerfile
ENV PIP_DEFAULT_TIMEOUT=100
```

---

## 💡 最佳实践

### 1. 定期清理镜像

```bash
# 清理未使用的镜像
docker image prune -f

# 清理所有未使用的资源
docker system prune -a -f
```

### 2. 使用多阶段构建（如果需要）

```dockerfile
# 构建阶段
FROM python:3.11-slim AS builder
COPY . .
RUN pip install -e .

# 运行阶段
FROM python:3.11-slim
COPY --from=builder /app /app
```

### 3. 监控资源使用

```bash
# 查看容器资源
docker stats levistock-service

# 设置资源限制（已在 deploy.sh 中配置）
--cpus=1.0
--memory=512m
```

### 4. 备份配置

```bash
# 备份到 OSS
ossutil cp config/config.py oss://your-bucket/config-backup/

# 或者备份到 NAS
cp config/config.py /mnt/nas/backups/config.$(date +%Y%m%d).py
```

---

## 📝 阿里云服务集成

### 1. 日志服务 SLS

```bash
# 安装 logtail
docker run -d \
    --name logtail \
    -v /var/log:/var/log \
    registry.cn-hangzhou.aliyuncs.com/log-service/logtail
```

### 2. 监控服务 CloudMonitor

```bash
# 安装云监控插件
docker run -d \
    --name cms-agent \
    registry.cn-hangzhou.aliyuncs.com/cms/cms-agent
```

### 3. ACM 配置中心

```python
# 在 config.py 中使用 ACM
import acm

client = acm.ACMClient(endpoint='acm.aliyun.com')
config = client.get_config(data_id='levistock', group='DEFAULT_GROUP')
```

---

## 🎯 总结

**阿里云环境三大优化：**
1. ✅ PyPI 使用 `mirrors.aliyun.com`
2. ✅ DNS 使用 `100.100.2.136/138`
3. ✅ APT 使用 `mirrors.aliyun.com`

**预期效果：**
- 构建速度提升 4-6 倍
- 网络稳定性显著提升
- 完全避免跨地域访问

---

**祝在阿里云部署顺利！** 🚀
