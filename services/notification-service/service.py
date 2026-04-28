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
