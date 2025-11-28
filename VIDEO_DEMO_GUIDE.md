# 🎥 Panduan Membuat Video Demo Food Delivery System

## Target: Video ≤10 menit yang menampilkan semua requirement

---

## **REQUIREMENT VIDEO DEMO**

Video harus menampilkan:
1. Arsitektur sistem
2. Cara menjalankan komponen (Gateway → Services → Frontend)
3. Demo inter-service communication via Gateway
4. Dokumentasi API (Swagger UI + Postman)
5. Frontend konsumsi Gateway

**Durasi:** ≤10 menit  
**Format:** MP4 (recommended)  
**Platform:** YouTube (Unlisted) atau Google Drive  
**Quality:** 720p minimum, 1080p recommended

---

## **STORYBOARD VIDEO (10 MENIT)**

### **Segment 1: Opening + Intro (1 menit)**

**Teks/Narasi:**
```
"Halo, selamat datang di demo Food Delivery System.
Ini adalah project kelompok 01 untuk tugas Microservices.
Sistem ini dibangun menggunakan arsitektur microservices 
dengan Python Flask dan modern web frontend."
```

**Yang ditampilkan:**
- Title slide dengan nama project
- Anggota kelompok:
  * ARTHUR - User Service (Port 5001)
  * rizki - Restaurant Service (Port 5002)
  * Nadia - Order Service (Port 5003)
  * aydin - Delivery Service (Port 5004)
  * reza - Payment Service (Port 5005)

**Tools:** PowerPoint atau browser dengan slide HTML

---

### **Segment 2: Arsitektur Sistem (2 menit)**

**Teks/Narasi:**
```
"Sistem ini menggunakan arsitektur microservices modern.
Client atau Frontend berkomunikasi dengan API Gateway di port 5000.
Gateway kemudian meneruskan request ke microservices yang sesuai.
Setiap microservice memiliki database SQLite sendiri untuk independence."
```

**Yang ditampilkan:**
- Buka file `README.md` di browser atau text editor
- Tunjukkan diagram arsitektur (line 90-103):
  ```
  Frontend (HTML/JS @8080)
          │ fetch API
          ▼
  API Gateway (Flask @5000, JWT, Swagger)
          │ routing per prefix
          ▼
  Microservices (Flask @5001-5005)
          │ SQLAlchemy ORM
          ▼
  SQLite Database per service
  ```
- Tunjukkan table port assignments (line 111-119)
- Jelaskan flow komunikasi:
  * Frontend → Gateway (port 5000)
  * Gateway → User Service (port 5001)
  * Gateway → Restaurant Service (port 5002)
  * Gateway → Order Service (port 5003)
  * Gateway → Delivery Service (port 5004)
  * Gateway → Payment Service (port 5005)

**Highlight penting:**
- Client TIDAK memanggil microservices langsung
- Semua request melalui API Gateway
- Gateway bertanggung jawab untuk routing dan authentication

---

### **Segment 3: Menjalankan Komponen (2 menit)**

**Teks/Narasi:**
```
"Sekarang saya akan menunjukkan cara menjalankan sistem.
Pertama, kita start API Gateway, kemudian seluruh microservices,
dan terakhir frontend server."
```

**Yang ditampilkan:**

#### 3.1 Start API Gateway (20 detik)
```powershell
cd c:\xampp\htdocs\food_delivery_system\microservices\api-gateway
python app.py
```
- Tunjukkan output: `Running on http://127.0.0.1:5000`
- Akses di browser: `http://localhost:5000/health`
- Tunjukkan response JSON

#### 3.2 Start Microservices (60 detik)
**Speed up dengan split screen atau fast forward!**

```powershell
# Terminal 2
cd microservices\user-service
python app.py

# Terminal 3
cd microservices\restaurant-service
python app.py

# Terminal 4
cd microservices\order-service
python app.py

# Terminal 5
cd microservices\delivery-service
python app.py

# Terminal 6
cd microservices\payment-service
python app.py
```

- Tunjukkan sekilas setiap terminal (tidak perlu detail)
- ATAU gunakan screenshot 6 terminal sekaligus

