const axios = require("axios");
const Pothole = require("../models/Pothole");
const reverseGeocode = require('../utils/reverseGeocode')

// Normalize incoming timestamps (accept seconds or ms) and return a Date
function parseIncomingTimestamp(timestamp) {
  if (!timestamp) return new Date();
  if (!isNaN(Number(timestamp))) {
    let n = Number(timestamp);
    if (String(timestamp).length <= 10) n = n * 1000;
    return new Date(n);
  }
  const d = new Date(timestamp);
  if (isNaN(d.getTime())) return new Date();
  return d;
}

exports.createFromPi = async (req, res) => {
  try {
    const { gps_lat, gps_lon, lidar_cm, image, timestamp } = req.body;

    const gpsLat = Number(gps_lat);
    const gpsLon = Number(gps_lon);
    if (!isFinite(gpsLat) || !isFinite(gpsLon)) {
      return res.status(400).json({ success: false, message: "Missing or invalid GPS" });
    }

    // ---- TIMESTAMP: set receipt time server-side (UTC) ----
    let ts = new Date();
    console.log('createFromPi received: coords', gpsLat, gpsLon, 'server timestamp(UTC ms):', ts.getTime());

    // ---- REVERSE GEOCODING ----
    const geoURL = `https://nominatim.openstreetmap.org/reverse?lat=${gps_lat}&lon=${gps_lon}&format=json`;

    let address = null;
    try {
      const geo = await axios.get(geoURL, {
        headers: { "User-Agent": "PatchPoint/1.0" }
      });
      address = geo.data?.display_name || null;
    } catch (e) {
      console.log("Reverse geocoding failed:", e.message);
    }

    // ---- SAVE TO DATABASE ----
    const pothole = await Pothole.create({
      gpsLat: gpsLat,
      gpsLon: gpsLon,
      depthCm: lidar_cm !== undefined ? Number(lidar_cm) : undefined,
      address: address || null,
      timestamp: ts,
      imageUrl: image || null
    });

    return res.json({ success: true, pothole });

  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

// Create pothole via UI (authenticated)
exports.createPothole = async (req, res) => {
  try {
    const { gpsLat, gpsLon, depthCm, address, imageUrl } = req.body;
    if (gpsLat === undefined || gpsLon === undefined) {
      return res.status(400).json({ success: false, message: "Missing GPS coordinates" });
    }

    const pothole = await Pothole.create({
      gpsLat: Number(gpsLat),
      gpsLon: Number(gpsLon),
      depthCm: depthCm !== undefined ? Number(depthCm) : undefined,
      address: address || null,
      imageUrl: imageUrl || null,
      createdBy: req.user ? req.user.id : undefined
    });

    return res.json({ success: true, pothole });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

// List potholes
exports.listPotholes = async (req, res) => {
  try {
    let potholes = await Pothole.find().sort({ timestamp: -1 });

    // Sanitize legacy placeholder values (e.g., '-' saved previously) so UI shows an empty value
    potholes = potholes.map(ph => {
      const obj = ph.toObject ? ph.toObject() : ph;
      if (obj.address === '-') obj.address = null;
      return obj;
    });

    // Backfill missing addresses asynchronously but return a consistent response.
    // If address is missing for a pothole, perform reverse geocoding and persist it.
    const toBackfill = potholes.filter(p => !p.address);
    if (toBackfill.length > 0) {
      // Run in background but wait so UI sees the resolved address on next fetch
      await Promise.all(toBackfill.map(async p => {
        try {
          const geo = await reverseGeocode(p.gpsLat, p.gpsLon);
          const full = geo?.fullAddress || null;
          if (full) {
            await Pothole.findByIdAndUpdate(p._id, { address: full });
            p.address = full; // reflect change in current response
            console.log('Backfilled address for', p._id, full);
          } else {
            // fallback: store a friendly non-coordinate placeholder so UI does not display GPS
            const unavailable = 'Address unavailable';
            await Pothole.findByIdAndUpdate(p._id, { address: unavailable });
            p.address = unavailable;
          }
        } catch (e) {
          console.log('Failed to backfill address for', p._id, e.message);
          p.address = `${p.gpsLat}, ${p.gpsLon}`;
        }
      }));
    }

    return res.json({ success: true, potholes });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};

// POST /api/potholes/:id/geocode  --- derive address for a single pothole and persist it
exports.geocodePothole = async (req, res) => {
  try {
    const { id } = req.params;
    const pothole = await Pothole.findById(id);
    if (!pothole) return res.status(404).json({ success: false, message: 'Pothole not found' });

    // If address already present, return it by default
    if (pothole.address) return res.json({ success: true, pothole });

    const geo = await reverseGeocode(pothole.gpsLat, pothole.gpsLon);
    const full = geo?.fullAddress || 'Address unavailable';

    pothole.address = full;
    await pothole.save();


    console.log('Geocoded pothole', pothole._id, '->', full);
    return res.json({ success: true, pothole });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: 'Server error' });
  }
};

// Get single pothole
exports.getPothole = async (req, res) => {
  try {
    const { id } = req.params;
    const pothole = await Pothole.findById(id);
    if (!pothole) return res.status(404).json({ success: false, message: "Pothole not found" });
    return res.json({ success: true, pothole });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, message: "Server error" });
  }
};