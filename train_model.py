"""
Script untuk training model Random Forest Regressor untuk prediksi harga rumah
dan menyimpan model serta preprocessor ke file.
"""

import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


def preprocess_data(df):
    """
    Fungsi untuk preprocessing data
    
    Args:
        df: DataFrame dengan kolom SalePrice
        
    Returns:
        X_encoded: DataFrame fitur yang sudah diproses
        y: Series target (SalePrice)
    """
    # Memisahkan X (fitur) dan y (target: SalePrice)
    X = df.drop('SalePrice', axis=1)
    y = df['SalePrice']
    
    # Kolom kategorikal yang nilai NA-nya berarti "tidak ada"
    categorical_na_cols = ['PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu', 
                           'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond',
                           'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2',
                           'MasVnrType']
    
    # Imputasi 'None' untuk kolom kategorikal yang NA berarti tidak ada
    for col in categorical_na_cols:
        if col in X.columns:
            X[col] = X[col].fillna('None')
    
    # Identifikasi kolom numerik dan kategorikal
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    
    # Hapus kolom Id jika ada
    if 'Id' in numeric_cols:
        numeric_cols.remove('Id')
        X = X.drop('Id', axis=1)
    
    # Imputasi nilai Median untuk semua kolom numerik yang tersisa
    numeric_medians = {}
    for col in numeric_cols:
        if X[col].isnull().sum() > 0:
            median_value = X[col].median()
            numeric_medians[col] = median_value
            X[col] = X[col].fillna(median_value)
    
    # Imputasi untuk kolom kategorikal yang tersisa (selain yang sudah diisi 'None')
    categorical_modes = {}
    for col in categorical_cols:
        if X[col].isnull().sum() > 0:
            # Isi dengan mode (nilai paling sering muncul)
            mode_value = X[col].mode()[0] if len(X[col].mode()) > 0 else 'Unknown'
            categorical_modes[col] = mode_value
            X[col] = X[col].fillna(mode_value)
    
    # One-Hot Encoding untuk semua fitur kategorikal
    X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=False)
    
    # Simpan informasi preprocessing untuk digunakan saat prediksi
    preprocessing_info = {
        'categorical_na_cols': categorical_na_cols,
        'numeric_cols': numeric_cols,
        'categorical_cols': categorical_cols,
        'numeric_medians': numeric_medians,
        'categorical_modes': categorical_modes,
        'feature_columns': X_encoded.columns.tolist()
    }
    
    return X_encoded, y, preprocessing_info


def train_model():
    """
    Fungsi untuk training model dan menyimpan hasilnya
    """
    print("="*60)
    print("TRAINING MODEL PREDIKSI HARGA RUMAH")
    print("="*60)
    
    # Memuat dataset
    print("\n1. Memuat dataset...")
    df = pd.read_csv('train.csv')
    print(f"   Dataset dimuat: {df.shape[0]} baris, {df.shape[1]} kolom")
    
    # Preprocessing
    print("\n2. Melakukan preprocessing data...")
    X_encoded, y, preprocessing_info = preprocess_data(df)
    print(f"   Preprocessing selesai. Fitur setelah encoding: {X_encoded.shape[1]}")
    
    # Split data
    print("\n3. Membagi data menjadi training dan test set...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42
    )
    print(f"   Training set: {X_train.shape[0]} samples")
    print(f"   Test set: {X_test.shape[0]} samples")
    
    # Training model
    print("\n4. Melatih model Random Forest Regressor...")
    rf_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    print("   Training selesai!")
    
    # Evaluasi
    print("\n5. Mengevaluasi model...")
    y_pred = rf_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print("   Hasil Evaluasi:")
    print(f"   - RMSE: {rmse:.2f}")
    print(f"   - R² Score: {r2:.4f}")
    
    # Menyimpan model
    print("\n6. Menyimpan model dan preprocessor...")
    joblib.dump(rf_model, 'model.pkl')
    joblib.dump(preprocessing_info, 'preprocessing_info.pkl')
    print("   Model disimpan sebagai 'model.pkl'")
    print("   Preprocessing info disimpan sebagai 'preprocessing_info.pkl'")
    
    # Feature Importance
    feature_importance = pd.DataFrame({
        'Feature': X_encoded.columns,
        'Importance': rf_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\n7. Top 10 Fitur Terpenting:")
    print("   " + "-"*60)
    top_10 = feature_importance.head(10)
    for idx, row in top_10.iterrows():
        print(f"   {row['Feature']:40s} : {row['Importance']:.6f}")
    
    print("\n" + "="*60)
    print("TRAINING SELESAI!")
    print("="*60)


if __name__ == "__main__":
    train_model()

