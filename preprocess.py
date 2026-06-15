# preprocess.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess_data(file_path):
    """
    Loads the cleaned Amazon CSV and extracts categorical 
    and numerical features for model training.
    """
    df = pd.read_csv(file_path)
    
    category_col = 'product_category' if 'product_category' in df.columns else 'category'
    price_col = 'discounted_price' if 'discounted_price' in df.columns else 'actual_price'
    
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce').fillna(25.0)
    
    # Label Encode the product category strings dynamically
    label_encoder = LabelEncoder()
    df['category_encoded'] = label_encoder.fit_transform(df[category_col].astype(str))
    
    # Formulate wholesale cost floor proxy
    if 'wholesale_cost' not in df.columns:
        df['wholesale_cost'] = df[price_col] * 0.45 
    
    X = df[['category_encoded', 'wholesale_cost']].copy()
    y = df[price_col]
    
    return X, y, label_encoder