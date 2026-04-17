# PatchPoint - Quick Start Guide

## 📋 Prerequisites

- Node.js v18+
- MongoDB Atlas account (free tier)
- Cloudinary account (free tier)
- Python 3.8+ (for Pi script)
- Git

---

## 🚀 Quick Local Setup (5 minutes)

### 1️⃣ Clone & Install

```bash
# Clone repository
git clone https://github.com/Keerthiii21/temp.git
cd temp

# Backend setup
cd backend
npm install
cp .env.example .env
# Edit .env with your MongoDB & Cloudinary credentials

# Frontend setup
cd ../frontend
npm install
cp .env.example .env
# .env is already set to http://localhost:5000
```

### 2️⃣ Configure Secrets

**backend/.env**

```dotenv
PORT=5000
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/potholeDB
JWT_SECRET=your_secret_key_here
CORS_ORIGIN=http://localhost:5173,http://localhost:5174
CLOUDINARY_CLOUD_NAME=your_name
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret
```

**frontend/.env** (already configured)

```dotenv
VITE_API_URL=http://localhost:5000
```

### 3️⃣ Start Both Servers

**Terminal 1 - Backend**

```bash
cd backend
npm run dev
# Should see: "Server running on port 5000"
```

**Terminal 2 - Frontend**

```bash
cd frontend
npm run dev
# Should see: "VITE ready in 643 ms"
# Open http://localhost:5173 or http://localhost:5174
```

### 4️⃣ Test the App

1. **Sign up** at `http://localhost:5173/signup`
2. **Login** at `http://localhost:5173/login`
3. **View Dashboard** - should see "Total Reports: 0"
4. **Upload Pothole** - upload an image with location
5. **View on Map** - see markers appear

---

## 🔄 Project Structure

```
temp/
├── backend/
│   ├── src/
│   │   ├── models/        # MongoDB schemas
│   │   ├── controllers/   # API logic
│   │   ├── routes/        # API endpoints
│   │   ├── middleware/    # Auth, validation
│   │   └── config/        # DB, Cloudinary
│   ├── .env              # ⚠️ DO NOT COMMIT
│   ├── .env.example      # Template (commit this)
│   └── server.js         # Express app
│
├── frontend/
│   ├── src/
│   │   ├── pages/        # Page components
│   │   ├── components/   # Reusable UI
│   │   ├── api/          # API calls
│   │   ├── context/      # Auth context
│   │   └── styles.css    # Tailwind directives
│   ├── .env              # ⚠️ DO NOT COMMIT
│   ├── .env.example      # Template (commit this)
│   └── vite.config.js    # Build config
│
├── FINAL_INTEGRATION_STORED_VIDEO.py  # Pi upload helper
├── DEPLOYMENT.md         # Production deploy guide
└── README.md            # Project overview
```

---

## 🔑 API Quick Reference

### Register User

```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name":"John",
    "email":"john@example.com",
    "password":"password123"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"john@example.com",
    "password":"password123"
  }' \
  -c cookies.txt  # Save cookies for auth
```

### Get All Potholes

```bash
curl http://localhost:5000/api/potholes
```

### Upload Pothole from Pi

```bash
curl -X POST http://localhost:5000/api/potholes/pi-upload \
  -F "image=@/path/to/pothole.jpg" \
  -F "lat=37.7749" \
  -F "lon=-122.4194" \
  -F "depth=8.5" \
  -F "timestamp=$(date +%s)000"
```

---

## 📱 Pi Setup (Optional)

### Install Dependencies

```bash
pip3 install requests numpy opencv-python onnx onnxruntime
```

### Configure & Run

```python
# In FINAL_INTEGRATION_STORED_VIDEO.py, update:
BACKEND_URL = "http://your-pc-ip:5000/api/potholes/pi-upload"

# Then call in your detection pipeline:
from FINAL_INTEGRATION_STORED_VIDEO import send_to_backend

send_to_backend(
    image_path='frame.jpg',
    lat=37.7749,
    lon=-122.4194,
    depth_cm=8.5,
    timestamp_ms=int(time.time() * 1000)
)
```

---

## 🛠 Common Issues & Fixes

### "Invalid URL" Error

- Check `VITE_API_URL` in `frontend/.env`
- Should be `http://localhost:5000` for local dev
- Restart frontend: `npm run dev`

### CORS Error in Browser Console

- Check `CORS_ORIGIN` in `backend/.env`
- Should include `http://localhost:5173,http://localhost:5174`
- Restart backend: `npm run dev`

### MongoDB Connection Error

- Verify `MONGO_URI` is correct
- Check MongoDB Atlas IP whitelist includes your IP
- Test: `mongosh "your_mongo_uri"`

### Cloudinary Upload Fails

- Verify `CLOUDINARY_CLOUD_NAME`, `API_KEY`, `API_SECRET`
- Check Cloudinary dashboard for errors
- Ensure folder exists: `patchpoint/pi` (auto-created if not)

### Port Already in Use

```bash
# Kill process on port 5000 (Windows)
Get-NetTCPConnection -LocalPort 5000 | Stop-Process -Force

# Kill process on port 5000 (Mac/Linux)
lsof -ti:5000 | xargs kill -9
```

---

## 📚 Development Commands

### Backend

```bash
npm run dev       # Start with hot reload (nodemon)
npm start         # Start without auto-reload
npm test          # Run tests (if added)
```

### Frontend

```bash
npm run dev       # Start dev server (Vite)
npm run build     # Build for production
npm run preview   # Preview production build
```

---

## 🎨 Features Overview

### Authentication

- ✅ Signup/Login with JWT
- ✅ HTTP-only secure cookies
- ✅ Protected routes (Dashboard, Upload, Comments)

### Dashboard

- ✅ Real-time stats (total potholes, avg depth, today's count)
- ✅ Interactive Leaflet map with markers
- ✅ Auto-refresh every 10s for live Pi detections
- ✅ Recent potholes table with filtering

### Upload

- ✅ Drag-and-drop file upload
- ✅ GPS coordinates input
- ✅ Depth measurement input
- ✅ Image preview before upload
- ✅ Upload to Cloudinary with MongoDB record

### Pi Integration

- ✅ YOLOv5 ONNX detection
- ✅ LiDAR depth measurement
- ✅ GPS coordinates capture
- ✅ Auto-upload to backend
- ✅ Best frame selection

### Comments (Future)

- 📝 Add comments to potholes
- 📝 View comment threads
- 📝 Real-time comment updates

---

## 🚀 Next Steps

1. **Local Testing**: Run all 3 components locally
2. **Verification**: Test every endpoint
3. **Deployment**: Follow DEPLOYMENT.md
4. **Pi Integration**: Deploy Python script to Raspberry Pi
5. **Monitoring**: Set up logs and alerts

---

## 📞 Support

- Check error logs in browser console (`F12`)
- Check server logs in terminal
- Test endpoints with curl or Postman
- Review DEPLOYMENT.md for prod issues

---

**Happy detecting! 🚀**
