#!/bin/bash
# Reset all service files to v1 state for fresh pipeline runs
cd "$(dirname "$0")"

cat > services/user-service/service.py << 'PYEOF'
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
PYEOF

cat > services/order-service/service.py << 'PYEOF'
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
PYEOF

cat > services/payment-service/service.py << 'PYEOF'
"""
Payment Service - v1 API 调用
该服务使用了旧版CoreLib API，升级v2后编译全部失败
"""

from corelib import auth, data, messaging, logging


class PaymentService:
    def __init__(self):
        self.db = data.get_connection("payments_db")

    def process_payment(self, user_id: str, amount: float):
        """处理支付"""
        # [SCAN-HIT] auth.check_permission - 需要迁移
        user = {"id": user_id, "role": "user"}
        if not auth.check_permission(user, "payment", "execute"):
            raise PermissionError("No payment permission")

        sql = "INSERT INTO payments (user_id, amount, status) VALUES (%s, %s, 'processing')"
        # [SCAN-HIT] data.execute - 需要迁移
        result = data.execute(sql, (user_id, amount))

        # [SCAN-HIT] messaging.send_message - 需要迁移
        messaging.send_message("payment_events", f"payment_processed:{amount}", priority=8)

        # [SCAN-HIT] logging.log_info - 需要迁移
        logging.log_info(f"Payment {amount} processed for user {user_id}")
        return result

    def refund(self, payment_id: int, amount: float):
        """退款"""
        sql = "UPDATE payments SET status = 'refunded', refund_amount = %s WHERE id = %s"
        # [SCAN-HIT] data.execute - 需要迁移
        return data.execute(sql, (amount, payment_id))

    def get_payment(self, payment_id: int):
        """获取支付记录"""
        # [SCAN-HIT] data.fetch_one - 需要迁移
        return data.fetch_one("payments", {"id": payment_id})

    def get_user_payments(self, user_id: str):
        """获取用户支付记录"""
        # [SCAN-HIT] data.fetch_all - 需要迁移
        return data.fetch_all("payments", {"user_id": user_id})

    def notify_refund(self, user_id: str, payment_id: int):
        """通知退款"""
        event = {"user_id": user_id, "payment_id": payment_id}
        # [SCAN-HIT] messaging.publish_event - 需要迁移
        messaging.publish_event("payment.refunded", event)
        logging.log_info(f"Refund notified: payment={payment_id}")
PYEOF

cat > services/notification-service/service.py << 'PYEOF'
"""
Notification Service - v1 API 调用
该服务使用了旧版CoreLib API，升级v2后编译全部失败
"""

from corelib import data, messaging, config, logging


class NotificationService:
    def __init__(self):
        # [SCAN-HIT] config.load_config_file - 需要迁移
        self.cfg = config.load_config_file("/etc/notifications/config.yaml")
        # [SCAN-HIT] config.get_config - 需要迁移
        self.queue_name = config.get_config("notifications.queue", "notify_default")

    def send_email(self, user_id: str, subject: str, body: str):
        """发送邮件通知"""
        # [SCAN-HIT] messaging.send_message - 需要迁移
        messaging.send_message(
            self.queue_name,
            f"email:{user_id}:{subject}",
            priority=3
        )
        logging.log_info(f"Email queued: {subject}")

    def send_push(self, user_id: str, message: str):
        """发送推送通知"""
        # [SCAN-HIT] messaging.send_message - 需要迁移
        messaging.send_message(
            self.queue_name,
            f"push:{user_id}:{message}",
            priority=5
        )

    def get_notification_history(self, user_id: str):
        """获取通知历史"""
        # [SCAN-HIT] data.fetch_all - 需要迁移
        return data.fetch_all("notifications", {"user_id": user_id})

    def get_notification(self, notif_id: int):
        """获取单条通知"""
        # [SCAN-HIT] data.fetch_one - 需要迁移
        return data.fetch_one("notifications", {"id": notif_id})

    def create_notification_queue(self):
        """创建通知队列"""
        # [SCAN-HIT] messaging.create_queue - 需要迁移
        return messaging.create_queue(self.queue_name, dlq=True)

    def log_error(self, error_msg: str):
        """记录错误"""
        # [SCAN-HIT] logging.log_error - 需要迁移
        logging.log_error(f"Notification error: {error_msg}")

    def log_warning(self, warn_msg: str):
        """记录警告"""
        # [SCAN-HIT] logging.log_warning - 需要迁移
        logging.log_warning(f"Notification warning: {warn_msg}")
