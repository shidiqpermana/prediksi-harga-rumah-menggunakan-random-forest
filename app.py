"""
Aplikasi Streamlit untuk Prediksi Harga Rumah
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Prediksi Harga Rumah",
    page_icon="🏠",
    layout="wide"
)

# Load model dan preprocessing info
@st.cache_resource
def load_model():
    """Load model dan preprocessing info"""
    try:
        model = joblib.load('model.pkl')
        preprocessing_info = joblib.load('preprocessing_info.pkl')
        return model, preprocessing_info
    except FileNotFoundError:
        st.error("❌ Model tidak ditemukan! Silakan jalankan train_model.py terlebih dahulu.")
        st.stop()

# Load model
model, prep_info = load_model()

# Judul aplikasi
st.title("🏠 Prediksi Harga Rumah")
st.markdown("### Aplikasi Machine Learning untuk Memperkirakan Harga Jual Rumah")

st.sidebar.title("📋 Menu")
menu = st.sidebar.radio(
    "Pilih halaman:",
    ["🔮 Prediksi Single", "📊 Prediksi Batch", "ℹ️ Informasi Model"]
)

if menu == "🔮 Prediksi Single":
    st.header("Prediksi Harga Rumah (Single Input)")
    st.markdown("Masukkan detail rumah untuk mendapatkan prediksi harga.")
    
    # Buat form input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Informasi Dasar")
        ms_sub_class = st.selectbox("MS SubClass", [20, 30, 40, 45, 50, 60, 70, 75, 80, 85, 90, 120, 150, 160, 180, 190])
        lot_frontage = st.number_input("Lot Frontage (feet)", min_value=0.0, value=70.0)
        lot_area = st.number_input("Lot Area (sq ft)", min_value=0.0, value=8450.0)
        overall_qual = st.slider("Overall Quality", 1, 10, 5)
        overall_cond = st.slider("Overall Condition", 1, 10, 5)
        year_built = st.number_input("Year Built", min_value=1800, max_value=2024, value=2000)
        year_remod_add = st.number_input("Year Remodeled", min_value=1800, max_value=2024, value=2000)
        
        st.subheader("Luas Bangunan")
        total_bsmt_sf = st.number_input("Total Basement SF", min_value=0.0, value=0.0)
        first_flr_sf = st.number_input("1st Floor SF", min_value=0.0, value=856.0)
        second_flr_sf = st.number_input("2nd Floor SF", min_value=0.0, value=854.0)
        gr_liv_area = st.number_input("Above Grade Living Area", min_value=0.0, value=1710.0)
        
    with col2:
        st.subheader("Fasilitas")
        total_bathrooms = st.number_input("Total Bathrooms", min_value=0.0, value=2.0)
        bedrooms = st.number_input("Bedrooms", min_value=0, value=3)
        kitchen_qual = st.selectbox("Kitchen Quality", ["Ex", "Gd", "TA", "Fa", "Po"])
        garage_cars = st.number_input("Garage Cars", min_value=0.0, value=2.0)
        garage_area = st.number_input("Garage Area (sq ft)", min_value=0.0, value=548.0)
        
        st.subheader("Lainnya")
        full_bath = st.number_input("Full Bath", min_value=0, value=2)
        half_bath = st.number_input("Half Bath", min_value=0, value=0)
        tot_rms_abv_grd = st.number_input("Total Rooms Above Grade", min_value=0, value=5)
        fireplaces = st.number_input("Fireplaces", min_value=0, value=0)
        
        st.subheader("Kategori")
        ms_zoning = st.selectbox("MS Zoning", ["RL", "RM", "C (all)", "FV", "RH"])
        street = st.selectbox("Street Type", ["Pave", "Grvl"])
        lot_shape = st.selectbox("Lot Shape", ["Reg", "IR1", "IR2", "IR3"])
        neighborhood = st.selectbox("Neighborhood", [
            "CollgCr", "Veenker", "Crawfor", "NoRidge", "Mitchel", "Somerst",
            "NWAmes", "OldTown", "BrkSide", "Sawyer", "NridgHt", "NAmes",
            "SawyerW", "IDOTRR", "MeadowV", "Edwards", "Timber", "Gilbert",
            "StoneBr", "ClearCr", "NPkVill", "Blmngtn", "BrDale", "SWISU",
            "Blueste"
        ])
    
    # Tombol prediksi
    if st.button("🔮 Prediksi Harga", type="primary"):
        try:
            # Buat dictionary input
            input_data = {
                'MSSubClass': ms_sub_class,
                'LotFrontage': lot_frontage,
                'LotArea': lot_area,
                'OverallQual': overall_qual,
                'OverallCond': overall_cond,
                'YearBuilt': year_built,
                'YearRemodAdd': year_remod_add,
                'TotalBsmtSF': total_bsmt_sf,
                '1stFlrSF': first_flr_sf,
                '2ndFlrSF': second_flr_sf,
                'GrLivArea': gr_liv_area,
                'FullBath': full_bath,
                'HalfBath': half_bath,
                'BedroomAbvGr': bedrooms,
                'KitchenAbvGr': 1,
                'TotRmsAbvGrd': tot_rms_abv_grd,
                'Fireplaces': fireplaces,
                'GarageCars': garage_cars,
                'GarageArea': garage_area,
                'MSZoning': ms_zoning,
                'Street': street,
                'LotShape': lot_shape,
                'Neighborhood': neighborhood,
                'KitchenQual': kitchen_qual,
            }
            
            # Buat DataFrame
            input_df = pd.DataFrame([input_data])
            
            # Preprocessing
            # Tambahkan nilai default untuk kolom yang mungkin hilang
            for col in prep_info['categorical_na_cols']:
                if col not in input_df.columns:
                    input_df[col] = 'None'
            
            # Fill missing numeric dengan median
            for col, median_val in prep_info['numeric_medians'].items():
                if col in input_df.columns and pd.isna(input_df[col].iloc[0]):
                    input_df[col] = median_val
            
            # Fill missing categorical dengan mode
            for col, mode_val in prep_info['categorical_modes'].items():
                if col in input_df.columns and pd.isna(input_df[col].iloc[0]):
                    input_df[col] = mode_val
            
            # One-hot encoding
            X_encoded = pd.get_dummies(input_df, columns=prep_info['categorical_cols'], drop_first=False)
            
            # Align columns dengan training data
            for col in prep_info['feature_columns']:
                if col not in X_encoded.columns:
                    X_encoded[col] = 0
            
            X_encoded = X_encoded[prep_info['feature_columns']]
            
            # Prediksi
            prediction = model.predict(X_encoded)[0]
            
            # Tampilkan hasil
            st.success("✅ Prediksi Berhasil!")
            st.markdown("---")
            st.metric(
                label="**Prediksi Harga Rumah**",
                value=f"${prediction:,.2f}",
                delta=None
            )
            st.info(f"💡 Harga prediksi: **${prediction:,.0f}**")
            
        except Exception as e:
            st.error(f"❌ Error saat prediksi: {str(e)}")
            st.info("Pastikan semua input sudah diisi dengan benar.")

elif menu == "📊 Prediksi Batch":
    st.header("Prediksi Harga Rumah (Batch Upload)")
    st.markdown("Upload file CSV untuk prediksi batch.")
    
    uploaded_file = st.file_uploader("Upload file CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ File berhasil diupload: {df.shape[0]} baris, {df.shape[1]} kolom")
            
            if st.button("🔮 Lakukan Prediksi Batch", type="primary"):
                with st.spinner("Memproses data..."):
                    # Preprocessing mirip dengan fungsi di train_model.py
                    X = df.copy()
                    
                    # Hapus kolom yang tidak diperlukan jika ada
                    if 'Id' in X.columns:
                        X = X.drop('Id', axis=1)
                    
                    # Apply preprocessing
                    for col in prep_info['categorical_na_cols']:
                        if col in X.columns:
                            X[col] = X[col].fillna('None')
                    
                    for col, median_val in prep_info['numeric_medians'].items():
                        if col in X.columns:
                            X[col] = X[col].fillna(median_val)
                    
                    for col, mode_val in prep_info['categorical_modes'].items():
                        if col in X.columns:
                            X[col] = X[col].fillna(mode_val)
                    
                    # One-hot encoding
                    X_encoded = pd.get_dummies(X, columns=prep_info['categorical_cols'], drop_first=False)
                    
                    # Align columns
                    for col in prep_info['feature_columns']:
                        if col not in X_encoded.columns:
                            X_encoded[col] = 0
                    
                    X_encoded = X_encoded[prep_info['feature_columns']]
                    
                    # Prediksi
                    predictions = model.predict(X_encoded)
                    
                    # Buat hasil
                    results_df = df.copy()
                    if 'Id' not in results_df.columns:
                        results_df['Id'] = range(1, len(results_df) + 1)
                    results_df['PredictedSalePrice'] = predictions
                    
                    st.success(f"✅ Prediksi selesai untuk {len(predictions)} rumah!")
                    st.dataframe(results_df)
                    
                    # Download button
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Hasil Prediksi (CSV)",
                        data=csv,
                        file_name="predictions.csv",
                        mime="text/csv"
                    )
                    
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

elif menu == "ℹ️ Informasi Model":
    st.header("Informasi Model")
    
    st.subheader("📊 Model Details")
    st.info("""
    **Model:** Random Forest Regressor
    
    **Parameter:**
    - n_estimators: 100
    - max_depth: 15
    - random_state: 42
    
    **Dataset:** Kaggle House Prices Dataset
    """)
    
    st.subheader("🔧 Preprocessing Steps")
    st.markdown("""
    1. **Missing Value Handling:**
       - Kategori khusus: 'None' untuk fitur seperti PoolQC, Garage, dll
       - Numerik: Median imputation
       - Kategori lainnya: Mode imputation
    
    2. **Encoding:**
       - One-Hot Encoding untuk semua fitur kategorikal
    
    3. **Feature Engineering:**
       - Hapus kolom Id
       - Standardisasi fitur sesuai training data
    """)
    
    st.subheader("📈 Feature Importance")
    st.info("""
    Model menggunakan Random Forest yang secara otomatis menghitung 
    importance untuk setiap fitur. Fitur dengan importance tinggi 
    memiliki pengaruh lebih besar dalam prediksi harga rumah.
    """)

# Footer
st.markdown("---")
st.markdown("### 📝 Catatan")
st.info("""
**Cara menggunakan aplikasi:**
1. Pastikan model sudah di-train dengan menjalankan `train_model.py`
2. Jalankan aplikasi dengan command: `streamlit run app.py`
3. Pilih menu di sidebar untuk prediksi single atau batch
""")