#### 3.3 Verify Health Endpoints (20 detik)
```
http://localhost:5000/health  
http://localhost:5001/health  
http://localhost:5002/health  
http://localhost:5003/health  
http://localhost:5004/health  
http://localhost:5005/health  
```

- Buka browser tabs dengan semua health endpoints
- Fast forward, tidak perlu buka satu-satu

#### 3.4 Start Frontend (20 detik)
```powershell
cd frontend
python -m http.server 8080
```

- Akses: `http://localhost:8080`
- Tunjukkan home page muncul

---

### **Segment 4: Dokumentasi API (2 menit)**

**Teks/Narasi:**
```
"Project ini memiliki dokumentasi API yang lengkap,
yaitu Swagger UI dan Postman Collection.
Mari kita lihat keduanya."
```

#### 4.1 Swagger UI (60 detik)

**Akses:** `http://localhost:5000/api-docs/`

**Yang ditampilkan:**
1. Tunjukkan Swagger UI title
2. Scroll list endpoints:
   - GET /health
   - GET /services
   - POST /auth/register
   - POST /auth/login
   - GET /api/user-service/api/users
   - GET /api/restaurant-service/api/restaurants
   - POST /api/order-service/api/orders
   - dll

3. **Demo Try Out (PENTING!):**
   - Click endpoint `GET /health`
   - Click "Try it out"
   - Click "Execute"
   - Tunjukkan response:
     ```json
     {
       "status": "healthy",
       "service": "api-gateway",
       "timestamp": "..."
     }
     ```

#### 4.2 Postman Collection (60 detik)

**Buka Postman:**

**Yang ditampilkan:**
1. Collection "Food Delivery System API"
2. Expand folders:
   - Auth
   - User Service
   - Restaurant Service
   - Order Service
   - Delivery Service
   - Payment Service

3. **Demo 1 request:**
   - Click "Register User" atau "Login"
   - Tunjukkan request body (JSON)
   - Click "Send"
   - Tunjukkan response sukses (200/201)

**ATAU run Collection Runner:**
- Click "Run"
- Pilih beberapa requests
- Click "Run"
- Tunjukkan test results (PASSED)

---

### **Segment 5: Frontend Konsumsi Gateway (3 menit)**

**Teks/Narasi:**
```
"Sekarang saya akan mendemonstrasikan bagaimana frontend
memanggil API Gateway untuk mendapatkan data dari multiple services."
```

**PENTING:** Jelaskan bahwa frontend **HANYA** memanggil Gateway, TIDAK langsung ke services!

#### 5.1 Show API Configuration (20 detik)

**Buka file:** `frontend/js/main.js` di text editor

**Highlight line 2:**
```javascript
const API_GATEWAY = 'http://localhost:5000';
```

**Narasi:**
```
"Perhatikan bahwa frontend dikonfigurasi untuk memanggil
API Gateway di port 5000, bukan langsung ke microservices."
```

#### 5.2 Demo Flow #1: Restaurant List (60 detik)

**Akses:** `http://localhost:8080/`

**Yang ditampilkan:**
1. Home page dengan list restaurants
2. Buka Developer Tools (F12)
3. Tab "Network"
4. Refresh page
5. Tunjukkan fetch request ke:
   - `http://localhost:5000/api/restaurant-service/api/restaurants`
   - **BUKAN** `http://localhost:5002/...` (langsung ke service)
6. Tunjukkan response JSON dengan data restaurants

**Service yang terlibat:**
- Restaurant Service (via Gateway)

#### 5.3 Demo Flow #2: Order + Payment (60 detik)

**Akses:** `http://localhost:8080/checkout.html`

**Yang ditampilkan:**
1. Checkout page
2. Isi form checkout
3. Buka Network tab
4. Click "Place Order"
5. Tunjukkan multiple fetch requests ke Gateway:
   - POST `/api/order-service/api/orders` (Create Order)
   - POST `/api/payment-service/api/payments` (Process Payment)
6. Tunjukkan sukses message

**Services yang terlibat:**
- Order Service (via Gateway)
- Payment Service (via Gateway)

