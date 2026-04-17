# Deploy PatchPoint with Render Only (Backend + Frontend)

This guide shows how to deploy **both** the backend and frontend to **Render.com** in one place.

---

## 🎯 Why Deploy Everything to Render?

✅ **One dashboard** to manage both services  
✅ **Free tier** available for testing  
✅ **Auto-deploy** from GitHub  
✅ **Easy scaling** if needed  
✅ **No need** for Vercel/Netlify

---

## 📋 Prerequisites

- Render account (create at [render.com](https://render.com))
- MongoDB Atlas connection string (get from [mongodb.com](https://mongodb.com))
- Cloudinary credentials (get from [cloudinary.com](https://cloudinary.com))

---

## Step 1️⃣: Deploy Backend to Render

### Create Web Service for Backend

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Select **"Build and deploy from a Git repository"**
4. Choose your repo: **`Keerthiii21/temp`**

### Configure Service

| Setting            | Value                           |
| ------------------ | ------------------------------- |
| **Name**           | `patchpoint-backend`            |
| **Environment**    | `Node`                          |
| **Region**         | `Frankfurt` (or closest to you) |
| **Branch**         | `main`                          |
| **Root Directory** | `backend`                       |
| **Build Command**  | `npm install`                   |
| **Start Command**  | `npm start`                     |

### Set Environment Variables

Click **"Add Environment Variable"** and add these:

```env
PORT=5000
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/potholeDB
JWT_SECRET=your-very-secret-key-here-min-32-chars
CORS_ORIGIN=https://patchpoint-frontend.render.com
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Deploy

Click **"Create Web Service"**

⏳ Wait 3-5 minutes for deployment

✅ Note your backend URL: `https://patchpoint-backend.render.com`

---

## Step 2️⃣: Deploy Frontend to Render

### Create Static Site for Frontend

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Static Site"**
3. Select **"Build and deploy from a Git repository"**
4. Choose your repo: **`Keerthiii21/temp`**

### Configure Service

| Setting               | Value                          |
| --------------------- | ------------------------------ |
| **Name**              | `patchpoint-frontend`          |
| **Region**            | `Frankfurt` (same as backend)  |
| **Branch**            | `main`                         |
| **Build Command**     | `cd frontend && npm run build` |
| **Publish Directory** | `frontend/dist`                |

### Set Environment Variables

Click **"Add Environment Variable"** and add:

```env
VITE_API_URL=https://patchpoint-backend.render.com
```

(Replace with your actual backend URL from Step 1)

### Deploy

Click **"Create Static Site"**

⏳ Wait 2-3 minutes for deployment

✅ Note your frontend URL: `https://patchpoint-frontend.render.com`

---

## Step 3️⃣: Update CORS on Backend

Now that frontend is deployed, update the backend CORS setting:

1. Go to **Backend Service** in Render
2. Go to **Settings** → **Environment**
3. Update **`CORS_ORIGIN`** to your frontend URL:
   ```
   CORS_ORIGIN=https://patchpoint-frontend.render.com
   ```
4. Click **"Save"**
5. Service auto-redeploys (wait 1-2 minutes)

---

## Step 4️⃣: Test Everything

### Test Frontend

```bash
# Visit in browser
https://patchpoint-frontend.render.com
```

- ✅ Login page loads (no CORS errors)
- ✅ Sign up works
- ✅ Dashboard loads
- ✅ Map displays

### Test Backend API

```bash
# Get all potholes
curl https://patchpoint-backend.render.com/api/potholes

# Test signup
curl -X POST https://patchpoint-backend.render.com/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name":"John",
    "email":"john@example.com",
    "password":"password123"
  }'
```

### Test Pi Upload

```bash
curl -X POST https://patchpoint-backend.render.com/api/potholes/pi-upload \
  -F "image=@./sample.jpg" \
  -F "lat=37.7749" \
  -F "lon=-122.4194" \
  -F "depth=8.5" \
  -F "timestamp=$(date +%s)000"
```

---

## 🚀 Auto-Deploy on GitHub Push

Both services are now connected to GitHub and will auto-deploy when you push to `main`:

```bash
# Make changes locally
git add .
git commit -m "feat: Update feature"
git push origin main

# Render automatically re-deploys both services
# Check Render Dashboard for deployment status
```

---

## 📊 Free Tier Limits on Render

| Limit            | Free Tier        | Notes                             |
| ---------------- | ---------------- | --------------------------------- |
| Web Service      | 750 hrs/month    | That's ~1 service running 24/7    |
| Static Site      | Unlimited        | Frontend only counts as bandwidth |
| Build minutes    | 500/month        | Should be plenty                  |
| Database storage | Your own MongoDB | Use MongoDB Atlas free tier       |

**Pro Tip:** To keep free tier active, make a commit every 30 days or your services may sleep.

---

## 🔧 If Something Goes Wrong

### Frontend won't build

- Check **Build Logs** in Render Dashboard
- Verify `VITE_API_URL` is set correctly
- Ensure `frontend/dist` folder exists locally

### Backend connection error

- Check **Logs** in Render Dashboard
- Verify `MONGO_URI` is correct
- Check MongoDB Atlas IP whitelist includes Render's IPs (use 0.0.0.0)

### CORS errors in browser

- Frontend should see: `Access-Control-Allow-Origin: https://patchpoint-frontend.render.com`
- Update backend `CORS_ORIGIN` and redeploy
- Wait 2-3 minutes for full redeploy

### Login fails

- Check backend logs for JWT errors
- Verify `JWT_SECRET` is set
- Try signup (create new account)

---

## 📈 Next: Scale & Monitor

### Monitor Performance

- Render Dashboard shows metrics for both services
- Watch CPU, memory, bandwidth usage
- Free tier runs on shared infrastructure

### Scale When Needed

1. Upgrade to Paid Plan on Render
2. Get dedicated resources
3. Higher memory/CPU for better performance

### Add Custom Domain

1. Go to Service → Settings
2. Add custom domain (requires DNS setup)
3. Render provides SSL automatically

---

## 🎉 You're Done!

Your PatchPoint system is now live:

| Component | URL                                      | Status       |
| --------- | ---------------------------------------- | ------------ |
| Frontend  | `https://patchpoint-frontend.render.com` | ✅ Live      |
| Backend   | `https://patchpoint-backend.render.com`  | ✅ Live      |
| Database  | MongoDB Atlas                            | ✅ Connected |
| Images    | Cloudinary                               | ✅ Uploading |

---

## 📚 Troubleshooting

### Service sleeping?

Render puts free services to sleep after 15 mins of inactivity. To keep awake:

1. Upgrade to Paid
2. Or use external uptime monitor (ping every 5 mins)

### Can't connect to MongoDB?

1. Add Render backend IP to MongoDB whitelist (or use 0.0.0.0)
2. Verify `MONGO_URI` has correct credentials
3. Test: `mongosh "your_mongo_uri"`

### Deployment taking too long?

1. Check logs in Render Dashboard
2. npm install can take 2-3 mins
3. First deploy is slowest; subsequent deploys are faster

### Want to use Render for Pi?

Update `FINAL_INTEGRATION_STORED_VIDEO.py`:

```python
BACKEND_URL = "https://patchpoint-backend.render.com/api/potholes/pi-upload"
```

---

## 🎯 Summary

✅ Backend deployed to Render  
✅ Frontend deployed to Render (static)  
✅ Both auto-deploy on GitHub push  
✅ CORS configured between services  
✅ Ready for Pi uploads  
✅ Monitoring and logs available

**Everything running on Render! 🚀**
