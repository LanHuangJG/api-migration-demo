"""
Order Service - v1 API 调用
该服务使用了旧版CoreLib API，升级v2后编译全部失败
"""

from corelib import auth, data, messaging, config, logging


class OrderService:
    def __init__(self):
        # [SCAN-HIT] config.load_config_file - 需要迁移
        self.cfg = config.load_config_file("/etc/orders/config.yaml")
        self.db = data.get_connection("orders_db")

    def create_order(self, user_id: str, items: list):
        """创建订单"""
        sql = "INSERT INTO orders (user_id, status) VALUES (%s, 'pending')"
        # [SCAN-HIT] data.execute - 需要迁移
        result = data.execute(sql, (user_id,))

        # [SCAN-HIT] messaging.send_message - 需要迁移
        messaging.send_message("order_events", f"order_created:{user_id}")

        # [SCAN-HIT] logging.log_info - 需要迁移
        logging.log_info(f"Order created for user {user_id}")
        return result

    def get_order(self, order_id: int):
        """获取订单"""
        # [SCAN-HIT] data.fetch_one - 需要迁移
        return data.fetch_one("orders", {"id": order_id})

    def list_orders(self, user_id: str, status: str = None):
        """列出订单"""
        where = {"user_id": user_id}
        if status:
            where["status"] = status
        # [SCAN-HIT] data.fetch_all - 需要迁移
        return data.fetch_all("orders", where)

    def get_order_config(self):
        """获取订单配置"""
        # [SCAN-HIT] config.get_config - 需要迁移
        max_orders = config.get_config("orders.max_per_user", 100)
        # [SCAN-HIT] config.get_config - 需要迁移
        timeout = config.get_config("orders.timeout_ms", 5000)
        return {"max_orders": max_orders, "timeout": timeout}

    def notify_order_status(self, order_id: int, status: str):
        """通知订单状态变更"""
        event = {"order_id": order_id, "status": status}
        # [SCAN-HIT] messaging.publish_event - 需要迁移
        messaging.publish_event("order.status.changed", event)
        logging.log_info(f"Order {order_id} status: {status}")

    def validate_session(self, session_id: str):
        """验证会话"""
        # [SCAN-HIT] auth.validate_session - 需要迁移
        return auth.validate_session(session_id)
