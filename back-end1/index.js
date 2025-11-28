require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = Number(process.env.PORT || 4000);
const BACKEND2 = process.env.BACKEND2_URL || 'http://back-end2-service:5000';

app.use(cors({ origin: true }));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// Health
app.get('/healthz', (req, res) => res.json({ ok: true }));

// Forward GET submissions to backend2
app.get('/api/submissions', async (req, res) => {
  try {
    const r = await axios.get(`${BACKEND2}/api/submissions`, { timeout: 5000 });
    return res.status(r.status).json(r.data);
  } catch (err) {
    console.error('Error calling backend2 GET /api/submissions:', err?.message || err);
    const msg = err?.response?.data || { error: 'backend2 unreachable' };
    return res.status(502).json(msg);
  }
});

// Forward POST submit to backend2
app.post('/api/submit', async (req, res) => {
  try {
    const payload = { name: req.body.name, email: req.body.email };
    const r = await axios.post(`${BACKEND2}/api/submit`, payload, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 5000
    });
    return res.status(r.status).json(r.data);
  } catch (err) {
    console.error('Error calling backend2 POST /api/submit:', err?.message || err);
    const msg = err?.response?.data || { error: 'backend2 unreachable' };
    return res.status(502).json(msg);
  }
});

app.listen(port, () => {
  console.log(`back-end1 (middleware) listening on port ${port} -> backend2=${BACKEND2}`);
});

