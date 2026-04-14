# order_test_demo

最小 order 流程测试项目。

这个 demo 使用 `basic_data_db.cbond.stock_basic_info` 读取真实股票标的代码，
并生成一批标准 order DataFrame，用于验证：

- 项目配置可以被当前系统识别
- `output.type = "order"` 能正确路由到订单批次存储
- 生成结果符合 `time/symbol/value/deal_settings` 的固定订单格式
