const express = require('express');
const router = express.Router();
const multer = require('multer');
const streamifier = require('streamifier');
const cloudinary = require('../config/cloudinary');
const Pothole = require('../models/Pothole');
const axios = require('axios'); // reverse geocoding

// Memory storage for Pi upload
const upload = multer({ storage: multer.memoryStorage() });

// Parse incoming timestamp (accepts seconds or milliseconds or ISO strings) and return a Date
function parseIncomingTimestamp(timestamp) {
  if (!timestamp) return new Date();
  // If it's numeric string or number, normalize to milliseconds
  if (!isNaN(Number(timestamp))) {
    let n = Number(timestamp);
    // Seconds -> convert to ms
    if (String(timestamp).length <= 10) n = n * 1000;
    return new Date(n);
  }
  // otherwise let Date try to parse ISO
  const d = new Date(timestamp);
  if (isNaN(d.getTime())) return new Date();
  return d;
}

async function getAddressFromCoords(lat, lon) {
  try {
    const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`;
    const res = await axios.get(url, {
      headers: { 'User-Agent': 'PatchPoint/1.0 Student Project' }
    });

    const data = res.data || {};

    // Prefer display_name when present, else build a small human-readable fallback
    if (data.display_name) return data.display_name;

    const addr = data.address || {};
    const parts = [];
    if (addr.road) parts.push(addr.road);
    if (addr.suburb) parts.push(addr.suburb);
    if (addr.city) parts.push(addr.city);
    if (addr.state) parts.push(addr.state);
    if (addr.postcode) parts.push(addr.postcode);

    if (parts.length > 0) return parts.join(', ');

    // Final fallback: return null so we don't store GPS coordinates as the address
    return null;
  } catch (err) {
    console.log('Reverse geocoding failed:', err.message);
    return null;
  }
}

// POST /api/potholes/pi-upload
router.post('/pi-upload', upload.single('image'), async (req, res) => {
  try {
    const { lat, lon, depth, timestamp } = req.body;

    if (!req.file) return res.status(400).json({ success: false, message: 'No image uploaded' });

    // Validate GPS coordinates
    const gpsLat = parseFloat(lat);
    const gpsLon = parseFloat(lon);
    if (!isFinite(gpsLat) || !isFinite(gpsLon)) {
      console.error('Invalid GPS coords received:', lat, lon);
      return res.status(400).json({ success: false, message: 'Invalid GPS coordinates' });
    }

    const address = await getAddressFromCoords(gpsLat, gpsLon);

    const uploadStream = cloudinary.uploader.upload_stream(
      { folder: 'patchpoint/pi' },
      async (error, result) => {
        if (error) {
          console.error('Cloudinary upload error:', error);
          return res.status(500).json({ success: false, message: 'Image upload failed', error });
        }

        // TIMESTAMP: set receipt time server-side (UTC) so DB captures exact arrival time from Pi
        let ts = new Date();

        console.log('Received PI upload coords (server timestamp):', gpsLat, gpsLon, 'timestamp(UTC ms):', ts.getTime(), 'resolved address:', address);

        const pothole = new Pothole({
          imageUrl: result.secure_url,
          gpsLat,
          gpsLon,
          depthCm: depth ? parseFloat(depth) : undefined,
          address: address || null,
          timestamp: ts
        });

        await pothole.save();
        return res.json({ success: true, pothole });
      }
    );

    streamifier.createReadStream(req.file.buffer).pipe(uploadStream);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
