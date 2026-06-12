# Docker Hub 连接超时解决方案

## ❌ 错误信息

```
failed to resolve source metadata for docker.io/library/python:3.11-slim
dial tcp 202.160.129.6:443: i/o timeout
```

**原因：** 无法访问 Docker Hub（registry-1.docker.io）

---

## ✅ 解决方案（三选一）

### 方案1：使用自动配置脚本（推荐）

```bash
# 赋予执行权限
chmod +x setup_docker_mirror.sh

# 运行配置脚本（需要 sudo）
sudo ./setup_docker_mirror.sh

# 重新构建
./deploy.sh start
```

**脚本会自动配置：**
- ✅ Docker 镜像加速器
- ✅ DNS 服务器
- ✅ 日志配置

---

### 方案2：手动配置 Docker daemon

#### 步骤1：编辑配置文件

```bash
sudo vim /etc/docker/daemon.json
```

#### 步骤2：添加以下内容

```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://huecker.io",
    "https://dockerhub.timeweb.cloud",
    "https://noohub.ru"
  ],
  "dns": [
    "100.100.2.136",
    "100.100.2.138",
    "223.5.5.5",
    "223.6.6.6"
  ]
}
```

#### 步骤3：重启 Docker

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

#### 步骤4：验证配置

```bash
docker info | grep -A 5 "Registry Mirrors"
```

应该看到：

```
Registry Mirrors:
  https://docker.m.daocloud.io/
  https://huecker.io/
  ...
```

---

### 方案3：使用阿里云容器镜像服务（阿里云用户专属）

#### 步骤1：获取加速器地址

1. 登录 [阿里云容器镜像服务](https://cr.console.aliyun.com/)
2. 左侧菜单：**镜像工具** → **镜像加速器**
3. 复制你的专属加速器地址，例如：
   ```
   https://xxxxx.mirror.aliyuncs.com
   ```

#### 步骤2：配置 daemon.json

```bash
sudo vim /etc/docker/daemon.json
```

```json
{
  "registry-mirrors": [
    "https://xxxxx.mirror.aliyuncs.com"
  ],
  "dns": [
    "100.100.2.136",
    "100.100.2.138"
  ]
}
```

#### 步骤3：重启 Docker

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## 🧪 测试是否成功

### 测试1：拉取基础镜像

```bash
docker pull python:3.11-slim
```

应该很快完成（几秒钟）。

### 测试2：构建项目镜像

```bash
./deploy.sh start
```

---

## 🐛 如果仍然失败

### 检查1：网络连接

```bash
# 测试是否能访问 Docker Hub
curl -I https://registry-1.docker.io/v2/

# 测试镜像加速器
curl -I https://docker.m.daocloud.io/v2/
```

### 检查2：防火墙

```bash
# 检查防火墙状态
sudo firewall-cmd --list-all

# 如果需要，开放 Docker 端口
sudo firewall-cmd --permanent --add-port=2375/tcp
sudo firewall-cmd --reload
```

### 检查3：DNS 解析

```bash
# 测试 DNS
nslookup registry-1.docker.io

# 如果失败，修改 /etc/resolv.conf
echo "nameserver 223.5.5.5" | sudo tee /etc/resolv.conf
```

### 检查4：Docker 服务状态

```bash
# 查看 Docker 状态
sudo systemctl status docker

# 查看 Docker 日志
sudo journalctl -u docker -f
```

---

## 💡 其他可用的镜像加速器

| 加速器 | 地址 | 说明 |
|--------|------|------|
| DaoCloud | https://docker.m.daocloud.io | 稳定可靠 |
| Huecker | https://huecker.io | 速度快 |
| TimeWeb | https://dockerhub.timeweb.cloud | 俄罗斯 |
| NooHub | https://noohub.ru | 俄罗斯 |
| 阿里云 | https://xxx.mirror.aliyuncs.com | 阿里云专属 |
| 腾讯云 | https://mirror.ccs.tencentyun.com | 腾讯云专属 |

---

## 🎯 最佳实践

1. **配置多个镜像源**（提高可用性）
2. **使用内网 DNS**（阿里云：100.100.2.136）
3. **定期清理缓存**：
   ```bash
   docker system prune -a -f
   ```
4. **监控 Docker 日志**：
   ```bash
   sudo journalctl -u docker -f
   ```

---

## 📝 常见问题

### Q1: 配置后需要重启容器吗？

**A:** 不需要，只需要重启 Docker 服务即可。

### Q2: 镜像加速器会影响已下载的镜像吗？

**A:** 不会，只影响新拉取的镜像。

### Q3: 如何临时使用代理？

**A:** 
```bash
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
docker pull python:3.11-slim
```

### Q4: 如何在 CI/CD 中配置？

**A:** 在 CI 脚本开头添加：
```bash
sudo mkdir -p /etc/docker
sudo cat > /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": ["https://docker.m.daocloud.io"]
}
EOF
sudo systemctl restart docker
```

---

**祝部署顺利！** 🚀
