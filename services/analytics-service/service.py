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
