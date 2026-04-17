# Render Deployment Guide

This guide provides exact, repeatable steps to deploy both the backend and frontend of PatchPoint to Render (https://render.com). It lists the build/start commands, environment variables, health checks and recommended Render settings.

If you prefer, follow this guide from your Render dashboard to create two services: one for the backend (Web Service) and one for the frontend (Static Site or Web Service).

---

## 1) Backend — Render Web Service

Create a new Web Service on Render and connect your GitHub repository (the `main` branch).

- Repository root path: `/` (repo contains `backend/` and `frontend/` folders)
- Environment: `Node` (Render will detect Node)

Build & Start settings

- Build Command: `cd backend && npm install`
- Start Command: `cd backend && npm run start`
  - Note: `npm run start` should run `node server.js` (check `backend/package.json` `scripts.start`).

Advanced

- Instance type: Free or Starter for testing; choose paid for production.
- Region: Choose nearest region to your users.
- Auto Deploy: enable to deploy on pushes to `main`.

Required environment variables (set in Render dashboard -> Environment):

- `MONGO_URI` — MongoDB Atlas connection string (example: `mongodb+srv://<user>:<pass>@cluster0.mongodb.net/potholeDB`)
- `JWT_SECRET` — strong random secret for signing tokens
- `CLOUDINARY_CLOUD_NAME` — Cloudinary cloud name
- `CLOUDINARY_API_KEY` — Cloudinary API key
- `CLOUDINARY_API_SECRET` — Cloudinary API secret
- `CORS_ORIGIN` — allowed origins (comma-separated). Example:
  - `https://<your-frontend>.onrender.com,https://temp-pdb7.onrender.com` or use `*` carefully for testing
- `PORT` — usually not required on Render (Render sets a dynamic port in `PORT`), but you can set to `5000` for local parity

Health check & static files

- Health check path: `/api/potholes` (or `/`), Method: `GET` — Render will see 200 if the backend is healthy.
- Serve static visualization: `backend/public/best_pothole_map.html` is served by Express at `/best_pothole_map.html`.

Tips

- Ensure `backend/.env` is NOT committed to the repository. Use Render environment variables for secrets.
- If you accidentally committed secrets, rotate them immediately (DB and Cloudinary) and remove the file from repo history (see Security section below).

---

## 2) Frontend — Static Site (recommended) or Web Service

Option A — Static Site (recommended)

- Create a new Static Site in Render and connect your GitHub repo.
- Build Command: `cd frontend && npm install && npm run build`
- Publish Directory: `frontend/dist`
- Environment variables (Static Site -> Environment):
  - `VITE_API_URL` = `https://<your-backend>.onrender.com` (example: `https://temp-pdb7.onrender.com`)

Option B — Web Service (serve `dist` with a small static server)

- Build Command: `cd frontend && npm install && npm run build`
- Start Command: `cd frontend && npx serve -s dist -l $PORT` (or configure a lightweight server script)
- Environment: set `VITE_API_URL` as above

Notes on `VITE_API_URL`

- The frontend reads `import.meta.env.VITE_API_URL` (in `frontend/src/api/axiosClient.js`). Set this in Render to point to your backend.
- Do NOT hardcode the URL in the codebase — use the environment variable.

---

## 3) CORS & Cookies

- If your backend uses cookies for session/JWT, set `withCredentials: true` in the frontend axios client and add the frontend origin to the backend `CORS_ORIGIN`.
- Example allowed origin (backend env): `https://<your-frontend>.onrender.com`

Cookies and SameSite

- If using cookies, ensure the backend sets cookie attributes appropriate for cross-site usage. For production: `secure: true`, `sameSite: 'lax'` or `none` (if cross-site), and set `domain` if needed.

---

## 4) Post-deploy verification

1. Open frontend URL (Render static site). Verify the app loads.
2. Open browser DevTools → Network. Confirm API requests go to `https://<your-backend>.onrender.com/api/*`.
3. Verify authentication flows (signup/login) work. Check cookies or auth headers are set.
4. Test image upload: try uploading an image from UI and verify Cloudinary upload completes.
5. Verify Pi endpoint: POST a sample payload to `https://<your-backend>.onrender.com/api/potholes/pi` and confirm it appears in the dashboard.

---

## 5) Troubleshooting

- 500 errors: check backend logs on Render (Dashboard → Service → Logs). Look for DB connection issues.
- CORS errors: ensure `CORS_ORIGIN` includes the exact frontend origin.
- Missing environment variables: verify all required keys set in Render env vars.
- Static assets 404: ensure `backend/public` files are present and Express static middleware is configured.

---

## 6) Security — remove committed secrets and rotate

If you accidentally committed `.env` with secrets (API keys, DB creds):

1. Remove file from repository (do _not_ keep it in history):

```powershell
git rm --cached backend/.env
echo "backend/.env" >> .gitignore
git add .gitignore
git commit -m "chore: remove backend .env from repo and add to .gitignore"
git push origin main
```

2. To purge secrets from git history completely, use the BFG Repo-Cleaner or `git filter-branch` and then rotate the secrets (change API keys and DB passwords).

Example BFG steps (local machine):

```bash
# Backup your repo first
git clone --mirror https://github.com/<owner>/<repo>.git
java -jar bfg.jar --delete-files backend/.env <repo>.git
cd <repo>.git
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push
```

After purge: rotate credentials in MongoDB Atlas and Cloudinary.

---

## 7) Helpful Render settings checklist

- Enable auto-deploy on push to `main`.
- Set environment variables in the Render dashboard for both services.
- Configure instance/plan and region.
- Set health check path to `/api/potholes` on backend service.

---

If you want, I can:

- Prepare exact Render dashboard screenshots with the values filled in (I will list the values and where to paste them).
- Run a local `curl` checklist to verify endpoints prior to Render deployment.

Tell me which of the two you'd like next: `screenshots` or `curl-checks`.
