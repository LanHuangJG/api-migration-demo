"""
CoreLib v1 - 旧版核心库 (被破坏性升级前的版本)

本模块模拟一个内部核心库，包含以下模块：
- auth: 认证鉴权
- data: 数据访问层
- messaging: 消息队列
- config: 配置管理
- logging: 日志
"""

# ============================================================
# auth 模块 - v1 API
# ============================================================

def authenticate(token: str, secret: str):
    """旧版认证: 两个位置参数"""
    return {"user_id": "u123", "role": "admin"}

def check_permission(user: dict, resource: str, action: str):
    """旧版权限检查: 三个位置参数"""
    return user.get("role") == "admin"

def get_current_user(request_headers: dict):
    """旧版获取用户: 单参数"""
    return {"id": "u123", "name": "test_user"}

def validate_session(session_id: str):
    """旧版会话验证"""
    return True


# ============================================================
# data 模块 - v1 API
# ============================================================

def query(sql: str, params: tuple = ()):
    """旧版查询: 直接传SQL字符串"""
    return [{"id": 1, "name": "test"}]

def execute(sql: str, params: tuple = ()):
    """旧版执行: 直接传SQL"""
    return {"affected_rows": 1}

def get_connection(db_name: str):
    """旧版获取连接"""
    return f"connection_to_{db_name}"

def fetch_one(table: str, where: dict):
    """旧版单条查询"""
    return {"id": 1, "value": "data"}

def fetch_all(table: str, where: dict = None):
    """旧版批量查询"""
    return [{"id": 1}, {"id": 2}]


# ============================================================
# messaging 模块 - v1 API
# ============================================================

def send_message(queue: str, body: str, priority: int = 5):
    """旧版发送消息: queue + body 位置参数"""
    return {"message_id": "msg_001"}

def create_queue(name: str, dlq: bool = False):
    """旧版创建队列"""
    return {"queue_arn": f"arn:queue:{name}"}

def publish_event(topic: str, event: dict):
    """旧版发布事件"""
    return {"event_id": "evt_001"}


# ============================================================
# config 模块 - v1 API
# ============================================================

def get_config(key: str, default=None):
    """旧版获取配置"""
    return f"value_of_{key}"

def load_config_file(path: str):
    """旧版加载配置文件"""
    return {"loaded": True, "path": path}

def set_config(key: str, value):
    """旧版设置配置"""
    return True


# ============================================================
# logging 模块 - v1 API
# ============================================================

def log_info(msg: str):
    """旧版info日志"""
    return f"[INFO] {msg}"

def log_error(msg: str, exc: Exception = None):
    """旧版error日志"""
    return f"[ERROR] {msg}"

def log_warning(msg: str):
    """旧版warning日志"""
    return f"[WARN] {msg}"
