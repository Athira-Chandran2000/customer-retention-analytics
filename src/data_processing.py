# src/data_processing.py
import pandas as pd
import numpy as np

def load_and_preprocess_data(file_path):
    """Loads dataset and engineers engagement & retention features."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'. Please check the path.")
        return None

    # Calculate dynamic thresholds
    median_balance = df['Balance'].median()
    median_sal = df['EstimatedSalary'].median()
    premium_threshold = df['Balance'].quantile(0.75)

    # 1. Engagement Classification
    conditions = [
        (df['IsActiveMember'] == 1) & (df['NumOfProducts'] > 1),
        (df['IsActiveMember'] == 1) & (df['NumOfProducts'] == 1),
        (df['IsActiveMember'] == 0) & (df['Balance'] > median_balance),
        (df['IsActiveMember'] == 0) & (df['Balance'] <= median_balance)
    ]
    choices = [
        'Active Engaged',
        'Active Low-Product',
        'Inactive High-Balance',
        'Inactive Disengaged'
    ]
    df['EngagementProfile'] = np.select(conditions, choices, default='Unknown')

    # 2. Product Utilization
    df['ProductDepth'] = np.where(df['NumOfProducts'] == 1, 'Single-Product', 'Multi-Product')

    # 3. Financial Commitment vs Engagement
    df['BalanceCategory'] = np.where(df['Balance'] > median_balance, 'High Balance', 'Low/Zero Balance')
    
    df['PremiumRisk'] = np.where(
        (df['Balance'] > premium_threshold) & (df['IsActiveMember'] == 0), 
        'At-Risk Premium', 
        'Other/Standard'
    )

    df['MismatchProfile'] = np.where(
        (df['EstimatedSalary'] > median_sal) & (df['Balance'] == 0), 
        'High Salary / Zero Balance', 
        'Standard Profile'
    )

    # 4. Retention Strength Assessment
    df['RelationshipStrength'] = df['IsActiveMember'] + df['HasCrCard'] + np.where(df['NumOfProducts'] == 2, 2, 0)

    return df

if __name__ == "__main__":
    # Test the module by running it directly from the terminal
    # python src/data_processing.py
    processed_df = load_and_preprocess_data('data/European_Bank.csv')
    if processed_df is not None:
        print("Data processed successfully!")
        print("Dataset Shape:", processed_df.shape)
        print("Columns added:", list(processed_df.columns[-6:]))