**Highlight:** "Perhatikan frontend memanggil 2 services berbeda melalui Gateway"

#### 5.4 Demo Flow #3: Order Tracking (60 detik)

**Akses:** `http://localhost:8080/order-tracking.html`

**Yang ditampilkan:**
1. Order tracking page
2. Input order ID
3. Buka Network tab
4. Click "Track Order"
5. Tunjukkan fetch requests ke Gateway:
   - GET `/api/order-service/api/orders/{id}` (Get Order)
   - GET `/api/delivery-service/api/deliveries/{id}` (Get Delivery Status)
6. Tunjukkan tracking info dengan delivery status

**Services yang terlibat:**
- Order Service (via Gateway)
- Delivery Service (via Gateway)

**Highlight:** "2 microservices berbeda bekerja sama untuk 1 fitur tracking"

---

### **Segment 6: Closing (30 detik)**

**Teks/Narasi:**
```
"Jadi ini adalah Food Delivery System kami dengan arsitektur microservices.
Fitur utama yang sudah diimplementasikan:
- User authentication
- Restaurant dan menu management
- Order processing
- Delivery tracking
- Payment handling

Semua komunikasi melalui API Gateway dengan dokumentasi lengkap
di Swagger UI dan Postman Collection.

Terima kasih!"
```

**Yang ditampilkan:**
- Summary slide dengan checklist:
  - 5 Microservices
  - API Gateway with JWT
  - SQLite Database per service
  - Swagger + Postman Documentation
  - Modern Web Frontend
  - Health Check Endpoints

---

## **TOOLS YANG DIBUTUHKAN**

### **Recording Software:**

**Option 1: OBS Studio (FREE, RECOMMENDED)**
- Download: https://obsproject.com/
- Pros: Professional, free, high quality
- Cons: Perlu setup awal

**Option 2: Windows Game Bar (BUILT-IN)**
- Shortcut: `Win + G`
- Pros: Sudah ada, simple
- Cons: Terbatas fiturnya

**Option 3: ShareX (FREE)**
- Download: https://getsharex.com/
- Pros: All-in-one, bisa screenshot + record
- Cons: Perlu install

**Option 4: Camtasia (PAID)**
- Download: https://www.techsmith.com/video-editor.html
- Pros: Full featured editor
- Cons: Berbayar (trial 30 hari)

### **Presentation Tools:**
- PowerPoint untuk title slides
- Browser untuk demo
- Text editor (VS Code) untuk show code
- Postman
- Multiple browser tabs

### **Editing Software (Optional):**
- DaVinci Resolve (FREE)
- Windows Video Editor (BUILT-IN)
- Adobe Premiere (PAID)

---

## **RECORDING CHECKLIST**

### **Pre-Recording:**
- [ ] Semua services sudah running
- [ ] Browser sudah open di tabs yang perlu
- [ ] Postman sudah setup dengan collection + environment
- [ ] Close aplikasi yang tidak perlu (Spotify, Discord, dll)
- [ ] Clear notifications (Do Not Disturb mode)
- [ ] Siapkan skrip/bullet points
- [ ] Test microphone (jika pakai narasi)

### **Recording Setup:**
- [ ] Resolution: 1920x1080 (1080p) atau 1280x720 (720p)
- [ ] Frame rate: 30 FPS minimum
- [ ] Audio quality: Clear (jika pakai narasi)
- [ ] Hide bookmark bar di browser
- [ ] Full screen browser untuk demo
- [ ] Zoom in jika perlu (text harus readable)

### **During Recording:**
- [ ] Slow down mouse movement (jangan terlalu cepat)
- [ ] Pause 1-2 detik sebelum pindah scene
- [ ] Highlight poin penting dengan cursor
- [ ] Jangan skip loading/waiting time (tapi bisa di-speed up saat edit)

### **Post-Recording:**
- [ ] Review video, pastikan tidak ada error
- [ ] Cut bagian yang tidak perlu
- [ ] Add title slide di awal (optional)
- [ ] Add text overlay untuk highlight (optional)
- [ ] Export video dalam format MP4

---

