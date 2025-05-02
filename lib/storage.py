import json
import os
import traceback
from datetime import datetime
from config.settings import NOTIFICATIONS_DIR, LOGS_DIR, HISTORY_FILE
from models.notification import Notification

class Storage:
    def __init__(self):
        # 确保目录存在
        for directory in [NOTIFICATIONS_DIR, LOGS_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                
        # 加载历史记录
        self.history = self.load_history()
                
    def save_notification(self, notification, index):
        """保存通知到JSON文件"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        safe_title = "".join([c if c.isalnum() or c in " -_" else "_" for c in notification.title])
        safe_title = safe_title[:50]  # 限制长度
        filename = f"{NOTIFICATIONS_DIR}/notification_{timestamp}_{index}_{safe_title}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(notification.to_dict(), f, ensure_ascii=False, indent=4)
        
        print(f"通知已保存到: {filename}")
        
        # 记录到历史
        self.add_to_history(notification)
        
    def log_error(self, title, errors):
        """记录错误到日志文件"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(f"{LOGS_DIR}/log.md", 'a', encoding='utf-8') as f:
            f.write(f"\n## 错误 - {title} - {timestamp}\n\n")
            for error in errors:
                f.write(f"* {error}\n")
            f.write(f"* 详细堆栈信息: ```\n{traceback.format_exc()}```\n")
    
    def load_history(self):
        """加载历史记录"""
        history = {}
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except Exception as e:
                print(f"加载历史记录失败: {str(e)}")
        return history
    
    def save_history(self):
        """保存历史记录"""
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)
    
    def add_to_history(self, notification):
        """将通知添加到历史记录，只记录标题与时间"""
        key = notification.get_unique_key()
        self.history[key] = {
            "title": notification.title,
            "time": notification.time
        }
        self.save_history()
    
    def is_notification_in_history(self, notification):
        """检查通知是否在历史记录中"""
        key = notification.get_unique_key()
        return key in self.history
