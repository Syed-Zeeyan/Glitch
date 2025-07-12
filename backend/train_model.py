# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.utils import class_weight
# from sklearn.metrics import classification_report
# import joblib
# import os

# # Step 1: Load cleaned data
# df = pd.read_csv('../data/cleaned_data.csv')

# # Step 2: Split features and label
# X = df.drop(columns=['label'])
# y = df['label']

# # 🔍 Check class balance
# print("Class distribution:")
# print(y.value_counts())

# # Step 3: Scale numeric features
# scaler = MinMaxScaler()
# X_scaled = X.copy()
# numeric_cols = ['income', 'expenses', 'transactions', 'dti', 'emp_length']
# X_scaled[numeric_cols] = scaler.fit_transform(X[numeric_cols])

# # Step 4: Train-test split
# X_train, X_test, y_train, y_test = train_test_split(
#     X_scaled, y, test_size=0.2, random_state=42, stratify=y
# )

# # ⚖️ Step 5: Compute class weights for imbalance
# weights_array = class_weight.compute_class_weight(
#     class_weight='balanced',
#     classes=np.array([0, 1]),
#     y=y
# )
# class_weights = {0: weights_array[0], 1: weights_array[1]}
# print("Class weights:", class_weights)

# # ✅ Step 6: Train model
# model = RandomForestClassifier(
#     n_estimators=100,
#     class_weight=class_weights,
#     random_state=42
# )
# model.fit(X_train, y_train)

# # Step 7: Evaluate performance
# accuracy = model.score(X_test, y_test)
# print(f"\n✅ Model accuracy: {accuracy:.2f}")
# print("\nDetailed classification report:")
# print(classification_report(y_test, model.predict(X_test)))

# # Step 8: Save model and artifacts
# os.makedirs('model', exist_ok=True)
# joblib.dump(model, 'model/credit_model.pkl')
# joblib.dump(scaler, 'model/scaler.pkl')
# joblib.dump(X_scaled.columns.tolist(), 'model/columns.pkl')

# print("\n📦 Model, scaler, and columns saved to /model/")


# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics import classification_report
# import joblib
# import os

# # Load dataset
# df = pd.read_csv('../data/cleaned_data.csv')
# X = df.drop(columns=['label'])
# y = df['label']

# # Scale numeric features
# scaler = MinMaxScaler()
# numeric_cols = ['income', 'expenses', 'transactions', 'dti', 'emp_length']
# X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

# # Train-test split
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42, stratify=y
# )

# # Train model with class_weight balanced
# model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
# model.fit(X_train, y_train)

# # Evaluate
# print("✅ Model accuracy:", model.score(X_test, y_test))
# print(classification_report(y_test, model.predict(X_test)))

# # Save model artifacts
# os.makedirs('model', exist_ok=True)
# joblib.dump(model, 'model/credit_model.pkl')
# joblib.dump(scaler, 'model/scaler.pkl')
# joblib.dump(X.columns.tolist(), 'model/columns.pkl')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
import joblib
import os

# Step 1: Load dataset
df = pd.read_csv('../data/cleaned_data.csv')

# Step 2: Separate features and label
X = df.drop(columns=['label'])
y = df['label']

# Step 3: Identify numeric columns
required_numeric = [
    'income', 'expenses', 'transactions', 'dti', 'emp_length',
    'credit_score', 'loan_amount_outstanding', 'existing_loans', 'land_size'
]
# numeric_cols = [col for col in required_numeric if col in X.columns]  # safe check

for col in required_numeric:
    if col not in df.columns:
        df[col] = 0

X = df.drop(columns=['label'])
y = df['label']

# Step 4: Scale numeric columns
scaler = MinMaxScaler()
X_scaled = X.copy()
X_scaled[required_numeric] = scaler.fit_transform(X[required_numeric])

# Step 5: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

# Step 6: Train model
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Step 7: Evaluation
print("✅ Accuracy:", model.score(X_test, y_test))
print(classification_report(y_test, model.predict(X_test)))

# Step 8: Save model and scalers
os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/credit_model.pkl')
joblib.dump(scaler, 'model/scaler.pkl')
joblib.dump(X_scaled.columns.tolist(), 'model/columns.pkl')

print("✅ Artifacts saved in /model")