PYEOF

cat > services/analytics-service/service.py << 'PYEOF'
"""
Analytics Service - v1 API 调用
该服务使用了旧版CoreLib API，升级v2后编译全部失败
"""

from corelib import data, config, logging


class AnalyticsService:
    def __init__(self):
        # [SCAN-HIT] config.load_config_file - 需要迁移
        self.cfg = config.load_config_file("/etc/analytics/config.yaml")
        # [SCAN-HIT] config.get_config - 需要迁移
        self.batch_size = config.get_config("analytics.batch_size", 1000)

    def run_report(self, report_type: str, params: dict):
        """运行报表"""
        sql = f"SELECT * FROM analytics WHERE type = %s AND date >= %s"
        # [SCAN-HIT] data.query - 需要迁移
        rows = data.query(sql, (report_type, params.get("since")))
        logging.log_info(f"Report {report_type} generated: {len(rows)} rows")
        return rows

    def aggregate_metrics(self, metric_name: str, date_range: tuple):
        """聚合指标"""
        sql = "SELECT SUM(value), COUNT(*) FROM metrics WHERE name = %s AND date BETWEEN %s AND %s"
        # [SCAN-HIT] data.query - 需要迁移
        return data.query(sql, (metric_name, date_range[0], date_range[1]))

    def save_metric(self, name: str, value: float):
        """保存指标"""
        sql = "INSERT INTO metrics (name, value) VALUES (%s, %s)"
        # [SCAN-HIT] data.execute - 需要迁移
        return data.execute(sql, (name, value))

    def get_config(self, key: str):
        """获取分析配置"""
        # [SCAN-HIT] config.get_config - 需要迁移
        return config.get_config(key)

    def set_config(self, key: str, value):
        """设置分析配置"""
        # [SCAN-HIT] config.set_config - 需要迁移
        return config.set_config(key, value)

    def get_user_events(self, user_id: str):
        """获取用户事件"""
        # [SCAN-HIT] data.fetch_all - 需要迁移
        return data.fetch_all("analytics_events", {"user_id": user_id})
PYEOF

cat > services/gateway-service/service.py << 'PYEOF'
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
PYEOF

cat > services/search-service/service.py << 'PYEOF'
"""
Search Service - v1 API 调用
该服务使用了旧版CoreLib API，升级v2后编译全部失败
"""

from corelib import data, config, messaging, logging


class SearchService:
    def __init__(self):
        # [SCAN-HIT] config.load_config_file - 需要迁移
        self.cfg = config.load_config_file("/etc/search/config.yaml")
        # [SCAN-HIT] config.get_config - 需要迁移
        self.index_name = config.get_config("search.index", "default_index")

    def search(self, query: str, filters: dict = None):
        """执行搜索"""
        # [SCAN-HIT] data.query - 需要迁移
        results = data.query(f"SELECT * FROM search_index WHERE text LIKE %s", (f"%{query}%",))
        logging.log_info(f"Search: '{query}' found {len(results)} results")
        return results

    def index_document(self, doc_id: str, content: str):
        """索引文档"""
        sql = "INSERT INTO search_index (doc_id, content) VALUES (%s, %s)"
        # [SCAN-HIT] data.execute - 需要迁移
        return data.execute(sql, (doc_id, content))

    def delete_document(self, doc_id: str):
        """删除文档"""
        sql = "DELETE FROM search_index WHERE doc_id = %s"
        # [SCAN-HIT] data.execute - 需要迁移
        return data.execute(sql, (doc_id,))

    def get_search_stats(self):
        """获取搜索统计"""
        # [SCAN-HIT] data.fetch_one - 需要迁移
        return data.fetch_one("search_stats", {})

    def get_all_indices(self):
        """获取所有索引"""
        # [SCAN-HIT] data.fetch_all - 需要迁移
        return data.fetch_all("search_indices")

    def notify_index_complete(self, index_name: str, doc_count: int):
        """通知索引完成"""
        event = {"index": index_name, "count": doc_count}
        # [SCAN-HIT] messaging.publish_event - 需要迁移
        messaging.publish_event("search.index_complete", event)

    def create_search_queue(self):
        """创建搜索队列"""
        # [SCAN-HIT] messaging.create_queue - 需要迁移
        return messaging.create_queue("search_queue", dlq=True)

    def log_search_error(self, error: str):
        """记录搜索错误"""
        # [SCAN-HIT] logging.log_error - 需要迁移
        logging.log_error(f"Search error: {error}")
