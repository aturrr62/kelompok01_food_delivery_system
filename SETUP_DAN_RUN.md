# PANDUAN LENGKAP SETUP DAN MENJALANKAN PROGRAM

Dokumen ini menjelaskan langkah-langkah untuk setup dan menjalankan **Food Delivery System** di komputer Anda.

---

## Prasyarat (Prerequisites)

Sebelum mulai, pastikan sudah terinstall:
- **Python 3.8+** — cek dengan: `python --version`
- **Git** — cek dengan: `git --version`
- **pip** (Python package manager) — biasanya sudah dengan Python

Jika belum ada, download dari:
- Python: https://www.python.org/downloads/
- Git: https://git-scm.com/download/

---

## Struktur Project

```
food_delivery_system/
├── microservices/
│   ├── api-gateway/           # Gateway utama (port 5000)
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── run.sh
│   ├── service-template/      # Template untuk microservice (port 5001)
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── run.sh
├── frontend/                   # Frontend HTML/JS
│   ├── index.html
│   └── js/
├── scripts/                    # Script helper
│   ├── setup.sh
│   └── run-all.sh
└── docs/                       # Dokumentasi
```

---

## CARA TERCEPAT (Recommended)

Buka **PowerShell** atau **Command Prompt** dan jalankan perintah ini:

### 1️⃣ Clone Repository (Jika belum punya folder lokal)
```powershell
git clone https://github.com/aturrr62/kelompok01_food_delivery_system.git
cd kelompok01_food_delivery_system
```

### 2️⃣ Buka 3 Terminal Terpisah

Buka **3 PowerShell windows** untuk menjalankan:
- Terminal 1: API Gateway
- Terminal 2: Service Template
- Terminal 3: (Optional) Test/monitoring

---

## 📖 STEP-BY-STEP DETAIL

### Terminal 1: Setup & Jalankan API Gateway (port 5000)

```powershell
# 1. Pindah ke folder api-gateway
cd c:\xampp\htdocs\food_delivery_system\microservices\api-gateway

# 2. Install dependencies (hanya perlu 1x, atau jika ada perubahan requirements.txt)
pip install -r requirements.txt

# 3. Jalankan server
python app.py
```

**Output yang diharapkan:**
```
API Gateway starting on port 5000
📡 Available services:
   - user-service: http://localhost:5001
   - restaurant-service: http://localhost:5002
   - order-service: http://localhost:5003
   - delivery-service: http://localhost:5004
   - payment-service: http://localhost:5005

 WARNING in app.run
 * Running on http://0.0.0.0:5000 (Press CTRL+C to quit)
 * Restarting with reloader
```

**Gateway siap di:** http://localhost:5000

---

### Terminal 2: Setup & Jalankan Service Template (port 5001)

Buka PowerShell **baru** dan jalankan:

```powershell
# 1. Pindah ke folder service-template
cd c:\xampp\htdocs\food_delivery_system\microservices\service-template

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan server
python app.py
```

**Output yang diharapkan:**
```
Service starting on port 5001
 WARNING in app.run
 * Running on http://0.0.0.0:5001 (Press CTRL+C to quit)
```

**Service siap di:** http://localhost:5001

---

### Terminal 3 (Optional): Test API dengan curl atau Postman

Buka PowerShell **ketiga** untuk test:

```powershell
# Test Gateway Health
curl http://localhost:5000/health

# Test Service Health (langsung)
curl http://localhost:5001/health

# Test GET semua data (sebelum ada data, akan return array kosong)
curl http://localhost:5001/api/examples

# Test POST data baru
curl -X POST http://localhost:5001/api/examples `
  -H "Content-Type: application/json" `
  -d '{"name":"Contoh","description":"Test data"}'
```

---

## Akses Aplikasi

Setelah kedua server berjalan:

### Gateway (API + Proxy)
- URL: **http://localhost:5000**
- Swagger Docs: **http://localhost:5000/api/docs/** (jika ada)
- Health: **http://localhost:5000/health**

### Service Langsung
- URL: **http://localhost:5001**
- Health: **http://localhost:5001/health**
- API Contoh: **http://localhost:5001/api/examples**

### Frontend (opsional)
- Buka `frontend/index.html` di browser atau gunakan live server di VS Code

---

## Troubleshooting

### Error: `ModuleNotFoundError: No module named 'flask_cors'`
**Solusi:**
```powershell
pip install -r requirements.txt
```
Pastikan sudah di folder yang tepat (`api-gateway/` atau `service-template/`).

### Error: `Address already in use` (port sudah dipakai)
**Solusi:**
- Ubah port di `app.py` (cari `app.run(host='0.0.0.0', port=5000, debug=True)`)
- Atau stop program lain yang pakai port 5000/5001

### Error: `python: command not found`
**Solusi:**
- Pastikan Python sudah terinstall dan ditambah ke PATH
- Coba gunakan `python3` atau path lengkap: `C:\Python311\python.exe app.py`

### ModuleNotFoundError di tengah eksekusi
**Solusi:**
```powershell
# Re-install semua dependencies
pip install --upgrade -r requirements.txt
```

---

## Quick Reference Commands

```powershell
# Install dependencies
pip install -r requirements.txt

# Jalankan api-gateway
python c:\xampp\htdocs\food_delivery_system\microservices\api-gateway\app.py

# Jalankan service-template
python c:\xampp\htdocs\food_delivery_system\microservices\service-template\app.py

# Test endpoint (Windows PowerShell)
curl http://localhost:5000/health
curl http://localhost:5001/health

# List semua proses Python yang berjalan
Get-Process python

# Kill proses Python (jika perlu)
Stop-Process -Name python -Force
```

---

## Advanced: Jalankan Semua Sekaligus (Script)

Jika sudah setup semua, bisa gunakan script batch:

**Windows: `run-all.bat` (buat file baru)**
```batch
@echo off
start cmd /k "cd microservices\api-gateway && python app.py"
start cmd /k "cd microservices\service-template && python app.py"
```

Simpan sebagai `run-all.bat` di root folder, lalu double-click untuk jalankan.

---

## Dokumentasi Lainnya

- `CRUD_FEATURES.md` — Fitur CRUD yang tersedia
- `POSTMAN_TESTING_STEPS.md` — Cara test di Postman
- `PANDUAN_LENGKAP_RUNNING.md` — Panduan lebih detail

---

## Tips

1. **Gunakan Python Virtual Environment** (opsional tapi recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Buat shortcut untuk buka folder cepat**:
   - Windows: Buat `.lnk` file ke folder project

3. **Gunakan VS Code Terminal**:
   - Built-in terminal di VS Code lebih mudah untuk manage multiple terminals

---

## ❓ Butuh Bantuan?

Jika ada error atau masalah:
1. Baca pesan error dengan teliti
2. Cek apakah semua requirements sudah diinstall (`pip list`)
3. Pastikan Python version compatible (3.8+)
4. Lihat folder `docs/` untuk dokumentasi lainnya

---

**Happy coding! **
