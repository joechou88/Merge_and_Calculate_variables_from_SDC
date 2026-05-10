# Folder name
SDC_FOLDER = "SDC_xlsx"

# File name
MERGED_OUTPUT = "Merged_All_countries_SDC_2015-2024.xlsx"
FILTERED_OUTPUT = "Filtered_All_countries_SDC_2015-2024.xlsx"
DUPLICATED_OUTPUT = "Duplicated_company_list.xlsx"
UNIQUE_OUTPUT     = "Unique_All_countries_SDC_2015-2024.xlsx"
CALCULATED_OUTPUT = "Calculated_All_countries_SDC_2015-2024.xlsx"
TOP25_UNDERWRITERS = "Top-25-lead-underwriter-league-table_Proceeds-Amount-All-Markets-(USD Millions).xlsx"

# Filter country
EXCLUDE_COUNTRIES = [
    "Ireland",
    "Japan",
    "China",
    "India",
    "Indonesia",
    "Switzerland",
    "Vietnam"
]

# Filter columns
TARGET_COLUMNS = [
    "Dates: Issue Date",
    "Dates: Offer Year (CCYY)",
    "Issuer/Borrower Name Full",
    "Issuer/Borrower Nation",
    "Percent Change Offer Price to Closing Price at Offer/First Trade",
    "Original IPO Flag",
    "Issuer/Borrower Founded Date",
    "Proceeds Amount All Markets (USD Millions)",
    "Financials: Total Assets Before Offering (USD Millions)",
    "Venture Capital Backed IPO Issue Flag",
    "Offering Technique",
    "Bookrunner",
    "Offer Price (USD)",
    "Issuer/Borrower SEDOL",
    "ISIN",
    "Datastream"
]

# Other params
SHEET_NAME = 'Request 3'
START_YEAR = 2015
END_YEAR = 2024