const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API endpoint to verify payment (for production use)
app.post('/api/verify-payment', express.json(), (req, res) => {
  const { paymentChargeId } = req.body;
  // In production: verify with your database
  res.json({ verified: true, id: paymentChargeId });
});

app.listen(PORT, () => {
  console.log(`Mini App server running on port ${PORT}`);
});
