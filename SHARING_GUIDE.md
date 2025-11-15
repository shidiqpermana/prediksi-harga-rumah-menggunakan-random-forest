# 📤 Panduan Sharing Proyek - Prediksi Harga Rumah

Panduan lengkap tentang file apa saja yang perlu di-share untuk deployment atau berbagi proyek.

## 📋 File yang PERLU Di-share

### ✅ File Utama (WAJIB)

1. **`app.py`** - Aplikasi Streamlit utama
2. **`train_model.py`** - Script untuk training model
3. **`requirements.txt`** - Dependencies Python
4. **`README.md`** - Dokumentasi proyek
5. **`model.pkl`** - Model yang sudah di-train (ATAU training script jika ingin re-train)
6. **`preprocessing_info.pkl`** - Info preprocessing untuk prediksi

### ✅ File Deployment (Opsional tapi Disarankan)

7. **`Procfile`** - Untuk deployment Heroku
8. **`Dockerfile`** - Untuk deployment Docker
9. **`.dockerignore`** - File ignore untuk Docker
10. **`runtime.txt`** - Python version untuk Streamlit Cloud
11. **`DEPLOYMENT.md`** - Panduan deployment
12. **`.gitignore`** - File ignore untuk Git

### ✅ File Dataset (Opsional)

13. **`train.csv`** - Dataset training (jika ukurannya tidak terlalu besar)
14. **`test.csv`** - Dataset testing (opsional)
15. **`data_description.txt`** - Deskripsi fitur dataset

### ✅ File Dokumentasi

16. **`SHARING_GUIDE.md`** - Panduan ini
17. **`check_setup.py`** - Script untuk cek setup

## ❌ File yang TIDAK Perlu Di-share

1. **`__pycache__/`** - Python cache files
2. **`.vscode/`** - VS Code settings (kecuali team menggunakan config yang sama)
3. **`*.pyc`** - Compiled Python files
4. **`.DS_Store`** - macOS system files
5. **`.venv/` atau `venv/`** - Virtual environment (jangan share, cukup requirements.txt)
6. **`*.log`** - Log files
7. **`house_price_prediction.ipynb`** - Jupyter notebook (opsional, hanya untuk eksplorasi)

## 🚀 Skenario Sharing

### 1. Sharing untuk Deployment (Streamlit Cloud / Heroku)

**File yang diperlukan:**
```
✅ app.py
✅ train_model.py
✅ requirements.txt
✅ model.pkl (ATAU pastikan train_model.py bisa dijalankan)
✅ preprocessing_info.pkl
✅ README.md
✅ Procfile (untuk Heroku)
✅ runtime.txt (untuk Streamlit Cloud)
```

**File dataset:**
- `train.csv` - Jika ingin re-train di cloud (tidak disarankan jika file besar)
- Atau upload `model.pkl` yang sudah di-train

### 2. Sharing untuk Collaborator (GitHub/GitLab)

**File yang diperlukan:**
```
✅ Semua file Python (.py)
✅ requirements.txt
✅ README.md
✅ .gitignore
✅ DEPLOYMENT.md (opsional)
✅ train.csv (jika file tidak terlalu besar < 100MB)
```

**File yang TIDAK perlu:**
```
❌ model.pkl (bisa di-generate dengan train_model.py)
❌ preprocessing_info.pkl (bisa di-generate dengan train_model.py)
❌ __pycache__/
❌ .venv/
❌ *.pyc
```

**Catatan:** Jika `model.pkl` besar, bisa:
- Upload ke Google Drive / Dropbox dan share link
- Gunakan Git LFS (Large File Storage)
- Atau instruksikan untuk run `train_model.py` sendiri

### 3. Sharing untuk Presentation/Demo

**File yang diperlukan:**
```
✅ app.py
✅ model.pkl
✅ preprocessing_info.pkl
✅ requirements.txt
✅ README.md (singkat)
```

**Cara:**
1. Zip file-file tersebut
2. Share via Google Drive / Dropbox / email
3. Atau jalankan di local dan share link (jika menggunakan ngrok/tunneling)

### 4. Sharing via Docker

**File yang diperlukan:**
```
✅ Semua file dari skenario #1
✅ Dockerfile
✅ .dockerignore
```

