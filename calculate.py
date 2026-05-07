import pandas as pd
import numpy as np
import config

df = pd.read_excel(config.FILTERED_OUTPUT)
underwriter_df = pd.read_excel(config.TOP25_UNDERWRITERS)
top_25_underwriters = set(underwriter_df.iloc[:, 0].dropna().astype(str).str.upper().unique())

print(f"Columns in filtered SDC file: {df.columns.tolist()}\n")
print(f"Top 25 underwriters between {config.START_YEAR} and {config.END_YEAR}:\n{top_25_underwriters}\n")

def get_col(df, name):
    return df[name] if name in df.columns else pd.Series([np.nan] * len(df))

# 1. Underpricing
df['Underpricing'] = get_col(df, 'Percent Change Offer Price to Closing Price at Offer/First Trade')

# 2. Ln_Age
issue_date = pd.to_datetime(get_col(df, 'Dates: Issue Date'), errors='coerce')
founded_date = pd.to_datetime(get_col(df, 'Issuer/Borrower Founded Date'), errors='coerce')
age = (issue_date - founded_date).dt.days / 365.25
df['Ln_Age'] = age.apply(lambda x: np.log1p(x) if pd.notna(x) and x >= 0 else (np.nan if pd.isna(x) else 0))

# # 3. Relative_Offer_Size
# proceeds = pd.to_numeric(get_col(df, 'Proceeds Amount All Markets (USD Millions)'), errors='coerce')
# assets = pd.to_numeric(get_col(df, 'Financials: Total Assets Before Offering (USD Millions)'), errors='coerce')
# df['Relative_Offer_Size'] = proceeds / assets

# 4. VC_backed
def check_vc_backed(x):
    if pd.isna(x) or str(x).strip() == '':
        return np.nan
    return 1 if str(x).strip().upper() in ['TRUE', '1', '1.0', 'YES', 'Y'] else 0
df['VC_backed'] = get_col(df, 'Venture Capital Backed IPO Issue Flag').apply(check_vc_backed)

# 5. Firm_Commitment
def check_firm_commitment(tech):
    if pd.isna(tech):
        return np.nan
    tech_str = str(tech).upper().replace(" ", "")
    return 1 if 'FIRMCOMMITMENT' in tech_str else 0
df['Firm Commitment'] = get_col(df, 'Offering Technique').apply(check_firm_commitment)

# 6. Underwriter_Reputation
def check_reputation(bookrunner):
    if pd.isna(bookrunner) or str(bookrunner).strip() == '': 
        return np.nan
    b_str = str(bookrunner).upper()
    for top_bank in top_25_underwriters:
        if top_bank in b_str: return 1
    return 0
df['Underwriter_Reputation'] = get_col(df, 'Bookrunner').apply(check_reputation)

# 7. Integer_Offer_Price
def is_integer_price(price):
    if pd.isna(price): return np.nan
    try:
        val = float(price)
        return 1 if round(val, 6).is_integer() else 0
    except (ValueError, TypeError) as e:
        print(f"Warning: Cannot convert '{price}' to float. Error: {e}")
        return np.nan
df['Integer_Offer_Price'] = get_col(df, 'Offer Price (USD)').apply(is_integer_price)

#  一間公司在同一年分好幾天可能有好幾筆紀錄，需合併為一筆並決定各欄位適合的計算方式
df['Proceeds_Amount_All_Markets'] = pd.to_numeric(get_col(df, 'Proceeds Amount All Markets (USD Millions)'), errors='coerce')
df['Assets_Raw'] = pd.to_numeric(get_col(df, 'Financials: Total Assets Before Offering (USD Millions)'), errors='coerce')
df = df.sort_values(by=['ISIN', 'Dates: Issue Date'])

def get_main_isin(group):
    if group['ISIN'].dropna().empty:
        return np.nan
    return group['ISIN'].value_counts().idxmax()

isin_mapping = df.dropna(subset=['ISIN', 'Issuer/Borrower SEDOL']).groupby('Issuer/Borrower SEDOL').apply(get_main_isin, include_groups=False).to_dict()
df['ISIN'] = df['Issuer/Borrower SEDOL'].map(isin_mapping).fillna(df['ISIN'])

group_keys = ['ISIN', 'Dates: Offer Year (CCYY)']
df_grouped = df.groupby(group_keys).agg({
    'Underpricing': 'first',                # 取當年的第一筆紀錄
    'Ln_Age': 'first',                      # 通常年齡在同一年內不會差異太大，取第一筆
    'VC_backed': 'max',                     # 其中一筆是 1 即為 1，通常不會忽 0 忽 1
    'Firm Commitment': 'max',               # 其中一筆是 1 即為 1，通常不會忽 0 忽 1
    'Underwriter_Reputation': 'max',        # 其中一筆是 1 即為 1，通常不會忽 0 忽 1
    'Integer_Offer_Price': 'max',           # 其中一筆是 1 即為 1，通常不會忽 0 忽 1
    'Proceeds_Amount_All_Markets': 'sum',   # 加總當年所有 Proceeds_Amount，作為 Relative_Offer_Size 的分子
    'Assets_Raw': 'first',                  # 取當年第一筆期初總資產，作為 Relative_Offer_Size 的分母
    'Issuer/Borrower SEDOL': 'first',
    'Datastream': 'first'
}).reset_index()

df_grouped['Relative_Offer_Size'] = df_grouped['Proceeds_Amount_All_Markets'] / df_grouped['Assets_Raw']
# Since Stata cannot handle inf, we change inf to nan
df_grouped['Relative_Offer_Size'] = df_grouped['Relative_Offer_Size'].replace([np.inf, -np.inf], np.nan)

calculated_cols = ['Underpricing', 'Ln_Age', 'Relative_Offer_Size', 'VC_backed', 
                   'Firm Commitment', 'Underwriter_Reputation', 'Integer_Offer_Price']
id_cols = ['Issuer/Borrower SEDOL', 'ISIN', 'Datastream']
year_col = ['Dates: Offer Year (CCYY)']
output_cols = calculated_cols + id_cols + year_col

df_grouped = df_grouped[output_cols]
df_grouped.to_excel(config.CALCULATED_OUTPUT, index=False)
print(f"結果已儲存至: {config.CALCULATED_OUTPUT}")
