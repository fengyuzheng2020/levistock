# Levistock Docker 快速参考

## 📦 文件清单

| 文件 | 说明 |
|------|------|
| `Dockerfile` | Docker 镜像构建文件 |
| `deploy.sh` | 部署管理脚本（推荐） |
| `run_docker.sh` | 简化版启动脚本 |
| `.dockerignore` | Docker 忽略文件 |
| `config/` | 宿主机配置目录 |

## 🚀 一键部署

### 方法1：使用 deploy.sh（推荐）

```bash
# 首次部署
chmod +x deploy.sh
./deploy.sh start

# 修改配置后重新加载
vim config/config.py
./deploy.sh reload
```

### 方法2：使用 run_docker.sh（简化版）

```bash
chmod +x run_docker.sh
./run_docker.sh
```

## 🔧 常用命令速查

```bash
# 启动
./deploy.sh start

# 停止
./deploy.sh stop

# 重启
./deploy.sh restart

# 查看日志
./deploy.sh logs

# 查看状态
./deploy.sh status

# 重新构建
./deploy.sh rebuild

# 清理资源
./deploy.sh cleanup
```

## 📝 配置修改流程

```bash
# 1. 编辑配置文件
vim config/config.py

# 2. 验证配置（可选）
cd config && python3 -c "import config"

# 3. 重新加载
./deploy.sh reload

# 4. 查看日志确认
docker logs -f levistock-service
```

## 🐛 故障排查

```bash
# 查看容器状态
docker ps -a | grep levistock

# 查看日志
docker logs levistock-service

# 进入容器调试
docker exec -it levistock-service bash

# 查看资源使用
docker stats levistock-service
```

## 💡 提示

- ✅ 配置文件映射：`config/config.py` → 容器内自动读取
- ✅ 修改配置后只需重启，无需重新构建镜像
- ✅ 日志自动轮转，最多保留 3 个文件，每个 10MB
- ✅ 容器自动重启策略：`unless-stopped`

---

详细文档见：[DOCKER_DEPLOY.md](DOCKER_DEPLOY.md)
