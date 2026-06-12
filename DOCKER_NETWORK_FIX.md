# Docker 网络问题排查指南

## ❌ 常见错误

### 错误1: DNS 解析失败

```
Temporary failure in name resolution
Could not find a version that satisfies the requirement
```

**原因：** Docker 容器无法解析域名

**解决方案：** ✅ 已自动配置国内 DNS

---

## 🔧 已实施的优化

### 1. 配置国内 PyPI 镜像

```dockerfile
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
```

### 2. 配置 DNS 服务器

**Dockerfile 内：**
```dockerfile
RUN echo "nameserver 223.5.5.5" > /etc/resolv.conf
RUN echo "nameserver 223.6.6.6" >> /etc/resolv.conf
RUN echo "nameserver 114.114.114.114" >> /etc/resolv.conf
```

**容器启动时：**
```bash
docker run --dns 223.5.5.5 --dns 223.6.6.6 --dns 114.114.114.114 ...
```

### 3. 预安装必要工具

```dockerfile
RUN pip install setuptools wheel
```

避免构建依赖时的网络问题。

---

## 🚀 使用方法

### 标准部署（已包含所有优化）

```bash
./deploy.sh start
```

### 快速部署（额外使用清华镜像）

```bash
./deploy.sh start fast
```

---

## 🐛 如果仍然失败

### 方案1: 检查宿主机网络

```bash
# 测试 DNS
ping 223.5.5.5

# 测试 PyPI
curl https://pypi.tuna.tsinghua.edu.cn/simple/requests/
```

### 方案2: 手动指定 Docker DNS

编辑 `/etc/docker/daemon.json`：

```json
{
  "dns": ["223.5.5.5", "223.6.6.6", "114.114.114.114"]
}
```

然后重启 Docker：

```bash
sudo systemctl restart docker
```

### 方案3: 使用代理

如果有 HTTP 代理：

```bash
docker build \
    --build-arg HTTP_PROXY=http://proxy:port \
    --build-arg HTTPS_PROXY=http://proxy:port \
    -t levistock:latest .
```

### 方案4: 离线构建

1. 在有网络的机器上构建镜像
2. 导出镜像：
   ```bash
   docker save levistock:latest -o levistock.tar
   ```
3. 传输到目标机器
4. 导入镜像：
   ```bash
   docker load -i levistock.tar
   ```

---

## 📊 DNS 服务器推荐

| DNS | 地址 | 说明 |
|-----|------|------|
| 阿里 DNS | 223.5.5.5 | 稳定快速 |
| 阿里 DNS | 223.6.6.6 | 备用 |
| 114 DNS | 114.114.114.114 | 通用 |
| Google DNS | 8.8.8.8 | 国际 |
| Cloudflare | 1.1.1.1 | 国际 |

---

## 💡 最佳实践

1. **始终使用国内镜像源**（如果在国内）
2. **配置多个 DNS 服务器**（提高可靠性）
3. **预安装常用工具**（减少网络请求）
4. **利用 Docker 缓存**（避免重复下载）

---

## 🔍 调试命令

```bash
# 查看容器 DNS 配置
docker exec -it levistock-service cat /etc/resolv.conf

# 测试容器内网络
docker exec -it levistock-service ping 223.5.5.5

# 测试 PyPI 连接
docker exec -it levistock-service pip install --dry-run requests

# 查看构建日志
docker build --progress=plain -t levistock:latest .
```

---

**祝部署顺利！** 🎉
