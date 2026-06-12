# 新浪财经快讯功能实现总结

## 概述

已成功实现新浪财经（finance.sina.com.cn）快讯的拉取和飞书推送功能，与第一财经、财联社保持一致的设计。

## 已完成的功能

### 1. 核心数据接口

**文件**: `levistock/news/news_sina.py`

- ✅ 实现了 `news_brief_sina()` 函数
- ✅ 支持自定义获取数量（默认20条）
- ✅ 自动处理分页请求
- ✅ **特殊处理 JSONP 格式响应**
- ✅ 返回标准化的数据结构
- ✅ 包含完整的 docstring 和使用示例

**关键技术点**:
```python
def _parse_jsonp(text: str) -> dict:
    """解析 JSONP 响应"""
    # 提取 JSON 部分：去除 callback 函数包裹
    match = re.search(r'\((\{.*\})\);?\s*$', text, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json.loads(json_str)
```

**返回字段**:
```python
{
    "id": 4932293,                    # 快讯ID
    "title": "云南发行7年期棚改...",   # 标题（从标签提取）
    "content": "云南发行7年期...",     # 正文内容（Unicode解码）
    "time": "2026-06-12 16:44:22",    # 发布时间
    "source": "其他",                  # 来源分类
    "view_num": "4.38万 阅读"         # 阅读量
}
```

### 2. 飞书推送监控服务

**文件**: `levistock/news/sina_monitor.py`

- ✅ 实现了 `SinaBriefMonitor` 类
- ✅ 支持定时轮询检测新消息
- ✅ 自动去重（基于消息ID）
- ✅ 支持关键词过滤
- ✅ 支持自定义过滤函数
- ✅ 富文本消息格式化（包含时间、标题、内容、来源、阅读量）
- ✅ 详细DEBUG日志输出
- ✅ 优雅的服务启停控制

**消息格式**:
```
⏰ 时间: 2026-06-12 16:44:22
📰 标题: 其他
📝 内容: 云南发行7年期棚改专项地方债...
ℹ️  来源: 其他 | 4.38万 阅读
🔗 来源: 新浪财经
---
```

### 3. 配置文件更新

**文件**: `levistock/news/config.py`

新增配置项：
```python
ENABLE_SINA_MONITOR = False      # 是否开启监控
SINA_POLL_INTERVAL = 30          # 轮询间隔（秒）
SINA_KEYWORDS = None             # 关键词过滤
```

### 4. 统一服务集成

**文件**: `levistock/news/unified_service.py`

- ✅ 新增 `run_sina_monitor()` 函数
- ✅ 在主函数中集成新浪财经监控
- ✅ 支持与其他服务并行运行
- ✅ 显示配置信息和状态

**可与其他服务同时运行**:
- 财联社电报监控
- 市场数据播报
- 风口板块播报
- 第一财经快讯监控
- 新浪财经快讯监控 ⭐ 新增

### 5. SDK 导出

**文件**: `levistock/__init__.py`

- ✅ 导出 `news_brief_sina` 函数
- ✅ 添加到 `__all__` 列表

**使用方式**:
```python
import levistock as lk
data = lk.news_brief_sina()
```

### 6. 测试文件

**文件**: `tests/test_news_sina.py`

- ✅ 基础功能测试
- ✅ 自定义数量测试
- ✅ 数据结构验证
- ✅ 完整的错误处理

### 7. 文档

**文件**: `README.md`

- ✅ 在接口文档表格中添加新浪财经快讯
- ✅ 添加详细的使用说明和参数说明
- ✅ 提供代码示例

## 技术特点

### 1. JSONP 格式处理

新浪财经 API 返回的是 **JSONP 格式**，不是标准 JSON：

```javascript
jQuery111209202656311626936_1781253850003({...});
```

解决方案：
- 使用正则表达式提取 JSON 部分
- 去除 callback 函数包裹
- 解析纯 JSON 数据

### 2. Unicode 转义解码

API 返回的内容包含 Unicode 转义字符：

```
"\u4e91\u5357\u53d1\u884c..." 
```

解决方案：
```python
content = rich_text.encode().decode('unicode_escape')
```

### 3. 动态 callback 参数

每次请求需要生成唯一的 callback 参数：

```python
"callback": f"jQuery{int(time.time() * 1000)}"
```

### 4. 嵌套数据结构解析

响应结构较深：
```
result.data.feed.list[]
```

需要逐层安全访问：
```python
result = data.get("result", {})
feed_data = result.get("data", {}).get("feed", {})
feed_list = feed_data.get("list", [])
```

## 使用方法

### 方式一：API调用

```python
import levistock as lk

# 获取最新快讯
data = lk.news_brief_sina(limit=20)

# 处理数据
for item in data:
    print(f"[{item['time']}] {item['title']}")
    print(f"  来源: {item['source']}")
    print(f"  阅读: {item['view_num']}")
```

### 方式二：单独运行监控服务

```bash
cd levistock/news
python sina_monitor.py
```

需要先配置 `config.py` 中的飞书 Webhook URL。

### 方式三：统一服务（推荐）

编辑 `config.py`:
```python
ENABLE_SINA_MONITOR = True
SINA_POLL_INTERVAL = 30
SINA_KEYWORDS = ["涨停", "利好"]  # 可选
```

运行：
```bash
cd levistock/news
python unified_service.py
```

## 注意事项

1. **JSONP 格式**: API 返回 JSONP 而非 JSON，已自动处理
2. **Unicode 解码**: 内容中的 Unicode 转义字符会自动解码
3. **轮询间隔**: 建议设置为 30-60 秒，避免频繁请求
4. **历史消息**: 服务启动时会加载最近20条历史消息，避免重复推送
5. **标题提取**: 如果没有标签，会使用内容前50个字符作为标题

## 与其他新闻源对比

| 特性 | 财联社 | 第一财经 | 新浪财经 |
|------|--------|----------|----------|
| API 格式 | JSON | JSON | **JSONP** ⚠️ |
| 数据解析 | 简单 | 简单 | **需特殊处理** |
| Unicode | 正常 | 正常 | **需解码** ⚠️ |
| 标题字段 | title | LiveTitle | tag.name |
| 内容字段 | content | LiveContent | rich_text |
| 时间字段 | ctime | CreateDate | create_time |
| 来源标识 | - | IsImportant | tag |
| 阅读量 | - | - | view_num ✅ |

## 文件清单

```
levistock/
├── news/
│   ├── news_sina.py                     # 核心数据接口 ⭐ 新增
│   ├── sina_monitor.py                  # 飞书推送监控 ⭐ 新增
│   ├── config.py                        # 配置文件（已更新）
│   └── unified_service.py               # 统一服务（已更新）
├── __init__.py                          # SDK导出（已更新）
tests/
└── test_news_sina.py                   # 测试文件 ⭐ 新增
README.md                                # 主文档（已更新）
```

## 总结

✅ 所有功能已完整实现  
✅ 代码质量良好，无语法错误  
✅ 文档齐全，易于使用  
✅ 与现有代码风格保持一致  
✅ 支持外部调用和飞书推送  
✅ **特殊处理 JSONP 格式和 Unicode 解码**  

可以立即投入使用！🎉
