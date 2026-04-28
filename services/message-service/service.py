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
