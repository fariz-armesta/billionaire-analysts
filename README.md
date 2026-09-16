# Billionaire Insights 💰

An interactive Streamlit dashboard exploring global billionaire data from 1997–2024 — who they are, where they're from, how they made their money, and how that's shifted over nearly three decades.

**Live structure:** raw data → cleaning pipeline → exploratory analysis → interactive dashboard.

## Features

- **Interactive filters** — explore by year range and country of citizenship
- **Headline metrics** — unique billionaire count, total net worth, and average age for any selected filter combination
- **Country & category breakdowns** — top countries and business categories by billionaire count
- **Time trends** — billionaire count over time by country, with a multi-select comparison view
- Built on a cleaned, deduplicated dataset spanning **1997–2024**

## Key Insight

Across the dataset, the United States consistently holds the largest share of billionaires, but China's rise — particularly in technology and manufacturing — has visibly reshaped the global distribution of billionaire wealth over the past two decades.

## Project Structure

```
billionaire-analysts/
├── 1_cleaning.ipynb    # Data cleaning: missing-value imputation, type fixes, deduplication
├── 2_all_eda.ipynb     # Exploratory data analysis and visualization
├── app.py                # Streamlit dashboard (filters, charts, trend lines)
└── .gitignore
```

### 1. Data Cleaning (`1_cleaning.ipynb`)

Takes the raw `all_billionaires_1997_2024.csv` and produces a clean, analysis-ready dataset:

- Parses `net_worth` out of a mixed string format into a numeric field
- Manually backfills missing `rank` and `country_of_citizenship` values for specific known individuals where the source data had gaps
- Derives missing `age` from `birth_date` where available, and imputes remaining gaps with the column mean
- Fills categorical nulls (`organization_name`, `position_in_organization`, `wealth_status`, `gender`, `business_category`, `business_industries`, `city_of_residence`) with explicit placeholder values rather than dropping rows
- Outputs `billionaire_cleaned.csv` for downstream analysis

### 2. Exploratory Data Analysis (`2_all_eda.ipynb`)

Analyzes the cleaned dataset across several dimensions:

- Distribution by country of citizenship, gender, business category, and self-made status
- Cross-tabulations of business category by country
- Time trends: billionaire count and total net worth by country (1997–2024)
- Business category trends over time, including per-country breakdowns (e.g. Japan)
- Mean billionaire age by year

### 3. Dashboard (`app.py`)

A Streamlit app that turns the cleaned dataset into an interactive tool:

- Sidebar filters for year range and country
- Headline metric cards (unique billionaires, total net worth, average age)
- Side-by-side bar charts for top countries and top business categories
- A country-comparison line chart of billionaire count over time

## Tech Stack

- **Python** (pandas, NumPy)
- **Jupyter Notebook** — cleaning and EDA
- **Streamlit** — interactive dashboard
- **Plotly Express** — interactive charts in the dashboard
- **Matplotlib** — static charts in the EDA notebook

## Getting Started

```bash
# Clone the repository
git clone https://github.com/fariz-armesta/billionaire-analysts.git
cd billionaire-analysts

# Install dependencies
pip install streamlit pandas plotly matplotlib numpy

# Run the dashboard
streamlit run app.py
```

Note: `app.py` expects a `billionaire_cleaned.csv` file (produced by `1_cleaning.ipynb`) in the project root.

## License

Personal project — license TBD.
