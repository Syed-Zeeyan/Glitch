# ✅ Full Preprocessing Code for LendingClub with 6 Features
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

print("📥 Loading dataset...")
df = pd.read_csv('../data/lendingclub.csv', low_memory=False, nrows=10000)

# Step 1: Select relevant columns
cols_to_use = ['annual_inc', 'installment', 'total_pymnt', 'loan_status', 'dti', 'emp_length', 'purpose']
df = df[cols_to_use]

# Step 2: Drop missing values
df.dropna(inplace=True)
df = df[df['annual_inc'] > 0]

# Step 3: Rename basic features
df.rename(columns={
    'annual_inc': 'income',
    'installment': 'expenses',
    'total_pymnt': 'transactions'
}, inplace=True)

# Step 4: Convert emp_length to numeric
def parse_emp_length(val):
    if pd.isnull(val):
        return 0
    if '<' in val:
        return 0.5
    if '10+' in val:
        return 10
    digits = ''.join([c for c in val if c.isdigit()])
    return float(digits) if digits else 0

df['emp_length'] = df['emp_length'].apply(parse_emp_length)

# Step 5: One-hot encode 'purpose'
df = pd.get_dummies(df, columns=['purpose'], drop_first=True)

# Step 6: Create binary label from loan_status
df['label'] = df['loan_status'].apply(lambda x: 1 if x == 'Fully Paid' else 0)
df.drop(columns=['loan_status'], inplace=True)

# Step 7: Normalize continuous features
features_to_normalize = ['income', 'expenses', 'transactions', 'dti', 'emp_length']
scaler = MinMaxScaler()
df[features_to_normalize] = scaler.fit_transform(df[features_to_normalize])

# Step 8: Save the cleaned data
df.to_csv('../data/cleaned_data.csv', index=False)
print("✅ Cleaned dataset with 6+ features saved to ../data/cleaned_data.csv")