**Cara:**
```bash
# Build image
docker build -t house-price-prediction .

# Save image
docker save house-price-prediction > house-price-prediction.tar

# Atau push ke Docker Hub
docker tag house-price-prediction username/house-price-prediction
docker push username/house-price-prediction
```

## 📦 Cara Membuat Package untuk Sharing

### Opsi 1: Zip File Manual

```bash
# Buat folder untuk sharing
mkdir house-price-prediction-package

# Copy file yang diperlukan
cp app.py train_model.py requirements.txt README.md house-price-prediction-package/
cp model.pkl preprocessing_info.pkl house-price-prediction-package/  # jika ada
cp Procfile runtime.txt house-price-prediction-package/  # jika ada

# Zip folder
zip -r house-price-prediction.zip house-price-prediction-package/
```

### Opsi 2: Git Archive (untuk Git repository)

```bash
# Buat archive dari Git
git archive -o house-price-prediction.zip HEAD

# Atau exclude file tertentu
git archive -o house-price-prediction.zip HEAD --prefix=house-price-prediction/ \
  --exclude='*.csv' \
  --exclude='__pycache__' \
  --exclude='.venv'
```

### Opsi 3: Menggunakan Script Python

Buat file `package_project.py`:

```python
import os
import shutil
import zipfile

# File yang akan di-include
files_to_include = [
    'app.py',
    'train_model.py',
    'requirements.txt',
    'README.md',
    'DEPLOYMENT.md',
    'SHARING_GUIDE.md',
    'check_setup.py',
    'Procfile',
    'Dockerfile',
    '.dockerignore',
    'runtime.txt',
    'model.pkl',  # jika ada
    'preprocessing_info.pkl',  # jika ada
]

# Buat zip
with zipfile.ZipFile('house-price-prediction.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in files_to_include:
        if os.path.exists(file):
            zipf.write(file)
            print(f"✅ Added: {file}")
        else:
            print(f"⚠️  Skipped (not found): {file}")

print("\n✅ Package created: house-price-prediction.zip")
```

## 🔗 Cara Sharing

### 1. GitHub/GitLab

```bash
# Initialize git
git init
git add app.py train_model.py requirements.txt README.md
git add Procfile runtime.txt Dockerfile .gitignore
git commit -m "Initial commit"
git remote add origin <repository-url>
git push -u origin main
```

**Note:** Jangan push file besar seperti `model.pkl` atau `train.csv` jika ukurannya > 50MB

### 2. Google Drive / Dropbox

1. Zip semua file yang diperlukan
2. Upload ke Google Drive / Dropbox
3. Share link dengan permission yang sesuai

### 3. Email (untuk file kecil)

1. Zip file yang diperlukan
2. Pastikan ukuran < 25MB (limit Gmail)
3. Attach ke email

### 4. USB Drive / Flashdisk

1. Copy folder proyek
2. Pastikan termasuk `model.pkl` dan `preprocessing_info.pkl`
3. Pastikan ada `requirements.txt` untuk install dependencies

## 📝 Checklist Sebelum Sharing

- [ ] File `.gitignore` sudah benar (tidak include file sensitif)
- [ ] `requirements.txt` sudah lengkap dan up-to-date
- [ ] `README.md` sudah jelas dan lengkap
- [ ] `model.pkl` dan `preprocessing_info.pkl` ada (atau ada instruksi untuk generate)
- [ ] Tidak ada password/API key yang hardcoded di code
- [ ] Test aplikasi setelah install dependencies baru
- [ ] Dokumentasi cara install dan run sudah jelas

## 🎯 Rekomendasi

### Untuk Deployment (Streamlit Cloud / Heroku):
✅ Share semua file kecuali dataset besar
✅ Pastikan `model.pkl` sudah di-commit (atau ada instruksi re-train)

### Untuk Kolaborasi (GitHub):
✅ Share code dan requirements.txt
✅ Model bisa di-generate dengan `train_model.py`
✅ Dataset bisa di-download terpisah

### Untuk Demo/Presentasi:
✅ Share `app.py`, `model.pkl`, `preprocessing_info.pkl`, `requirements.txt`
✅ Zip dan share via Google Drive

---

**Tips:** Selalu sertakan `README.md` yang jelas agar penerima tahu cara setup dan menjalankan proyek!