## 🎙️ **NARASI TIPS**

### **Option 1: Voice Over (RECOMMENDED)**
**Pros:**
- Lebih engaging
- Lebih mudah explain detail
- Terasa lebih personal

**Tips:**
- Gunakan microphone yang clear (built-in laptop OK)
- Record di ruangan yang sepi
- Speak clearly, tidak terlalu cepat
- Pause di antara sentences
- Gunakan skrip tapi jangan terlalu kaku

### **Option 2: Text Overlay Only**
**Pros:**
- Tidak perlu mic bagus
- Bisa dilakukan tanpa suara
- Lebih cepat

**Tips:**
- Gunakan text editor atau subtitle
- Font size harus besar dan readable
- Durasi text cukup lama untuk dibaca
- Gunakan warna kontras (putih di background gelap)

### **Option 3: Silent with Background Music**
**Cons:** TIDAK RECOMMENDED untuk video demo teknis

---

## **SKRIP LENGKAP (Copy-Paste Ready)**

```markdown
[00:00-00:30] OPENING
"Halo, selamat datang di demo Food Delivery System - Kelompok 01.
Project ini menggunakan arsitektur microservices dengan Python Flask
dan modern web frontend."

[SHOW: Title slide]

[00:30-01:00] TEAM
"Tim kami terdiri dari 5 anggota, masing-masing bertanggung jawab
atas satu microservice:
- ARTHUR untuk User Service di port 5001
- rizki untuk Restaurant Service di port 5002
- Nadia untuk Order Service di port 5003
- aydin untuk Delivery Service di port 5004
- Dan reza untuk Payment Service di port 5005"

[SHOW: Team table]

[01:00-02:00] ARSITEKTUR
"Sistem ini menggunakan arsitektur microservices modern.
Frontend berkomunikasi dengan API Gateway di port 5000.
Gateway kemudian meneruskan request ke microservices yang sesuai.
Setiap microservice memiliki database SQLite sendiri yang independent."

[SHOW: Diagram arsitektur]

"Poin penting: Client tidak pernah memanggil microservices langsung.
Semua request harus melalui API Gateway untuk centralized authentication
dan routing."

[02:00-04:00] RUNNING SERVICES
"Sekarang saya akan menunjukkan cara menjalankan sistem.
Pertama, kita start API Gateway..."

[SHOW: Terminal running gateway]

"Kemudian start seluruh microservices..."

[SHOW: Multiple terminals atau screenshot]

"Dan terakhir, frontend server..."

[SHOW: Frontend server running]

"Mari kita verify bahwa semua services healthy..."

[SHOW: Health endpoints di browser]

[04:00-06:00] DOKUMENTASI API
"Project ini memiliki dokumentasi API yang lengkap.
Pertama, kita punya Swagger UI..."

[SHOW: Swagger UI]

"Di sini kita bisa lihat seluruh endpoints yang tersedia.
Mari kita coba execute salah satu endpoint..."

[SHOW: Try out endpoint]

"Selain Swagger, kami juga punya Postman Collection lengkap
dengan environment..."

[SHOW: Postman]

"Collection ini berisi semua endpoints dari 5 microservices..."

[SHOW: Folders dalam collection]

"Mari kita jalankan salah satu request..."

[SHOW: Send request dan response]

[06:00-09:30] FRONTEND DEMO
"Sekarang yang paling penting: frontend konsumsi API Gateway.
Perhatikan bahwa frontend dikonfigurasi untuk hanya memanggil Gateway
di port 5000..."

[SHOW: main.js code]

"Mari kita lihat home page yang menampilkan list restaurants..."

[SHOW: Home page + Network tab]

"Perhatikan request fetch ke Gateway, bukan langsung ke Restaurant Service..."

[SHOW: Network request detail]

"Sekarang mari kita coba flow checkout yang melibatkan 2 services:
Order Service dan Payment Service..."

[SHOW: Checkout page]

"Ketika kita submit order, frontend akan memanggil Gateway
yang kemudian meneruskan ke Order Service dan Payment Service..."

[SHOW: Network tab dengan multiple requests]

"Dan terakhir, order tracking yang melibatkan Order Service
dan Delivery Service untuk realtime tracking..."

[SHOW: Order tracking page]

[09:30-10:00] CLOSING
"Jadi itu adalah demo Food Delivery System kami.
Fitur utama yang sudah diimplementasikan:
- User authentication dan authorization
- Restaurant dan menu management
- Order processing
- Delivery tracking
- Payment handling

Semua komunikasi melalui API Gateway dengan dokumentasi lengkap
di Swagger UI dan Postman Collection.

Terima kasih atas perhatiannya!"

[SHOW: Summary slide]
```

