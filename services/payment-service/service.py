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
