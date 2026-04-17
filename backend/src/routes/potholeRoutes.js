const express = require('express');
const router = express.Router();
const auth = require('../middleware/authMiddleware');
const { createPothole, listPotholes, createFromPi, getPothole, geocodePothole } = require('../controllers/potholeController');

router.get('/', listPotholes);
router.post('/', auth, createPothole);
router.post('/pi', createFromPi);
// Trigger reverse-geocoding and persist address for a single pothole (used by frontend when clicked)
router.post('/:id/geocode', geocodePothole);
router.get('/:id', getPothole);

module.exports = router;
