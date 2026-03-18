```markdown
# Customer Engagement & Product Utilization Analytics for Retention Strategy

## Executive Summary for Government Stakeholders
This project evaluates banking customer retention through the lens of behavioral engagement and relationship depth, moving beyond traditional demographic or wealth-based metrics. The analysis of 10,000 customer records from the European Central Bank reveals a critical insight: **high financial balances do not guarantee loyalty**. 

Customers categorized as "Inactive High-Balance" represent the highest flight risk, churning at a rate of 32.33%. Conversely, customers with strong engagement and optimal product depth (exactly two products) show significantly higher retention rates. By shifting the strategic focus from balance accumulation to active product utilization, financial institutions can proactively mitigate silent churn and design highly targeted loyalty programs.

## Analytical Methodology
1. **Data Validation:** Evaluated 10,000 records for consistency across geographical (France, Spain, Germany) and financial metrics.
2. **Engagement Classification:** Segmented customers into four behavioral profiles based on activity status and median balance.
3. **Product Utilization Analysis:** Correlated the number of active products with churn probability.
4. **Retention Strength Assessment:** Developed a 4-point Relationship Strength Index to quantify customer loyalty.

## Research Findings & Insights (EDA)
* **The "Sweet Spot" of Product Depth:** Customers with exactly 2 products have the lowest churn rate (7.58%). Single-product customers churn at 27.71%, meaning single-product customers are **3.66x more likely to churn** than dual-product customers. Over-bundling is highly detrimental; churn spikes to over 82% for customers with 3 or more products.
* **The High-Balance Churn Risk:** Wealth does not equal loyalty. Inactive customers with balances above the median churn at **32.33%**, which is significantly higher than active customers with low/zero balances (10.74%).
* **Engagement Overpowers Credit Cards:** Simply holding a credit card has a negligible impact on retention (~20% churn for both cardholders and non-cardholders). However, overall active engagement reduces churn from 21.23% to 9.66%.
* **Relationship Strength Index:** Combining activity, credit card ownership, and optimal product count creates a strong predictor of retention. Customers scoring a '4' on this index churn at only 5.19%, compared to 38.28% for those scoring '0'.

## Strategic Recommendations
1. **Targeted Cross-Selling:** Implement campaigns specifically designed to move single-product customers to dual-product relationships. Avoid aggressive cross-selling that pushes customers to 3+ products.
2. **Re-engagement Campaigns for Premium Accounts:** Deploy immediate, personalized outreach to "At-Risk Premium" customers (high balance, inactive) before they silently exit.
3. **Behavior-Based Loyalty Programs:** Shift reward structures away from pure balance tiers and towards consistent transaction activity and multi-product utilization.

## Project Structure & Setup

```text
customer-retention-analytics/
│
├── data/
│   └── dataset.csv          # Raw data file
├── src/
│   └── data_processing.py   # Feature engineering and cleaning logic
├── app.py                   # Streamlit dashboard application
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

### How to Run the Dashboard Locally
1. Ensure Python is installed on your system.
2. Clone this repository and navigate to the project folder.
3. Install the required dependencies:
   `pip install -r requirements.txt`
4. Run the Streamlit application:
   `streamlit run app.py`
```