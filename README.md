## Data Source
### SDC
- Download .csv files by country and put them under `SDC_xlsx` folder
- Manual: https://drive.google.com/file/d/1bq7LzHWOJbOkfsZx-fkoMGtvZUg4EGqw/view?usp=drive_link

## Python Scripts
#### 1. Country Integration (`merge.py`)
- **Objective**: combine all country files to one single `Merged_All_countries_SDC_2015-2024.xlsx`
- **Output**: `Merged_All_countries_SDC_2015-2024.xlsx`
#### 2. Columns Filtering (`filter.py`)
- **Objective**: filter dataframe columns to retain only the predefined `TARGET_COLUMNS`
- **Input**: `Merged_All_countries_SDC_2015-2024.xlsx`
- **Output**: `Filtered_All_countries_SDC_2015-2024.xlsx`
#### 3. Variable Calculation (`calculate.py`)
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
