# CoreLib v1 → v2 API 迁移映射表

> 自动生成于 2026-04-28
> 来源: OpenAPI Spec Diff + 迁移指南
> 适用于: 所有依赖 corelib 的微服务

## 一、auth 模块

| v1 调用 | v2 调用 | 迁移策略 | 难度 |
|---------|---------|----------|------|
| `auth.authenticate(token, secret)` | `auth.login(secret, token, scope="default")` | 交换参数顺序 + 加默认值 | ⭐ 简单 |
| `auth.check_permission(user, resource, action)` | `auth.has_permission(user_id=user["id"], resource=resource, action=action)` | 改为关键字参数, 提取user_id | ⭐⭐ 中等 |
| `auth.get_current_user(request_headers)` | `auth.get_user_from_request(request, include_profile=False)` | 参数改名 + 加默认值 | ⭐ 简单 |
| `auth.validate_session(session_id)` | `auth.session.is_valid(session_id, ttl=3600)` | 移入子模块 + 加默认值 | ⭐ 简单 |

## 二、data 模块

| v1 调用 | v2 调用 | 迁移策略 | 难度 |
|---------|---------|----------|------|
| `data.query(sql, params)` | `data.query_builder.select(...)` | 需重写为构建器模式 | ⭐⭐⭐ 复杂 |
| `data.execute(sql, params)` | `data.query_builder.execute(statement)` | 需重构 | ⭐⭐⭐ 复杂 |
| `data.fetch_one(table, where)` | `data.repository.get_one(table, filters=where)` | 参数名映射 | ⭐ 简单 |
| `data.fetch_all(table, where)` | `data.repository.list(table, filters=where)` | 参数名映射 | ⭐ 简单 |
| `data.get_connection(db_name)` | `data.get_connection(pool_name=db_name)` | 参数重命名 | ⭐ 简单 |

## 三、messaging 模块

| v1 调用 | v2 调用 | 迁移策略 | 难度 |
|---------|---------|----------|------|
| `messaging.send_message(queue, body, priority)` | `messaging.queue.publish(queue, body={"text": body})` | 结构体包裹 | ⭐⭐ 中等 |
| `messaging.create_queue(name, dlq)` | `messaging.queue.create(name, dead_letter=dlq)` | 参数重命名 | ⭐ 简单 |
| `messaging.publish_event(topic, event)` | `messaging.events.emit(topic, payload=event)` | 参数重命名 | ⭐ 简单 |

## 四、config 模块

| v1 调用 | v2 调用 | 迁移策略 | 难度 |
|---------|---------|----------|------|
| `config.get_config(key, default)` | `config.get_value(ConfigKey.XXX, fallback=default)` | key→枚举 + 参数重命名 | ⭐⭐ 中等 |
| `config.load_config_file(path)` | `config.load.from_yaml(path)` | 函数重命名 | ⭐ 简单 |
| `config.set_config(key, value)` | `config.set_value(ConfigKey.XXX, value)` | key→枚举 | ⭐⭐ 中等 |

## 五、logging 模块

| v1 调用 | v2 调用 | 迁移策略 | 难度 |
|---------|---------|----------|------|
| `logging.log_info(msg)` | `logging.logger.info(msg)` | 移入对象 | ⭐ 简单 |
| `logging.log_error(msg, exc)` | `logging.logger.error(msg, exception=exc)` | 移入对象 + 参数名 | ⭐ 简单 |
| `logging.log_warning(msg)` | `logging.logger.warning(msg)` | 移入对象 | ⭐ 简单 |

## 迁移策略优先级

1. **直接替换**: 参数顺序/名称改变 → 加默认值或交换顺序
2. **结构体包裹**: 参数从标量变为字典 → 包裹一层
3. **适配器模式**: 无法直接映射 → 写wrapper函数过渡
