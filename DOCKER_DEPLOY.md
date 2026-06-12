# Levistock Docker 部署指南

## 📋 目录结构

```
levistock/
├── Dockerfile              # Docker 镜像构建文件
├── deploy.sh               # 部署管理脚本
├── run_docker.sh           # 简化版启动脚本
├── .dockerignore           # Docker 忽略文件
├── config/                 # 宿主机配置目录（需要创建）
│   └── config.py          # 配置文件（从示例复制）
└── levistock/
    └── news/
        ├── config_example.py  # 配置示例文件
        └── unified_service.py # 统一服务入口
```

## 🚀 快速开始

### 1. 准备工作

确保已安装 Docker：

```bash
# 检查 Docker
docker --version
```

### 2. 首次部署

```bash
# 赋予脚本执行权限
chmod +x deploy.sh

# 启动服务（会自动创建配置目录和示例配置）
./deploy.sh start
```

编辑配置文件：

```bash
vim config/config.py
```

修改以下配置：

```python
# 飞书机器人 Webhook URL（必填）
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN_HERE"

# 飞书签名密钥（如果启用了签名验证）
FEISHU_SECRET = None  # 或 "your_secret_here"

# 功能开关
ENABLE_NEWS_MONITOR = True      # 电报快讯监控
ENABLE_MARKET_REPORT = False    # 市场数据播报
ENABLE_MARKET_WIND = False      # 风口板块播报
ENABLE_YICAI_MONITOR = False    # 第一财经快讯
ENABLE_SINA_MONITOR = False     # 新浪财经快讯
ENABLE_EM_MONITOR = False       # 东方财富快讯
```

### 3. 重新加载配置

修改配置后，无需重新构建镜像，只需重启容器：

```bash
# 方法1：使用部署脚本（推荐）
./deploy.sh reload

# 方法2：手动重启
docker restart levistock-service
```

## 📖 常用命令

```bash
./deploy.sh start
```

### 停止服务

```bash
./deploy.sh stop
```

### 重启服务

```bash
./deploy.sh restart
```

### 查看日志

```bash
# 实时查看日志
./deploy.sh logs

# 查看最近100行日志
docker logs --tail 100 levistock-service
```

### 查看状态

```bash
./deploy.sh status
```

### 重新构建

```bash
./deploy.sh rebuild
```

### 清理资源

```bash
./deploy.sh cleanup
```

## 🔧 配置说明

### 配置文件映射原理

`deploy.sh` 中的 docker run 命令：

```bash
docker run -d \
    --name levistock-service \
    -v $(pwd)/config/config.py:/app/levistock/news/config.py:ro \
    ...
```

- `./config`：宿主机的配置目录
- `/app/levistock/news/config.py`：容器内的配置文件路径
- `:ro`：只读模式（read-only），容器内无法修改

**工作流程：**
1. 在宿主机修改 `config/config.py`
2. 运行 `./deploy.sh reload` 重启容器
3. 容器启动时自动读取新的配置文件

### 环境变量配置

可以在 `deploy.sh` 或 `run_docker.sh` 中设置环境变量：

```bash
-e TZ=Asia/Shanghai              # 时区设置
-e PYTHONUNBUFFERED=1            # Python 输出不缓冲
-e FEISHU_WEBHOOK_URL=xxx        # 通过环境变量传递配置
```

### 日志持久化

如果需要保存日志到宿主机，可以添加日志卷：

```bash
-v $(pwd)/logs:/app/logs
```

## 🐛 故障排查

### 1. 容器启动失败

```bash
# 查看容器日志
docker logs levistock-service

# 查看容器状态
docker ps -a | grep levistock
```

### 2. 配置文件错误

```bash
# 验证配置文件语法
cd config
python3 -c "import config"
```

### 3. 网络连接问题

```bash
# 进入容器内部测试网络
docker exec -it levistock-service bash
ping www.baidu.com
```

### 4. 资源不足

调整 `deploy.sh` 或 `run_docker.sh` 中的资源限制：

```bash
--cpus=2.0      # 增加 CPU 限制
--memory=1G     # 增加内存限制
```

## 📊 监控和维护

### 查看资源使用

```bash
# 实时资源使用
docker stats levistock-service

# 容器详细信息
docker inspect levistock-service
```

### 备份配置

```bash
# 备份配置文件
cp config/config.py config/config.py.bak.$(date +%Y%m%d)
```

### 更新代码

```bash
# 拉取最新代码
git pull

# 重新构建并启动
./deploy.sh rebuild
```

## 🔐 安全建议

1. **不要提交敏感信息到 Git**
   ```bash
   # 确保 config/config.py 在 .gitignore 中
   echo "config/config.py" >> .gitignore
   ```

2. **使用 Docker Secret 管理敏感配置**（生产环境）

3. **定期更新基础镜像**
   ```bash
   docker pull python:3.11-slim
   ./deploy.sh rebuild
   ```

4. **限制容器权限**
   ```bash
   # 在 docker run 命令中添加
   --security-opt no-new-privileges:true \
   --read-only
   ```

## 🎯 高级用法

### 多环境配置

创建不同环境的配置文件：

```bash
config/
├── config.dev.py      # 开发环境
├── config.test.py     # 测试环境
└── config.prod.py     # 生产环境
```

修改 `deploy.sh` 或 `run_docker.sh` 中的卷映射：

```bash
-v $(pwd)/config/config.prod.py:/app/levistock/news/config.py:ro
```

### 使用 Docker Swarm（可选）

```bash
# 初始化 Swarm
docker swarm init

# 创建 docker-compose.yml 用于 Swarm
cat > docker-stack.yml << 'EOF'
version: '3.8'
services:
  levistock:
    image: levistock:latest
    volumes:
      - ./config/config.py:/app/levistock/news/config.py:ro
EOF

# 部署服务
docker stack deploy -c docker-stack.yml levistock
```

### 自动化部署

结合 CI/CD 工具（如 Jenkins、GitLab CI）实现自动化部署。

## 📞 支持

如有问题，请查看：
- 项目 README
- Docker 官方文档
- 提交 Issue

---

**祝使用愉快！** 🎉
