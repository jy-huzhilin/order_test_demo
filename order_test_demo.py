import json
from datetime import datetime
from typing import Dict

import pandas as pd


class order_test_demo:
    """使用真实股票基础信息生成最小订单输出的 demo。"""

    input_name = "cbond.stock_basic_info"
    output_name = "demo_stock_target_order"

    def _to_dataframe(self, value):
        if hasattr(value, "to_pandas"):
            return value.to_pandas()
        if isinstance(value, pd.DataFrame):
            return value
        raise TypeError(f"{self.input_name} 必须是 DataFrame 或可转 DataFrame 的 Arrow 对象，实际类型: {type(value)}")

    def _build_order_rows(self, basic_info_df: pd.DataFrame, current_time: datetime) -> pd.DataFrame:
        if basic_info_df.empty:
            raise RuntimeError("cbond.stock_basic_info 输入为空，无法生成订单 demo")
        if "ths_code" not in basic_info_df.columns:
            raise RuntimeError("cbond.stock_basic_info 缺少 ths_code 字段")

        symbols = (
            basic_info_df["ths_code"]
            .dropna()
            .astype(str)
            .drop_duplicates()
            .sort_values()
            .head(3)
            .tolist()
        )
        if not symbols:
            raise RuntimeError("cbond.stock_basic_info 不包含可用的 ths_code")

        current_ts = pd.Timestamp(current_time).strftime("%Y-%m-%d %H:%M:%S")
        target_values = [1000000.0, 2000000.0, 3000000.0]
        rows = []
        for index, symbol in enumerate(symbols):
            rows.append(
                {
                    "time": current_ts,
                    "symbol": symbol,
                    "value": target_values[index],
                    "deal_settings": {
                        "account": "demo_stock_account",
                        "algo": "limit",
                        "market": "cn_stock",
                        "priority": index + 1,
                    },
                }
            )
        return pd.DataFrame(rows, columns=["time", "symbol", "value", "deal_settings"])

    def compute(self, input: Dict[str, object], current_time: datetime) -> Dict[str, pd.DataFrame]:
        basic_info_df = self._to_dataframe(input[self.input_name])
        result_df = self._build_order_rows(basic_info_df, current_time)
        return {self.output_name: result_df}
