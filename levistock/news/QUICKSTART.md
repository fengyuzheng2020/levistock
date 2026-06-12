# 快速开始 - 5分钟部署飞书推送服务

## 第一步：获取飞书机器人 Webhook URL

1. 打开飞书，进入要接收消息的群聊
2. 点击群设置（右上角）→ 添加机器人
3. 选择"自定义机器人"
4. 设置名称（如"股市资讯助手"），可选上传头像
5. 复制 **Webhook 地址**（类似：`https://open.feishu.cn/open-apis/bot/v2/hook/xxx`）
6. （可选）启用"签名验证"，复制签名密钥

## 第二步：配置服务

```bash
# 进入 news 目录
cd levistock/news/

# 复制配置模板
cp config_example.py config.py

# 编辑配置文件
vim config.py  # 或使用你喜欢的编辑器
```

修改以下内容：

```python
# 粘贴你的 Webhook URL
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN_HERE"

# 如果启用了签名验证，填写密钥；否则保持 None
FEISHU_SECRET = None  # 或 "your_secret"

# 其他配置使用默认值即可
```

保存并退出。

## 第三步：测试配置

```bash
# 运行测试脚本
python3 test_feishu_bot.py
```

如果看到：
```
[SUCCESS] 所有测试通过！✅
```

说明配置正确，飞书群里应该收到了测试消息。

如果失败，检查：
- Webhook URL 是否正确
- 网络连接是否正常
- 飞书机器人是否已添加到群聊

## 第四步：启动服务

### 方式一：前台运行（测试用）

```bash
python3 feishu_monitor_service.py
```

你会看到实时日志输出，按 `Ctrl+C` 停止。

### 方式二：后台运行（推荐）

```bash
# 添加执行权限
chmod +x background_service.sh

# 启动服务
./background_service.sh start

# 查看状态
./background_service.sh status

# 查看实时日志
tail -f cls_feishu_monitor.log
```

## 第五步：验证服务

等待几分钟，当财联社发布新的电报快讯时，飞书群会自动收到消息。

消息格式示例：
```
⏰ 时间: 2026-06-12 14:30:00
📰 标题: XX板块异动拉升，多股涨停
📝 内容: 今日盘中，XX板块表现强势...
---
```

## 常用命令

```bash
# 查看服务状态
./background_service.sh status

# 查看日志
tail -f cls_feishu_monitor.log

# 重启服务
./background_service.sh restart

# 停止服务
./background_service.sh stop
```

## 个性化配置（可选）

### 只关注重要消息

编辑 `config.py`：

```python
# 只推送加红重要消息
MESSAGE_CATEGORY = "important"  # 默认值
```

### 关键词过滤

只推送包含特定关键词的消息：

```python
# 只推送包含这些关键词的消息
KEYWORDS = ["涨停", "利好", "重组", "业绩"]
```

### 调整推送频率

```python
# 每60秒检查一次（更省资源）
POLL_INTERVAL = 60

# 每15秒检查一次（更及时）
POLL_INTERVAL = 15
```

## 常见问题

**Q: 收不到消息？**
- 确认有新消息产生（可以先手动调用 `news_telegraph_cls()` 测试）
- 检查日志文件是否有错误
- 确认 Webhook URL 正确

**Q: 消息太多？**
- 使用关键词过滤
- 增加轮询间隔
- 改为只推送"important"类型

**Q: 如何开机自启？**
- Linux: 使用 systemd 服务（见 FEISHU_SERVICE_README.md）
- Mac: 使用 launchd
- Windows: 使用任务计划程序

## 下一步

详细文档请查看：[FEISHU_SERVICE_README.md](FEISHU_SERVICE_README.md)

祝使用愉快！🎉
