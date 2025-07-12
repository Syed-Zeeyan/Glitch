# from flask import Flask, request, jsonify
# import joblib
# import pandas as pd
# import shap
# import matplotlib
# matplotlib.use('Agg')  # Headless mode
# import matplotlib.pyplot as plt
# import os
# import base64

# app = Flask(__name__)

# # Load model and scaler
# model = joblib.load('./model/credit_model.pkl')
# scaler = joblib.load('./model/scaler.pkl')

# @app.route("/")
# def home():
#     return "✅ DeFi Credit Agent API is running!"

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.json
#         df = pd.DataFrame([data])

#         # Handle dummy features
#         required_cols = model.feature_names_in_
#         for col in required_cols:
#             if col not in df.columns:
#                 df[col] = 0

#         # Scale numeric features
#         numeric_cols = ['income', 'expenses', 'transactions', 'dti', 'emp_length']
#         df[numeric_cols] = scaler.transform(df[numeric_cols])

#         # Reorder
#         df = df[required_cols]

#         # Prediction
#         prediction = int(model.predict(df)[0])

#         # SHAP explanation
#         explainer = shap.Explainer(model.predict, df)
#         shap_values = explainer(df)
#         explanation = shap_values[0]

#         os.makedirs("outputs", exist_ok=True)
#         explanation_path = "outputs/user_explanation.png"
#         plt.figure()
#         shap.plots.bar(explanation, show=False)
#         plt.savefig(explanation_path, bbox_inches='tight')
#         plt.close()

#         # Encode image as base64
#         with open(explanation_path, "rb") as image_file:
#             encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

#         return jsonify({
#             "prediction": prediction,
#             "explanation_image": encoded_image
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# import joblib
# import pandas as pd
# import shap
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import os
# import base64
# import numpy as np
# import io

# app = Flask(__name__)

# # Load model and scaler
# model = joblib.load('./model/credit_model.pkl')
# scaler = joblib.load('./model/scaler.pkl')

# def generate_shap_plot(shap_values, features, feature_names):
#     """Generate SHAP bar plot and return as base64"""
#     plt.figure(figsize=(10, 6))
#     shap.summary_plot(shap_values, features, feature_names=feature_names, plot_type="bar", show=False)
#     img = io.BytesIO()
#     plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
#     plt.close()
#     img.seek(0)
#     return base64.b64encode(img.getvalue()).decode('utf-8')

# @app.route("/")
# def home():
#     return "✅ DeFi Credit Agent API is running!"

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # 1. Prepare input data
#         data = request.json
#         df = pd.DataFrame([data])
        
#         # Add missing columns
#         for col in model.feature_names_in_:
#             if col not in df.columns:
#                 df[col] = 0
#         df = df[model.feature_names_in_]

#         # Scale numeric features
#         numeric_cols = ['income', 'expenses', 'transactions', 'dti', 'emp_length']
#         df[numeric_cols] = scaler.transform(df[numeric_cols])

#         # 2. Make prediction
#         prediction = int(model.predict(df)[0])

#         # 3. Generate explanation
#         explanation_image = None
#         reason = ""
#         warning = None

#         # Try SHAP first
#         try:
#             explainer = shap.TreeExplainer(model)
#             shap_values = explainer.shap_values(df)
            
#             # Handle different SHAP output formats
#             if isinstance(shap_values, list):
#                 # For classifiers, use the predicted class's SHAP values
#                 if prediction < len(shap_values):
#                     shap_vals = shap_values[prediction]
#                 else:
#                     shap_vals = shap_values[0]
#             else:
#                 shap_vals = shap_values
            
#             # Ensure correct shape
#             if len(shap_vals.shape) == 2:
#                 shap_vals = shap_vals[0]  # Take first sample
            
#             # Generate plot
#             explanation_image = generate_shap_plot(
#                 shap_vals.reshape(1, -1),  # Reshape for summary_plot
#                 df.values,
#                 df.columns.tolist()
#             )
            
#             # Get top feature
#             top_idx = np.argmax(np.abs(shap_vals))
#             reason = f"Most influential: {df.columns[top_idx]} (SHAP: {shap_vals[top_idx]:.2f})"

#         except Exception as e:
#             warning = f"SHAP explanation failed: {str(e)}"
#             # Fallback to feature importance
#             if hasattr(model, 'feature_importances_'):
#                 importances = model.feature_importances_
#                 top_idx = np.argmax(importances)
#                 reason = f"Most important: {df.columns[top_idx]}"
                
#                 # Create simple importance plot
#                 plt.figure(figsize=(10, 6))
#                 pd.Series(importances, index=df.columns).sort_values().plot(kind='barh')
#                 plt.title("Feature Importance")
#                 img = io.BytesIO()
#                 plt.savefig(img, format='png', bbox_inches='tight')
#                 plt.close()
#                 img.seek(0)
#                 explanation_image = base64.b64encode(img.getvalue()).decode('utf-8')
#             else:
#                 reason = "Prediction succeeded but no explanation available"

#         # Prepare response
#         response = {
#             "prediction": prediction,
#             "reason": reason,
#             "status": "success" if warning is None else "partial_success"
#         }
        
#         if explanation_image:
#             response["explanation_image"] = explanation_image
#         if warning:
#             response["warning"] = warning

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({
#             "error": f"Prediction failed: {str(e)}",
#             "type": type(e).__name__,
#             "status": "error"
#         }), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, request, jsonify
import joblib
import pandas as pd
import shap
import matplotlib
matplotlib.use('Agg')  # Disable GUI backend
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import os

app = Flask(__name__)

# Load model and assets
model = joblib.load('./model/credit_model.pkl')
scaler = joblib.load('./model/scaler.pkl')
columns = joblib.load('./model/columns.pkl')  # Needed for consistent feature order

numeric_cols = ['income', 'expenses', 'transactions', 'dti', 'emp_length']

@app.route('/')
def home():
    return "✅ API Running. Use POST /predict"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame([data])

        # Add any missing dummy columns
        for col in columns:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[columns]  # reorder

        # Scale numeric columns
        input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

        # Predict
        prediction = int(model.predict(input_df)[0])

        # SHAP Explanation
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_df)

        # For binary classification: shap_values is a list of 2 arrays
        shap_input = shap_values[1] if isinstance(shap_values, list) else shap_values
        single_shap = shap_input[0]

        # Create explanation object
        explanation = shap.Explanation(
            values=single_shap,
            base_values=explainer.expected_value[1] if isinstance(explainer.expected_value, list) else explainer.expected_value,
            data=input_df.iloc[0],
            feature_names=input_df.columns.tolist()
        )

        # Plot
        plt.figure()
        shap.plots.bar(explanation, show=False)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        encoded_img = base64.b64encode(buf.getvalue()).decode('utf-8')

        # Get most impactful feature
        top_idx = np.argmax(np.abs(single_shap))
        reason = f"Most influential feature: {input_df.columns[top_idx]} (Impact: {single_shap[top_idx]:.3f})"

        return jsonify({
            "prediction": prediction,
            "explanation_image": encoded_img,
            "reason": reason,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "prediction": None,
            "reason": "Prediction succeeded but explanation failed.",
            "warning": str(e),
            "status": "partial_success"
        })

if __name__ == '__main__':
    app.run(debug=True)

