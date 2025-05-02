# 校园门户通知爬虫
基于中国社会科学院大学（UCASS）校园门户通知开发。

作为“社问”平台的基础性软件，该工具提供了一种方便的方式来获取校园通知，根本目的是定期自动更新DIFY的知识库。

一个用于自动爬取校园门户通知的工具，支持多页面爬取、通知去重、附件下载和无头模式运行。

## 📋 功能特点

- **自动登录**：使用配置的用户名和密码自动登录校园门户
- **多页面爬取**：支持批量爬取多个页面的通知
- **通知去重**：基于标题和时间检测重复通知，避免重复爬取
- **内容解析**：提取通知标题、时间、来源、类型和详细内容
- **附件链接**：自动爬取通知附带的文件下载链接
- **数据存储**：将爬取的通知保存为JSON格式
- **无头模式**：支持后台运行，不显示浏览器界面
- **灵活配置**：通过配置文件自定义爬虫行为

## 🗂️ 项目结构

```
campus_portal_scraper/
│
├── config/
│   ├── __init__.py
│   └── settings.py          # 配置信息
│
├── lib/
│   ├── __init__.py
│   ├── browser.py           # 浏览器相关功能
│   ├── storage.py           # 数据存储功能
│   └── scraper.py           # 爬虫核心逻辑
│
├── models/
│   ├── __init__.py
│   └── notification.py      # 通知数据模型
│
├── main.py                  # 程序入口
│
└── requirements.txt         # 项目依赖
```

## 🛠️ 安装与配置

### 1. 克隆仓库

```bash
git clone https://github.com/Unable-teenager/UCASS_University_Notification_Crawler.git
cd campus-portal-scraper
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置文件

修改 `config/settings.py` 文件，填入您的登录信息和其他配置：

推荐使用绝对路径以减少报错情况。

```python
# 网站URL
URL_LOGIN = ''  #校园门户登录地址
URL_NOTIFYLIST = '' #校园门户通知列表地址

# 登录凭据
USERNAME = '' #校园账号
PASSWORD = '' #密码

# 浏览器配置
CHROME_DATA_DIR = r'' #Chrome数据目录（推荐绝对地址）
```

## 🚀 使用方法

### 基本用法

```bash
# 普通模式（显示浏览器界面）
python main.py

# 无头模式（后台运行，不显示浏览器界面）
python main.py --headless
```

### 定时任务

您可以使用系统的计划任务工具（如cron、Windows任务计划程序）设置定期运行爬虫：

#### Linux (Cron)
```bash
# 每天上午10点运行爬虫
0 10 * * * cd /path/to/campus-portal-scraper && python main.py --headless
```

#### Windows (Task Scheduler)
创建一个批处理文件 `run_scraper.bat`：
```batch
cd /d "C:\path\to\campus-portal-scraper"
python main.py --headless
```

然后在任务计划程序中添加此批处理文件作为定时任务。

## 📊 输出结果

### 通知文件

爬取的通知将保存在 `notifications` 目录中，格式为JSON：

```json
{
  "title": "关于XX通知",
  "time": "2023-09-01",
  "source": "教务处",
  "type": "通知公告",
  "content": "通知详细内容...",
  "attachments": [
    {
      "name": "附件1.pdf",
      "url": "https://example.com/file1.pdf",
    }
  ]
}
```

### 历史记录

历史记录保存在 `history.json` 文件中，包含标题和时间信息：

```json
{
  "关于XX通知_2023-09-01": {
    "title": "关于XX通知",
    "time": "2023-09-01"
  }
}
```

## ⚠️ 重要事项

### 1. 初次登录

- 因为学校有设备认证，初次登录使用时需要输入验证码

### 2. 降低爬虫被检测概率

- 尝试调整随机延迟的范围
- 使用普通模式而非无头模式

### 3. 无头模式失效

某些网站可能会检测无头浏览器。如果遇到问题，请尝试：
- 使用普通模式进行爬取
- 修改 `browser.py` 中的无头模式配置，添加更多的伪装参数

## 🔧 高级配置

### 自定义浏览器选项

您可以在 `browser.py` 中修改 Chrome 选项，例如：

```python
# 添加代理
chrome_options.add_argument('--proxy-server=http://your-proxy:port')

# 禁用图片加载以提高速度
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
```

### 调整爬取页数

在 `scraper.py` 中修改爬取的页数：

```python
# 修改MAX_PAGES常量或添加命令行参数
```

## 📜 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 免责声明

本工具仅用于学习和研究目的，请遵守学校相关规定和法律法规，合理使用此工具。不当使用造成的任何后果由使用者自行承担。

---

希望这个工具能帮助您更方便地获取校园通知！如有问题或建议，欢迎提交 issue 或 pull request。
