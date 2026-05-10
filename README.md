## Data Source
### SDC
- Download .csv files by country and put them under `SDC_xlsx` folder
- Manual: https://drive.google.com/file/d/1bq7LzHWOJbOkfsZx-fkoMGtvZUg4EGqw/view?usp=drive_link

## Python Scripts
#### 1. Country Integration (`merge.py`)
- **Objective**: combine all country files in `SDC_xlsx` folder to one single `Merged_All_countries_SDC_2015-2024.xlsx`, except for countries in `EXCLUDE_COUNTRIES`
- **Output**: `Merged_All_countries_SDC_2015-2024.xlsx`
#### 2. Columns Filtering (`column_filter.py`)
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
#### 4. Ensure Company Uniqueness (`handle_duplicates.py`)
- **Objective**: Ensures each company only have one record in the Excel file.
- **Key Functions**:
  - Entries sharing the exact same `Issuer/Borrower Name Full` with an `Dates: Issue Date` that is either identical or within 3-day are treated as a single IPO event. We should sum `Proceeds Amount All Markets (USD Millions)` together and retain values from record that held the highest `Proceeds Amount All Markets (USD Millions)` for other columns.
  - If `Dates: Issue Date` for the same `Issuer/Borrower Name Full` are too far apart (beyond 3-day threshold), we only keep the first record.
  - You can see an example to understand how duplicate records are merged: https://docs.google.com/spreadsheets/d/14AC16w1ZYBycbO3lvXgmCCPowfnXYNCR/edit?usp=sharing&ouid=108393837815697167094&rtpof=true&sd=true
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