PYEOF

cat > services/message-service/service.py << 'PYEOF'
"""
Message Service - v1 API 调用
该服务使用了旧版CoreLib API，升级v2后编译全部失败
"""

from corelib import auth, data, messaging, config, logging


class MessageService:
    def __init__(self):
        # [SCAN-HIT] config.load_config_file - 需要迁移
        self.cfg = config.load_config_file("/etc/messages/config.yaml")
        # [SCAN-HIT] config.get_config - 需要迁移
        self.max_msg_size = config.get_config("messages.max_size", 4096)
        self.db = data.get_connection("messages_db")

    def send_message(self, sender_id: str, recipient_id: str, body: str):
        """发送消息"""
        user = {"id": sender_id, "role": "user"}
        # [SCAN-HIT] auth.check_permission - 需要迁移
        auth.check_permission(user, "messages", "send")

        sql = "INSERT INTO messages (sender_id, recipient_id, body) VALUES (%s, %s, %s)"
        # [SCAN-HIT] data.execute - 需要迁移
        result = data.execute(sql, (sender_id, recipient_id, body))

        # [SCAN-HIT] messaging.send_message - 需要迁移
        messaging.send_message("msg_notifications", f"new_message:{recipient_id}")

        logging.log_info(f"Message sent: {sender_id} -> {recipient_id}")
        return result

    def get_messages(self, user_id: str, limit: int = 50):
        """获取消息列表"""
        # [SCAN-HIT] data.fetch_all - 需要迁移
        return data.fetch_all("messages", {"recipient_id": user_id})

    def get_message(self, msg_id: int):
        """获取单条消息"""
        # [SCAN-HIT] data.fetch_one - 需要迁移
        return data.fetch_one("messages", {"id": msg_id})

    def validate_user_session(self, session_id: str):
        """验证用户会话"""
        # [SCAN-HIT] auth.validate_session - 需要迁移
        return auth.validate_session(session_id)

    def get_user_info(self, request_headers: dict):
        """获取用户信息"""
        # [SCAN-HIT] auth.get_current_user - 需要迁移
        return auth.get_current_user(request_headers)

    def create_message_queue(self):
        """创建消息队列"""
        # [SCAN-HIT] messaging.create_queue - 需要迁移
        return messaging.create_queue("messages_main", dlq=True)

    def notify_message_sent(self, msg_id: int, recipient_id: str):
        """通知消息已发送"""
        event = {"msg_id": msg_id, "recipient_id": recipient_id}
        # [SCAN-HIT] messaging.publish_event - 需要迁移
        messaging.publish_event("message.sent", event)

    def update_max_size(self, new_size: int):
        """更新最大消息大小"""
        # [SCAN-HIT] config.set_config - 需要迁移
        return config.set_config("messages.max_size", new_size)

    def log_message_error(self, error: str):
        """记录消息错误"""
        # [SCAN-HIT] logging.log_error - 需要迁移
        logging.log_error(f"Message error: {error}")

    def log_queue_warning(self, msg: str):
        """记录队列警告"""
        # [SCAN-HIT] logging.log_warning - 需要迁移
        logging.log_warning(f"Message queue warning: {msg}")
PYEOF

echo "All 8 services reset to v1 state. Ready for pipeline run."
