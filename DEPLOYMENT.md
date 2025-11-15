# 🚀 Panduan Deployment - Prediksi Harga Rumah

Panduan lengkap untuk mendeploy aplikasi Prediksi Harga Rumah ke berbagai platform.

## 📋 Persiapan Sebelum Deployment

### 1. Training Model Terlebih Dahulu

Sebelum deployment, pastikan model sudah di-train:

```bash
python train_model.py
```

Ini akan menghasilkan:
- `model.pkl` - Model yang sudah di-train
- `preprocessing_info.pkl` - Informasi preprocessing

**⚠️ PENTING:** File `model.pkl` dan `preprocessing_info.pkl` harus ada di repository saat deployment!

## 🌐 Opsi Deployment

### 1. Streamlit Cloud (RECOMMENDED - Paling Mudah) ⭐

**Keuntungan:**
- ✅ Gratis
- ✅ Mudah digunakan
- ✅ Auto-deploy dari GitHub
- ✅ Tidak perlu setup server

**Langkah-langkah:**

1. **Push code ke GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy ke Streamlit Cloud**
   - Kunjungi https://share.streamlit.io/
   - Login dengan akun GitHub
   - Klik tombol "New app"
   - Isi form:
     - **Repository:** Pilih repository Anda
     - **Branch:** main (atau branch yang digunakan)
     - **Main file path:** `app.py`
     - **Python version:** 3.9
   - Klik "Deploy"

3. **Tunggu deployment selesai**
   - Streamlit akan otomatis install dependencies
   - Pastikan `model.pkl` dan `preprocessing_info.pkl` ada di repo
   - Jika model belum ada, jalankan training di local dan commit file tersebut

**Troubleshooting:**
- Jika model tidak ditemukan, pastikan file `.pkl` sudah di-commit ke GitHub
- Jika error dependencies, periksa `requirements.txt`

---

### 2. Heroku

**Langkah-langkah:**

1. **Install Heroku CLI**
   - Download dari https://devcenter.heroku.com/articles/heroku-cli

2. **Login ke Heroku**
   ```bash
   heroku login
   ```

3. **Buat aplikasi Heroku**
   ```bash
   heroku create your-app-name
   ```

4. **Deploy ke Heroku**
   ```bash
   git push heroku main
   ```

5. **Buka aplikasi**
   ```bash
   heroku open
   ```

**Catatan:**
- File `Procfile` sudah disediakan untuk Heroku
- Pastikan model sudah di-train dan di-commit
- Heroku gratis tier memiliki limit resources

---

### 3. Docker

**Langkah-langkah:**

1. **Build Docker image**
   ```bash
   docker build -t house-price-prediction .
   ```

2. **Run container**
   ```bash
   docker run -p 8501:8501 house-price-prediction
   ```

3. **Akses aplikasi**
   - Buka browser: http://localhost:8501

**Deploy ke Docker Hub:**

1. **Tag image**
   ```bash
   docker tag house-price-prediction your-username/house-price-prediction
   ```

2. **Push ke Docker Hub**
   ```bash
   docker push your-username/house-price-prediction
   ```

**Deploy ke Cloud yang support Docker:**
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

---

### 4. AWS EC2 / VPS

**Langkah-langkah:**

1. **SSH ke server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   ```

3. **Clone repository**
   ```bash
   git clone <your-repo-url>
   cd "uts machine learning"
   ```

4. **Setup virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Train model (jika belum)**
   ```bash
   python train_model.py
   ```

6. **Jalankan aplikasi**
   ```bash
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```

**Untuk Production (menggunakan systemd):**

1. **Buat service file**
   ```bash
   sudo nano /etc/systemd/system/streamlit-app.service
   ```

2. **Isi file service:**
   ```ini
   [Unit]
   Description=Streamlit House Price Prediction App
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/your/app
   Environment="PATH=/path/to/venv/bin"
   ExecStart=/path/to/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Aktifkan dan start service**
   ```bash
   sudo systemctl enable streamlit-app
   sudo systemctl start streamlit-app
   sudo systemctl status streamlit-app
   ```

4. **Setup reverse proxy dengan Nginx** (optional)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

---

### 5. Google Cloud Run

**Langkah-langkah:**

1. **Install Google Cloud SDK**
   - Download dari https://cloud.google.com/sdk/docs/install

2. **Build dan push Docker image**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/house-price-prediction
   ```

3. **Deploy ke Cloud Run**
   ```bash
   gcloud run deploy house-price-prediction \
     --image gcr.io/YOUR_PROJECT_ID/house-price-prediction \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

---

## ✅ Checklist Sebelum Deployment

- [ ] Model sudah di-train (`model.pkl` ada)
- [ ] Preprocessing info ada (`preprocessing_info.pkl` ada)
- [ ] `requirements.txt` sudah lengkap
- [ ] File deployment sudah ada (Procfile, Dockerfile, dll)
- [ ] README sudah update
- [ ] Kode sudah di-test di local

## 🐛 Troubleshooting Umum

### Error: Model tidak ditemukan
**Solusi:**
- Pastikan `train_model.py` sudah dijalankan
- Pastikan `model.pkl` dan `preprocessing_info.pkl` ada di directory yang sama dengan `app.py`
- Jika deploy ke cloud, pastikan file `.pkl` sudah di-commit ke repository

### Error: Port sudah digunakan
**Solusi:**
```bash
# Gunakan port lain
streamlit run app.py --server.port 8502
```

### Error: Dependencies tidak terinstall
**Solusi:**
- Periksa `requirements.txt`
- Install manual: `pip install -r requirements.txt`
- Pastikan versi Python sesuai (3.8+)

### Error saat deployment ke Heroku/Cloud
**Solusi:**
- Periksa log deployment
- Pastikan semua file yang diperlukan sudah di-commit
- Pastikan `Procfile` atau `Dockerfile` sudah benar
- Periksa ukuran file (beberapa cloud punya limit)

## 📞 Bantuan

Jika mengalami masalah, periksa:
1. Log error di platform deployment
2. README.md untuk instruksi umum
3. Dokumentasi platform yang digunakan

---

**Selamat Deploying! 🚀**

