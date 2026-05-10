import pandas as pd
import numpy as np
import config

df = pd.read_excel(config.UNIQUE_OUTPUT)
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

# 3. Relative_Offer_Size
proceeds = pd.to_numeric(get_col(df, 'Proceeds Amount All Markets (USD Millions)'), errors='coerce')
assets = pd.to_numeric(get_col(df, 'Financials: Total Assets Before Offering (USD Millions)'), errors='coerce')
df['Relative_Offer_Size'] = proceeds / assets
df['Relative_Offer_Size'] = df['Relative_Offer_Size'].replace([np.inf, -np.inf], np.nan)    # Replace infinite values with NaN since Stata cannot handle inf

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
df['Firm_Commitment'] = get_col(df, 'Offering Technique').apply(check_firm_commitment)

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

calculated_cols = ['Underpricing', 'Ln_Age', 'Relative_Offer_Size', 'VC_backed', 
                   'Firm_Commitment', 'Underwriter_Reputation', 'Integer_Offer_Price']
id_cols = ['Issuer/Borrower SEDOL', 'ISIN', 'Datastream']
year_col = ['Dates: Offer Year (CCYY)']
output_cols = calculated_cols + id_cols + year_col

df_final = df[output_cols]
df_final.to_excel(config.CALCULATED_OUTPUT, index=False)
print(f"結果已儲存至: {config.CALCULATED_OUTPUT}")
