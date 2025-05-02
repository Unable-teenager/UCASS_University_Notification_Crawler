class Notification:
    def __init__(self, title="", time="", source="", type="", content="", attachments=None):
        self.title = title
        self.time = time
        self.source = source
        self.type = type
        self.content = content
        self.attachments = attachments or []
        
    def to_dict(self):
        """将通知对象转换为字典"""
        return {
            "title": self.title,
            "time": self.time,
            "source": self.source,
            "type": self.type,
            "content": self.content,
            "attachments": self.attachments
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建通知对象"""
        return cls(
            title=data.get("title", ""),
            time=data.get("time", ""),
            source=data.get("source", ""),
            type=data.get("type", ""),
            content=data.get("content", ""),
            attachments=data.get("attachments", [])
        )
        
    def get_unique_key(self):
        """生成唯一标识用于检测重复通知，只使用标题和时间"""
        return f"{self.title}_{self.time}"
