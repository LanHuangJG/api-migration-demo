"""
Gateway Service - v1 API 调用
该服务使用了旧版CoreLib API，升级v2后编译全部失败
"""

from corelib import auth, data, config, logging


class GatewayService:
    def __init__(self):
        # [SCAN-HIT] config.load_config_file - 需要迁移
        self.cfg = config.load_config_file("/etc/gateway/config.yaml")
        # [SCAN-HIT] config.get_config - 需要迁移
        self.rate_limit = config.get_config("gateway.rate_limit", 100)
        # [SCAN-HIT] config.get_config - 需要迁移
        self.timeout = config.get_config("gateway.timeout_ms", 3000)

    def handle_request(self, request_headers: dict):
        """处理网关请求"""
        # [SCAN-HIT] auth.get_current_user - 需要迁移
        user = auth.get_current_user(request_headers)
        logging.log_info(f"Request from user: {user['name']}")
        return user

    def authenticate_request(self, token: str, secret: str):
        """网关认证"""
        # [SCAN-HIT] auth.authenticate - 需要迁移
        result = auth.authenticate(token, secret)
        return result

    def validate_session(self, session_id: str):
        """验证网关会话"""
        # [SCAN-HIT] auth.validate_session - 需要迁移
        if not auth.validate_session(session_id):
            logging.log_warning("Session validation failed")
            return False
        return True

    def check_route_permission(self, user_id: str, route: str):
        """检查路由权限"""
        user = {"id": user_id, "role": "admin"}
        # [SCAN-HIT] auth.check_permission - 需要迁移
        return auth.check_permission(user, route, "access")

    def log_request(self, path: str, method: str):
        """记录请求日志"""
        # [SCAN-HIT] logging.log_info - 需要迁移
        logging.log_info(f"{method} {path}")

    def log_error(self, error: str):
        """记录错误日志"""
        # [SCAN-HIT] logging.log_error - 需要迁移
        logging.log_error(f"Gateway error: {error}")

    def update_rate_limit(self, new_limit: int):
        """更新限流配置"""
        # [SCAN-HIT] config.set_config - 需要迁移
        return config.set_config("gateway.rate_limit", new_limit)

    def get_route_config(self, route: str):
        """获取路由配置"""
        sql = "SELECT * FROM routes WHERE path = %s"
        # [SCAN-HIT] data.query - 需要迁移
        return data.query(sql, (route,))
