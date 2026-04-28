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
