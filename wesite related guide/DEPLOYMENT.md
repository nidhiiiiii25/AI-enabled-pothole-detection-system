# PatchPoint Deployment Guide

## Overview

PatchPoint is a full-stack pothole detection system consisting of:

- **Frontend**: React + Vite + TailwindCSS (deployed to Vercel/Netlify)
- **Backend**: Node.js + Express (deployed to Render/Railway/Heroku)
- **Pi Detection**: Python script with YOLOv5 + LiDAR + GPS

---

## 🚀 Frontend Deployment (Vercel / Netlify / Render)

### Option 1: Deploy to Vercel (Recommended for Frontend)

1. **Connect GitHub**

   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository (Keerthiii21/temp)

2. **Configure Build Settings**

   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `frontend/dist`
   - Root Directory: `frontend`

3. **Set Environment Variables** (in Vercel Dashboard)

   ```
   VITE_API_URL=https://your-backend-url.com
   ```

4. **Deploy**
   - Click Deploy
   - Vercel auto-deploys on every push to `main`

### Option 2: Deploy to Netlify

1. **Connect GitHub**

   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Select your repository

2. **Configure Build Settings**

   - Build Command: `cd frontend && npm run build`
   - Publish Directory: `frontend/dist`
   - Add Environment Variable: `VITE_API_URL=https://your-backend-url.com`

3. **Deploy**
   - Netlify auto-deploys on push to `main`

### Option 3: Deploy to Render (Both Frontend & Backend on Same Platform)

