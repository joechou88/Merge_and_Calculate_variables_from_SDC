## Data Source
### SDC
- Download .csv files by country and put them under `SDC_xlsx` folder
- Manual: https://drive.google.com/file/d/1bq7LzHWOJbOkfsZx-fkoMGtvZUg4EGqw/view?usp=drive_link

## Python Scripts
#### 1. Country Integration (`merge.py`)
- **Objective**: combine all country files in `SDC_xlsx` folder to one single `Merged_All_countries_SDC_2015-2024.xlsx`, except for countries in `EXCLUDE_COUNTRIES`
- **Output**: `Merged_All_countries_SDC_2015-2024.xlsx`
#### 2. Columns Filtering (`filter.py`)
- **Objective**:
  - filter dataframe columns to retain only the predefined `TARGET_COLUMNS`
  - retain records only if `Original IPO Flag = TRUE`
- **Input**: `Merged_All_countries_SDC_2015-2024.xlsx`
- **Output**: `Filtered_All_countries_SDC_2015-2024.xlsx`
#### 3. Company Uniqueness Check (`check_company_uniqueness.py`)
- **Objective**:
  - Ensures each company should ideally have only one IPO record.
  - Identifies and list duplicate company to help a deeper investigation into why duplicates exist
- **Input**: `Filtered_All_countries_SDC_2015-2024.xlsx`
- **Output**: `Duplicated_company_list.xlsx`
#### 4. Company Uniqueness Check (`handle_duplicates.py`)
- **Objective**: Ensures each company only have one record in the Excel file.
- **Key Functions**:
  - 「Issuer/Borrower Name Full 相同」且「Dates: Issue Date 完全相同或相差 3 天以內」的紀錄視為同一次 IPO 事件，將這幾筆的 Proceeds Amount All Markets (USD Millions) 金額加總，其他欄位則取原紀錄 Proceeds Amount All Markets (USD Millions) 最大那筆的值
  - 若 Dates: Issue Date 相差太遠，只取第一筆
- **Input**: `Filtered_All_countries_SDC_2015-2024.xlsx`
- **Output**: `Unique_All_countries_SDC_2015-2024.xlsx`
#### 5. Variable Calculation (`calculate.py`)
- **Objective**: calculate variables to be served as statistical model input
- **Variables**
  - Underpricing
  - Ln_Age
  - Relative_Offer_Size
  - VC_backed
  - Firm_Commitment
  - Underwriter_Reputation
  - Integer_Offer_Price
- **Input**: `Filtered_All_countries_SDC_2015-2024.xlsx`
- **Output**: `Calculated_All_countries_SDC_2015-2024.xlsx`
