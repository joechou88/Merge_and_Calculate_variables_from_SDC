import pandas as pd
import config

def filter_columns():
    try:
        print(f"正在讀取 {config.MERGED_OUTPUT}...")
        df = pd.read_excel(config.MERGED_OUTPUT)

        existing_cols = [col for col in config.TARGET_COLUMNS if col in df.columns]
        missing_cols = [col for col in config.TARGET_COLUMNS if col not in df.columns]

        if missing_cols:
            print(f"警告：以下欄位未在檔案中找到，將被跳過：\n{missing_cols}")

        df_filtered = df[existing_cols]

        df_filtered.to_excel(config.FILTERED_OUTPUT, index=False)
        print(f"\n篩選完成！剩餘欄位數量: {len(existing_cols)}")
        print(f"結果已儲存至: {config.FILTERED_OUTPUT}")

    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {config.MERGED_OUTPUT}，請確認該檔案與腳本在同一資料夾。")
    except Exception as e:
        print(f"發生意外錯誤: {e}")

if __name__ == "__main__":
    filter_columns()
