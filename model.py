# model.py
import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from preprocess import load_and_preprocess_data

def train_market_models():
    print("⏳ Initializing Machine Learning Multi-Model Pipeline...")
    
    # File target path
    data_path = 'C:\\Users\\HP\\Desktop\\New folder (2)\\data\\amazon_products_sales_data_cleaned.csv'
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset missing at mapped path: {data_path}")
        
    # Load feature matrices from preprocess engine 
    # (Note: X already contains your 'category_encoded' via your LabelEncoder!)
    X, y, label_encoder = load_and_preprocess_data(data_path)
    
    # Segment data into Train and Validation vectors
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize dictionary to hold all architectures
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42),
        "XGBoost Regressor": XGBRegressor(n_estimators=150, learning_rate=0.08, max_depth=6, random_state=42)
    }
    
    performance_metrics = []
    os.makedirs('models', exist_ok=True)
    
    print(f"🚀 Commencing training across {X_train.shape[0]} data samples...\n")
    
    # Loop through each model architecture
    for name, model in models.items():
        print(f"⚙️ Training {name}...")
        model.fit(X_train, y_train)
        
        # Validate accuracy metrics
        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        # Store tracking matrix scores
        performance_metrics.append({"Model": name, "MAE ($)": round(mae, 2), "R² Score": round(r2, 4)})
        
        # Standardize file naming conventions for binary exports
        file_safe_name = name.lower().replace(" ", "_")
        joblib.dump(model, f'models/{file_safe_name}_model.pkl')
        print(f"💾 Saved: models/{file_safe_name}_model.pkl")
    
    # Save the central label encoder so app.py can decode UI entries identically
    joblib.dump(label_encoder, 'models/label_encoder.pkl')
    print("💾 Saved: models/label_encoder.pkl\n")
    
    # ----------------------------------------------------
    # 📊 REPORT CARD GENERATION
    # ----------------------------------------------------
    print("=" * 60)
    print("🏆 SIMULATION MODEL BENCHMARK PERFORMANCE REPORT")
    print("=" * 60)
    metrics_df = pd.DataFrame(performance_metrics)
    print(metrics_df.to_string(index=False))
    print("=" * 60)
    print("🏁 All training loops finalized successfully!")

if __name__ == '__main__':
    train_market_models()