---

## 📤 **UPLOAD DAN SUBMIT**

### **YouTube Upload (RECOMMENDED):**

1. **Login ke YouTube**
2. **Click "Create" → "Upload video"**
3. **Pilih file video MP4**
4. **Settings:**
   - Title: "Food Delivery System - Microservices Demo - Kelompok 01"
   - Description:
     ```
     Demo Food Delivery System dengan arsitektur microservices.
     
     Tech Stack:
     - Python Flask
     - SQLite
     - HTML/CSS/JavaScript
     - Swagger UI
     - Postman
     
     Team:
     - ARTHUR (User Service)
     - rizki (Restaurant Service)
     - Nadia (Order Service)
     - aydin (Delivery Service)
     - reza (Payment Service)
     ```
   - Visibility: **UNLISTED** (penting!)
   - Category: Education
   - Tags: microservices, flask, python, api gateway

5. **Click "Publish"**
6. **Copy URL** (format: `https://youtu.be/xxxxxxxxxxxxx`)
7. **Paste URL ke file** `video/link.txt`

### **Google Drive Upload (ALTERNATIVE):**

1. **Upload file ke Google Drive**
2. **Right-click → Share**
3. **Change to "Anyone with the link can view"**
4. **Copy link**
5. **Paste ke** `video/link.txt`

---

## **TIME MANAGEMENT**

| Task | Duration | When |
|------|----------|------|
| Preparation | 30 min | Now |
| Recording (multiple takes) | 60-90 min | Today |
| Review | 15 min | Today |
| Edit (optional) | 30-60 min | Today/Tomorrow |
| Export | 15 min | Tomorrow |
| Upload | 20 min | Tomorrow |
| Update link.txt | 5 min | Tomorrow |
| **TOTAL** | **~3-4 hours** | |

**Recommended Schedule:**
- **Today (27 Nov):** Preparation + Recording attempts
- **Tomorrow (28 Nov) Morning:** Final recording + Edit
- **Tomorrow Afternoon:** Upload + Submit

---

## 🚨 **COMMON MISTAKES TO AVOID**

### **DON'T:**
- Berbicara terlalu cepat (slow down!)
- Skip loading time tanpa penjelasan
- Lupa show API Gateway config di frontend
- Record dalam resolusi rendah (<720p)
- Lupa mention bahwa frontend calls Gateway, NOT services directly
- Upload sebagai "Public" (harus Unlisted)

### **DO:**
- Speak clearly dan tidak terburu-buru
- Highlight poin penting dengan mouse cursor
- Emphasize Gateway sebagai single entry point
- Test play video sebelum upload
- Verify URL accessible sebelum submit

---

## 🎓 **FINAL CHECKLIST**

Sebelum upload, pastikan video menampilkan:

- [ ] Arsitektur diagram (Client → Gateway → Services → DB)
- [ ] Start API Gateway
- [ ] Start minimal 3 microservices (tidak harus semua, bisa screenshot)
- [ ] Health check endpoints
- [ ] Swagger UI + try out minimal 1 endpoint
- [ ] Postman Collection + execute minimal 1 request
- [ ] Frontend code showing `API_GATEWAY` config
- [ ] Frontend demo dengan Network tab showing requests to Gateway
- [ ] Minimal 2 pages dari ≥2 services berbeda
- [ ] Emphasize: "Frontend memanggil Gateway, BUKAN langsung ke services"

---

**READY TO RECORD? LET'S GO! **

**Next step:** Setelah video selesai → Update `video/link.txt` → DONE! 
