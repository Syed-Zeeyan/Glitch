# import pandas as pd
# import joblib
# import shap
# import matplotlib.pyplot as plt
# import os

# # Step 1: Load model and data
# print("📥 Loading model and cleaned data...")
# model = joblib.load('../model/credit_model.pkl')
# df = pd.read_csv('../../data/cleaned_data.csv')

# # Step 2: Prepare feature matrix (X)
# X = df.drop(columns=['label'])

# # Step 3: Convert bool columns to int
# X = X.astype({col: 'int' for col in X.select_dtypes('bool').columns})

# # Step 4: Ensure all columns are numeric and drop NaNs
# X = X.apply(pd.to_numeric, errors='coerce')
# X.dropna(inplace=True)

# # Optional: Confirm all dtypes
# print("\n[Cleaned] Column types:\n", X.dtypes)

# # Step 5: Generate SHAP values
# print("🔍 Creating SHAP explainer...")
# explainer = shap.Explainer(model, X)
# # shap_values = explainer(X)
# shap_values = explainer(X, check_additivity=False)


# # Step 6: Save SHAP summary plot
# print("📊 Generating SHAP summary plot...")
# os.makedirs('outputs', exist_ok=True)
# plt.figure()
# shap.summary_plot(shap_values, X, show=False)
# plt.tight_layout()
# plt.savefig('outputs/shap_summary.png')
# print("✅ SHAP summary saved to backend/explainability/outputs/shap_summary.png")

import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
import os
import numpy as np

# Step 1: Load model and cleaned data
print("📥 Loading model and cleaned data...")
model = joblib.load('../model/credit_model.pkl')
df = pd.read_csv('../../data/cleaned_data.csv')

# Step 2: Prepare feature matrix (X)
X = df.drop(columns=['label'])

# Step 3: Convert boolean columns to integers
X = X.astype({col: 'int' for col in X.select_dtypes('bool').columns})

# Step 4: Ensure all columns are numeric and drop NaNs
X = X.apply(pd.to_numeric, errors='coerce')
X.dropna(inplace=True)

# Optional: Confirm column types
print("\n[Cleaned] Column types:\n", X.dtypes)

# Step 5: Create SHAP explainer
print("🔍 Creating SHAP explainer...")
explainer = shap.Explainer(model, X)

# Step 6: Choose one row for force/waterfall explanation (first row)
sample = X.iloc[[0]]
shap_values = explainer(sample, check_additivity=False)

# Step 7: Select class 1 (positive class) SHAP values
if isinstance(shap_values.values, np.ndarray) and shap_values.values.ndim == 3:
    shap_val = shap_values.values[0, :, 1]
    base_val = explainer.expected_value[1]
else:
    shap_val = shap_values.values[0]
    base_val = explainer.expected_value

# Step 8: Save force/waterfall plot
print("📊 Generating SHAP waterfall plot...")
os.makedirs('outputs', exist_ok=True)
shap.plots.waterfall(shap.Explanation(
    values=shap_val,
    base_values=base_val,
    data=sample.values[0],
    feature_names=sample.columns
), show=False)

plt.savefig("outputs/sample_waterfall.png", bbox_inches='tight')
print("✅ Waterfall plot saved to backend/explainability/outputs/sample_waterfall.png")

# Step 9: SHAP Summary Plot for all
print("📊 Generating SHAP summary plot...")
shap_values_all = explainer(X, check_additivity=False)
plt.figure()
shap.summary_plot(shap_values_all, X, show=False)
plt.tight_layout()
plt.savefig('outputs/shap_summary.png')
print("✅ SHAP summary saved to backend/explainability/outputs/shap_summary.png")

