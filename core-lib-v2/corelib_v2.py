"""
CoreLib v2 - 新版核心库 (破坏性升级后的版本)

破坏性变更清单：
1. auth.authenticate -> auth.login (参数顺序改变)
2. auth.check_permission -> auth.has_permission (参数名改变)
3. auth.get_current_user -> auth.get_user_from_request (新增必填参数)
4. auth.validate_session -> auth.session.is_valid (移入子模块)
5. data.query -> data.query_builder.select (不再支持原始SQL)
6. data.execute -> data.query_builder.execute
7. data.fetch_one -> data.repository.get_one
8. data.fetch_all -> data.repository.list
9. messaging.send_message -> messaging.queue.publish (参数改为对象)
10. messaging.publish_event -> messaging.events.emit (参数签名改变)
11. config.get_config -> config.get_value (key改为枚举)
12. config.load_config_file -> config.load.from_yaml
13. logging.log_info -> logging.logger.info (移入logger对象)
14. logging.log_error -> logging.logger.error
15. logging.log_warning -> logging.logger.warning
"""

# ============================================================
# auth 模块 - v2 API
# ============================================================

def login(secret: str, token: str, scope: str = "default"):
    """v2: 参数顺序反转, 新增scope参数"""
    return {"user_id": "u123", "role": "admin", "scope": scope}

def has_permission(*, user_id: str, resource: str, action: str):
    """v2: 改为关键字参数, user替代user对象"""
    return True

def get_user_from_request(request: dict, include_profile: bool = False):
    """v2: 参数从headers改为request对象, 新增include_profile"""
    return {"id": "u123", "name": "test_user"}

class session:
    @staticmethod
    def is_valid(session_id: str, ttl: int = 3600):
        """v2: 移入session子模块, 新增ttl参数"""
        return True


# ============================================================
# data 模块 - v2 API
# ============================================================

class query_builder:
    @staticmethod
    def select(table: str, columns: list = None, where: dict = None, limit: int = 100):
        """v2: 替代原始SQL, 改为构建器模式"""
        return f"SELECT * FROM {table}"

    @staticmethod
    def execute(statement):
        """v2: 替代execute(sql, params)"""
        return {"affected_rows": 1}


class repository:
    @staticmethod
    def get_one(table: str, filters: dict, include: list = None):
        """v2: 替代fetch_one"""
        return {"id": 1, "value": "data"}

    @staticmethod
    def list(table: str, filters: dict = None, pagination: dict = None):
        """v2: 替代fetch_all, 新增pagination参数"""
        return [{"id": 1}, {"id": 2}]


def get_connection(pool_name: str, config: dict = None):
    """v2: 参数名和签名改变"""
    return f"pool:{pool_name}"


# ============================================================
# messaging 模块 - v2 API
# ============================================================

class queue:
    @staticmethod
    def publish(name: str, body: dict, options: dict = None):
        """v2: body从str改为dict, 参数顺序改变"""
        return {"message_id": "msg_001"}

    @staticmethod
    def create(name: str, dead_letter: bool = False, retention: int = 86400):
        """v2: dlq改为dead_letter, 新增retention"""
        return {"queue_arn": f"arn:queue:{name}"}


class events:
    @staticmethod
    def emit(topic: str, payload: dict, metadata: dict = None):
        """v2: event改为payload, 新增metadata"""
        return {"event_id": "evt_001"}


# ============================================================
# config 模块 - v2 API
# ============================================================

class ConfigKey:
    """v2: 新增枚举"""
    DATABASE_URL = "database.url"
    CACHE_TTL = "cache.ttl"
    API_ENDPOINT = "api.endpoint"

def get_value(key: ConfigKey, fallback=None):
    """v2: key必须是ConfigKey枚举, default改为fallback"""
    return f"value_of_{key}"

class load:
    @staticmethod
    def from_yaml(path: str, encoding: str = "utf-8"):
        """v2: 替代load_config_file, 新增encoding"""
        return {"loaded": True, "path": path}

def set_value(key: ConfigKey, value):
    """v2: key改为ConfigKey枚举"""
    return True


# ============================================================
# logging 模块 - v2 API
# ============================================================

class logger:
    @staticmethod
    def info(message: str, context: dict = None):
        """v2: 移入logger对象, 新增context"""
        return f"[INFO] {message}"

    @staticmethod
    def error(message: str, exception: Exception = None, trace: bool = False):
        """v2: exc改为exception, 新增trace"""
        return f"[ERROR] {message}"

    @staticmethod
    def warning(message: str, context: dict = None):
        """v2: 移入logger对象"""
        return f"[WARN] {message}"

    @staticmethod
    def debug(message: str, context: dict = None):
        """v2: 新增"""
        return f"[DEBUG] {message}"