1. **Create Render Account** at [render.com](https://render.com)

2. **Create New Static Site**

   - Click "New +" → "Static Site"
   - Connect GitHub Repository
   - Select repo: `temp`
   - Name: `patchpoint-frontend`
   - Build Command: `cd frontend && npm run build`
   - Publish Directory: `frontend/dist`

3. **Set Environment Variables** (in Render Dashboard)

   ```
   VITE_API_URL=https://your-backend-url-on-render.com
   ```

4. **Deploy**
   - Click Deploy
   - Render auto-deploys on push to `main`
   - Your frontend will be at `*.render.com`

### Post-Deploy: Update Backend URL

After backend is deployed, update the frontend environment variable:

```bash
# In Vercel/Netlify/Render Dashboard
VITE_API_URL=https://your-production-backend.com
```

---

## 🔧 Backend Deployment (Render / Railway / Heroku)

### Option 1: Deploy to Render

1. **Create Render Account** at [render.com](https://render.com)

2. **Create New Web Service**

   - Connect GitHub Repository
   - Select repo: `temp`
   - Name: `patchpoint-backend`
   - Runtime: Node
   - Root Directory: `backend`
   - Build Command: `npm install`
   - Start Command: `npm start`

3. **Set Environment Variables** (in Render Dashboard)

   ```
   PORT=5000
   MONGO_URI=<your_mongodb_uri>
   JWT_SECRET=<your_jwt_secret>
   CORS_ORIGIN=https://your-frontend-domain.com
   CLOUDINARY_CLOUD_NAME=<your_cloudinary_name>
   CLOUDINARY_API_KEY=<your_cloudinary_key>
   CLOUDINARY_API_SECRET=<your_cloudinary_secret>
   ```

4. **Deploy**
   - Click Deploy
   - Render auto-deploys on push to `main`

### Option 2: Deploy to Railway

1. **Create Railway Account** at [railway.app](https://railway.app)

2. **New Project → Deploy from GitHub**

   - Select repo: `temp`

3. **Configure Service**

   - Root Directory: `backend`
   - Add Variables (same as above)

4. **Deploy**
   - Railway auto-deploys on push

### Option 3: Deploy to Heroku

1. **Create Heroku Account** at [heroku.com](https://heroku.com)

2. **Create New App**

   - Name: `patchpoint-backend`

3. **Connect GitHub**

   - Connect to your repository
   - Enable auto-deploy on main

4. **Set Config Vars** (Heroku Dashboard → Settings → Config Vars)

   - Same variables as above

5. **Deploy**
   - Manual deploy or enable auto-deploy

---

## 📱 Pi Deployment (Raspberry Pi)

### Prerequisites

```bash
pip3 install requests numpy opencv-python onnx onnxruntime
```

### Setup

1. **Update Backend URL**

   - Edit `FINAL_INTEGRATION_STORED_VIDEO.py`
   - Replace `<PC_IP>` with your backend domain:

   ```python
   BACKEND_URL = "https://your-production-backend.com/api/potholes/pi-upload"
   ```

2. **Install Dependencies**

   ```bash
   pip3 install requests
   ```

3. **Run Detection Script**
   ```bash
   python3 FINAL_INTEGRATION_STORED_VIDEO.py
   ```

### Integration with Your Pipeline

In your existing detection code, call:

```python
from FINAL_INTEGRATION_STORED_VIDEO import send_to_backend

# After detecting a pothole:
send_to_backend(
    image_path='/path/to/frame.jpg',
    lat=37.7749,
    lon=-122.4194,
    depth_cm=8.5,
    timestamp_ms=int(time.time() * 1000)
)
```

---

## 🔗 API Endpoints

### Public Endpoints (No Auth Required)

- `GET /api/potholes` - List all potholes
- `POST /api/potholes/pi-upload` - Pi upload (multipart/form-data)

### Protected Endpoints (Auth Required)

- `POST /api/auth/signup` - Register user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Current user
- `POST /api/potholes` - User upload pothole

### Upload Format (Pi)

```bash
curl -X POST 'https://your-backend.com/api/potholes/pi-upload' \
  -F "image=@/path/to/image.jpg" \
  -F "lat=37.7749" \
  -F "lon=-122.4194" \
  -F "depth=8.5" \
  -F "timestamp=1670000000000"
```

---

## 📊 Database Setup

### MongoDB Atlas

1. Create account at [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)
2. Create free cluster
3. Get connection string: `mongodb+srv://user:pass@cluster.mongodb.net/dbname`
4. Add to backend environment variables as `MONGO_URI`

---

## ☁️ Image Storage (Cloudinary)

1. Create account at [cloudinary.com](https://cloudinary.com)
2. Get your credentials:
   - Cloud Name
   - API Key
   - API Secret
3. Add to backend environment variables

---

## 🌐 Domain & CORS Configuration

### Update CORS After Deployment

Once you have your frontend domain, update backend `CORS_ORIGIN`:

**For Render Dashboard:**

```
CORS_ORIGIN=https://your-frontend-domain.com,https://your-frontend-domain.com
```

**For Local Testing:**

```
CORS_ORIGIN=http://localhost:5173,http://localhost:5174
```

---

## ✅ Verification Checklist

After deployment:

- [ ] Frontend loads at `https://your-frontend-domain.com`
- [ ] Backend API responds at `https://your-backend.com/api/potholes`
- [ ] Login works without CORS errors
- [ ] Dashboard loads and fetches potholes
- [ ] Map displays pothole markers
- [ ] Can upload potholes from frontend
- [ ] Pi can send requests to backend without "Invalid URL" errors
- [ ] New Pi detections appear in dashboard within 10 seconds

---

## 🐛 Troubleshooting

### "Invalid URL" Frontend Error

- Check `VITE_API_URL` in environment variables
- Ensure backend domain is correct: `https://your-backend.com`
- Restart frontend build

### CORS Error

- Update backend `CORS_ORIGIN` to include your frontend domain
- Make sure to restart backend after env changes

### Pi Upload Fails

- Verify `BACKEND_URL` in `FINAL_INTEGRATION_STORED_VIDEO.py`
- Check that Pi can reach backend (test with `curl`)
- Ensure Cloudinary credentials are set in backend

### Slow Pothole Polling

- Frontend polls every 10 seconds (see Dashboard.jsx)
- Reduce interval in code if needed, but watch API rate limits

---

## 📝 Important Notes

- **Never commit `.env` files** - they're in `.gitignore` for security
- **Use `.env.example`** as a reference for required variables
- **Rotate JWT_SECRET** in production
- **Keep Cloudinary credentials private**
- **Monitor Cloudinary storage** for image costs
- **Set up MongoDB backup** for production data

---

## 🚀 Summary

1. **Push Code** → Already done ✅
2. **Deploy Backend** → Render/Railway/Heroku
3. **Set Backend ENV** → MongoDB, Cloudinary, CORS, JWT
4. **Deploy Frontend** → Vercel/Netlify
5. **Set Frontend ENV** → Backend URL
6. **Test Endpoints** → Verify all working
7. **Deploy Pi** → Update URL and run

**Your PatchPoint system is now ready for production! 🎉**
