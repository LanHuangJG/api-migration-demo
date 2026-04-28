"""
User Service - v1 API 调用
该服务使用了旧版CoreLib API，升级v2后编译全部失败
"""

from corelib import auth, data, logging


class UserService:
    def __init__(self, db_name: str):
        self.conn = data.get_connection(db_name)

    def login(self, token: str, secret: str):
        """用户登录"""
        # [SCAN-HIT] auth.authenticate - 需要迁移
        user = auth.authenticate(token, secret)
        logging.log_info(f"User logged in: {user['user_id']}")
        return user

    def get_profile(self, request_headers: dict):
        """获取用户资料"""
        # [SCAN-HIT] auth.get_current_user - 需要迁移
        user = auth.get_current_user(request_headers)
        # [SCAN-HIT] data.fetch_one - 需要迁移
        profile = data.fetch_one("user_profiles", {"user_id": user["id"]})
        return profile

    def update_profile(self, user_id: str, updates: dict):
        """更新用户资料"""
        sql = "UPDATE user_profiles SET name = %s WHERE user_id = %s"
        # [SCAN-HIT] data.execute - 需要迁移
        result = data.execute(sql, (updates.get("name"), user_id))
        return result

    def list_users(self, role: str = None):
        """列出用户"""
        where = {"role": role} if role else None
        # [SCAN-HIT] data.fetch_all - 需要迁移
        return data.fetch_all("users", where)

    def check_admin(self, user_id: str, resource: str):
        """检查管理员权限"""
        user = {"id": user_id, "role": "admin"}
        # [SCAN-HIT] auth.check_permission - 需要迁移
        return auth.check_permission(user, resource, "read")
